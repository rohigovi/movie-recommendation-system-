from os import path
import sys, os
from datetime import datetime
from json import dumps, loads
from time import sleep
from random import randint
import numpy as np
from datetime import datetime, timedelta
from kafka import KafkaConsumer, KafkaProducer

topic = 'movielog2'

def createConsumer(offset_reset):
    # Create a consumer to read data from kafka
    consumer = KafkaConsumer(
        topic,
        bootstrap_servers=['localhost:9092'],
        # Read from the start of the topic; Default is latest
        auto_offset_reset=offset_reset,
        # auto_offset_reset='latest',
        group_id='team2',
        # Commit that an offset has been read
        enable_auto_commit=True,
        # How often to tell Kafka, an offset has been read
        # auto_commit_interval_ms=1000
    )
    return consumer

def fetchDataKafka(log_file, offset_reset, consume_time):
    kafka_consumer = createConsumer(offset_reset=offset_reset)
    print('Reading Kafka Broker')
    end_time = datetime.now() + timedelta(seconds=consume_time)
    for message in kafka_consumer:
        message = message.value.decode('utf-8')
        # Default message.value type is bytes!
        os.system(f"echo {message} >> {log_file}")
        if datetime.now() >= end_time:
            break
    return True

def main():
    fetchDataKafka("sample.log", "earliest", 60)

if __name__ == "__main__":
    main()