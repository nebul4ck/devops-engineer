#!/bin/bash

# // Colors definition
endcolor="\e[0m"

red="\e[31m"
green="\e[32m"
yellow="\e[33m"
magenta="\e[35m"

RED="31"
GREEN="32"
YELLOW="33"
MAGENTA="35"
b_red="\e[1;$${RED}m"
b_green="\e[1;$${GREEN}m"
b_yellow="\e[1;$${YELLOW}m"
b_magenta="\e[1;$${MAGENTA}m"

# Install Ansible
echo -e "$${yellow}$(date "+[%x %X]") - INFO: Installing Ansible...$${endcolor}"
apt install ansible -y \
&& echo -e "$${green}$(date "+[%x %X]") - INFO: OK, Ansible was installed.$${endcolor}"

# Configure ssh client in order to login as root@localhost
echo -e "$${yellow}$(date "+[%x %X]") - INFO: Configure root authorized keys with lg_master_root_rsa...$${endcolor}"
ssh-keygen -t rsa -b 2048 -C 'local_root_rsa' -N '' -f /root/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
cat <<EOF > /root/.ssh/config
# Defaults
StrictHostKeyChecking no

EOF
echo -e "$${green}$(date "+[%x %X]") - INFO: OK, ssh client root@localhost configured.$${endcolor}"

# Configure user RSA
echo -e "$${yellow}$(date "+[%x %X]") - INFO: Configure root RSA with user RSA KEY...$${endcolor}"
cat <<EOF >> /root/.ssh/id_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAv72D6GuGN54MQjcSFqiLZ2JLWegWDwoc0Fn+W2gi2yAa9Btr
oKxdzBDSRdl36JQ9hmaNyia/o5lD8khtHre9Ej6dR1PuxoqjqwzJvT4S/uEdV2ul
rAwkMP4wlxr6T47tXGDcJmtzG1g6EIFsESxuAdeMe4DVpgEB3t7RYF4HZoDdNydB
/6Vpycz5e4t4E56tedCKOcQOg8MJc/Lp1d4zec/ZKfQfhPPkogT9ZlvfRV6b3yq1
RSAz
6FkauOvhT+E0365mKvhHOwgo4vVByruqUKp8dVfTrIHewOSKwuEQkk0scKWViz2q
K3haavECgYBUstiamcO5eO+ZzNJqwGRcjWUbqZqKw5PbXlgPKXf6GYRRNf36OfSO
uPf00PLt6EhX2olwhFItLk8sr7M58xniI47UXGcyR2oSprCvDbw6tsfKRy9/J8hG
giK4fr+MChdZhJHCL8g0T4EoAJas4I8PRMBUSiqKy6nbJP2l8GcTdg==
-----END RSA PRIVATE KEY-----
EOF
chmod 0400 /root/.ssh/id_rsa
eval "$(ssh-agent -s)"
ssh-add /root/.ssh/id_rsa
echo -e "$${green}$(date "+[%x %X]") - INFO: OK, user RSA KEY was installed.$${endcolor}"

# Install and configure git
echo -e "$${yellow}$(date "+[%x %X]") - INFO: Installing and configuring Git...$${endcolor}"
apt install git -y
git config --global core.sshCommand 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
cat <<EOF >> /root/.ssh/config
# Work GitHub: user account
Host github.com
 HostName github.com
 User git
 AddKeysToAgent yes
 IdentitiesOnly yes
 IdentityFile /root/.ssh/id_rsa
EOF
echo -e "$${green}$(date "+[%x %X]") - INFO: OK, Git was installed and configured.$${endcolor}"

# git clone Ansible repository
echo -e "$${yellow}$(date "+[%x %X]") - INFO: Clonning ansible git repository...$${endcolor}"
mkdir -p /root/git
git clone git@github.com:NEBUL4CK/REPO.git /root/git/ansible-auto-hosting-instance-configure \
&& echo -e "$${green}$(date "+[%x %X]") - INFO: OK, Ansible Git repository was clonned.$${endcolor}"

# Configure Ansible
echo -e "$${yellow}$(date "+[%x %X]") - INFO: Configuring Ansible...$${endcolor}"
cat <<EOF >> /root/.ansible.cfg
[defaults]
python_interpreter=auto
deprecation_warnings=False
# SSH timeout
timeout = 120
log_path = /var/log/ansible-auto-hosting-instance-configure.log
nocolor = 0
EOF

echo "localhost" > /root/git/ansible-auto-hosting-instance-configure/hosts \
&& echo -e "$${green}$(date "+[%x %X]") - INFO: OK, Ansible was configured.$${endcolor}"

# Sleep for 5minutes while the Failover IP is moved to the new instance from ovh panel
sleep 300

# run common role
echo -e "$${yellow}$(date "+[%x %X]") - INFO: Play ansible common provisioner role...$${endcolor}"

# Tags: the module which the program will run.
# Extra Vars: variables needed in order to deploy all ansible modules.
#   ipFailover: the ip that was attached to thhe new server.
#   cloud_provider: the cloud provider (ovh or aws).
#   client_alias: the main domain of the client (ej, glowrias.com, sinhumo-sevilla.net, etc..).
#   serverFQDN: the fqdn of the host, ej:
#       - hosting project: hosting-2557-10286-cloud.lineagrafica.es
#       - intranet project: intranet-2557-10286-cloud.lineagrafica.es
#   productID: the ID of the product, see the whmcs product URL.
ansible-playbook -i /root/git/ansible-auto-hosting-instance-configure/hosts /root/git/ansible-auto-hosting-instance-configure/auto-configure-instance.yml \
    -u root \
    --tags "system,\
    network,\
    mount,\
    rsa,\
    environment,\
    packages,\
    inventory,\
    monitoring,\
    keepsafe" \
    --extra-vars \
        "ipFailover=xxx.xxx.xxx.xxx \
        cloud_provider=<provider> \
        client_alias=bar.com \
        serverFQDN=bar.foo.es \
        productID=10752" \
    && echo -e "$${green}$(date "+[%x %X]") - INFO: OK, Ansible common role was played without errors.$${endcolor}"

# Reboot the system
# echo -e "$${green}$(date "+[%x %X]") - INFO: rebooting the system...$${endcolor}"
# shutdown -r now
