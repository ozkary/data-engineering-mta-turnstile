#!/usr/bin/env python
# coding: utf-8

import argparse
import os
from pathlib import Path
from prefect_gcp import GcpCredentials

# insert your own service_account_file path or service_account_info dictionary from the json file
# IMPORTANT - do not store credentials in a publicly available repository!

def main(params) -> None:
    """entry point to create the prefect block for GCP service account"""
    gcp_file_path = params.file_path
    account_block_name = params.gcp_acc_block_name
    
    file_handle = Path(gcp_file_path) #.read_text()
    print(file_handle.read_text())
    if file_handle.exists() :
        content = file_handle.read_text()

        if content :
            credentials_block = GcpCredentials(
                service_account_info=content     # set the file credential
            )
            credentials_block.save(account_block_name, overwrite=True)
            print('block was saved')
    else:
        print(F'{gcp_file_path} not found')

    os.system('prefect block ls')
            
if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a reusable GCP Credential block')

    parser.add_argument('--file_path', required=True, help='GCP key file path for the service account')
    parser.add_argument('--gcp_acc_block_name', required=True, help='prefect block name to hold the service account setting')
        
    args = parser.parse_args()

    main(args)
