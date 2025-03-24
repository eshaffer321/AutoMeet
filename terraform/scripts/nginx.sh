#!/bin/bash

apt update && apt install -y nginx
cat <<EOF > /etc/nginx/sites-enabled/default
server {
    listen 8000 default_server;
    listen [::]:8000 default_server;

    root /var/www/html;
    index index.html;

    server_name _;

    location / {
        try_files \$uri \$uri/ =404;
    }
}
EOF
systemctl restart nginx
echo "<h1>Tunnel is working</h1>" > /var/www/html/index.html
