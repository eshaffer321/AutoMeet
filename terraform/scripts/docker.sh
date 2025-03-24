# 1. Uninstall any old versions (if any)
sudo apt-get remove docker docker-engine docker.io containerd runc

# 2. Update the apt package index and install dependencies
sudo apt-get update
sudo apt-get install -y \
  apt-transport-https \
  ca-certificates \
  curl \
  gnupg \
  lsb-release

# 3. Add Docker’s official GPG key
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /usr/share/keyrings/docker-archive-keyring.gpg

# 4. Set up the stable repository
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/docker-archive-keyring.gpg] \
https://download.docker.com/linux/ubuntu $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null

# 5. Update the apt package index again
sudo apt-get update

# 6. Install Docker CE, CLI, and containerd
sudo apt-get install -y docker-ce docker-ce-cli containerd.io

# 7. Verify Docker installation
sudo docker run hello-world