#! /usr/bin/env python3

import json
from multiprocessing.sharedctypes import Value
from pathlib import Path
import random
from urllib import request
import requests
import validators

def validate_config_keys(config:dict):
    required_keys = {
            "count",
            "data_files",
            "tags"
    }
    missing_keys = required_keys - set(config.keys())
    if missing_keys:
        raise ValueError("Missing params {} in the config file".format(missing_keys))

def get_config(config_file:str) -> dict:
    '''
    Read the config data from the given file and return a
    dict.
    '''
    with open(config_file) as fp:
        config = json.load(fp)
        validate_config_keys(config)
        return config

def get_tips(config) -> list:
    '''
    Returns a list of tips by reading from the files
    specified in the config file and filtering them
    by the tags specified.
    '''
    # Make sure we have all the keys
    validate_config_keys(config)

    data_files = config["data_files"]
    tags_to_show = {tag.lower() for tag in config["tags"]}
    count = config["count"]

    tips = []
    
    def by_tags(tip):
        # Filter tips by tag if tip is enabled and matching
        # tags are specified in config file
        return (
            tip.get("enabled", True) and
            (not tags_to_show or
            tags_to_show.intersection({tag.lower() for tag in tip["tags"]}))
            )

    # TODO
    # Add a parameter to config file ("default_config")
    # when default_config is True
    #   use the package config and db files
    # 
    module_dir = Path(__file__).parent
    for data_file in data_files:
        if config.get("is_package_config", False):
            data_file = module_dir / data_file
        with open(data_file) as fp:
            db = json.load(fp)
            tips += list(filter(by_tags, db["tips"]))
    
    remote_files = filter(lambda x: validators.url(x), config.get("remote_files", []))
    for remote_file in remote_files:
        response = requests.get(remote_file)
        db = response.json()
        tips += list(filter(by_tags, db["tips"]))

    try:
        return random.sample(tips, k=count)
    except ValueError:
        # raises ValueError: Sample larger than population or is negative when list is empty
        return []
    
def show_tip(tip):
    '''
    Prints the contents of the given tip
    '''
    header = "\n= = = = = = = = = A TIP TO REMEMBER = = = = = = = = =\n"
    print(header)
    print("*> {}\n".format(tip.get("description", "")))
    for line in tip["contents"]:
        print(line)
    footer = "\n= = = = = = = = = = = = = = = = = = = = = = = = = = =\n"
    print(footer)
