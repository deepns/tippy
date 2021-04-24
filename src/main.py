#! /usr/bin/env python3

import json
import random
import os

CONFIG_FILE = "config.json"

def get_config(config_file:str) -> dict:
    '''
    Read the config data from the given file and return a
    dict.
    '''
    with open(config_file) as fp:
        config = json.load(fp)
        return config

def get_tips(config) -> list:
    '''
    Returns a list of tips by reading from the files
    specified in the config file and filtering them
    by the tags specified.
    '''

    db_files = config["db_files"]
    tags_to_show = set(config["tags"])
    count = config["count"]

    tips = []
    
    def by_tags(tip):
        # Filter tips by tag if tag is specified in config file
        return (not tags_to_show 
                or tags_to_show.intersection(set(tip["tags"])))

    for db_file in db_files:
        with open(db_file) as fp:
            db = json.load(fp)
            tips += list(filter(by_tags, db["tips"]))

    return random.choices(tips, k=count)

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

def main():
    config = get_config(CONFIG_FILE)
    tips = get_tips(config)
    for tip in tips:
        show_tip(tip)

if __name__ == "__main__":
    main()
