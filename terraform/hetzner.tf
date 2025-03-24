resource "hcloud_server" "server" {
  name        = "automeet-server"
  server_type = "cpx21" # 3 vCPUs, 4GB RAM
  image       = "ubuntu-22.04"
  location    = "hil"
  ssh_keys    = [hcloud_ssh_key.default.id]

  firewall_ids = [hcloud_firewall.default.id]

  connection {
    type        = "ssh"
    user        = "root"
    private_key = file("~/.ssh/id_hetzner")
    host        = self.ipv4_address
  }

  provisioner "file" {
    source      = "${path.module}/scripts/cloudflared-setup.sh"
    destination = "/root/cloudflared_setup.sh"
  }

  provisioner "file" {
    source      = "${path.module}/scripts/nginx.sh"
    destination = "/root/nginx.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /root/cloudflared_setup.sh",
      "/root/cloudflared_setup.sh '${base64encode(jsonencode({
        a = var.cloudflare_account_id
        t = cloudflare_zero_trust_tunnel_cloudflared.hetzner_tunnel.id
        s = random_id.tunnel_secret.b64_std
      }))}'",
      # "chmod +x /root/nginx.sh",
      # "/root/nginx.sh"
    ]
  }
}

resource "hcloud_ssh_key" "default" {
  name       = "default-key"
  public_key = file("~/.ssh/id_hetzner.pub")
}

resource "hcloud_firewall" "default" {
  name = "server-firewall"

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "22"
    source_ips = ["0.0.0.0/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "80"
    source_ips = ["0.0.0.0/0"]
  }

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "443"
    source_ips = ["0.0.0.0/0"]
  }
}