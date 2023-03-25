#!/usr/bin/env python
# coding: utf-8

import argparse
from prefect.infrastructure.docker import DockerContainer

def main(params) -> None:
    """Create a Docker prefect block"""
    block_name = params.block_name
    image_name = params.image_name

    # alternative to creating DockerContainer block in the UI
    docker_block = DockerContainer(
        image=image_name,  # insert your image here
        image_pull_policy="ALWAYS",
        auto_remove=True,
    )

    docker_block.save(block_name, overwrite=True)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Create a reusable Docker image block from DockerHub')

    parser.add_argument('--block_name', required=True, help='Prefect block name')    
    parser.add_argument('--image_name', required=True, help='Docker image name used when the image was build')    
        
    args = parser.parse_args()

    main(args)
