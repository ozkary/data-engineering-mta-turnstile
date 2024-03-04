#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#
from datetime import date, datetime

settings = {
        'min_date': '2023-01-01',
        'max_date': '2025-01-01',
        'gcs_block_name': 'blk-gcs-name',
        'src_url':'http://web.mta.info/developers/data/nyct/turnstile',
        'prefix': 'turnstile'
}    

def get_config(name: str) -> str:
    return settings[name]

def get_block_name() -> str:
    return settings['gcs_block_name']

def get_prefix() -> str:
    return settings['prefix']

def get_url() -> str:
    return settings['src_url']

def get_min_date() -> date:
    return datetime.strptime(settings['min_date'], '%Y-%m-%d').date()

def get_max_date() -> date:
    return datetime.strptime(settings['max_date'], '%Y-%m-%d').date()