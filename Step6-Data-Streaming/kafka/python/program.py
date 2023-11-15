#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

import os
import argparse
import signal
from producer import KafkaProducer

# Define a function to handle Ctrl-C signal
def handle_sigint(signal, frame, producer):
    print("Ctrl-C pressed. Stopping the Kafka producer...")
    exit(0)
    # producer.close()
    print("Kafka producer stopped.")
    

def main_flow(params) -> None:
    """
    Main flow to read and send the messages
    """    
    topic = params.topic    
    config_path = params.config    
    producer = KafkaProducer(config_path, topic)

    # Register the signal handler to handle Ctrl-C       
    signal.signal(signal.SIGINT, lambda signal, frame: handle_sigint(signal, frame, producer.producer))

    producer.produce_messages()

# Usage
if __name__ == "__main__":

    """main entry point with argument parser"""
    os.system('clear')
    print('publisher running...')
    parser = argparse.ArgumentParser(description='Producer : --topic mta-turnstile --config path-to-config')
    
    parser.add_argument('--topic', required=True, help='stream topic')    
    parser.add_argument('--config', required=True, help='kafka setting') 
    
    args = parser.parse_args()
    main_flow(args)
    
    print('publisher end')

# usage
# python3 program.py --topic mta-turnstile --config ~/.kafka/azure.properties
# python3 program.py --topic mta-turnstile --config ~/.kafka/localhost-nosasl.properties
