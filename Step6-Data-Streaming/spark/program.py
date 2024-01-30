#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

# Standard Library Imports
import os
import argparse
# from ast import List
from pathlib import Path
from datetime import datetime

# Third-Party Library Imports
from pyspark.sql import SparkSession, DataFrame
import pyspark.sql.functions as F
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
import pandas as pd

# Local libraries
from consumer import SparkSettings, SparkConsumer
from settings import get_block_name, get_prefix
from schema import turnstiles_schema


# Local Module Imports
PROJECT = 'ozkary-de-101'
BUCKET = 'gs://ozkary_data_lake_ozkary-de-101/turnstile'


def write_to_console(df: DataFrame, output_mode: str = 'append', processing_time: str = '15 seconds') -> None:
    """
        Output stream values to the console
    """
    console_query = df.writeStream\
        .outputMode(output_mode) \
        .trigger(processingTime=processing_time) \
        .format("console") \
        .option("truncate", False) \
        .start()
    
    # this suspends execution until the stream is stopped must run using async
    # console_query.awaitTermination()     

# @task(name="Stream write GCS", description='Write stream file to GCS', log_prints=False)
def stream_write_gcs(local_path: Path, file_name: str) -> None:
    
    """
        Upload local parquet file to GCS
        Args:
            path: File location
            prefix: the folder location on storage

    """    
    block_name = get_block_name()
    prefix = get_prefix()
    gcs_path = f'{prefix}/{file_name}'
    print(f'{block_name} {local_path} {gcs_path}')
    
    gcs_block = GcsBucket.load(block_name)        
    gcs_block.upload_from_path(from_path=local_path, to_path=gcs_path)
    
    return


# @task (name="MTA Spark Data Stream - Process Mini Batch", description="Write batch to the data lake")
def process_mini_batch(df, batch_id, path):
    """Processes a mini-batch, converts to Pandas, and writes to GCP Storage as CSV.gz."""

     # Check if DataFrame is empty
    if df.count() == 0:
        print(f"DataFrame for batch {batch_id} is empty. Skipping processing.")
        return

    # Convert to Pandas DataFrame
    df_pandas = df.toPandas()

    # Convert 'DATE' column to keep the same date format
    df_pandas['DATE'] = pd.to_datetime(df_pandas['DATE'], format='%m-%d-%y').dt.strftime('%m/%d/%Y')

    print(df_pandas.head())

    # Get the current timestamp
    timestamp = datetime.now()
    # Format the timestamp as needed
    time = timestamp.strftime("%Y%m%d_%H%M%S")    

    # Write to Storage as CSV.gz    
    file_name = f"batch_{batch_id}_{time}.csv.gz"
    file_path = f"{path}/{file_name}"
    df_pandas.to_csv(file_path, compression="gzip")

    # send to the data lake
    stream_write_gcs(file_path, file_name)

@task (name="MTA Spark Data Stream - Aggregate messages", description="Aggregate the data in time windows")
def aggregate_messages(consumer, df_messages, window_duration, window_slide) -> DataFrame:
    df_windowed = consumer.agg_messages(df_messages, window_duration, window_slide)
    return df_windowed

@task (name="MTA Spark Data Stream - Read data stream", description="Read the data stream")
def read_data_stream(consumer, spark_session) -> None:
    consumer.read_kafka_stream(spark_session) 

# write a streaming data frame to storage ./storage
@task (name="MTA Spark Data Stream - Write to Storage", description="Write batch to the data lake")
def write_to_storage(df: DataFrame, output_mode: str = 'append', processing_time: str = '60 seconds') -> None:
    """
        Output stream values to the console
    """   
    df_csv = df.select(
        "CA", "UNIT", "SCP", "STATION", "LINENAME", "DIVISION", "DATE", "TIME", "DESC","ENTRIES", "EXITS"
    )

    path = "./storage/"     

    folder_path = Path(path)
    if not os.path.exists(folder_path):
        folder_path.mkdir(parents=True, exist_ok=True)

    storage_query = df_csv.writeStream \
        .outputMode(output_mode) \
        .trigger(processingTime=processing_time) \
        .format("csv") \
        .option("header", True) \
        .option("path", path) \
        .option("checkpointLocation", "./checkpoint") \
        .foreachBatch(lambda batch, id: process_mini_batch(batch, id, path)) \
        .option("truncate", False) \
        .start()
        
    try:
        # Wait for the streaming query to terminate
        storage_query.awaitTermination()
    except KeyboardInterrupt:
        # Handle keyboard interrupt (e.g., Ctrl+C)
        storage_query.stop()

@flow (name="MTA Spark Data Stream flow", description="Data Streaming Flow")
def main_flow(params) -> None:
    """
    main flow to process stream messages with spark
    """    
    topic = params.topic
    group_id = params.group    
    client_id = params.client
    config_path = params.config    

    # define a window for n minutes aggregations group by station
    default_span = '5 minutes'
    window_duration = default_span if params.duration is None else f'{params.duration} minutes'
    window_slide = default_span if params.slide is None else f'{params.slide} minutes'
    
    # create the consumer settings
    spark_settings = SparkSettings(config_path, topic, group_id, client_id)    
        
    # create the spark consumer
    spark_session = SparkSession.builder \
            .appName("turnstiles-consumer") \
            .config("spark.sql.adaptive.enabled", "false") \
            .getOrCreate()                
    
    spark_session.sparkContext.setLogLevel("WARN")
    
    # create an instance of the consumer class
    consumer = SparkConsumer(spark_settings, topic, group_id, client_id)

    # set the data frame stream
    read_data_stream(consumer, spark_session)
    # consumer.read_kafka_stream(spark_session) 
    
    # parse the messages
    df_messages = consumer.parse_messages(schema=turnstiles_schema)    
      
    df_windowed = aggregate_messages(consumer, df_messages, window_duration, window_slide)
    # df_windowed = consumer.agg_messages(df_messages, window_duration, window_slide)
        
    write_to_storage(df=df_windowed, output_mode='append',processing_time=window_duration)
  
    spark_session.streams.awaitAnyTermination()


if __name__ == "__main__":
    """
        Main entry point for streaming data between kafka and spark        
    """
    os.system('clear')
    print('Spark streaming running...')
    parser = argparse.ArgumentParser(description='Producer : --topic mta-turnstile --group spark_group --client app1 --config path-to-config')
    
    parser.add_argument('--topic', required=True, help='kafka topics')    
    parser.add_argument('--group', required=True, help='consumer group')
    parser.add_argument('--client', required=True, help='client id group')
    parser.add_argument('--config', required=True, help='cloud settings')    
    parser.add_argument('--duration', required=False, help='window duration for aggregation 5 mins')        
    parser.add_argument('--slide', required=False, help='window slide 5 mins')        
    
    args = parser.parse_args()

    # if (args.master is None):
    #     args.master = 'spark://localhost:7077'

    main_flow(args)

    print('end')

# Usage
# load spark shell
# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:your_spark_version

# run the app using spark-submit
# python3 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties
# spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties

# export KAFKA_OPTS="java.security.auth.login.config=~/.kafka/azure.properties.jaas"

# spark-submit --conf spark.kafka.sasl.jaas.config=~/.kafka/azure.properties.jaas --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties

# spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2