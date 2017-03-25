#!/usr/bin/python

import json
import pickle
import os.path
import sys
from NessiWrapper import Nessi


class FraudAlert(object):

    def __init__(self):

        self.oldPurchases = []
        self.accounts = []
        # Load config
        with open('secret.json') as json_data:
            config = json.load(json_data)
            self.apiKey = config['nessi_key']
            self.customerId = config['customer_id']

        # setup Nessi
        self.nessi = Nessi('customer', self.apiKey)

        # Restore state
        if os.path.isfile('purchases.pkl'):
            with open('purchases.pkl', 'rb') as handle:
                self.oldPurchases = pickle.load(handle)

        # Get accounts
        resp = self.nessi.getAccountsByCustomerId(self.customerId)
        for acc in resp:
            self.accounts.append(acc['_id'])

    def run(self):
        self.setupMockAcc()


    def getNewPurchases(self):
        #resp = nessi.get 
        print('todo')

    def setupMockAcc(self):
        print('todo')

        
def main():
    fraud = FraudAlert()
    fraud.run()

if __name__ == "__main__":
        main()
