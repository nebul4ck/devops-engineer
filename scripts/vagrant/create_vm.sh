#!/bin/bash

# Export environment #
vagrant_base='/opt/Vagrant'
database=${vagrant_base}/address.db
vms=('deploy-dev' 'deploy-pro')
os="ubuntu/xenial64"
id_net="192.168.33."
last_id_host=$(cat $database|tail -1|cut -d "." -f4)
id_host=$(expr $last_id_host + 1)

# Set colours #
#Num  Colour
#0    black
#1    red
#2    green
#3    yellow
#4    blue
#5    magenta
#6    cyan
#7    white

magenta=$(tput setaf 5)
green=$(tput setaf 2)
unset_color=$(tput sgr0)

for vm in ${vms[@]};
do
	# Create new vm #
	echo -e "\n${magenta}[$(date)]\tDeploying a new $vm machine...${unset_color}"
	cd $vagrant_base
	mkdir $vm && echo -e "${green}[$(date)]\tMade $vm base directory...${unset_color}"
	cd $vm
	vagrant init $os && echo -e "${green}[$(date)]\t$vm created!${unset_color}"

	# Set ip address #
	echo -e "${green}[$(date)]\tSetting ip address...${unset_color}"
	sed -i s/'# config.vm.network "private_network", ip: "192.168.33.10"'/"config.vm.network \"private_network\", ip: \"${id_net}${id_host}\""/ Vagrantfile \
	&& echo -e "${green}[$(date)]\tIP address (${id_net}${id_host}) assigned!${unset_color}"

	# Register new vm #
	echo -e "${green}[$(date)]\tRegistering new virtual machine in $database...${unset_color}"
	echo "$vm,${id_net}${id_host}" >> ${database} && echo -e "${green}[$(date)]\tvm registered!${unset_color}"

	# Start new vm #
	echo -e "${green}[$(date)]\tStarting new $vm virtual machine...${unset_color}"
	vagrant up 

	# Configure new vm #
	echo -e "${green}[$(date)]\tSetting locale...${unset_color}"
	vagrant ssh -c "sudo locale-gen es_ES.UTF-8"
	echo -e "${green}[$(date)]\tChanging the name to the vm...${unset_color}"
	vagrant ssh -c "sudo sed -i s/127.0.1.1/${id_net}${id_host}/ /etc/hosts"
	vagrant ssh -c "sudo sed -i s/ubuntu-xenial/$vm/g /etc/hosts"
	vagrant ssh -c "sudo sed -i s/ubuntu-xenial/$vm/g /etc/hostname"
	vagrant ssh -c "sudo hostname $vm"

	id_host=$(expr $id_host + 1)
done
