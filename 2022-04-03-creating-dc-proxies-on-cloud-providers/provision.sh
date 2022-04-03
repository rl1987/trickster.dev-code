#!/bin/bash

apt-get update
apt-get install -y squid apache2-utils

systemctl enable squid

# Based on: https://stackoverflow.com/questions/3297196/how-to-set-up-a-squid-proxy-with-basic-username-and-password-authentication
sed -i 's/http_access deny all//' /etc/squid/squid.conf
echo "auth_param basic program /usr/lib/squid3/basic_ncsa_auth /etc/squid/passwords" >> /etc/squid/squid.conf
echo "auth_param basic realm proxy" >> /etc/squid/squid.conf
echo "acl authenticated proxy_auth REQUIRED" >> /etc/squid/squid.conf
echo "http_access allow authenticated" >> /etc/squid/squid.conf

htpasswd -bc /etc/squid/passwords user trust_no_1

systemctl reload squid

ufw disable
