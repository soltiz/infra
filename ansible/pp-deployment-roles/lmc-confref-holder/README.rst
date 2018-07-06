###############################################################
        LMC reference git repository (bare) holder role
###############################################################


********************
    Role purpose
********************

To deploy a reference git repository that can be pulled (at least locally)

*********************
    prerequisites
*********************

- a pullable reference repository
- a local passwordless ssh key that can connect to target servers

**************************
    Required variables
**************************

punchplatform_deployment_user:

    the login of the user that will own the reference git repository

punchplatform_users_group:

	the linux group that will own the reference git repository (should be the primary group of the previous user)


pp_conf_repository:
  
    the url to a cloneable log resources repo (containing reference for target platform configuration)

pp_conf_branch:

	git branch to use as remote default branch

remote_repository_dir:

	the folder that will be the remote root of the repo clone.