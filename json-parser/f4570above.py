#!/usr/bin/python3

from ripe.atlas.sagan import DnsResult
import json
from response4570 import response4570 
import base64
import dns.message


class f4570above():
   
   def __init__(self, m):
        
     #parse it here
          
     #https://atlas.ripe.net/docs/data_struct/#v4570
     self.fw=m["fw"] # firmware version 
     self.af=-1
    
    #"af" -- [optional] IP version: "4" or "6" (int)
     try:
       self.af= m["af"]
       ##print( str(af))
	#break
     except KeyError:
       ##print( "Measurement does not have af")
       pass
     
     self.dst_addr=""
     
     #dst_addr=m["dst_addr"]# -- [optional] IP address of the destination (string)
     try:
       self.dst_addr= m["dst_addr"]
       ##print( str(dst_addr))
     except KeyError:
       ##print( "Measurement does not have dst_addr")
       pass
    
     self.dst_name=""
     
     #dst_name=m["dst_name"]# -- [optional] IP address of the destination (string)
     try:
       self.dst_name= m["dst_name"]
       ##print( str(dst_name))
	#break
     except KeyError:
       ##print( "Measurement does not have dst_name")
       pass
    
     #"error" -- [optional] error message (associative array)
     self.error={}
     self.timeout=-1
     self.getaddrinfo=""
     ##print( "gothere")
     try:
       self.error= m["error"]
       #	"timeout" -- query timeout (int)
       #"getaddrinfo" -- error message (string)
       
       ##print( self.error)	
       if len(self.error) >  0: 
         
          self.timeout=str(self.error['timeout'])
          
          try:
            self.getaddrinfo=str(self.error['getaddrinfo'])
          except KeyError:
            ##print( "Measurement has error, but no getaddrinfo ")
            pass
          ##print( str("whatever"))
	#break
     except KeyError:
       ##print( "Measurement does not have error")
       pass

      ##"from" -- [optional] IP address of the source (string)
      
     self.From=''
     try:
       self.From= m["from"]
       ##print( str(self.From))
	#break
     except KeyError:
       ##print( "Measurement does not have from")
       pass
     
     
      
      #"msm_id" -- measurement identifier (int)
      
      
     self.msm_id=''
     try:
       self.msm_id= m["msm_id"]
       ##print( str(self.msm_id))
	#break
     except KeyError:
       ##print( "Measurement does not have msm_id")
       pass
     
      #"prb_id" -- source probe ID (int)
     
     self.prb_id=''
     try:
       self.prb_id= m["prb_id"]
       ##print( str(self.prb_id))
	#break
     except KeyError:
       ##print( "Measurement does not have prb_id")
       pass
     
      
      #"proto" -- "TCP" or "UDP" (string)
     self.proto=''
     try:
       self.proto= m["proto"]
       ##print( str(self.proto))
	#break
     except KeyError:
       ##print( "Measurement does not have proto")
       pass
      
      #"qbuf" -- [optional] query payload buffer which was sent to the server, UU encoded (string)
     self.qbuf=''
     try:
       self.qbuf= m["qbuf"]
       ##print( str(self.qbuf))
	#break
     except KeyError:
       ##print( "Measurement does not have qbuf")
       pass
     
     self.timestamp=m["timestamp"]
     self.typeM=m["type"]
     self.retry=-1
     
     try:
       self.retry= m["retry"]
       ##print( str(self.retry))
	#break
     except KeyError:
       #print( "Measurement does not have retry")
       pass
     
     
     
     
     
     #here we start to parse the response
     #if there's no answer, all the values are negative, and they're printed as it
     
     self.result={}
     self.ANCOUNT=-1
     self.ARCOUNT=-1
     self.ID=-1
     self.NSCOUNT=-1
     self.QDCOUNT=-1
     self.abuf=""
     
     self.answers=[]
     
    
     self.rt=-1
     self.size=-1
     self.src_addr=""
     self.subid=""
     self.submax=-1
     self.rcode=-1
     
      ##print( "gothere")
     try:
       self.result= m["result"]
       if len(self.result) >  0: 
          
          ##print( self.result)
          self.ANCOUNT=self.result['ANCOUNT']
          self.ARCOUNT=self.result['ARCOUNT']
          self.ID=self.result['ID']
          self.NSCOUNT=self.result['NSCOUNT']
          self.QDCOUNT=self.result['QDCOUNT']
          self.abuf=self.result['abuf']
          
          #now we have to parse this BS abuf to get the RCODE field
          dnsmsg = dns.message.from_wire(base64.b64decode(self.abuf))
          self.rcode=dnsmsg.rcode()
          
          #self.timeout=self.result['timeout']
          #self.timeout=self.result['timeout']
         
          #answers" -- first two records from the response decoded by the probe, if they are TXT or SOA; other RR can be decoded from "abuf" (array) 

	  #we create an object with answers , then we have to pull it out later on
          try:
            tempz=self.result['answers']
            ###print( tempz)
            ##print( "the number of answers is: " + str(len(tempz)))
            
            for k in tempz:
              ##print( k)
              self.answers.append(response4570(k))
        
          except KeyError:
            #print( "Measurement has result, but no answer ")
            pass
          
          try:
            self.rt=self.result['rt']

          except KeyError:
            #print( "Measurement has result, but no rt ")
            pass
              
          try:
            self.size=self.result['size']

          except KeyError:
            #print( "Measurement has result, but no size ")
            pass
            
          try:
            self.src_addr=self.result['src_addr']

          except KeyError:
            #print( "Measurement has result, but no src_addr ")            
            pass

          try:
            self.subid=self.result['subid']

          except KeyError:
            #print( "Measurement has result, but no subid ")
            pass
            
          try:
            self.submask=self.result['submask']

          except KeyError:
            #print( "Measurement has result, but no submask ")            
            pass
        
        
          ##print( str("whatever"))
	#break
     except KeyError:
       #print( "Measurement does not have result")
       pass
      ##"from" -- [optional] IP address of the source (string)
      
      
      
      #See example code for decoding the value
      #"result" -- [optional] response from the DNS server (associative array)
	  #"ANCOUNT" -- answer count, RFC 1035 4.1.1 (int)
	  #"ARCOUNT" -- additional record count, RFC 1035, 4.1.1 (int)
	  #"ID" -- query ID, RFC 1035 4.1.1 (int)
	  #"NSCOUNT" -- name server count (int)
	  #"QDCOUNT" -- number of queries (int)
	  #"abuf" -- answer payload buffer from the server, UU encoded (string)
	  #See example code for decoding the value
	  #"answers" -- first two records from the response decoded by the probe, if they are TXT or SOA; other RR can be decoded from "abuf" (array)
	  #Each element is an associative array consisting of:
	      #"MNAME" -- domain name, RFC 1035, 3.1.13 (string)
	      #"NAME" -- domain name. (string)
	      #"RDATA" -- [type TXT] txt value, (string)
	      #"RNAME" -- [if type SOA] mailbox, RFC 1035 3.3.13 (string)
	      #"SERIAL" -- [type SOA] zone serial number, RFC 1035 3.3.13 (string)
	      #"TTL" -- [type SOA] time to live, RFC 1035 4.1.3 (int)
	      #"TYPE" -- RR "SOA" or "TXT" (string), RFC 1035
	  #"rt" -- [optional] response time in milli seconds (float)
	  #"size" -- [optional] response size (int)
	  #"src_addr" -- [optional] the source IP address added by the probe (string).
	  #"subid" -- [optional] sequence number of this result within a group of results, available if the resolution is done by the probe's local resolver
	  #"submax" -- [optional] total number of results within a group (int)
      #"retry" -- [optional] retry count (int)
      #"timestamp" -- start time, in Unix timestamp (int)
      #"type" -- "dns" (string)
