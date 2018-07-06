##################################
        CEPH Demonstration
##################################

**************
    SCRIPT
**************

* Setup of demo infrastructure :


	- Show VMs in virtualbox. Explain : a LMC in a box, with very similar version as currently deployed in production
	  
	- Say "will now create new VMs for the demonstration of CEPH function ; in production, these may be existing servers (targetted : coexistence with elasticsearch for hardware cost optimization)"
  
  	- run ansible :
  	
  		source demo-env
  		ansible-playbook -i demo-infra.inv  deploy_generic_cluster.yml

  		#And Say "Not the LMC deployer, just infrastructure"

* Show slides about Demo :
  
  	Infra ( LMC Mono noeud + 3 noeuds CEPH)



* Launch LMC Deployer for ceph
  
  	ssh adm-infra@ansible

  	punchplatform-cluster.sh deploy -l ceph1,ceph2,ceph3
	punchplatform-cluster.sh deploy -l lmc1 -t ceph


* Show slides about Ceph : 
  
  		why + topologies


* Show that system metrics are now available on ceph*
  

* Show that CEPH dashboard now receives basic graph (storage space)	

	#using lmcadmin@lmc1

    ceph --cluster main --user client

    	health
    	df
	



* Configure channels with ceph

		#using lmcadmin@lmc1
		punchplatform-channel.sh --configure $PUNCHPLATFORM_CONF_DIR/tenants/mytenant/configurations_for_channels_generation --force


* Start channels
  
   	punchplatform-channel.sh --start mytenant


* Show Admin ?


* Start Injection


punchplatform-log-injector.sh -c /home/lmcadmin/soc_conf/resources/injector/lmc/arkoon_injector.json,/home/lmcadmin/soc_conf/resources/injector/lmc/BlueCoat_ProxySG_sslreporter_injector.json



* Show Dashboard. Show difference between compressed and raw

* Show Objects usage in command line

    punchplatform-objects-storage.sh list-topics --cluster ceph_configuration:///etc/ceph/main.conf --pool mytenant --details

	punchplatform-objects-storage.sh extract-scope --cluster ceph_configuration:///etc/ceph/main.conf --pool mytenant --topic parsed_arkoon --into extraction

	tree extraction

	gunzip d'un fichier + vi

	## not useful punchplatform-objects-storage.sh pool-status --cluster ceph_configuration:///etc/ceph/main.conf --pool mytenant


Reinjection
===========

Remove logs from Elasticsearch

  curl -XDELETE http://localhost:9200/events-*

cd soc_conf/samples/reinject_jobs
vi reinject_from_ceph_job.json
# Edit dates
punchplatform-topology.sh reinject_from_ceph_job.json

* Go to jobs tab

	Wait for 100%

	Compare log counts in kibana


*******************************
    Re-deployment procedure
*******************************

- Deploy infra :

	. demo-env
	ansible-playbook -i demo-infra.inv  deploy_generic_cluster.yml	

- Deploy everything but ceph :


	ssh adm-infra@ansible
	punchplatform-cluster.sh deploy --skip-tags ceph,cephbeat,elastalert



- At this step, admin is not green (see punchplatform-admin-pythonordering issue at the end)
  
  	ssh adm-infra@lmc1
  	sudo supervisorctl restart punchplatform-admin-python

- Ensure admin is green
  

- Remove ES indexes

  	curl -XDELETE localhost:9200/cephb*
  	curl -XDELETE localhost:9200/metric*
	

- Create Grafana datasources :
  
  + ES          : IndexName=[metrics-]YYYY.MM.DD    GroupByTermInterval>40s (timestamp ts)
  + ES-cephbeat : IndexName=[cephbeat-]YYYY.MM.DD   GroupByTermInterval>40s (timestamp @timestamp)
  + Metricbeat  : IndexName=[metricbeat-]YYYY.MM.DD GroupByTermInterval>40s (timestamp @timestamp)


