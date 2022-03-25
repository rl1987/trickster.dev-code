#!/bin/bash

set -x

apt-get update

curl -fsSL https://deb.nodesource.com/setup_17.x -o /tmp/install_node.sh
bash /tmp/install_node.sh
apt-get install -y gcc g++ make nodejs

curl -sL https://dl.yarnpkg.com/debian/pubkey.gpg | gpg --dearmor | sudo tee /usr/share/keyrings/yarnkey.gpg >/dev/null
echo "deb [signed-by=/usr/share/keyrings/yarnkey.gpg] https://dl.yarnpkg.com/debian stable main" | sudo tee /etc/apt/sources.list.d/yarn.list
apt-get update 
apt-get install -y yarn

npm install n8n -g
npm install pm2 -g

pm2 start n8n
pm2 startup
pm2 save
