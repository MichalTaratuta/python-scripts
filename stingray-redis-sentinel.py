import redis
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
    
(options, args) = parser.parse_args()

# connect to Redis
sentinel_host = options.sentinel_witness
sentinel_port = options.sentinel_port
r = redis.StrictRedis(host='poc-witness-sentinel.int.mol.dmgt.net', port=26379)
# r = redis.StrictRedis(host=ipaddr_from_stingray, port=26379)

# Query Sentinel for the IP of the master for "monitor_name" group.
def sentinel_check_master(monitor_name):
    get_master_bytes = r.sentinel_get_master_addr_by_name(monitor_name)
    
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
    print (get_host_by_addr[0])
    return get_host_by_addr[0]
    
    
#get_arguments()    
get_host_name(sentinel_check_master('poc-a1'))
print (options.ipaddr)
print (options.node)
print (options.port)
print (options.sentinel_witness)
print (options.sentinel_port)