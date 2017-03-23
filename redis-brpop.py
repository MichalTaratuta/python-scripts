import redis


r = redis.StrictRedis(host='<HOSTNAME>', port=6379, db=0, password='<PASSWORD>')



print (r.info(section='Keyspace'))
for i in range (0, 200):
    
    r.brpop('time', timeout=10)
    
