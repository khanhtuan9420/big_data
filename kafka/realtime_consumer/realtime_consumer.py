import logging
import os
import tempfile
import datetime
from logging.handlers import RotatingFileHandler
from kafka import KafkaConsumer

class RealtimeStockConsumer:
    def __init__(self):
        log_handler = RotatingFileHandler(
            f"{os.path.abspath(os.getcwd())}/kafka/consumer/logs/consumer.log",
            maxBytes=104857600, backupCount=10)
        logging.basicConfig(
            format='%(asctime)s,%(msecs)d <%(name)s>[%(levelname)s]: %(message)s',
            datefmt='%H:%M:%S',
            level=logging.DEBUG,
            handlers=[log_handler])
        self.logger = logging.getLogger('realtimeConsumer')
        self.consumer = KafkaConsumer(
            'realtimeStockData',
            bootstrap_servers=['localhost:19092',
                               'localhost:29092', 'localhost:39092'],
            group_id='realtimeStockDataConsummers',
            auto_offset_reset='earliest',
            enable_auto_commit=False)

    def run(self):
        try:
            self.logger.info("Subcribe to topic stockData")
            while True:
                msgs_pack = self.consumer.poll(10.0)
                if msgs_pack is None:
                    continue

                for tp, messages in msgs_pack.items():
                    for message in messages:
                        true_msg = str(message[6])[2: len(str(message[6])) - 1]
                        print(true_msg)

        except Exception as e:
            self.logger.error(
                f"An error happened while processing messages from kafka: {e}")
        finally:
            self.consumer.close()