- Import Grafana dashboards :
  
  + OS_System.json
  + ceph_dashboard.json (and resave it with "last 5 minutes")

  + Change unit to % on OS System/CPU Top 10 dashboard
  + Change order and colors on Storage Usage, Ceph dasboard
  + Change dash name for ceph to "Ceph Demo"
    


 - Configure and start arkoon channel (to create metrics indexes)
   
		punchplatform-channel.sh --configure $PUNCHPLATFORM_CONF_DIR/tenants/lmc/configurations_for_channels_generation/technos/arkoon_channel.json  --force

		punchplatform-channel.sh --start lmc/arkoon

		punchplatform-log-injector.sh -c $PUNCHPLATFORM_CONF_DIR/resources/injector/lmc/arkoon_injector.json


  - create Kibana index settings :
    	
    	events-*  (timestamp : input.ts)

    	check that logs are displayed

  - create Grafana datasource
  
    punchplatform-channel.sh --stop 
     rm -rf soc_conf/tenants/lmc/channels/
     git config --global user.email "you@example.com"
	git config --global user.name "Your Name"

     commit, push


	curl -XDELETE localhost:9200/events-*
  	curl -XDELETE localhost:9200/cephb*
  	curl -XDELETE localhost:9200/metric*
	

     sudo shutdown -h now
  - take snapshot

Ceph/StorageUsage/ Red + Fill 4

**************************
    Pre-demo checklist
**************************


- stop mytenant

 		punchplatform-channel.sh --stop mytenant



git commmit, push lmc1 pull ansible

- apt-get update and upgrade on ceph1 to update cache

- delete topics

  	punchplatform-kafka-topics.sh --list | xargs -n 1 punchplatform-kafka-topics.sh --delete --topic
  	punchplatform-zookeeper-console.sh
  		rmr /punchplatform/kafka-consumer

- delete jobs

    punchplatform-jobs.sh delete --force --job <ID>
    punchplatform-zookeeper-console.sh
  		rmr /punchplatform/admin/jobs

- delete ceph topic

    punchplatform-objects-storage.sh delete-scope --cluster ceph_configuration:///etc/ceph/main.conf --pool mytenant --topic parsed_bluecoat_proxysg --max-deletion-percentage 100
      mytenant/parsed_bluecoat_proxysg
    punchplatform-objects-storage.sh delete-scope --cluster ceph_configuration:///etc/ceph/main.conf --pool mytenant --topic parsed_arkoon --max-deletion-percentage 100
      mytenant/parsed_arkoon

- remove files from extraction folder

    rm -r extraction/*

- Delete elasticsearch indexes (including metrics) except kibana
	curl -XDELETE localhost:9200/ev*
    curl -XDELETE localhost:9200/met*
    curl -XDELETE localhost:9200/ceph*

    curl localhost:9200/_cat/indices

- Ensure Host PCs and VMs are with the same datetime
sudo reboot


- disconnect network


- Put apt-cacher ng offline


- restart dnsmask (CED) without external server
  
	
sed -i '/ceph/d'   ~/.hosts/resolved_ips
    sudo killall dnsmasq
sudo dnsmasq --hostsdir /home/cedric/.hosts --max-cache-ttl=10000


- git push depuis lmcadmin, git pull depuis ansible
  
- check mount -a on lmc1
  
- delete ceph*  



ssh adm-infra@lmc1 sudo date --set=@$(date +%s) ; ssh adm-infra@ansible sudo date --set=@$(date +%s)


Cedric : 
========

- go back to "pre-demo" snapshot of LMC1 VM
delete ceph vms
  # NO sudo service nfs-server stop on ansible
service date restart sur LMC1 si pas a l'heure

sudo apt-update sur LMC1
passage offline du acng
	refresh dnsmasq to clear old ips
	fond blanc pour les fenetres
	offline aptcacher or tethering

	delete topics
	zookemer : rmr kafka consumer

Leo : 
=====

 - VMs up (LMC + 3 Ceph), 
 - Admin PP green
 - Channel arkoon, bluecoat and output stopped
 - pp-ceph list-topics --details     shows pool "mytenant" with no topics inside
 - Grafana dashboards displays remaining space


*******************************
    Additional informations
*******************************

Demo infrastructure + LMC has been successfully deployed on a VM template based on Ubuntu 16.04.1 with these additional pre-requisites (exhaustive):

 - 2 HDD: sda=32GB sdb=10GB (1 partition sdb1)
 - /etc/apt/sources.list patched to contact local apt repository
 - Public GPG adminomc key installed (with apt-key) (because of local apt repo signed with private adminomc key)
 - 2 interfaces, bridged on two local bridges br0, br1 (brctl add...)
 - /etc/netwo	interfaces patched
 - apt update & apt upgrade
 - /etc/wgetrc patched to contact local squid proxy
 - ntp client installed and configured to contact local ntp server
 - packages python2.7, python-pip, python-paramiko, sshpass, curl, jq, unzip, python-minimal, openssh-server, htop, ccze installed
 - user adm-infra is sudoer without password

These steps are not mandatory, this is just an indication of what has been used to deploy Ceph Demo.




