#!/usr/bin/python

import json

config = {}

def main():
    with open('config.json') as json_data:
        config = json.load(json_data)

if __name__ == "__main__":
        main()
