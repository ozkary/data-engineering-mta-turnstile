#!/usr/bin/env python
# coding: utf-8

import argparse
from prefect.deployments import Deployment
from etl_web_to_gcs import etl_web_to_gcs
from prefect.infrastructure.docker import DockerContainer

def main(params) -> None:
    """Create a prefect deployment"""
    block_name = params.block_name
    deploy_name = params.deploy_name

    # use the prefect block name for the container
    docker_block = DockerContainer.load(block_name)

    docker_dep = Deployment.build_from_flow(
        flow=etl_web_to_gcs,
        name=deploy_name,
        infrastructure=docker_block
    )
    docker_dep.apply()

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a reusable prefect deployment script')

    parser.add_argument('--block_name', required=True, help='Prefect Docker block name')    
    parser.add_argument('--deploy_name', required=True, help='Prefect deployment name')    
        
    args = parser.parse_args()

    main(args)
