#!/bin/bash
set -e

# 1. Uninstall any old versions (if any)
echo "Uninstall old versions of docker"
sudo apt-get remove -y docker || true
sudo apt-get remove -y docker-engine || true
sudo apt-get remove -y docker.io || true
sudo apt-get remove -y containerd || true
sudo apt-get remove -y runc || true

# 2. Update the apt package index and install dependencies
echo "Updating package index and installined dependencies"
sudo apt-get update
sudo apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# 3. Add Docker’s official GPG key
echo "Adding dockers gpg key"
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 4. Set up the stable repository
echo "Setting up repository"
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Update the apt package index again
echo "Updating back index (second time)"
sudo apt-get update

# 6. Install Docker CE, CLI, and containerd
echo "Installing docker"
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 7. Verify Docker installation
sudo docker run hello-world

# 8. Install Docker Compose (v2)
# Download the latest stable release (update version as needed)
COMPOSE_VERSION="v2.29.7"  # Adjust this version if needed
sudo curl -L "https://github.com/docker/compose/releases/download/${COMPOSE_VERSION}/docker-compose-$(uname -s)-$(uname -m)" -o /usr/local/bin/docker-compose

# 9. Apply executable permissions to the binary
sudo chmod +x /usr/local/bin/docker-compose

# 10. Verify Docker Compose installation
docker-compose --version

# 11. Install cloudflared
echo "Downloading cloudflared"
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && 
sudo dpkg -i cloudflared.deb