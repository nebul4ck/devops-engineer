#!/bin/bash

#  ¡¡¡¡ DON'T TOUCH !!!

# This script sets the Ansible environment on present session. 
# Run the script before to launch ansible-playbook command (per shell session).
# ie:
# 	1) open a new shell session tab
#		# agonzalez@anubis ~/ $
#	2) exec ANSIBLE-ENVIRONMENT.sh:
#		# agonzalez@anubis ~/ $ . ANSIBLE-ENVIRONMENT.sh
#	3) launch the Plays with ansible-playbooks!!:
#		# agonzalez@anubis ~/ $ cd some_templates_or_playbooks_directory
#		agonzalez@anubis ~/git/titan/DEPLOY/Ansible/templates $ ansible-playbooks -i hosts start-deploy.yml

## CONNEXION ##

export ANSIBLE_SSH_PIPELINING=True
export ANSIBLE_SSH_RETRIES=2
export ANSIBLE_KEEP_REMOTE_FILES=False
#export ANSIBLE_PRIVATE_KEY_FILE=/to/path/id_rsa
export ANSIBLE_REMOTE_USER='root'
#export ANSIBLE_GALAXY_IGNORE=True
#export ANSIBLE_GALAXY_SERVER="https://galaxy.ansible.com"
#export ANSIBLE_GALAXY_TOKEN=github_toker
export ANSIBLE_HOST_KEY_CHECKING=False
export ANSIBLE_USE_PERSISTENT_CONNECTIONS=False
export ANSIBLE_PERSISTENT_COMMAND_TIMEOUT=10
export ANSIBLE_PERSISTENT_CONNECT_RETRY_TIMEOUT=15
export ANSIBLE_PERSISTENT_CONNECT_TIMEOUT=30
export ANSIBLE_PARAMIKO_LOOK_FOR_KEYS=True
export ANSIBLE_PARAMIKO_HOST_KEY_AUTO_ADD=True

## ESCALATION ##

export BECOME_ALLOW_SAME_USER=False
export DEFAULT_ASK_PASS=False
export ANSIBLE_ASK_VAULT_PASS=False
export ANSIBLE_BECOME=True
export ANSIBLE_BECOME_ASK_PASS=False

## TASKS ##

export ANSIBLE_DIFF_ALWAYS=True
export ANSIBLE_DIFF_CONTEXT=3
export ANSIBLE_MAX_DIFF_SIZE=104448
export ANSIBLE_DISPLAY_ARGS_TO_STDOUT=False
export ANSIBLE_ENABLE_TASK_DEBUGGER=False
export ANY_ERRORS_FATAL=True
#export ANSIBLE_CALLABLE_WHITELIST=('list')
export ANSIBLE_EXECUTABLE=/bin/sh
export ANSIBLE_FORKS=5
export ANSIBLE_RETRY_FILES_ENABLED=True
export ANSIBLE_RETRY_FILES_SAVE_PATH='~/.ansible'

## LOGS ##

export ANSIBLE_FORCE_COLOR=True
#export ANSIBLE_LOG_FILTER=('list')
export ANSIBLE_LOG_PATH='~/.ansible/ansible.log'
export ANSIBLE_NO_LOG=False
export ANSIBLE_NO_TARGET_SYSLOG=True
export ANSIBLE_SYSLOG_FACILITY=LOG_USER
export ANSIBLE_SYSTEM_WARNINGS=True

## VARS AND HOSTS ##

export ANSIBLE_PLAYBOOK_VARS_ROOT=all
export ANSIBLE_GATHERING=smart
#export ANSIBLE_INVENTORY=('list')
#export ANSIBLE_HOSTS=('list')
export ANSIBLE_JINJA2_EXTENSIONS=''
export ANSIBLE_INJECT_FACT_VARS=True
#export ANSIBLE_INVENTORY_ENABLED=('host_list' 'script' 'yaml' 'ini' 'auto')
