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
b_red="\e[1;${RED}m"
b_green="\e[1;${GREEN}m"
b_yellow="\e[1;${YELLOW}m"
b_magenta="\e[1;${MAGENTA}m"

# Export the environment

echo -e "${magenta}==> builder: sourcing environment ...${endcolor}"
export OS_USERNAME="user-REAz4wHwfzFT"
export OS_PASSWORD="qQkusFhDUucbNU1hXMWsSpWtxjkY5P9XV"
export PROJECT_ID="8887d8a3775c4f71a0552da4b8f0e318"
export PROJECT_NAME="4246093315852258"
export OS_REGION_NAME="GRA5"
export OS_AUTH_URL="https://auth.cloud.ovh.net/v3"
export OS_USER_DOMAIN_NAME="Default"
export TENANT_ID="8887d8a3775c4f71a0552da4b8f0e318"
export INSTANCE_FLAVOR="b2-15"
export SOURCE_OS="Ubuntu"
export SOURCE_OS_V="21.04"
export SOURCE_IMAGE_NAME="${SOURCE_OS} ${SOURCE_OS_V}"
export SOURCE_IMG_ID=$(openstack image list -f json | jq -r '.[] | select(.Name == env.SOURCE_IMAGE_NAME) | .ID')
export FLAVOR_ID=$(openstack flavor list -f json | jq -r '.[] | select(.Name == env.INSTANCE_FLAVOR) | .ID')
export NETWORK_ID=$(openstack network list -f json | jq -r '.[] | select(.Name == "Ext-Net") | .ID')
export FINAL_IMAGE_NAME="${INSTANCE_FLAVOR}-${SOURCE_OS}-${SOURCE_OS_V}"

#1. Create clouds.yaml and secure.yaml files
echo -e "${magenta}==> builder: creating clouds.yaml file ...${endcolor}"

cat > clouds.yaml <<EOF
clouds:
  openstack:
    auth:
      auth_url: ${OS_AUTH_URL}
      username: "${OS_USERNAME}"
      project_id: ${PROJECT_ID}
      project_name: "${PROJECT_NAME}"
      user_domain_name: "${OS_USER_DOMAIN_NAME}"
    region_name: "${OS_REGION_NAME}"
    interface: "public"
    identity_api_version: 3
EOF

echo -e "${magenta}==> builder: creating secure.yaml file ...${endcolor}"
cat > secure.yaml <<EOF
clouds:
  openstack:
    auth:
      username: "${OS_USERNAME}"
      password: "${OS_PASSWORD}"
EOF

#2. Delete older image
echo -e "${magenta}==> builder: looking for older image ...${endcolor}"
if [[ $(openstack image list | grep ${FINAL_IMAGE_NAME}) ]];
then
  openstack image delete "${FINAL_IMAGE_NAME}" && \
  echo -e "${magenta}==> builder: older image was deleted.${endcolor}"
else
  echo -e "${magenta}==> builder: no older images found!. Skipping ...${endcolor}"
fi

#3. Create Packer builder json file
echo -e "${magenta}==> builder: creating builder file ...${endcolor}"
cat > ${FINAL_IMAGE_NAME}.json <<EOF
{
    "builders": [
        {
            "type": "openstack",
            "image_name": "${FINAL_IMAGE_NAME}",
            "ssh_username": "ubuntu",
            "source_image": "$SOURCE_IMG_ID",
            "flavor": "$FLAVOR_ID",
            "ssh_ip_version": "4",
            "networks": [
                "$NETWORK_ID"
            ]
        }
    ],
    "provisioners": [
        {
            "script": "setup_vm.sh",
            "type": "shell"
        }
    ]
}
EOF

#4. File validation and deploy
echo -e "${magenta}==> builder: packer json validation ...${endcolor}"
packer validate ${FINAL_IMAGE_NAME}.json && \
echo -e "${magenta}==> builder: building image ...${endcolor}" && \
packer build ${FINAL_IMAGE_NAME}.json

#5. Check if image was created.
echo -e "${magenta}==> builder: check that the image was created ...${endcolor}"
if [[ $(openstack image list | grep ${FINAL_IMAGE_NAME}) ]];
then
  echo -e "${magenta}==> builder: the new image was created successfully.${endcolor}"
else
  echo -e "${magenta}==> builder: error during the image creation. Exiting with errors ...${endcolor}"
  exit 1
fi
