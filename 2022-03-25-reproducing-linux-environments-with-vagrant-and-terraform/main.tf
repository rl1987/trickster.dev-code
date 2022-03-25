terraform {
  required_providers {
    digitalocean = {
      source  = "digitalocean/digitalocean"
      version = "~> 2.0"
    }
  }
}

provider "digitalocean" {
  token = file("do_token.txt")
}

resource "digitalocean_droplet" "n8n" {
  image  = "debian-11-x64"
  name   = "n8n"
  region = "sfo3"
  size   = "s-1vcpu-1gb"
  # Make sure this matches your SSH key fingerprint at:
  # https://cloud.digitalocean.com/account/security
  ssh_keys = ["[REDACTED]"]

  connection {
    host        = self.ipv4_address
    user        = "root"
    type        = "ssh"
    timeout     = "2m"
    private_key = file("~/.ssh/id_rsa")
  }

  provisioner "remote-exec" {
    script = "provision.sh"
  }
}

output "server_ip" {
  value = resource.digitalocean_droplet.n8n.ipv4_address
}

