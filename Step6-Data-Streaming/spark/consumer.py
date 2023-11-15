#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#
import os
import pyspark
from pyspark.sql import SparkSession, DataFrame, types
import pyspark.sql.functions as F
from config import read_config, key_deserializer, value_deserializer

class SparkSettings:
    def __init__(self, config_path: str, topic: str, group_id: str, client_id: str) -> None:
        self.settings = read_config(config_path)
        
        use_sasl = "sasl.mechanism" in self.settings and self.settings["sasl.mechanism"] is not None
                
        self.kafka_options = {
            "kafka.bootstrap.servers": self.settings["bootstrap.servers"],
            "subscribe": topic,
            "startingOffsets": "earliest",
            "failOnDataLoss": "false",
            "kafka.client.id": client_id,
            "kafka.group.id": group_id,            
            "auto.offset.reset": "earliest",
            "checkpointLocation": "checkpoint",
            "minPartitions": "2",
            "enable.auto.commit": "false",
            "enable.partition.eof": "true"                        
        }          

        if use_sasl:
            # set the JAAS configuration only when use_sasl is True
            sasl_config = f'org.apache.kafka.common.security.plain.PlainLoginModule required serviceName="kafka" username="{self.settings["sasl.username"]}" password="{self.settings["sasl.password"]}";'

            login_options = {
                "kafka.sasl.mechanisms": self.settings["sasl.mechanism"],
                "kafka.security.protocol": self.settings["security.protocol"],
                "kafka.sasl.username": self.settings["sasl.username"],
                "kafka.sasl.password": self.settings["sasl.password"],  
                "kafka.sasl.jaas.config": sasl_config          
            }
            # merge the login options with the kafka options
            self.kafka_options = {**self.kafka_options, **login_options}

        
    def __getitem__(self, key):
        """
            Get the value of a key from the settings dictionary.
        """
        return self.settings[key]
    
    def set_jass_config(self) -> None:
        """
            Set the JAAS configuration with variables
        """
        jaas_config = (
            "KafkaClient {\n"
            "    org.apache.kafka.common.security.plain.PlainLoginModule required\n"
            f"    username=\"{self['sasl.username']}\"\n"
            f"    password=\"{self['sasl.password']}\";\n"            
            "};"
        )
    
        print('========ENV===========>',jaas_config)
        # Set the JAAS configuration in the environment
        os.environ['KAFKA_OPTS'] = f"java.security.auth.login.config={jaas_config}"        
        os.environ['java.security.auth.login.config'] = jaas_config

class SparkConsumer:
    def __init__(self, settings: SparkSettings, topic: str, group_id: str, client_id: str):
        self.settings = settings
        self.topic = topic        
        self.group_id = group_id
        self.client_id = client_id
        self.stream = None
        self.data_frame = None   
        self.kafka_options = self.settings.kafka_options     
              
        
    def read_kafka_stream(self, spark: SparkSession) -> None:
        """
        Reads the Kafka Topic.
        Args:
            spark (SparkSession): The spark session object.
        """
        self.stream = spark.readStream.format("kafka").options(**self.kafka_options).load()

    def parse_messages(self, schema: str) -> DataFrame:
        """
        Parse the messages and use the provided schema to type cast the fields
        """
        assert self.stream.isStreaming is True, "DataFrame doesn't receive streaming data"

        self.data_frame = self.stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)") \
            .select(F.from_json(value_deserializer(F.col("value")), schema).alias("parsed_value")) \
            .select("parsed_value.*")
        
        return self.data_frame

        
    def agg_messages(self, window_duration: str, window_slide: str) -> DataFrame:
        """
            Window for 5 minutes aggregations group by station
        """
        df_windowed = self.data_frame \
            .withWatermark("TIMESTAMP", window_duration) \
            .groupBy(F.window("TIMESTAMP", window_duration, window_slide), "STATION") \
            .count() \
            .agg(
                sum("ENTRIES").alias("ENTRIES"),
                sum("EXITS").alias("EXITS")
            )
        
        df_windowed.awaitTermination()

        return df_windowed
