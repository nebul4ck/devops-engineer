#!/bin/bash

#----------------------------------------------#
# author: Alberto González
# date: 13/11/2019
#
# Use it for development environments
# Help us to deploy, delete and get info about
# cloudformation stacks
#
# ./multi-aws-cli.sh
# │
# ├── ec2
# │   ├── cf-compliance-ec2-instance.yaml
# │   ├── parameters
# │   │   └── parameters.json
# │   └── tags
# │       └── tags.json
# └── s3  
#     ├── cf-compliance-s3-bucket.yaml
#     ├── parameters
#     │   └── parameters.json
#     └── tags
#         └── tags.json
#
# run it:
# 	$ ./multi-aws-cli.sh <profile> <account>
#		<resource> <action>
#----------------------------------------------#

# Arguments #
profile="$1"
account="$2"
resource="$3"
action="$4"
random=`echo $(($RANDOM%100))`

stack="${account}-"`ls ./${resource} |egrep "*yaml|*yml"|cut -d. -f1`"-${random}-cf"
template="file://${resource}/"`ls ./${resource} |egrep "*yaml|*yml"`
parameters="file://${resource}/parameters/parameters.json"
tags="file://${resource}/tags/tags.json"
region="eu-west-1"
aws_cmd=`which aws`


test_stack () {

	# Sintax validator

    ${aws_cmd} cloudformation validate-template \
    --template-body "${template}"

    exit 0
}

create_stack () {

	# Create a new Stack

    ${aws_cmd} cloudformation create-stack \
    --profile ${profile} \
    --stack-name ${stack} \
    --template-body ${template} \
    --parameters ${parameters} \
    --tags ${tags} \
    --region ${region} \
    --capabilities CAPABILITY_NAMED_IAM

    # The following lines code will block the CLI
    # until the command is finished.
    # ${aws_cmd} cloudformation wait stack-create-complete \
    # --profile ${profile} \
    # --stack-name ${stack} \
    # --region ${region} && echo " done."

	exit 0
}

show_available_stacks () {

	# Select a stackname
	stacks=$(aws cloudformation describe-stacks \
        --profile ${profile} \
        --query "Stacks[].StackName" | tr -d "[|]|,|\"")

	echo "${stacks}"
	echo -e "\nSelect a Stack from above list and Copy&Paste it here:"

	read stack
}

stack_deploy_info () {

	show_available_stacks

	# Check the stack deployment status

	for event in $(aws cloudformation describe-stack-events \
		--stack-name ${stack} \
		--profile "${profile}" \
		--query "StackEvents[].ResourceStatus");
		do
	    	if [[ ${event} =~ 'CREATE_FAILED' ]];
	    	then
				echo -e "\n Status: `echo ${event}|tr -d ','`\n"

				select_failed=$(aws cloudformation describe-stack-events \
					--stack-name ${stack} \
					--profile ${profile} \
					--query "StackEvents[?ResourceStatus == 'CREATE_FAILED'].ResourceStatusReason")

		    	echo -e "`echo  ${select_failed}|tr -d '[|]'`"
	    	elif [[ ${event} =~ 'CREATE_COMPLETE' ]];
	   		then
	    		select_complete=$(aws cloudformation describe-stack-events \
	    			--stack-name ${stack} \
	    			--profile ${profile} \
	    			--query "StackEvents[?ResourceStatus == 'CREATE_COMPLETE'].ResourceStatus[] | [0]")

	    		echo -e "\n Status: `echo  ${select_complete}`" && exit 0
	    	fi
	done

	exit 0
}

delete_stack () {

	show_available_stacks

	# Delete a selected stack

	aws cloudformation delete-stack \
	--stack-name ${stack} \
	--profile ${profile}

	exit 0
}

if [ "$#" -lt 4 ] ; then
    echo "Usage: `basename $0` <profile> <account> <resource> <action>"
    echo -e "Actions:"
    echo -e "\ttest: validate a cloudformation template"
    echo -e "\tdeploy: create a new cloudformation stack"
    echo -e "\tinfo: Get info about new stack creation"
    echo -e "\tdelete: Delete a selected stack"
    exit 1
else
	case "$action" in
		"test")
			test_stack
		;;
		"deploy")
			create_stack
		;;
		"info")
			stack_deploy_info
		;;
		"delete")
			delete_stack
		;;
		*)
			echo "action not found!"
			echo "try with: test, deploy, info or delete"
		;;
	esac
fi
