---
layout: post
title: "Setup SSH Port Forward"
date: 2013-08-04 20:39
comments: true
categories: [Linux, SSH, Tunnel]
---
# Usefull SSH Command
```ssh -C -f -N -g -L listen_port:DST_Host:DST_port user@Tunnel_Host```

- -f Fork into background after authentication
- -L port:remotehost:remoteport Forward local request of ```localhost:port``` our remote server ```remotehost:remoteport```
- -R port:remotehost:remoteport Forward request from ```remotehost:remoteport``` to our local machine ```localhost:port```
- -D port Use a dynamic port, when there is a connection to this port, the request will be forwarded to our remote host, and the target host is determined by application protocal, [Support SOCKS4] 
- -C Enable compression.
- -N Do not execute a shell or command.
- -g Allow remote hosts to connect to forwarded ports.

# Scenarios
Assume our local machine is A, we have a server B which will forward packets for us. [We have a username/password on Server B]

ip addresses/port: 

- A: localhost:2121
- B: 111.111.111.111
- C: 222.222.222.222

## 1. localhost to remote host
We want to connect to server C's 80 port. Execute the following command:

sudo ssh -f -N -L 2121:222.222.222.222:80 username@111.111.111.111

Then open your browser, type url: localhost:2121, and you will find yourself connected to the web page of server: 222.222.222.222


##  2. remote host to localhost
We want to connect to our local machine A which does not have a public ip. Because of ```NAT```, we can not connect to this local machine from external network. But with ssh, we can create a tunnel which connects A to B. Then we can login our server B which has an external ip address, and then connect to our machine A. Execute the following command on machine A.

ssh -N -f -R 2222:127.0.0.1:22 username@111.111.111.111

This connect machine A's port 22 to server B's 2222 port. Then we can login to our server B, and execute the following command on server B:

ssh -p 2222 localhost

This will connect us to machine A.

# Some tricks
If we do nothing, after some period, our ssh tunnel will disconnect. In order to solve this issue, we can do the following tricks.
## Some important ssh option
	
- -o TCPKeepAlive=yes This will keep our tunnel open.
- We can remove ```-N``` and add some task which will generate output repeatly such as ```vmstat 30``` or ```top```. eg. ```ssh -R 2222:127.0.0.1:22 username@111.111.111.111 "vmstat 30"```
- -o ServerAliveInterval=n -o ServerAliveCountMax=m ```n``` and ```m``` is some number of your choice. These two options are quite important which will make your ssh quit automatically when your ssh get stuck. You may make a monitor script which will restart your ssh after quit.

# Grant access to other machines
Use the above command, we can only access the port in our local machine, what if we give other machine access to this port, we need make it bind to ```0.0.0.0``` instead of ```127.0.0.1```, and set SSH server's ```GatewayPorts yes``` in ```/etc/sshd_config``` file.

# Use SSH tunnel to create SOCKS server
As we can see, we can bind to port like ```22``` and ```80``` separately, but if we want to use our server B to access many other resourse, do we need to create all this port separately, the answer is no. We can use ```-D``` option. The following example does what we want. [PS: SOCK5 Protocol]

- ssh -N -f -D 1080 123.123.123 # Bind to 127.0.0.1
- ssh -N -f -D 0.0.0.0:1080 123.123.123.123 # Bind to 0.0.0.0

# Reference Link
http://blog.creke.net/722.html