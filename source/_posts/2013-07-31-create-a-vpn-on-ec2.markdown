---
layout: post
title: "Create a vpn on ec2"
date: 2013-07-31 18:25
categories: [Linux, VPN, EC2, OpenVPN]
comments: true
categories: 
---
## Server
### Install Packages
1. sudo apt-get install openvpn udev lzop libssl-dev openssl

### copy existing scripts
1. cd /etc/openvpn/
1. sudo mkdir easy-rsa
1. cp -r /usr/share/doc/openvpn/examples/easy-rsa/2.0/* /etc/openvpn/easy-rsa/
1. sudo chown -R $USER /etc/openvpn/easy-rsa/
1. cd /etc/openvpn/easy-rsa/

### Change vars file
1. vi /etc/openvpn/easy-rsa/vars and change to following fields, you need to adjust to your location and email address.

	```
	export KEY_COUNTRY="US"
	export KEY_PROVINCE="CA"
	export KEY_CITY="SanJose"
	export KEY_ORG="renoqiu.com"
	export KEY_EMAIL="me@renoqiu.com"
	export KEY_EMAIL=me@renoqiu.com
	export KEY_CN=renoqiu.com
	export KEY_NAME=Reno
	export KEY_OU=Personal
	export KEY_SIZE=2048
	```

### Generate Certificate Authority File
1. source vars
1. ./clean-all
1. source vars
1. ./build-ca
1. Do as the prompt

### Generate Server Certificate and Key
1. cd /etc/openvpn/easy-rsa/
1. source vars
1. ./pkitool --server server
1. cd keys
1. openvpn --genkey --secret ta.key
1. sudo cp server.crt server.key ca.crt dh2048.pem ta.key /etc/openvpn/
1. ./build-key-server server // ignore this line

### Generate Client Certificate and key
1. cd /etc/openvpn/easy-rsa/
1. source vars
1. Change someuniqueclientcn to a unique name, and change davion to any client name you like.

	```
	KEY_CN=someuniqueclientcn ./pkitool davion
	```
1. cd ..

### Generate Diffie Hellman Parameter
1. ./build-dh # ignore this for now

### Configure OpenVPN Server
1. vi /etc/openvpn/server.conf

	```
	port 443
	proto tcp
	dev tun
	ca /etc/openvpn/easy-rsa/keys/ca.crt
	cert /etc/openvpn/easy-rsa/keys/server.crt
	key /etc/openvpn/easy-rsa/keys/server.key
	dh /etc/openvpn/easy-rsa/keys/dh2048.pem
	server 10.168.1.0 255.255.255.0
	# push "redirect-gateway def1"
	push "redirect-gateway"
	push "dhcp-option DNS 8.8.8.8"
	push "dhcp-option DNS 8.8.4.4"
	client-to-client
	keepalive 10 120
	comp-lzo
	persist-key
	persist-tun
	verb 3
	status openvpn-status.log
	```

### Setup ip forward
1. iptables -t nat -A POSTROUTING -s 10.168.0.0/16 -o eth0 -j MASQUERADE
1. iptables-save > /etc/iptables.rules
1. vi /etc/network/if-up.d/iptables
	
	```
	#!/bin/sh
	iptables-restore < /etc/iptables.rules
	```
1. chmod +x /etc/network/if-up.d/iptables
1. vi /etc/sysctl.conf

	```
	net.ipv4.ip_forward = 1
	net.ipv4.conf.all.send_redirects = 0
	net.ipv4.conf.default.send_redirects = 0
	net.ipv4.conf.all.accept_redirects = 0
	net.ipv4.conf.default.accept_redirects = 0
	```
1. sudo sysctl -p
1. /etc/init.d/openvpn restart
1. /etc/init.d/networking restart

## Client for Mac
1. Install [Tunnelblick](https://sourceforge.net/projects/tunnelblick/files/All%20files/Tunnelblick_3.3.dmg/download):
2. Copy the generated keys from server: 
	- ca.crt
	- client.crt
	- client.key
	- ta.key
3. Create a folder on you Desktop, with name like ```myvpn```
4. Put all above 4 files into the foler
5. Create a text file named: ```config.ovpn```, PS: change ```107.20.217.201``` to your server's ip address.

	```
	client
	dev tun
	proto tcp
	remote 107.20.217.201 443
	resolv-retry infinite
	nobind
	persist-key
	persist-tun
	ca ca.crt
	cert davion.crt
	key davion.key
	ns-cert-type server
	# redirect-gateway
	comp-lzo
	verb 3
	```
6. Change folder ```myvpn``` to ```myvpn.tblk```
7. Double click ```myvpn.tblk``` to install this vpn
8. After install it, on the top right corner you can see a house-like icon, click it and selct ```connect```

## Reference Link
1. http://leapchasm.com/blog/2011/12/07/shearing-firesheep-with-the-cloud/
2. http://www.vpser.net/build/linode-install-openvpn.html