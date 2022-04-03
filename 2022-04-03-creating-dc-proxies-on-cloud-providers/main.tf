terraform {
  required_providers {
    vultr = {
      source  = "vultr/vultr"
      version = "2.10.1"
    }
  }
}

provider "vultr" {
  # Setting api_key is not required if VULTR_API_KEY environment variable is present with API key value.
  #api_key = "[REDACTED]"
}

resource "vultr_ssh_key" "my_ssh_key" {
  name    = "my-ssh-key"
  ssh_key = file("~/.ssh/id_rsa.pub")
}

variable "proxy_count" {
  default = 8
}

resource "vultr_instance" "proxy" {
  count       = var.proxy_count
  plan        = "vc2-1c-1gb"
  region      = "sea"
  os_id       = 477
  ssh_key_ids = [vultr_ssh_key.my_ssh_key.id]
  user_data   = file("provision.sh")
}

output "proxy_ip" {
  value = ["${vultr_instance.proxy.*.main_ip}"]
}
