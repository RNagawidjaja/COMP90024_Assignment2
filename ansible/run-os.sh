#!/usr/bin/env bash
. ./pt-44353-openrch.sh
ansible-playbook --key-file="~/.ssh/id_team77" --ask-vault-pass install.yml
