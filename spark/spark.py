from pyspark.sql import SparkSession
from pyspark.sql.functions import col
import sys


# replace host cassandra !!! 
spark = SparkSession.builder\
            .config("spark.app.name", "StockDataAnalyzer")\
            .config("spark.master", "spark://spark-master:7077")\
            .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0")\
            .config("spark.cassandra.connection.host", "172.18.0.9")\
            .config("spark.cassandra.auth.username", "cassandra")\
            .config("spark.cassandra.auth.password", "cassandra")\
            .enableHiveSupport()\
            .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

df = spark.read.format('csv')\
    .option('header', True)\
    .option('inferSchema', True)\
    .load("hdfs://namenode:9000/stockData/"+sys.argv[1])
print(df.head(10))

df = df.select(
    col('Symbol').alias('symbol'),
    col(' Trading date').alias('trading_date'),
    col(' High').alias('high'), col(' Low').alias('low'), col(' Open').alias('open'), col(' Close').alias('close'), col(' Volume').alias('volume')
)

# save data into cassandra
df.write.format('org.apache.spark.sql.cassandra')\
        .mode('append')\
        .options(table='stock_data', keyspace='stock')\
        .save()
