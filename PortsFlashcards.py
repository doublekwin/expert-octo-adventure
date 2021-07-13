import random

class flashcard:
    def __init__(self):

        self.ports={'http(Hyper Text Transfer Protocol) is what port?':'80 tcp',
                    'https(Hyper Text Transfer Protocol secure   SSL/TLS is what port?':'443 tcp',
                    'ssh, scp, sftp is what port?':'22 tcp/udp',
                    'telnet is what port?':'23 tcp/udp',
                    'ftp is what port?':'21 tcp',
                    'SMTP(Simple Mail Transfer Protocol) is what port?':'25 tcp',
                    'DNS(Domain Name Service) is what port?':'53 tcp/udp',
                    'TFTP(simplified version of FTP to put a file on a remote host or reverse) is what port?':'69 UDP',
                    'Kerberos(a system of tickets within a windows domain) is what port?':'88 tcp/udp',
                    'POP3(post office protocol mail server) is what port?':'110 tcp',
                    'NNTP(Network News Transfer Protocol  transport news articles is what port?':'119 tcp',
                    'RPC/DCOM-scm(REmote Procedure Call  com to com connection is what port?':'135 tcp/udp',
                    'NetBIOS  NetBIOS connection to send data is what port?':'137-139 tcp/udp',
                    'IMAP(Internet Message Access Protocol  receive email from mail server is what port?':'143 tcp',
                    'SNMP(Simple Network Management Protocol used to remotely monitor network devices is what port?':'161 udp',
                    'SNMPTRAP used to send trap and informrequests to the SNMP Manager is what port?':'162 tcp/udp',
                    'LDAP(lightweight directory access protocol maintain directories of users is what port?':'389 tcp/udp',
                    'SMB(Server Message Block provide shared access to files on network is what port?':'445 tcp',
                    'SMTP with SSL/TLS secured is what port?':'465/587 tcp',
                    'Syslog(Syslog is used to conduct computer message logging for routers and firewall is what port?':'514 udp',
                    'LDAP(lightweight directory access protocol maintain directories of users however secured is what port?':'636 tcp/udp',
                    'iSCSI   linking data storage facilities over IP is what port?':'860 tcp',
                    'FTPS  File Transfer Protocol Secure is what port?':'989/990 tcp',
                    'IMAP4 with SSL/TLS':'993 tcp',
                    'POP3 SSL/TLS':'995 tcp',
                    'Ms-sql-s     Microsoft SQL server is used to receive SQL database queries from clients':'1443 tcp',
                    'Radius   Remote Authentication Dial in user service is used for authentication and authorization  Accounting 1646':'1645/1646 udp',
                    'L2TP  layer 2 tunnel protocol is used as an underlying VPN Protocol but has no inherent security':'1701 udp',
                    'point to point tunneling protocol is an underlying VPN protocol with built in security':'1723 tcp/udp',
                    'Default RADIUS    ':'1812/1813 udp',
                    'FCIP   Fibre channel IP is used to encapsulate fibre channel frames with TCP/IP packets':'3225 tcp/udp',
                    'iSCSI Target     listening port for iSCSI when linking data storage over IP':'3260 tcp',
                    'RDP  Remote Desktop Protocol to remotely view and control other windows systems via Graphical user interface':'3389 tcp/udp',
                    'Diameter   A more advanced AAA protocol that is a replacement for RADIUS':'3368 tcp',
                    'Syslog over TLS   messaging log over a TLS encrypted connection':'6514 tcp'}

    def quiz(self):
        while (True):
            
            ports, numb = random.choice(list(self.ports.items()))

            print("What is the port of {}".format(ports))
            user_answer = input()

            if(user_answer.lower() == numb):
                print("Correct answer")
            else:
                print("Wrong answer")
                print("\n" + "The correct answer is:" + ports + numb + "\n")

            option = int(input("enter 0 , if you want to play again : "))
            if (option):
                break
print("Weclome to Ports Quiz")
fc=flashcard()
fc.quiz()