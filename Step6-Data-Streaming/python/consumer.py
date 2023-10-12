#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

from confluent_kafka import Consumer, KafkaException, KafkaError
from kafka.errors import KafkaTimeoutError
from config import read_config, key_deserializer, value_deserializer

class KafkaConsumer:
    
    def __init__(self, config_path, topic, group_id, client_id):
        settings = read_config(config_path)
        self.topic = topic        
        self.group_id = group_id
        self.client_id = client_id

        # Add additional settings.
        settings["group.id"] = self.group_id
        settings["client.id"] = self.client_id
        settings["enable.auto.commit"] = False
        settings["auto.offset.reset"] = "earliest"
        settings["enable.partition.eof"] = True
        
        # Create the consumer using the settings
        self.consumer = Consumer(settings)
        self.consumer.subscribe([topic])

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

    def consume_messages(self):
        """
        Consumes messages from the Kafka Topic.
        """
        try:
            while True:
                msg = self.consumer.poll(5.0)
                if msg is None or msg == {} or msg.key() is None:
                        print('Empty message was received')
                        continue 
                
                if msg.error():
                    if msg.error().code() == KafkaError._PARTITION_EOF:
                        # End of partition event - not an error
                        continue
                    else:
                        raise KafkaException(msg.error())
                                
                key = key_deserializer(msg.key())
                value = msg.value()

                if value is not None:
                    data = value_deserializer(value)
                    print(f'Message : {key}, {data}')

        except KeyboardInterrupt:
            pass
        except KafkaTimeoutError as e:
            print(f"Kafka Timeout {e.__str__()}")
        except Exception as e:
            print(f"Exception while producing record: {e.__str__()}")            
        finally:
            self.consumer.close()



