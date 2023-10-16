#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

import time
import uuid
import random
import os
import argparse
from datetime import datetime
from confluent_kafka import Producer
from kafka.errors import KafkaTimeoutError
from config import read_config, key_serializer, value_serializer
from provider import Provider

class KafkaProducer:
    def __init__(self, config_path, topic):
        settings = read_config(config_path)
        self.producer = Producer(settings)
        self.topic = topic
        self.provider = Provider(topic)
    
    def delivery_report(self, err, msg):
        """
        Reports the success or failure of a message delivery.
        Args:
            err (KafkaError): The error that occurred on None on success.
            msg (Message): The message that was produced or failed.
        """
        if err is not None:
            print(f'Message delivery failed: {err}')
        else:
            print('Record {} produced to {} [{}] at offset {}'.format(msg.key(), msg.topic(), msg.partition(), msg.offset()))

    
    def produce_messages(self):
        while True:
            # Get the message key and value from the provider
            key, message = self.provider.message()

            try:

                # Produce the message to the Kafka topic
                self.producer.produce(topic = self.topic, key=key_serializer(key),
                                    value=value_serializer(message),
                                    on_delivery = self.delivery_report)
                
                # Flush to ensure delivery
                self.producer.flush()

                # Print the message
                print(f'Sent message: {message}')

                # Wait for 10 seconds before sending the next message
                time.sleep(15)
            except KeyboardInterrupt:
                pass
            except KafkaTimeoutError as e:
                print(f"Kafka Timeout {e.__str__()}")
            except Exception as e:
                print(f"Exception while producing record - {key} {message}: {e}")
                continue            

