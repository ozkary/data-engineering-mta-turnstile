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
            "client.id": client_id,
            "group.id": group_id,            
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

    def parse_messages(self, schema) -> DataFrame:
        """
        Parse the messages and use the provided schema to type cast the fields
        """
        stream = self.stream

        assert stream.isStreaming is True, "DataFrame doesn't receive streaming data"

        options =  {'header': 'true', 'sep': ','}
        df = stream.selectExpr("CAST(key AS STRING)", "CAST(value AS STRING)")               
                                    
        # print("df =====>",df)
        # split attributes to nested array in one Column
        col = F.split(df['value'], ',')

        # expand col to multiple top-level columns
        for idx, field in enumerate(schema):
            df = df.withColumn(field.name.replace('`',''), col.getItem(idx).cast(field.dataType))

        result = df.select([field.name for field in schema])    

        print("parse_messages: DataFrame Schema:")        
        result.printSchema()
            
        return result

        
    def agg_messages(self, df: DataFrame,  window_duration: str, window_slide: str) -> DataFrame:
        """
            Window for 5 minutes aggregations group by station
        """

        # Ensure TIMESTAMP is in the correct format (timestamp type)
        df = df.withColumn("TIMESTAMP", F.col("TIMESTAMP").cast("timestamp"))
                        
        df_windowed = df \
            .withWatermark("TIMESTAMP", window_duration) \
            .groupBy(F.window("TIMESTAMP", window_duration, window_slide),"A/C", "UNIT","SCP","LINENAME","DIVISION", "STATION", "DATE", "DESC") \
            .agg(
                F.sum("ENTRIES").alias("ENTRIES"),
                F.sum("EXITS").alias("EXITS")
            ).withColumn("START", F.col("window.start")).withColumn("END", F.col("window.end")) \
            .drop("window")
                
        print("agg_messages: DataFrame Schema:")
        df_windowed.printSchema()

        return df_windowed

    def add_by_station(self, df: DataFrame, window_duration: str, window_slide: str) -> DataFrame:
            
        # Ensure TIMESTAMP is in the correct format (timestamp type)
        df = df.withColumn("TIMESTAMP", F.col("TIMESTAMP").cast("timestamp"))
        # df = df.withColumn("ENTRIES", F.col("ENTRIES").fillna(0))
        # df = df.withColumn("EXITS", F.col("EXITS"))
        
        # Group by 'STATION' and create a n-minute window
        df_windowed = df \
            .withWatermark("TIMESTAMP", window_duration) \
            .groupBy(F.window("TIMESTAMP", window_duration), "STATION") \
            .agg(
                F.sum("ENTRIES").alias("ENTRIES"),
                F.sum("EXITS").alias("EXITS")
            ).withColumn("START", F.col("window.start")).withColumn("END", F.col("window.end")) \
            .drop("window") \
            .select("STATION","START","END","ENTRIES","EXITS")
        
        print("add_by_station: DataFrame Schema:")
        df_windowed.printSchema()

        # df_windowed.awaitTermination()

        return df_windowed 