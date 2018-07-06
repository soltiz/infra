
from ansible.module_utils.basic import AnsibleModule
import virtualbox
from threading import Thread
import time
import subprocess
#from virtualbox import LockType

vbox=virtualbox.VirtualBox()

def create_machine(template,machine_name):
    template=vbox.find_machine(template)
    machine=template.clone(name=machine_name)
    return machine

def delete_machine(vm):
    vm.remove(delete=True)

def start_machine(vm,memory,nbcpu):
    if is_machine_stopped(vm):
        session=vm.create_session()
        session.machine.memory_size=memory
        session.machine.cpu_count=nbcpu
        session.machine.save_settings()
        session.unlock_machine()

        progress=vm.launch_vm_process(type_p='headless')
        #progress=vm.launch_vm_process(session,'headless','')


def stop_machine(vm):
    if not is_machine_stopped(vm):
        session=vm.create_session()
        session.console.power_down()


def get_machine(machine_name):
    for machine in vbox.machines:
        if machine.name==machine_name:
            return machine
    return None


def is_machine_stopped(machine):
    return (machine.state==1) or (machine.state==2) or (machine.state==3) or (machine.state==4)


def find_ip_using_arp(mac_address,timeout_in_s,network_range):
    ip=None
    stoptime=int(time.time())+int(timeout_in_s)
    firsttime=True
    while ip==None and int(time.time())<stoptime:
        if firsttime:
            arplines=subprocess.check_output("arp -n",shell=True).split('\n')
            firsttime=False
        else:
            arplines=subprocess.check_output("nmap -n -sn %s >/dev/null ; arp -n" % network_range,shell=True).split('\n')
        arpdict=dict()
        for arpline in arplines[+1:-1]:
            arprecord=arpline.split()
            mac=arprecord[2].replace(":","").upper()
            ip=arprecord[0]
            arpdict[mac]=ip
        ip=arpdict.get(mac_address.upper())
    return ip



def gather_facts(vm,arp_wait_timeout_in_s,network_range,network_interface):
    facts=dict()
    if vm is None:
        facts['vb_name']='!!!VM_NOT_FOUND!!!'
        return facts

    facts['vb_name']=vm.name
    adapter=vm.get_network_adapter(network_interface)
    mac=adapter.mac_address
    facts['vb_mac']=mac
    if not is_machine_stopped(vm):
        facts['vb_ip']=find_ip_using_arp(mac,arp_wait_timeout_in_s,network_range)
    return facts


def main():
    # This module WANT_JSON (do not change this comment, because Ansible uses it)
    module = AnsibleModule(
        argument_spec = dict(
            state     = dict(default='running', choices=['present', 'absent', 'running','stopped']),
            name      = dict(required=True),
            memory =    dict(default=1024),
            nbcpu =    dict(default=1),
            arp_wait_timeout = dict(default='60'),
            template     = dict(default='ubuntu'),
            network_range = dict(default="0.0.0.0-0"),
            network_interface = dict(default=1)
        )
    )

    # fill this with info that you want added to the ansible environment
    # http://docs.ansible.com/developing_modules.html#module-provided-facts
    facts = dict()
    name=module.params['name']
    target_state=module.params['state']
    template=module.params['template']
    arp_wait_timeout=module.params['arp_wait_timeout']
    memory=int(module.params['memory'])
    nbcpu=int(module.params['nbcpu'])
    network_range=module.params['network_range']
    network_interface=int(module.params['network_interface'])
    vm=get_machine(name)
    changed=False
    facts=gather_facts(vm,arp_wait_timeout,network_range,network_interface)

    if target_state=='absent':
        if vm is None:
            module.exit_json(changed=False, msg="VM does not exist", ansible_facts=facts)
        else:
            if module.check_mode:
                module.exit_json(changed=True, msg="VM has to be destroyed", ansible_facts=facts)
            delete_machine(vm)
            module.exit_json(changed=True, msg="VM has been destroyed", ansible_facts=facts)
    else:
        if vm is None:
            if module.check_mode:
                module.exit_json(changed=True, msg="VM has to be created", ansible_facts=facts)
            else:
                vm=create_machine(template,name)
                facts=gather_facts(vm,arp_wait_timeout,network_range,network_interface)
                changed=True
        if target_state=='stopped':
            if not is_machine_stopped(vm):
                facts=gather_facts(vm,arp_wait_timeout,network_range,network_interface)
                if module.check_mode:
                    module.exit_json(changed=True, msg="VM has to be stopped", ansible_facts=facts)
                stop_machine(vm)
                module.exit_json(changed=True, msg="VM was stopped", ansible_facts=facts)
        elif target_state=='running':
            if is_machine_stopped(vm):
                if module.check_mode:
                    module.exit_json(changed=True, msg="VM has to be started", ansible_facts=facts)
                start_machine(vm,memory,nbcpu)
                facts=gather_facts(vm,arp_wait_timeout,network_range,network_interface)
                module.exit_json(changed=True, msg="VM was started", ansible_facts=facts)
                facts=gather_facts(vm,arp_wait_timeout,network_range,network_interface)
    if changed:
        module.exit_json(changed=True, msg="VM was created", ansible_facts=facts)
    module.exit_json(changed=False, msg="did nothing", ansible_facts=facts)
    # ... otherwise, if failure
    # module.fail_json(msg="explain why the module failed here")


if __name__ == '__main__':
    main()
