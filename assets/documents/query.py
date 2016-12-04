#script for making and documenting DNS queries implemented in Python 2.7

"""
    dns_search
    
    DNS search and debug tool implemented in Python for the sake of recording debugging
    information and non-standard DNS responses. This script was designed to make poisoned 
    DNS responses easier to detect and record. This version looks at a variety of sites, with two
    control sites to see what a normal DNS would look like.
    
    Connor Dittmar 2016
"""
from datetime import datetime
from os.path import exists
import dns.resolver
import socket


def make_log_file():
    #all this does is increment the log file name so I don't overwrite data
    counter = 0
    while(1):
        filename = "logs\DNS_log%d.txt" % counter
        if exists(filename)==True:
            counter = counter+1
        else:
            return filename




host = socket.gethostname()
IP = socket.gethostbyname(host)

resolver = dns.resolver.Resolver()

resolver.timeout = 5

nameservers = 'gjjline.bta.net.cn'

domains = [
    'google.com',
    'facebook.com',
    'imgur.com',
    'gmail.com',
    'baidu.com',
    'weibo.com'
]

print "Opening log file..."

logfile = open(make_log_file(), 'w')
print "Success."

print "DNS query:"
for i in range(0,len(domains)):
    try: answers = resolver.query(domains[i], 'A',raise_on_no_answer=False)
    except: answers = ['timeout']
    for rdata in answers:
        print "Query: '%s' Response: %s" % (domains[i], rdata)
        date = datetime.now()
        logdata = "Server: %s \nAddress: %s \nDate: %s \nTime: %s \nQuery: '%s' \nRdata: %s"\
        % (nameservers, resolver.nameservers, date.strftime('%d%b%y'),
            date.strftime('%H:%M:%S'), domains[i], rdata)
        logfile.write(logdata)
        logfile.write("\n\n")
logfile.close()
