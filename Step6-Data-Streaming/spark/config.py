#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

import json

def read_config(config_file, parse_values=True):
    """
    Reads the kafka configuration information that is stored in the system    
    """
    conf = {}    
    with open(config_file) as fh:
        
        if not parse_values:
            return fh.read().strip()
        
        for line in fh:
            line = line.strip()
            if len(line) != 0 and line[0] != "#":
                parameter, value = line.strip().split('=', 1)
                conf[parameter] = value.strip()          
    return conf

def key_serializer(key: str) -> bytes:
    """
    Message key serializer
    """
    return str(key).encode()

def value_serializer(value: object) -> bytes:
    """
    Message value serializer
    """
    return json.dumps(value).encode('utf-8')    

def key_deserializer(key: bytes) -> str:
    """
    Message key deserializer
    """
    return bytes(key).decode()

def value_deserializer(value: bytes) -> any:
    """
    Message value deserializer
    """
    return json.loads(value) 