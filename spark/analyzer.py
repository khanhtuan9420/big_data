from pyspark.sql import SparkSession
from pyspark.sql.functions import to_date
import sys

# replace host cassandra !!! 
spark = SparkSession.builder\
            .config("spark.app.name", "StockAnalyzer")\
            .config("spark.master", "spark://spark-master:7077")\
            .config("spark.jars.packages", "com.datastax.spark:spark-cassandra-connector_2.12:3.2.0")\
            .config("spark.cassandra.connection.host", "172.18.0.9")\
            .config("spark.cassandra.auth.username", "cassandra")\
            .config("spark.cassandra.auth.password", "cassandra")\
            .enableHiveSupport()\
            .getOrCreate()
spark.sparkContext.setLogLevel("WARN")

# read data from cassandra
result_df = spark.read.format('org.apache.spark.sql.cassandra')\
            .options(table='stock_data', keyspace='stock')\
            .load()

#Xu ly them column % thay doi cua ma co phieu
data_df = result_df.withColumn("change", (result_df.close - result_df.open)/result_df.open*100)

def statistic (date):
    #Thong ke
    #Top ma tang nhieu nhat
    print("Top 10 ma co phieu tang nhieu nhat ngay {}".format(date))
    data_df.filter(to_date(data_df.trading_date) == date).sort(data_df.change.desc()).show(10)

    #Top giam nhieu nhat
    print("Top 10 ma co phieu giam nhieu nhat ngay {}".format(date))
    data_df.filter(to_date(data_df.trading_date) == date).sort(data_df.change.asc()).show(10)

    #Top ma co volumne lon nhat
    print("Top 10 ma co phieu co volumne lon nhat ngay {}".format(date))
    data_df.filter(to_date(data_df.trading_date) == date).sort(data_df.volume.desc()).show(10)

def history (ticker):
    #Lich su
    #Xem lich su 1 ma
    print("Lich su ma co phieu {} 10 ngay gan nhat".format(ticker))
    data_df.filter(data_df.symbol == ticker).show(10)

if (sys.argv[1] == "statistic"):
    statistic(sys.argv[2])
elif (sys.argv[1] == "history"):
    history(sys.argv[2])





