#!/usr/bin/python3

from ripe.atlas.sagan import DnsResult
import json


class 4570above():
   
   def __init__(self, m):
        
     #parse it here
          
     #https://atlas.ripe.net/docs/data_struct/#v4570
     fw=m["fw"] # firmware version 
     
     af=-1
     try:
       af= m["af"]#"af" -- [optional] IP version: "4" or "6" (int)
       break
     except ValueError:
       print("Measurement does not have af")
       
     
     dst_addr=m["dst_addr"]# -- [optional] IP address of the destination (string)
     dst_name=m["dst_name"]# -- [optional] hostname of the destination (string)

