# How create new images automatically

1. Clone the repository
```
git clone git@github.com:LINEA-GRAFICA/packer-build-custom-openstack-images.git
```

2. Create a local project folder, ie:
```
mkdir -p ~/projects/packer/images/b2-15-ubuntu
```

3. Copy the create_custom_image.sh and the setup_vm.sh file inside the new project folder
```
cp ./packer-build-custom-openstack-images/* ~/projects/packer/images/b2-15-ubuntu/
```

4. Edit the value of the variables inside of the ~/projects/packer/images/b2-15-ubuntu/create_custom_images.sh script. The main variables which you must edit are:
```
INSTANCE_FLAVOR
SOURCE_OS_V # Select the latest .04 major version, ie Ubuntu 21.04
```

5. Edit setup_vm.sh in order to customize the image (provisioning).

6. Run the script a new one image will be created
```
cd ~/projects/packer/images/b2-15-ubuntu/; ./create_custom_images.sh
```

Now a new one openstack image is ready for using.

* Get the new image info (from the folder where the clouds.yaml and secure file are):
```
openstack image list | grep ${FINAL_IMAGE_NAME}
```

* In order to delete a image, use the following command:
```
openstack image delete ${FINAL_IMAGE_NAME}
```

**NOTE** deploy a new OVHCloud Hosting instance using the new created image: [tf-hosting-instance-deployment](https://github.com/LINEA-GRAFICA/tf-hosting-instance-deployment)
