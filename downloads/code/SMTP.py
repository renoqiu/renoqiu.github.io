from socket import *
import sys
import ssl
import base64
import getpass

msg="\r\n I love computer networks!"
endmsg="\r\n.\r\n"

# choose a mail server (e.g. a Google server) and call it mailserver
mailserver = "smtp.gmail.com"
print "Welcome to Gmail..."
print "Gmail requires your user account to send mail."
username = raw_input("Your Gmail Address: ")
print "HINT: When you input your password, it will not echo back..."
password = getpass.getpass()
# create socket called clientSocket and establish a TCP connection with mailserver
clientSocket = None
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
except error, msg:
    print 'Create Socket Error. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();


#Fill in start  
try:
    remote_ip = gethostbyname(mailserver)
except gaierror:
    # could not resolve
    print "Coule Not Find Server: %s. Exiting..." % mailserver
    sys.exit()

#print 'Ip address of ' + mailserver + ' is ' + remote_ip

port = 587

clientSocket.connect((remote_ip , port))
print 'Socket Connect Successed...'

#Fill in end

recv=clientSocket.recv(1024)

print recv

if recv[:3]!='220':
    print '220 reply not received from server.'


#Send HELO command and print server response.

heloCommand='HELO Alice\r\n'


clientSocket.send(heloCommand)

recv1=clientSocket.recv(1024)

print recv1

if recv1[:3]!='250':
    print '250 reply not received from server.'

#Send MAIL FROM command and print server response.

#Fill in start
command = "STARTTLS\r\n"
print "STARTTLS"
clientSocket.send(command)
recvdiscard = clientSocket.recv(1024)
print recvdiscard

clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

authCommand='AUTH LOGIN\r\n'
print "AUTH LOGIN"
clientSocket.send(authCommand)
recv1=clientSocket.recv(1024)
print recv1

loginCommand = base64.b64encode(username)+'\r\n'
clientSocket.send(loginCommand)
recv1=clientSocket.recv(1024)
print recv1

loginCommand = base64.b64encode(password)+'\r\n'
clientSocket.send(loginCommand)
recv1=clientSocket.recv(1024)
print recv1

command = "MAIL FROM: <%s>\r\n" % username
clientSocket.send(command)
print command
recv1 = clientSocket.recv(1024)
print recv1

#Fill in end


#Send RCPT TO command and print server response.

#Fill in start
dest_email = "734589640@qq.com"
command = "RCPT TO: <%s>\r\n" % dest_email
clientSocket.send(command)
print command
recv1 = clientSocket.recv(1024)
print recv1

#Fill in end


#Send DATA command and print server response.

#Fill in start
command = "DATA\r\n"
clientSocket.send(command)
print command
recv1 = clientSocket.recv(1024)
print recv1

#Fill in end


#send message data.

#Fill in start
SUBJECT = "From Han Tang"
TEXT = msg + endmsg
message = """\
From: %s
To: %s
Subject: %s

%s
""" % (username, dest_email, SUBJECT, TEXT)
clientSocket.send(message)
print command
recv1 = clientSocket.recv(1024)
print recv1


#Fill in end


#message ends with a single period.

command = ".\r\n"
clientSocket.send(command)
print command
recv1 = clientSocket.recv(1024)
print recv1

#Fill in start


#Fill in end


#send QUIT command and get server response.

#Fill in start
command = "QUIT\r\n"
clientSocket.send(command)
print command
recv1 = clientSocket.recv(1024)
print recv1

#Fill in end
