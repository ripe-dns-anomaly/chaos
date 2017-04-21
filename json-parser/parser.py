#!/usr/bin/python3

from ripe.atlas.sagan import DnsResult
import json
from f4570above  import f4570above
import sys



#open file 
inputFile=str(sys.argv[1])
outputFile=str(sys.argv[2])

#open file 
f=open(inputFile, 'r')
f2=open(outputFile,'a')


#create a measurement
measurements = json.load(f)     

#DNS measurements on RIPE -- the root ones are no market as "resolve on probe" 
#what does it mean?
#https://www.mail-archive.com/ripe-atlas@ripe.net/msg00166.html
#Quick mental counting suggests that there are 3 different options:
#1) if resolve-on-probe is not set, the target is resolved by the Atlas
#backend and the probe only gets the IP address. The (glibc) stub
#resolver on CentOS does not do any case mangling.
#2) if resolve-on-probe is set then the probe resolves the target using
#the stub resolver in libevent. This stub resolver mangles the case.
#3) for DNS measurements, the domain name parameter is used as is.
#However the target of the measurement is subject to case 1 or 2.

#therefore, the flow as is follows: the probe send a DNS request to the Atlas backend, and then gets an IP address, which is 


#there are various types of errors that can occur with a DNS request
#The first type is when the message does not make it to the root server, so it timesouts
#To address it, we set all response values to -1 by default; and they reamin as it it

#The second type is when the it makes to the server buy somegoes wrong:
#it can get servfail, refused, then we have to print the "Status of the response"
#Is it RDATA? let's try

#determine which version
f2.write("#src_ip,dst_ip,proto, dst_name, rtt,prb_id, timestamp,rcode\n")
for m in measurements:

    fw = m["fw"]
    typeMeasurement=m["type"]
    #print(str(fw)) 
    
    #The data structure of each result contains the key fw which identifies the firmware version used by the probe that generated that result.

    #Version 1 is identified by the value "1".
    #Version 4400 is identified by a value of between "4400" and "4459".
    #Version 4460 is identified by a value of between "4460" and "4539".
    #Version 4540 is identified by a value of between "4540" and "4569".
    #Version 4570 is identified by a value of between "4570" and "4609".
    #Version 4610 is currently the most recent version of the datastructure documentation. At the moment any value greather than 4570 conforms to the 4570 documentation.
    #An upper limit to this version will added with the release of a firmware version that changes the datastructures.
    
    
    if (int(str(fw))>=4570 and str(typeMeasurement=="dns")):
     x = f4570above(m)
     
     temp = x.answers
     
     #print(len(temp))
     targetServer=""
     for k in temp:
       targetServer=k.RDATA
       #print(targetServer)
       #targetServer=k.dst_name
       
       ##print(k.RDATA)
       #print(str(targetName.MNAME))
       
     
     #f2.write(str(x.From) + "," + str(x.dst_addr) + "," + str(x.proto)+ "," +  str(targetServer) + "," + str(x.rt) + "," + str(x.prb_id) + "," + str(x.timestamp)+"," + str(x.rcode)+"\n")
     f2.write(str(x.prb_id) + " " + str(targetServer) + " " + str(x.rt) + " " + str(x.rcode) + "\n")
     
      
    
f.close()
f2.close()

#add your own thing
# this is just the beginning, if you have to accoutn for FIRMWARE VERSION (will do it, gio)
#https://atlas.ripe.net/docs/data_struct/
#then, we need to know what measuremnets and what fields to extract
