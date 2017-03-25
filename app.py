#!/usr/bin/python

import json
import pickle
from NessiWrapper import Nessi

apiKey = '';
customerId = '';
nessi = None

def get

def setup():
    with open('config.json') as json_data:
        config = json.load(json_data)
        apiKey = config['nessi_key']
        customerId = config['customer_id']
    nessi = Nessi('customer', apiKey)


def main():
    setup()
    
if __name__ == "__main__":
        main()
