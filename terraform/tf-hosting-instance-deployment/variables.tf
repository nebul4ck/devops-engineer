# Define authentication variables #
variable "client_ID" {
  description = "The WHMCS Client ID."
  type        = string
  default     = "4925"
}

variable "product_ID" {
  description = "The WHMCS Product ID."
  type        = string
  default     = "10752"
}

variable "domain" {
  description = "The main domain of the client. Use '-' instead of '.'. ie zaalc-com"
  type        = string
  default     = "bar-com"
}

variable "lg_project" {
  description = "The project for which the instance will be deployed. hosting for instance of client and intranet for instance with lg purpose (internal servers)."
  type        = string
  default     = "hosting"
}

variable "root_volume_size" {
  description = "Set the size that the instance model has. ie 'b2-60-flex' = 400GB SSD."
  type        = number
  default     = 400
}

variable "home_size" {
  description = "The size of the /home volume storage."
  type        = number
  default     = 200
}

variable "key_pair" {
  description = "The name of the key pair to use for instance access."
  type        = string
  default     = "bar-foo"
}

variable "flavor" {
  description = "The flex instance model (ever use '-flex' suffix). ie b2-15-flex"
  type        = string
  default     = "b2-15"
}

variable "image_os" {
  description = "The name of the OS image to use."
  type        = string
  default     = "Ubuntu 21.04"
}
