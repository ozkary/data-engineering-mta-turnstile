#!/usr/bin/env python
# coding: utf-8

import argparse
import os
from pathlib import Path
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

def main(params) -> None:
    """entry point to create the prefect block for gcs"""
    gcp_file_path = params.file_path
    prefect_block_name = params.block_name
    gcs_bucket_name = params.bucket_name
    gcs_block_name = params.gcs_block_name
    
    file_handle = Path(gcp_file_path) #.read_text()
    if file_handle.exists() :
        content = file_handle.read_text()

        if content :
            credentials_block = GcpCredentials(
                service_account_info=content     # set the file credential
            )
            credentials_block.save(prefect_block_name, overwrite=True)
            bucket_block = GcsBucket(
                gcp_credentials=GcpCredentials.load(prefect_block_name),
                bucket=gcs_bucket_name  # insert your  GCS bucket name
            )
            # save the bucket
            bucket_block.save(gcs_block_name, overwrite=True)
            print(F'{gcs_block_name} was saved')
            os.system('prefect block ls')

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')

    parser.add_argument('--file_path', required=True, help='GCP key file path')
    parser.add_argument('--block_name', required=True, help='prefect block name to hold the service account setting')
    parser.add_argument('--bucket_name', required=True, help='GCS bucket name')
    parser.add_argument('--gcs_block_name', required=True, help='GCS block name')
        
    args = parser.parse_args()

    main(args)
