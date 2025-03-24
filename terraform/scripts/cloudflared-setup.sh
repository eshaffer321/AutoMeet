#!/bin/bash

set -e  # Stop script on error

TUNNEL_SECRET=$1

if [ -z "$TUNNEL_SECRET" ]; then
  echo "Error: No tunnel secret provided!"
  exit 1
fi

echo "Downloading cloudflared"
curl -L --output cloudflared.deb https://github.com/cloudflare/cloudflared/releases/latest/download/cloudflared-linux-amd64.deb && 
sudo dpkg -i cloudflared.deb

sudo cloudflared service install $TUNNEL_SECRET
