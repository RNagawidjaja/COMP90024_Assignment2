#!/usr/bin/env bash
. ./unimelb-comp90024-group-77-openrc.sh
ansible-playbook --key-file="~/.ssh/id_team77" -i hosts deployHarvester.yml