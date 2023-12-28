from realtime_consumer.realtime_consumer import RealtimeStockConsumer


def run_services():
    realtimeConsumer = RealtimeStockConsumer()
    realtimeConsumer.run()


run_services()
