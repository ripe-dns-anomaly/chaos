#!/usr/bin/python3

from ripe.atlas.sagan import DnsResult
import json
#from f4570above  import f4570above





class response4570():
   
   def __init__(self, k):
      
     
     self.MNAME=""
     self.NAME=""
     self.RDATA=""
     self.RNAME=""
     self.SERIAL=""
     self.TTL=""
     self.TYPE=""

           
     try:
       self.MNAME=k['MNAME']
       ##(print self.MNAME)
       pass
     except KeyError:  
       #(print"Measurement nas no MNAME")
       pass
       
     try:
       self.NAME=k['NAME']
       ##(printself.NAME)
       
     except KeyError:  
       #(print"Measurement nas no NAME")
       pass
            
     try:
       self.RDATA=k['RDATA']
       ##(print self.RDATA)
     except KeyError:  
       #(print"Measurement nas no RDATA")
       pass
     try:
       self.RNAME=k['RNAME']
       ##(printself.RNAME)
     except KeyError:  
       #(print"Measurement nas no RNAME")
       pass

     try:
       self.SERIAL=k['SERIAL']
       ##(printself.SERIAL)
     except KeyError:  
       #(print"Measurement nas no SERIAL")
       pass
     try:
       self.TTL=k['TTL']
       ##(printself.TTL)
     except KeyError:  
       #(print"Measurement nas no TTL")
       pass
      
     try:
       self.TYPE=k['TYPE']
       ##(printself.TYPE)
     except KeyError:  
       #(print"Measurement nas no TYPE")
       pass

     #try:
       #self.MNAME=self.answers['MNAME']
     #except KeyError:  
       ##(print"Measurement nas no MNAME")

     #try:
       #self.MNAME=self.answers['MNAME']
     #except KeyError:  
       ##(print"Measurement nas no MNAME")

     #try:
       #self.MNAME=self.answers['MNAME']
     #except KeyError:  
       ##(print"Measurement nas no MNAME")

     #try:
       #self.MNAME=self.answers['MNAME']
     #except KeyError:  
       ##(print"Measurement nas no MNAME")
       
       
     #self.NAME=self.answers['NAME']
     #self.RDATA=self.answers['RDATA']
     #self.RNAME=self.answers['RNAME']
     #self.SERIAL=self.answers['SERIAL']
     #self.TTL=self.answers['TTL']
     #self.TYPE=self.answers['TYPE']
        
        