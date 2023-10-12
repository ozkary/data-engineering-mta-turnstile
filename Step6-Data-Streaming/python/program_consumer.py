#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

import os
import argparse
from consumer import KafkaConsumer
            
def main_flow(params) -> None:
    """
    Main flow to read the messages from a kafka topic
    """    
    topic = params.topic    
    config_path = params.config
    group_id = params.groupid
    client_id = params.clientid    
    producer = KafkaConsumer(config_path, topic, group_id, client_id)
    producer.consume_messages()

# Usage
if __name__ == "__main__":

    """main entry point with argument parser"""

    os.system('clear')
    print('consumer running...')
    parser = argparse.ArgumentParser(description='Consumer : --topic green_trips --groupid green_group --clientid app1 --config path-to-config')
    
    parser.add_argument('--topic', required=True, help='kafka topic')
    parser.add_argument('--groupid', required=True, help='consumer group')
    parser.add_argument('--clientid', required=True, help='client id')
    parser.add_argument('--config', required=True, help='kafka settings')    
    args = parser.parse_args()

    main_flow(args)
    
    print('consumer end')

# usage
# python3 program_consumer.py --topic mta-turnstile --groupid turnstile --clientid appTurnstile --config ~/.kafka/azure.properties
