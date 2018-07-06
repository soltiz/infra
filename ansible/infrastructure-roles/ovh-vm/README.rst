###########################################
        OVH VM role (ovh-vm)
###########################################


********************
    Role purpose
********************

To deploy/start an OVH cloud VM based on an Openstack image

To retrieve its IP (used for ssh) and inject it as 'ansible_ssh' variable so that subsequent roles
can actually connect to the VM if needed

To connect to the VM and assign it as actual hostname the provided 'inventory_hostname' variable

*********************
    prerequisites
*********************

* Have python "shade" module installed in local host, or user virtualenv.

#- The "template" Virtualbox VM must :
#
#    + have a secondary interface in DHCP automatic mode, on a Host-reachable virtualbox network
#    + have a snapshot (last snapshot will be used) taken WHILE THE VM WAS POWERED DOWN
#    + have appropriate configuration for ssh, sudoing, and must be configured to reach standard ubuntu repositories (or a cache).
#  
#- The local user must have rights to use virtualbox
#- nmap command must be available on local machine
#- if an other VM with the same name inside Virtualbox exists, then the role will not start a new one, even if the previous #VM was not based on the provided template vm.
#- playbooks and libraries are compatibles only with ansible 2.1.2

**************************
    Required variables
**************************

vm_image:

	Name of the openstack image to use

vm_flavor:

    Name of the OVH openstack vm size ("openstack flavor") such as 'eg-7-ssd'


Environment variables to define : (e.g. fictive Openstack auth) :

.. code-block:: shell

    OS_PASSWORD=xxxxxxx
    OS_AUTH_URL=https://auth.cloud.ovh.net/v2.0/
    OS_USERNAME=z2Cksab563
    OS_TENANT_NAME=LMC



inventory_hostname:

	This variable is set automatically by Ansible (see Ansible documentation), and will be used as new hostname for the VM, and as the name for the VM in the Virtualbox list

**************************
    Optional variables
**************************

access_user:
    Sudoer login to create for deployment in place of the default one (the default one will be removed if this key is defined with a different value)

access_key:
    ssh key to push for accss_user login (requires access_user variable to be defined)


************************
    Attention points
************************

