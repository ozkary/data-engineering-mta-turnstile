#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  2023 ozkary.com.
#
#  MTA turnstile data engineering and analysis
#

import os
import argparse
from time import time
from pathlib import Path
import pandas as pd


def read_local(file_path: str) -> Path:
    """
        Reads a local file
        Args:
            file_path:  local file            
    """
    print(F'Reading local file {file_path}')
    df_iter = pd.read_csv(file_path, iterator=True,compression="gzip", chunksize=10000) 
    if df_iter:        
        for df in df_iter:
            try:                                
                print('File headers',df.columns)                                
                print('Top 10 rows',df.head(10))            
                break
            except Exception as ex:
                print(f"Error found {ex}")
                return
                
        print(f"file was loaded {file_path}")        
    else:
        print(F"failed to read file {file_path}")

def write_local(df: pd.DataFrame, folder: str, file_name: str) -> Path:
    """
        Write DataFrame out locally as csv file
        Args:
            df: dataframe chunk
            folder: the download data folder
            file_name: the local file name
    """

    path = Path(f"{folder}")
    if not os.path.exists(path):
        path.mkdir(parents=True, exist_ok=True)
    
    file_path = Path(f"{folder}/{file_name}")

    if not os.path.isfile(file_path):
        df.to_csv(file_path, compression="gzip")
        print('new file')
    else:
        df.to_csv(file_path, header=None, compression="gzip", mode="a")    
        print('chunk appended')
        
    return file_path

def etl_web_to_local(url: str, name: str) -> None:
    """
       Download a file    
       Args:
            url : The file url
            name : the file name
   
    """
    print(url, name)      

    # skip an existent file
    path = f"../data/"
    file_path = Path(f"{path}/{name}.csv.gz")
    if os.path.exists(file_path):
            read_local(file_path)            
            return
        
    df_iter = pd.read_csv(url, iterator=True, chunksize=10000) 
    if df_iter:      
        file_name = f"{name}.csv.gz"    
        for df in df_iter:
            try:                                
                # print(df.columns)                                
                # print(df.head(10))
                write_local(df, path, file_name)
            except StopIteration as ex:
                print(f"Finished reading file {ex}")
                break
            except Exception as ex:
                print(f"Error found {ex}")
                return
                
        print(f"file was loaded {file_path}")        
    else:
        print("dataframe failed")

def main_flow(params: str) -> None:
    """
        Process a CSV file from a url location with the goal to understand the data structure
    """    
    url = params.url  
    prefix = params.prefix

    try:
        start_index = url.index('_')
        end_index = url.index('.txt')
        file_name = F"{prefix}{url[start_index:end_index]}"
        # print(file_name)
        etl_web_to_local(url, file_name)
    except ValueError:
        print("Substring not found")
          

if __name__ == '__main__':
    
    os.system('clear')    
    parser = argparse.ArgumentParser(description='Process CSV data to understand the data')
    parser.add_argument('--url', required=True, help='url of the csv file')
    parser.add_argument('--prefix', required=True, help='the file prefix or group name')
    args = parser.parse_args()
    
    print('running...')
    main_flow(args)
    print('end')

# Link files have this format
# http://web.mta.info/developers/data/nyct/turnstile/turnstile_230318.txt
# files are published every Sunday format turnstile_yyMMdd.txt
# python3 mta_discovery.py --url http://web.mta.info/developers/data/nyct/turnstile/turnstile_230318.txt --prefix turnstile
