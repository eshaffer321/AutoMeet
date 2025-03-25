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
    source      = "${path.module}/scripts/setup.sh"
    destination = "/root/setup.sh"
  }

  provisioner "remote-exec" {
    inline = [
      "chmod +x /root/setup.sh",
      "/root/setup.sh",
    ]
  }

  provisioner "remote-exec" {
    inline = [
      "mkdir -p /etc/cloudflared",
      "echo ${var.cloudflare_tunnel_base64_cred} > /etc/cloudflared/hetzner.json",
      "cat /etc/cloudflared/hetzner.json | xargs cloudflared service install",
      "systemctl restart cloudflared"
    ]
  }
}

resource "hcloud_ssh_key" "default" {
  name       = "default-key"
  public_key = file("~/.ssh/id_hetzner.pub")
}

resource "hcloud_ssh_key" "github_action" {
  name = "github_action_key"
  public_key = file("~/.ssh/github_autodeploy.pub")
}

resource "hcloud_firewall" "default" {
  name = "server-firewall"

  rule {
    direction  = "in"
    protocol   = "tcp"
    port       = "22"
    source_ips = ["0.0.0.0/0"]
  }
}