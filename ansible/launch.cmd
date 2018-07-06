cd pp-packaging/punchplatform-validation/ansible
ANSIBLE_ROLES_PATH=infrastructure-roles:pp-deployment-roles ansible-playbook -i monocluster-virtualbox.inv deploy_monocluster.yml -u adm-infra
