#! /usr/bin/env python3

import json
import random
import os

CONFIG_FILE = "config.json"

def validate_config_keys(config:dict):
    required_keys = {
            "count",
            "db_files",
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

    db_files = config["db_files"]
    tags_to_show = set(config["tags"])
    count = config["count"]

    tips = []
    
    def by_tags(tip):
        # Filter tips by tag if tip is enabled and matching
        # tags are specified in config file
        return (
            tip["enabled"] and
            (not tags_to_show or
            tags_to_show.intersection(set(tip["tags"])))
            )

    for db_file in db_files:
        with open(db_file) as fp:
            db = json.load(fp)
            tips += list(filter(by_tags, db["tips"]))
    try:
        return random.sample(tips, k=count)
    except(ValueError):
        return []

def show_tip(tip):
    '''
    Prints the contents of the given tip
    '''
    header = "\n= = = = = = = = = A TIP TO REMEMBER = = = = = = = = =\n"
    print(header)
    for line in tip["contents"]:
        print(line)
    footer = "\n= = = = = = = = = = = = = = = = = = = = = = = = = = =\n"
    print(footer)
