variable "cloudflare_zone_id" {
  type = string
}

variable "cloudflare_account_id" {
  type = string
}

data "cloudflare_zone" "automeet_cc" {
  zone_id = var.cloudflare_zone_id
}

################
# TUNNEL
###############
resource "cloudflare_zero_trust_tunnel_cloudflared" "hetzner_tunnel" {
  account_id    = var.cloudflare_account_id
  name          = "hetzner_tunnel"
  config_src    = "cloudflare"
  tunnel_secret = random_id.tunnel_secret.b64_std
}

resource "cloudflare_dns_record" "tunnel_dns" {
  zone_id = var.cloudflare_zone_id
  name    = data.cloudflare_zone.automeet_cc.name
  type    = "CNAME"
  content = "${cloudflare_zero_trust_tunnel_cloudflared.hetzner_tunnel.id}.cfargotunnel.com"
  proxied = true
  ttl     = 1
}

resource "random_id" "tunnel_secret" {
  byte_length = 32
}

output "tunnel_secret_base64" {
  value = base64encode(jsonencode({
    a = var.cloudflare_account_id
    t = cloudflare_zero_trust_tunnel_cloudflared.hetzner_tunnel.id
    s = random_id.tunnel_secret.id
  }))
  sensitive = true
}

resource "cloudflare_zero_trust_tunnel_cloudflared_config" "tunnel_config" {
  account_id = var.cloudflare_account_id
  tunnel_id  = cloudflare_zero_trust_tunnel_cloudflared.hetzner_tunnel.id
  source     = "cloudflare"

  config = {
    ingress = [{
      hostname = data.cloudflare_zone.automeet_cc.name
      service  = "http://localhost:8000"
      }, {
      service = "http_status:404"
    }]
  }
}
