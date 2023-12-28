from pyspark.sql import SparkSession
from pyspark.sql.functions import split, expr
from elasticsearch import Elasticsearch

spark = SparkSession.builder \
    .appName("StreamStock") \
    .master("local[*]") \
    .config("spark.jars.packages", "org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.1,org.elasticsearch:elasticsearch-spark-30_2.12:7.15.1") \
    .config("es.nodes", "elasticsearch") \
    .config("es.port", "9200") \
    .config("es.nodes.wan.only", "false") \
    .config("es.index.auto.create", "true") \
    .getOrCreate()

spark.sparkContext.setLogLevel("WARN")
es = Elasticsearch(hosts='http://elasticsearch:9200')
# es.indices.create(index="realtime_stocks_ssi")
df = spark.readStream.format('kafka') \
    .option('kafka.bootstrap.servers', 'kafka-1:9092,kafka-2:9092, kafka-3:9092') \
    .option('subscribe', 'realtimeStockData') \
    .load()

df.printSchema()

df = df.withColumn('symbol', (split(df['value'], ',').getItem(0)))
df = df.withColumn('price', (split(df['value'], ',').getItem(1)))
df = df.withColumn('volume', (split(df['value'], ',').getItem(2)))
df = df.withColumn('cp', (split(df['value'], ',').getItem(3)))
df = df.withColumn('rcp', (split(df['value'], ',').getItem(4)))
df = df.withColumn('ba', (split(df['value'], ',').getItem(5)))
df = df.withColumn('sa', (split(df['value'], ',').getItem(6)))
df = df.withColumn('hl', (split(df['value'], ',').getItem(7)))
df = df.withColumn('pcp', (split(df['value'], ',').getItem(8)))
df = df.withColumn('time', (split(df['value'], ',').getItem(9)))

def save_data(df, batch_id):
    data = df.collect()
    index = 0
    for row in data:
        index = index + 1
        # doc_send = {"symbol": "{}".format(row['symbol']), "price": "{}".format(row['price']), "volume": "{}".format(row['volume']),
        #             "cp": "{}".format(row['cp']), "rcp": "{}".format(row['rcp']),
        #             "ba": "{}".format(row['ba']), "sa": "{}".format(row['sa']), "hl": "{}".format(row['hl']),
        #             "pcp": "{}".format(row['pcp']), "time": "{}".format(row['time'])}
        doc_send = {
            "symbol": row['symbol'],
            "price": float(row['price']),
            "volume": int(row['volume']),
            "cp": float(row['cp']),
            "rcp": float(row['rcp']),
            "ba": float(row['ba']),
            "sa": float(row['sa']),
            "hl": bool(row['hl']),
            "pcp": float(row['pcp']),
            "time": "{}".format(row['time'])
        }
        es.index(index="realtime_stocks_ssi", document=doc_send)
        print(doc_send)
df.writeStream.foreachBatch(save_data).start().awaitTermination()
# df.writeStream.format('console').outputMode("append").start().awaitTermination()
# doc['your_string_field.keyword'].value != null ? Float.parseFloat(doc['your_string_field.keyword'].value) : 0



