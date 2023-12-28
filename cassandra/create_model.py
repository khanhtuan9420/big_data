from cassandra.cluster import Cluster

cluster = Cluster(['127.0.0.1'])
session = cluster.connect()

session.execute("CREATE KEYSPACE stock\
    WITH replication = {'class':'SimpleStrategy', 'replication_factor' : 1}")

session.execute("USE stock")

session.execute("CREATE TABLE stock_data (\
   symbol text,\
   high double,\
   low double,\
   open double,\
   close double,\
   volume double,\
   trading_date timestamp,\
   PRIMARY KEY (symbol, trading_date)\
) WITH CLUSTERING ORDER BY (trading_date DESC)")

session.execute("CREATE TABLE predicted_price (\
   symbol text,\
   high double,\
   low double,\
   open double,\
   close double,\
   PRIMARY KEY (symbol)\
)")

session.shutdown()
