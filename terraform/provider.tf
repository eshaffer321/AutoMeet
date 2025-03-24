terraform {
  required_version = ">= 0.13"
  required_providers {
    b2 = {
      source  = "Backblaze/b2"
      version = "~> 0.2"
    }
    hcloud = {
      source  = "hetznercloud/hcloud"
      version = "~> 1.45"
    }
    cloudflare = {
      source  = "cloudflare/cloudflare"
      version = "5.2.0"
    }
    random = {
      source  = "hashicorp/random"
      version = "3.7.1"
    }
  }
}

provider "b2" {}

provider "hcloud" {}

provider "cloudflare" {}
