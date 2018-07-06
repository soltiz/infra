#!/bin/bash -u
name=$1
ip=$(sed -n "/$name/s/ .*//p" /tmp/resolved_ips)
echo "ssh to $ip ...."
echo ssh-keygen -f "~/.ssh/known_hosts" -R $ip
ssh-keygen -f "/home/$USER/.ssh/known_hosts" -R $ip
ssh adm-infra@$ip -o StrictHostKeyChecking=no
