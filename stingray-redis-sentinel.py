#! /usr/bin/env python
import redis
import sys
import socket
from optparse import OptionParser

# Get the options passed by the Stingray
# https://www.brocade.com/content/dam/common/documents/content-types/user-guide/brocade-vtm-10.1-userguide.pdf (page 250)

parser = OptionParser()
parser.add_option("--ipaddr", dest="ipaddr")
parser.add_option("--node", dest="node")
parser.add_option("--port", dest="port")
parser.add_option("--sentinel-witness", dest="sentinel_witness")
parser.add_option("--sentinel-port", dest="sentinel_port")
parser.add_option("--sentinel-monitor-name", dest="sentinel_monitor_name")
parser.add_option("--stingray-pool-name", dest="stingray_pool_name")
parser.add_option("--verbose", action="store_false", dest="verbose")
parser.add_option("--failures_left", dest="failures_left")


    
(options, args) = parser.parse_args()

# Healthcheck variables
pool_node = options.node
sentinel_witness = options.sentinel_witness
sentinel_port = options.sentinel_port
sentinel_monitor_name = options.sentinel_monitor_name
stingray_pool_name = options.stingray_pool_name

# Script variables
node_list = [pool_node, sentinel_witness]
active_master_list = []

def sentinel_check_master(sentinel_monitor_name):
    #connect_sentinel(host_name, port_name)
    get_master_bytes = r.sentinel_get_master_addr_by_name(sentinel_monitor_name)
    
    list_master_bytes = list(get_master_bytes)

    # Create list [master IP, port]
    current_master = []
    # Decode the bytes IP entry to str
    current_master.append(list_master_bytes[0].decode())
    current_master.append(list_master_bytes[1])
    return current_master

# Convert Master IP to FQDN
def get_host_name(master_node):
    
    get_host_by_addr = socket.gethostbyaddr(master_node[0])
    return get_host_by_addr[0]

for node in node_list:
    # connect to Sentinel
    r = redis.StrictRedis(host=node, port=sentinel_port)
    # Get the hostname of current master
    active_master_list.append(get_host_name(sentinel_check_master(sentinel_monitor_name)))

if active_master_list[0] == active_master_list[1] and active_master_list[0] == pool_node:
    sys.exit(0)
else:
    sys.exit(1)