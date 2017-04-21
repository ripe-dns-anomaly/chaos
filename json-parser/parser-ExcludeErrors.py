#!/usr/bin/python3

from ripe.atlas.sagan import DnsResult
import json
from f4570above  import f4570above
import sys

inputFile=str(sys.argv[1])

#open file 
f=open(inputFile, 'r')

#create a measurement
measurements = json.load(f)     


#determine which version
print("#src_ip,dst_ip,proto, dst_name, rtt,prb_id, timestamp")
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
    
    
    if (int(str(fw))>=4570 and str(typeMeasurement=="dns") ):
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
       
     
     print(str(x.From) + "," + str(x.dst_addr) + "," + str(x.proto)+ "," +  str(targetServer) + "," + str(x.rt) + "," + str(x.prb_id) + "," + str(x.timestamp))
     
      
    

#add your own thing
# this is just the beginning, if you have to accoutn for FIRMWARE VERSION (will do it, gio)
#https://atlas.ripe.net/docs/data_struct/
#then, we need to know what measuremnets and what fields to extract
