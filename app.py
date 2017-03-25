#!/usr/bin/python

import json
import pickle
import os.path
import sys
import re
import datetime
import hashlib
import time
import random
from NessiWrapper import Nessi
import Svm

def idToint(x):
    hash_object = hashlib.md5(x)
    return int(hash_object.hexdigest(), 16)


class FraudAlert(object):

    def __init__(self, debug):
       
        self.runs = 0
        self.debug = debug
        self.oldPurchases = []
        self.accounts = []
        self.svm = Svm('svm.pkl')
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
        return
        while(True):
            
            if (self.debug):
                print("going to check for purchases")
            
            self.classifyPurchases()
            
            self.runs += 1;

            if (self.runs % 540 == 0):
                self.refit() 

            time.sleep(20)



    def getNewPurchases(self):
        newPurchases = []
        for acc in self.accounts:
            resp = self.nessi.getPurchasesByAccount(acc)
            for purchase in resp:
                if not purchase['_id'] in self.oldPurchases:
                    self.oldPurchases.append(purchase['_id'])
                    newPurchases.append(purchase)
        return newPurchases

    def getInputsFromPurchases(self, purchases):
        inputs = []
        for purc in purchases:
            merchant = self.nessi.getMerchant(purc['merchant_id'])
            dateParts = re.findall('(\d{4})-(\d{2})-(\d{2})', purc['purchase_date'])
            date = datetime.date(int(dateParts[0]), int(dateParts[1]), int(dateParts[2]))
            inp = {
                'lat': int(merchant['geocode']['lat']),
                'lng': int(merchant['geocode']['lng']),
                'merchantId': idToint(purc['merchant_id']),
                'dayOfWeek': date.weekday(),
                'month': int(dateParts[1]) - 1,
                'year': int(dateParts[0]),
                'amount': float(purc['amount'])
            }

            inputs.append(inp)

        return inputs

    def refit(self):
        purchases = []
        for acc in self.accounts:
            purchases += self.nessi.getPurchasesByAccount(acc)
        inputs = getInputsFromPurchases(purchases)

        #refit

    def classifyPurchases(self):

        purchases = self.getNewPurchases()
        if (self.debug):
            print("found these purchases")
            print(purchases)

        inputs = self.getInputsFromPurchases(purchases)
        if (self.debug):
            print("got these inputs")
            print(inputs)

        # Classify
        results = self.classify_new(inputs)
        frauds = []
        for i, res in enumerate(results):
            if res == -1:
                frauds.append(purchases[i])

        # write out checked purchases
        with open('purchases.pkl', 'wb') as handle:
            pickle.dump(self.oldPurchases, handle)
    
        
def main():
    debug = False
    if (len(sys.argv) > 1):
        if (sys.argv[1] == '-d'):
            debug = True
        else:
            print("Usage: ./app.py [-d]\n\t-d DebugMode")
    fraud = FraudAlert(debug)
    fraud.run()

if __name__ == "__main__":
        main()
