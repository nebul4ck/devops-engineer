# Install and Configure SSH Client

## Run the ansible playbook

```
$ cd ansible-role
$ ansible-playbook ssh-client.yaml \
    -K \
    --tags install_packages,configure
SUDO password: 

```
