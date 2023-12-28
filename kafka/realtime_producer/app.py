from realtime_producer.realtime_producer import RealtimeStockProducer


def run_services():
    realtimeProducer = RealtimeStockProducer()
    realtimeProducer.run()


run_services()
