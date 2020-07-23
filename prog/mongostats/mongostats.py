#!/usr/bin/python

import pprint

from pymongo import MongoClient

# Global vars
# COnectar con mongod en vez de mongos para el replicaset
host = '10.128.27.31'
port = 27017

# Connection
#client = MongoClient(host, port, replicaset='rs01')
client = MongoClient(host, port)

# All databases and collection by database
ddbb = client.database_names()

itersum = 0

# Open result test file
file = "/tmp/mongostats.output"
f = open(file,"w")

def sumalista(list_totaldocs):
    result_suma = 0
    for total in list_totaldocs:
        result_suma = result_suma + total
    return result_suma

f.write('DATABASES:\n')
for database in ddbb:
    f.write('  - %s\n' % database)

    db = client[database]
    stats = db.command("dbstats")
    indexSize = int(stats['indexSize'])
    dataSize = int(stats['dataSize'])
    totalSize = (dataSize + indexSize)
    f.write('      WorkingSet + IndexSize: %d\n' % (totalSize))
    globalSize = itersum + totalSize
    itersum= globalSize

f.write('\nTOTAL SIZE (Bytes)\n')
f.write('  Total Bytes: %d' % globalSize)

f.write('\n\nCOLLECTIONS & DOCS:\n')
list_totaldocs = []
for database in ddbb:
    db = client.get_database(database)
    collections = db.collection_names()
    f.write('  - %s:\n' % database)
    for collec in collections:
        get_collec = db.get_collection(collec)
        totaldocs = get_collec.count()
	list_totaldocs.append(totaldocs)
        f.write('      ' + str(collec)+ ' (%s)\n' % totaldocs)



sum_total = sumalista(list_totaldocs)
f.write('\nTOTAL DOCS: %d\n' % sum_total)

f.close()
print('Results in %s' % file)
