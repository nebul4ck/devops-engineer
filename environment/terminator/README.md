# Install and configure Terminator

## Run the ansible playbook

```
$ cd ansible-role
$ ansible-playbook terminator.yaml \
    -K \
    --tags install_packages,configure
SUDO password: 

```