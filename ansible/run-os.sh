#!/usr/bin/env bash
. ./unimelb-comp90024-group-77-openrc.sh
ansible-playbook --key-file="~/.ssh/id_team77" --ask-vault-pass install.yml