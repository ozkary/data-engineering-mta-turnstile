#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

import argparse
from prefect_gcp import GcpCredentials
from prefect_gcp.cloud_storage import GcsBucket

# insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!

def main(params) -> None:
    """entry point to create the prefect block for GCS"""    
    account_block_name = params.gcp_acc_block_name
    gcs_bucket_name = params.gcs_bucket_name
    gcs_block_name = params.gcs_block_name
    
    credentials = GcpCredentials.load(account_block_name)
    if credentials :
        bucket_block = GcsBucket(
            gcp_credentials=credentials,
            bucket=gcs_bucket_name  # insert your  GCS bucket name
        )
        # save the bucket
        bucket_block.save(gcs_block_name, overwrite=True)

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Ingest CSV data to Postgres')
    
    parser.add_argument('--gcp_acc_block_name', required=True, help='prefect block name which holds service account')
    parser.add_argument('--gcs_bucket_name', required=True, help='GCS bucket name')
    parser.add_argument('--gcs_block_name', required=True, help='GCS block name')
        
    args = parser.parse_args()

    main(args)
