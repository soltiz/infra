###########################################
        Virtual Box VM role (vb-vm)
###########################################


********************
    Role purpose
********************

To deploy/start a virtualbox VM based on last existing snapshot of a template virtualbox vm.

To retrieve its IP (used for ssh) and inject it as 'ansible_ssh' variable so that subsequent roles
can actually connect to the VM if needed

To connect to the VM and assign it as actual hostname the provided 'inventory_hostname' variable

*********************
    prerequisites
*********************

- The "template" Virtualbox VM must :

    + have a secondary interface in DHCP automatic mode, on a Host-reachable virtualbox network
    + have a snapshot (last snapshot will be used) taken WHILE THE VM WAS POWERED DOWN
    + have appropriate configuration for ssh, sudoing, and must be configured to reach standard ubuntu repositories (or a cache). Have python 2.7.X installed (be careful: it's not installed by default on Ubuntu since 16.04).
  
- The local user must have rights to use virtualbox
- nmap command must be available on local machine
- if an other VM with the same name inside Virtualbox exists, then the role will not start a new one, even if the previous VM was not based on the provided template vm.
- playbooks and libraries are compatibles only with ansible 2.1.2

**************************
    Required variables
**************************

vb_template:

	Name of the vm in the virtualbox list (not necessarily the hostname inside the VM)

inventory_hostname:

	This variable is set automatically by Ansible (see Ansible documentation), and will be used as new hostname for the VM, and as the name for the VM in the Virtualbox list


vm_nbcpu: 

    nb of vcpu of the vm (defaults to 1)

vm_memory:

    nb of MB of RAM of the vm (defaults to 1024, ie 1GB)


************************
    Attention points
************************

The created VM disk will be managed as a delta based on the template vm disk. If the template VM disk is removed from the filesystem, the created VM will not operate anymore.

