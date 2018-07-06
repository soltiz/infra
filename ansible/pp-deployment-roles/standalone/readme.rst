#####################n############################
        remote Standalone deployment role
#################################################

************
    Goal
************

Uploads, deploys and starts a remote standalone

Takes care of setting up prerequired packages using apt

*********************
    Prerequisites
*********************

* Enough room in /home (1G)
* configured up-to-date repository
  
****************************
    Behaviour highlights
****************************

* creates remote user
* deploys prerequired standard packages through sudo and apt ( can be skipped through the tag "prerequisites" )
* uploads standalone archive, and not remove it (even after setup)
* installs the standalone, and allow the setup process to patch the remote user .bashrc
* starts the standalone
* checks the running status
  

**************************
    Required variables
**************************


punchplatform_user:

	remote login to use for punchplatform deployment. For prerequired packages deployment (that can be skipped), sudoer rights are needed

punchplatform_standalone_archive:

	local path of the standalone archive to deploy 
