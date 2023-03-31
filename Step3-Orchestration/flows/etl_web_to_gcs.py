#!/usr/bin/env python
# coding: utf-8

import argparse
from pathlib import Path
import os
import pandas as pd
from prefect import flow, task
from prefect_gcp.cloud_storage import GcsBucket
from typing import List
# from prefect.tasks import task_input_hash
from settings import get_block_name, get_min_date, get_max_date, get_prefix, get_url
from datetime import timedelta, date

# _DEBUG = True

@task(name="write_gcs", description='Write file gcs', log_prints=False)
def write_gcs(local_path: Path, file_name: str, prefix: str) -> None:
    
    """
        Upload local parquet file to GCS
        Args:
            path: File location
            prefix: the folder location on storage

    """    
    block_name = get_block_name()
    gcs_path = f'{prefix}/{file_name}.csv.gz'
    print(f'{block_name} {local_path} {gcs_path}')
    
    gcs_block = GcsBucket.load(block_name)        
    gcs_block.upload_from_path(from_path=local_path, to_path=gcs_path)
    
    return

@task(name='write_local', description='Writes the file into a local folder')
def write_local(df: pd.DataFrame, folder: str, file_path: Path) -> Path:
    """
        Write DataFrame out locally as csv file
        Args:
            df: dataframe chunk
            folder: the download data folder
            file_name: the local file name
    """

    path = Path(folder)
    if not os.path.exists(path):
        path.mkdir(parents=True, exist_ok=True)

    df = df.rename(columns={'C/A': 'CA'})            
    df = df.rename(columns=lambda x: x.strip().replace(' ', ''))    
    # df = df.rename_axis('row_no').reset_index()

    if not os.path.isfile(file_path):
        df.to_csv(file_path, compression="gzip")
        # df.to_parquet(file_path, compression="gzip", engine='fastparquet')
        print('new file', flush=True)
    else:  
        df.to_csv(file_path, header=None, compression="gzip", mode="a")          
        # df.to_parquet(file_path, compression="gzip", engine='fastparquet', append=True) 
        print('chunk appended', flush=True)
        
    return file_path

@flow(name='etl_web_to_local', description='Download MTA File in chunks')
def etl_web_to_local(name: str, prefix: str) -> Path:
    """
       Download a file    
       Args:            
            name : the file name  
            prefix: the file prefix          
   
    """    

    # skip an existent file
    path = f"../../data/"
    file_path = Path(f"{path}/{name}.csv.gz")
    if os.path.exists(file_path):            
            print(f'{name} already processed')
            return file_path

    url = get_url()
    file_url = f'{url}/{prefix}_{name}.txt'
    print(file_url)
    # os.system(f'wget {url} -O {name}.csv')
    # return

    df_iter = pd.read_csv(file_url, iterator=True, chunksize=5000)     
    if df_iter:              
        for df in df_iter:
            try:                                                
                write_local(df, path, file_path)
            except StopIteration as ex:
                print(f"Finished reading file {ex}")
                break
            except Exception as ex:
                print(f"Error found {ex}")
                return
                
        print(f"file was downloaded {file_path}")                
    else:
        print("dataframe failed")

    return file_path

@task(name='get_the_file_dates', description='Downloads the file in chunks')
def get_the_file_dates(year: int, month: int, day: int = 1, limit: bool = True ) -> List[str]:
    """
        Process all the Sundays of the month
        Args:
            year : the selected year
            month : the selected month 
            day:  the file day
    """
    date_list = []    
    curr_date = date(year, month, day)    
    while curr_date.month == month and curr_date <= date.today():   
        # print(f'Current date {curr_date}')     
        if curr_date.weekday() == 5:
            # add the date filename format yyMMdd
            year_tag = str(curr_date.year)[2:4]
            file_name = f'{year_tag}{curr_date.month:02}{curr_date.day:02}'
            date_list.append(file_name)            
            curr_date = curr_date + timedelta(days=7)
            if limit:
                 break
        else:
            # find next week
            days_to_sunday = (5 - curr_date.weekday()) % 7
            curr_date = curr_date + timedelta(days=days_to_sunday)
    return date_list
                              

@task(name='valid_task', description='Validate the tasks input paranmeter')
def valid_task(year: int, month: int, day: int = 1) -> bool:
    """
        Validates the input parameters for the request
         Args:
            year : the selected year
            month : the selected month   
            day: file day
    """    
    isValid = False
    if month > 0 and month < 13:        
        curr_date = date(year, month, day)         
        min_date = get_min_date()
        max_date = get_max_date()
        isValid =  curr_date >= min_date and curr_date < max_date and curr_date <= date.today()

    print(f'task request status {isValid} input {year}-{month}')
    return isValid

@flow(name="MTA Multiple File Batch Data Flow")
def main_batch_flow(params) -> None:
    """
        Entry point to download the data
    """        
    try:
        year = int(params.year)
        month = int(params.month)
        limit = params.day != None
        day = 1 if params.day == None else int(params.day)

        if not valid_task(year, month, day):        
            return

        prefix = get_prefix()            
        
        file_list = get_the_file_dates(year, month, day, limit)        
        for file_name in file_list:        
            print(file_name)
            local_file_path = etl_web_to_local(file_name, prefix)        
            write_gcs(local_file_path, file_name, prefix)
                    
    except Exception as ex:
        print(f"error found {ex}")

if __name__ == '__main__':
    """main entry point with argument parser"""
    os.system('clear')
    print('Processing data load')
    parser = argparse.ArgumentParser(description='Download the MTA data')
    
    parser.add_argument('--year', required=True, help='File year ')
    parser.add_argument('--month', required=True, help='File month')        
    parser.add_argument('--day', required=False, help='File day')        
    args = parser.parse_args()

    main_batch_flow(args)

# Link files have this format
# http://web.mta.info/developers/data/nyct/turnstile/turnstile_230318.txt
# files are published every Sunday format turnstile_yyMMdd.txt
# python3 etl_web_to_gcs.py --year 2023 --month 3 --day 25