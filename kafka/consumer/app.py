from consumer import StockConsumer


def run_services():
    consumer = StockConsumer()
    consumer.run()
    # realtimeConsumer = RealtimeStockConsumer()
    # realtimeConsumer.run()


run_services()
