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
  image     = "debian-11-x64"
  name      = "n8n"
  region    = "sfo3"
  size      = "s-1vcpu-1gb"
  user_data = file("provision.sh")
  ssh_keys  = ["[REDACTED]"]
}

output "server_ip" {
  value = resource.digitalocean_droplet.n8n.ipv4_address
}

