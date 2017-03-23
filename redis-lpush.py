import redis
from datetime import datetime, date, time

r = redis.StrictRedis(host='<HOSTNAME>', port=6379, db=0, password='<PASSWORD>')

print (r.info(section='Keyspace'))
for i in range (0, 500):
    
    #print (datetime.now().isoformat())
    r.lpush('time', datetime.now().isoformat())

