---
layout: post
title: "Install vsftpd on Ubuntu"
date: 2013-07-31 08:51
comments: true
author: Reno
categories: [Ubuntu, Linux, Software]
---


1. sudo apt-get install vsftpd
2. change config: /etc/vsftpd.conf
2. anonymous_enable=NO
3. local_enable=YES
4. write_enable=YES
5. sudo service vsftpd restart

Client:

	If you are using Yummy FTP, you may have trouble get file list from ftp server. Try go to Preference, and go to Server Options, unselect ""Default to Passive FTP"