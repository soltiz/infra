#######################################################################
        Validation configuration deployment roles and playbooks
#######################################################################

***************
    Purpose
***************

The goal is to be able to quickly/automatically deploy repeatable test configuration on various infrastructure

This is used in particular by automated nightly tests (to be finalized) to ensure "standalone" and "mono-cluster" deployer are always tested in each PunchPlatform product release.

*********************
    Prerequisites
*********************

sudo pip install pyvbox

****************************************************************
    Deployment of a Virtualbox VM with a standalone on board
****************************************************************

* Prepare your Virtualbox template, and take a final snapshot (mandatory : this is the clone start point).
* Customize 'test.inv' with your template name (see infrastructure-roles/vb-vm/README) and standalone version
* Run ansible :

  .. code-block:: shell

      cd pp-packaging/punchplatform-validation/ansible
	  
	  export ANSIBLE_ROLES_PATH=infrastructure-roles:pp-deployment-roles

	  ansible-playbook -i test.inv deploy_standalone.yml


* connect to the vm and start the standalone :

  .. code-block:: shell

		./s.sh standalone

		punchplatform-admin.sh --start

  .. note:: The name "standalone" is not defined in your /etc/hosts. It is stored in /tmp/resolved_ips file, and used by the s.sh script to connect (by default, using adm-infra account) to your VM.

* if you want to use your browser easily, define the "standalone" name in association with the current ip of the VM as shown by ./s.sh command. 

  	.. warning:: the ip allocated to the vm by virtualbox may change after restart of the virtualbox service. In this case, running the "find-vms" role at start of a playbook will both refresh the /tmp/resolved_ips file, and apply the good ansible_host address to the end of the playbook.



*********************************************************************************************
    Deployment of two Virtualbox VM with respectively a deployer and monocluster on board
*********************************************************************************************

ANSIBLE_ROLES_PATH=infrastructure-roles:pp-deployment-roles ansible-playbook -i monocluster-virtualbox.inv deploy_monocluster.yml -u adm-infra --skip-tags elastalert


***********************************************************************************************
    Deployment of 4 Virtualbox VM with respectively a deployer and a cluster of 3 LMC nodes
***********************************************************************************************

ANSIBLE_ROLES_PATH=infrastructure-roles:pp-deployment-roles ansible-playbook -i trio  cluster-virtualbox.inv deploy_triocluster.yml -u adm-infra --skip-tags elastalert

