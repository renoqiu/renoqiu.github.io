from socket import *
import sys
import ssl
import base64
import getpass

msg="\r\n I love Computer Communication Networks!"
endmsg="\r\n.\r\n"

# choose a mail server (e.g. a Google server) and call it mailserver
mailserver = "smtp.gmail.com"
print "Welcome to Gmail..."
print "Gmail requires your user account to send mail."
username = raw_input("Your Gmail Address: ")
print "HINT: When you input your password, it will not echo back..."
password = getpass.getpass()

clientSocket = None
try:
    clientSocket = socket(AF_INET, SOCK_STREAM)
except error, msg:
    print 'Create Socket Error. Error code: ' + str(msg[0]) + ' , Error message : ' + msg[1]
    sys.exit();

print "Creating Socket Succeeded."
print "About to get %s's ip address." % mailserver
try:
    remote_ip = gethostbyname(mailserver)
except gaierror:
    # could not resolve
    print "Coule Not Find Server: %s. Exiting..." % mailserver
    sys.exit()

print 'Ip address of ' + mailserver + ' is ' + remote_ip

port = 587
clientSocket.connect((remote_ip , port))
print 'Socket Connect Successed...'

recv=clientSocket.recv(1024)

if recv[:3] != '220':
    print '220 reply not received from server.'

print "Server:\t%s" % recv
#Send HELO command and print server response.

heloCommand='HELO Alice\r\n'
print 'Client:\t%s' % heloCommand
clientSocket.send(heloCommand)

recv1=clientSocket.recv(1024)

if recv1[:3]!='250':
    print '250 reply not received from server.'

print "Server:\t%s" % recv1
#Send MAIL FROM command and print server response.

command = "STARTTLS\r\n"
print "Client:\tSTARTTLS"
clientSocket.send(command)
recvdiscard = clientSocket.recv(1024)
print "Server:\t%s" % recvdiscard

clientSocket = ssl.wrap_socket(clientSocket, ssl_version=ssl.PROTOCOL_SSLv23)

authCommand='AUTH LOGIN\r\n'
print "Client:\t%s" % authCommand
clientSocket.send(authCommand)
recv1=clientSocket.recv(1024)
print "Server:\t%s" % recv1

loginCommand = base64.b64encode(username)+'\r\n'
print "Client:\t%s" % loginCommand
clientSocket.send(loginCommand)
recv1=clientSocket.recv(1024)
print "Server:\t%s" % recv1

loginCommand = base64.b64encode(password)+'\r\n'
print "Client:\t%s" % loginCommand
clientSocket.send(loginCommand)
recv1=clientSocket.recv(1024)
print "Server:\t%s" % recv1

command = "MAIL FROM: <%s>\r\n" % username
print "Client:\t%s" % command
clientSocket.send(command)
recv1 = clientSocket.recv(1024)
print "Server:\t%s" % recv1

#Send RCPT TO command and print server response.

#Fill in start
dest_email = "me@renoqiu.com"
command = "RCPT TO: <%s>\r\n" % dest_email
print "Client:\t%s" % command
clientSocket.send(command)
recv1 = clientSocket.recv(1024)
print "Server:\t%s" % recv1

#Send DATA command and print server response.

command = "DATA\r\n"
print "Client:\t%s" % command
clientSocket.send(command)
recv1 = clientSocket.recv(1024)
print "Server:\t%s" % recv1

#send message data.

SUBJECT = "From Dechao Qiu"
TEXT = msg + endmsg
message = """\
From: %s
To: %s
Subject: %s
%s
""" % (username, dest_email, SUBJECT, TEXT)
print "Client:\t%s" % message
clientSocket.send(message)
recv1 = clientSocket.recv(1024)
print "Server:\t%s" % recv1

#send QUIT command and get server response.

command = "QUIT\r\n"
print "Client:\t%s" % command
clientSocket.send(command)
recv1 = clientSocket.recv(1024)
print "Server:\t%s" % recv1
