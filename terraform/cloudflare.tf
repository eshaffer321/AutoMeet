variable "cloudflare_zone_id" {
  type = string
}

variable "cloudflare_account_id" {
  type = string
}

data "cloudflare_zone" "automeet_cc" {
  zone_id = var.cloudflare_zone_id
}

locals {
  tunnel_hostnames = {
    redis = "redis.${data.cloudflare_zone.automeet_cc.name}"
    web   = "web.${data.cloudflare_zone.automeet_cc.name}"
  }
}

################
# SSH CONFIG
################
resource "cloudflare_dns_record" "ssh" {
  zone_id = var.cloudflare_zone_id
  name    = "automeet-ssh"
  type    = "A"
  content   = hcloud_server.server.ipv4_address
  ttl     = 60
  proxied = false
}

################
# TUNNEL
###############
resource "cloudflare_dns_record" "tunnel_dns" {
  for_each = local.tunnel_hostnames

  zone_id = var.cloudflare_zone_id
  name    = each.value
  type    = "CNAME"
  content   = "${var.cloudflare_tunnel_id}.cfargotunnel.com"
  proxied = true
  ttl     = 1
}

resource "cloudflare_zero_trust_tunnel_cloudflared_config" "tunnel_config" {
  account_id = var.cloudflare_account_id
  tunnel_id  = var.cloudflare_tunnel_id
  source     = "cloudflare"

  config = {
    ingress = [
      {
        hostname = "redis.${data.cloudflare_zone.automeet_cc.name}"
        service  = "tcp://localhost:6379"
      },
      {
        hostname = "web.${data.cloudflare_zone.automeet_cc.name}"
        service  = "http://localhost:8080"
      },
      {
        service = "http_status:404"
    }]
  }
}
