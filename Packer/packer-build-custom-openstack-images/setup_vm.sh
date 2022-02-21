#!/bin/bash

set -ex

if [ `id -u` -ne 0 ]; then
     sudo $0
    exit 0
fi

## Customize image ##

# Install Ansible
echo -e "INFO: Installing Ansible..."
apt install ansible -y \
&& echo -e "INFO: OK, Ansible was installed."

# Configure ssh client in order to login as root@localhost
echo -e "INFO: Configure root authorized keys with lg_master_root_rsa..."
ssh-keygen -t rsa -b 2048 -C 'local_root_rsa' -N '' -f /root/.ssh/id_rsa
cat /root/.ssh/id_rsa.pub >> /root/.ssh/authorized_keys
cat <<EOF > /root/.ssh/config
# Defaults
StrictHostKeyChecking no

EOF
echo -e "INFO: OK, ssh client root@localhost configured."

# Configure rundeck RSA
echo -e "INFO: Configure root RSA with rundeck RSA KEY..."
cat <<EOF >> /root/.ssh/rundeck_rsa
-----BEGIN RSA PRIVATE KEY-----
MIIEpAIBAAKCAQEAv72D6GuGN54MQjcSFqiLZ2JLWegWDwoc0Fn+W2gi2yAa9Btr
oKxdzBDSRdl36JQ9hmaNyia/o5lD8khtHre9Ej6dR1PuxoqjqwzJvT4S/uEdV2ul
rAwkMP4wlxr6T47tXGDcJmtzG1g6EIFsESxuAdeMe4DVpgEB3t7RYF4HZoDdNydB
/6Vpycz5e4t4E56tedCKOcQOg8MJc/Lp1d4zec/ZKfQfhPPkogT9ZlvfRV6b3yq1
S/hmwDDfiJC4VE2lerVX9ows+v9WqPlaMBLAPzx7Ra9u0+fXrxqzUEHsL1ejLUn5
yZ1Pu4HSq3jlocjzvoiOeRyP22DY5VePm1LRKwIDAQABAoIBAAnWDQhFS9NalkJn
VNQ4vT4GetsX3tnSqPu/Qh8qTm9zTC6toW3SqdUoH8FZkJ8ry6Qzap6uMjKQUD4D
nSVwQ5DGCYd5NMyWnCLQOyEsKAlPPxQW/5692LVytMdrqN+f82lDxsdpx7PlaMUj
/ok7AEGz7w7+4vbrIk9umssYx8RoTS7F78/u2CB4EyvrKNGjw8SGepXhi6Z4IGLN
uOsJMA0K4VolE7LCWfrDe5S3AoTrTWuNw+dCb7eQgXbHh1Gvd+WLyZljqAv0MOwL
SVottrj0ex9mUzxRCu/4U7LBfH8Ylm6xqZ3aTlwpbScugHcOWgaF/QL8vV3aljCs
Ihjt3FECgYEA6JmjQApe6p3dtxU/2SXFSUdF1Hrr/6oZIbd4AUD7YOc+6dMyTg6U
Qg7Incny/2x5DatPbCt0ZNCxzSEvXkKQsouwoCl1yBx16j5ivJFlsUIO7VRlU5F5
HAiJqkVasw7SY8yDIthl1omXBHBaZjTi72VStFK/I8cLS9buKbIop10CgYEA0weT
piMQlNlgvjZMeniKjNY8MiOmcnJtiHvmmVU4eq75OUYf8hCjzguWC9YVLE1pkLnv
H+475l70tseNWzH2suT9xxfEM0CX+gdHeIBw/NDFE9CWz/quwHJjEaQEXhbX+iQB
cp6uZVyTI3eayyW3fHBbgNVdjCrgb7h+z/nreicCgYEA1Pde3pLgRwaV6zy8gfCw
SyDD0gFeNW8jpZhbeyJpR1dTZjnmFEwK+NSaYMZ4A9/oklho1syOvIPMV9nrie1+
mMuHw41Sdw9/8yJ9utORfZPTIP+l6rcGYWF70ne/zLRkc9Xbt7rUu3Ks3/aS/oOr
yK9H4yzkLzjeoei/lVO3H00CgYEAz3IbSq4dlrU5zMJD3ACy8k+HTSKOdOLXmdty
jDiiFLf8drjgnmyNGfd5wJjqp2pR49tjndfrOkMN/L+dzZAIG0PP1O8gB+Hvg/Gz
6FkauOvhT+E0365mKvhHOwgo4vVByruqUKp8dVfTrIHewOSKwuEQkk0scKWViz2q
K3haavECgYBUstiamcO5eO+ZzNJqwGRcjWUbqZqKw5PbXlgPKXf6GYRRNf36OfSO
uPf00PLt6EhX2olwhFItLk8sr7M58xniI47UXGcyR2oSprCvDbw6tsfKRy9/J8hG
giK4fr+MChdZhJHCL8g0T4EoAJas4I8PRMBUSiqKy6nbJP2l8GcTdg==
-----END RSA PRIVATE KEY-----
EOF
chmod 0400 /root/.ssh/rundeck_rsa
eval "$(ssh-agent -s)"
ssh-add /root/.ssh/rundeck_rsa
echo -e "INFO: OK, rundeck RSA KEY was installed."

# Install and configure git
echo -e "INFO: Installing and configuring Git..."
apt install git -y
git config --global core.sshCommand 'ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no'
cat <<EOF >> /root/.ssh/config
# Work GitHub: rundeck account
Host github.com
 HostName github.com
 User git
 AddKeysToAgent yes
 IdentitiesOnly yes
 IdentityFile /root/.ssh/rundeck_rsa
EOF
echo -e "INFO: OK, Git was installed and configured."

# git clone Ansible repository
echo -e "INFO: Clonning ansible git repository..."
mkdir -p /root/git
git clone git@github.com:LINEA-GRAFICA/packer-hosting-instance-provisioner.git /root/git/packer-hosting-instance-provisioner \
&& echo -e "INFO: OK, Ansible Git repository was clonned."

# Configure Ansible
echo -e "INFO: Configuring Ansible..."
cat <<EOF >> /root/.ansible.cfg
[defaults]
python_interpreter=auto
deprecation_warnings=False
# SSH timeout
timeout = 120
log_path = /var/log/packer-hosting-instance-provisioner.log
nocolor = 0
EOF

echo "localhost" > /root/git/packer-hosting-instance-provisioner/hosts \
&& echo -e "INFO: OK, Ansible was configured."

# run common role
echo -e "INFO: Play ansible common provisioner role..."

# Tags: the module which the program will run.
# Extra Vars: variables needed in order to deploy all ansible modules.
#   ipFailover: the ip that was attached to thhe new server.
#   cloud_provider: the cloud provider (ovh or aws).
#   client_alias: the main domain of the client (ej, glowrias.com, sinhumo-sevilla.net, etc..).
#   serverFQDN: the fqdn of the host (ej, hosting-2557-10286-cloud.lineagrafica.es).
#   hostnameTarget: the short hostname without domain (ej, hosting-2557-10286-cloud).
#   mainDomain: lineagrafica.es (by default).
#   productID: the ID of the product, see the whmcs product URL.
ansible-playbook -i /root/git/packer-hosting-instance-provisioner/hosts /root/git/packer-hosting-instance-provisioner/packer-hosting-instance-provisioner.yml \
    -u root \
    --tags "system,\
    packages,\
    environment,\
    rsa,\
    directadmin" && \
    echo -e "INFO: OK, Ansible common role was played without errors."