#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com
#
#  MTA turnstile data engineering and analysis
#

import fastavro
from io import BytesIO

class AvroMessage:
    def __init__(self, key_schema, message_schema):
        self.key_schema = key_schema
        self.message_schema = message_schema

    def key_serializer(self, key):
        bio = BytesIO()
        fastavro.schemaless_writer(bio, self.key_schema, key)
        return bio.getvalue()

    def key_deserializer(self, key_bytes):
        return fastavro.schemaless_reader(BytesIO(key_bytes), self.key_schema)

    def message_serializer(self, message):
        bio = BytesIO()
        fastavro.schemaless_writer(bio, self.message_schema, message)
        return bio.getvalue()

    def message_deserializer(self, message_bytes):
        return fastavro.schemaless_reader(BytesIO(message_bytes), self.message_schema)