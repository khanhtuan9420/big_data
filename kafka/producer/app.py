from producer import StockProducer


def run_services():
    producer = StockProducer()
    producer.run()
    # realtimeProducer = RealtimeStockProducer()
    # realtimeProducer.run()


run_services()
