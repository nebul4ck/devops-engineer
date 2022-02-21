# Define required provider in order to download the plugins #
terraform {
  required_version = ">= 0.14.0"
  required_providers {
    openstack = {
      source  = "terraform-provider-openstack/openstack"
      version = "~> 1.44.0"
    }
  }
  # backend "swift" {
  #   container         = "terraform-state"
  #   archive_container = "terraform-state-archive"
  # }
}

# Define the provider authentication #
provider "openstack" {
  cloud = "openstack"
}

## Export local env ##

# Export the image name, ej. "Ubuntu 21.04"
data "openstack_images_image_v2" "golden_ami" {
  name = var.image_os
}

# Export cloud-init auto-provisioning template
data "template_file" "user_data" {
  template = file("./cloud-init/ovh-autoprovisioner.sh")
}

## Define the resources to be deployed ##
# 1. Create /home volume for storage
resource "openstack_blockstorage_volume_v2" "home_storage" {
  name        = "${var.lg_project}-${var.client_ID}-${var.product_ID}-${var.domain}-volume"
  description = "Volume for /home storage."
  size        = var.home_size
}

# 2. Create public instance
resource "openstack_compute_instance_v2" "public_instance" {
  name        = "${var.lg_project}-${var.client_ID}-${var.product_ID}-${var.domain}-cloud"
  key_pair    = var.key_pair
  flavor_name = var.flavor
  image_id    = data.openstack_images_image_v2.golden_ami.id
  user_data   = data.template_file.user_data.rendered

  network {
    name = "Ext-Net"
  }

  # Bootable storage device containing the OS
  block_device {
    uuid             = data.openstack_images_image_v2.golden_ami.id
    source_type      = "image"
    destination_type = "local"
    #volume_size           = 400
    boot_index            = 0
    delete_on_termination = true
  }

  # Previously created /home storage device
  block_device {
    uuid                  = openstack_blockstorage_volume_v2.home_storage.id
    source_type           = "volume"
    destination_type      = "volume"
    boot_index            = 1
    delete_on_termination = false
  }

  depends_on = [openstack_blockstorage_volume_v2.home_storage]
}



