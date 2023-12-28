import logging
import os
import tempfile
import datetime
from logging.handlers import RotatingFileHandler
from kafka import KafkaConsumer
from hdfs import InsecureClient


class StockConsumer:
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/kafka/consumer/logs/consumer.log",
            maxBytes=104857600, backupCount=10)
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])
        self.logger = logging.getLogger('consumer')
        self.consumer = KafkaConsumer(
            'stockData',
            bootstrap_servers=['localhost:19092',
                               'localhost:29092', 'localhost:39092'],
            group_id='stockDataConsummers',
            auto_offset_reset='earliest',
            enable_auto_commit=False)
        self.hdfs_client = InsecureClient('http://localhost:9870', user='root')

    def flush_to_hdfs(self, tmp_file_name):
        current_time = datetime.datetime.now()
        hdfs_filename = "/stockData/" +\
            str(current_time.year) + "/" +\
            str(current_time.month) + "/" +\
            str(current_time.day) + "/"\
            f"stockData.{int(round(current_time.timestamp()))}"
        self.logger.info(
            f"Starting flush file {tmp_file_name} to hdfs")
        flush_status = self.hdfs_client.upload(hdfs_filename, tmp_file_name)
        if flush_status:
            self.logger.info(
                f"Flush file {tmp_file_name} to hdfs as {hdfs_filename} successfully")
        else:
            raise RuntimeError(f"Failed to flush file {tmp_file_name} to hdfs")
        self.consumer.commit()

    def recreate_tmpfile(self):
        tmp_file = tempfile.NamedTemporaryFile(mode='w+t', delete=False)
        tmp_file.write('Symbol, Open, High, Low, Close, Volume, Trading date\n')
        return tmp_file

    def run(self):
        try:
            tmp_file = self.recreate_tmpfile()
            self.logger.info("Subcribe to topic stockData")
            while True:
                msgs_pack = self.consumer.poll(10.0)
                if msgs_pack is None:
                    continue

                for tp, messages in msgs_pack.items():
                    for message in messages:
                        true_msg = str(message[6])[2: len(str(message[6])) - 1]
                        tmp_file.write(f"{true_msg}\n")
                        print(true_msg)
                # File size > 10mb flush to hdfs  max = 10485760

                if tmp_file.tell() > 10000:
                    print("xooo")
                    self.flush_to_hdfs(tmp_file.name)
                    tmp_file.close()
                    tmp_file = self.recreate_tmpfile()
        except Exception as e:
            self.logger.error(
                f"An error happened while processing messages from kafka: {e}")
        finally:
            tmp_file.close()
            self.consumer.close()
