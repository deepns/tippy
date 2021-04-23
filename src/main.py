#! /usr/bin/env python3

# Define the class
#   load from json
#   convert to json
#   define __str__

import json
import random

CONFIG_FILE = "config.json"

def get_config():
    with open(CONFIG_FILE) as fp:
        config = json.load(fp)
        return config

def show_tip(tip):
    # header and footer can also go in config file?
    header = "================= TIP TO REMEMBER====================="
    footer = "======================================================"
    print(header)
    for line in tip["contents"]:
        print(line)
    print(footer)

def load_tips(config):
    config = get_config()
    tags_to_show = set(config["show_tags"])

    tips = []
    
    for db_file in config["db_files"]:
        with open(db_file) as fp:
            db = json.load(fp)
            tips += [
                        tip
                        for tip in db["tips"]
                            if not tags_to_show 
                                or tags_to_show.intersection(set(tip["tags"]))
                    ]

def main():
    tips = load_tips()
    if tips:
        show_tip(random.choice(tips))
    else:
        print("No tip show. You are all set.")
    
if __name__ == "__main__":
    main()
