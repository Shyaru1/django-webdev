#!/usr/bin/python
# Author plecomte, release 2017-10-24
# script fetching all entries from the node-db
# and then attempting to set IPMI for each of them
# scripts runs without arguments to limit human errors.

from ovca import ovm
from ovca import node
import sys,os
ip_list = []
try:
 # we only want ILOM entries
 tab_temp = [(mac, val) for mac, val in node.node_db_get_items() if val['type'] == 'ilom']
except Exception, e:
 print 'reading node db failed: %s' % e
 sys.exit(1)
# Building a list with ILOM_IP and compute node name
for i in tab_temp:
 server=i[1]['name']
 # the name here is ilom-ovcacnxxr1 - We strip the first five characters here
 server=server[5:]
 ip= i[1]['ip']
 ip_list.append((ip,server))

print 'Found '+ str(len(ip_list)) + ' Compute Nodes'

# for each couple ILOM_IP, server Name, call a built-in ovm_shell script
for entry in ip_list :
  print 'About to set IPMI on IP: ' +entry[0]+ ' for compute node '+ entry[1]
  ret=ovm.ovm_shell('enable_ipmi.py','--server=%s' % entry[1],'--ip=%s' % entry[0])[0]
  if(ret):
     print 'Successfully set IPMI for Compute node '+ entry[1]
  else:
    # there is no sys.exit(1) here because we want to carry on with other compute nodes
    # if we fail setting IPMI for a server e.g. because a node is offline or any other reason.
    print 'failed to set IPMI for Compute node ' + entry[1]
