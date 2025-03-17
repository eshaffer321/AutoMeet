terraform {
  required_version = ">= 0.13"
  required_providers {
    b2 = {
      source  = "Backblaze/b2"
      version = "~> 0.2"
    }
  }
}

provider "b2" {
}