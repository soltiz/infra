###########################################
        LMC deployer
###########################################


********************
    Role purpose
********************

To setup LMC cluster deployment environment on a server

*********************
    prerequisites
*********************

- a Local LMC deployer archive
- a local passwordless ssh key that can connect to target servers

**************************
    Required variables
**************************

punchplatform_deployment_user:

    the login of the user that will use the deployer, and that the deployer will use on  target machines

punchplatform_users_group:
	 
	 the common group of all accounts that will need to be able to update the reference configuration repository

punchplatform_local_deployer_archive:

    the local path to a punchplatform deployer archive


punchplatform_platform_dirname:
     
    the name of the platform to take configuration for in the resources (one of the subdirectories names in the 'platforms' directory of the configuration)
    e.g. : "mono"

pp_log_resources_repository:
  
    the url to a cloneable log resources repo (containing reference mono platform configuration)

production_interface:

    system name of the network interface to use for production flow on the target vm