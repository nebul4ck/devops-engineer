# Packer image provisioner

This ansible role is called from packer image builder ([packer-build-custom-openstack-images](https://github.com/LINEA-GRAFICA/packer-build-custom-openstack-images)) during the image creation.

1. Packer builds a new image: use *packer-build-custom-openstack-images* repository
2. During packer build stage this role is played in order to provisioning the image.
3. Finally when the instance is deployed based on new openstack image (build by packer) a another configure ansible role is played ([ansible-auto-hosting-instance-configure](https://github.com/LINEA-GRAFICA/ansible-auto-hosting-instance-configure))
