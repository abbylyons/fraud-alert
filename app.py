#!/usr/bin/python

import json
import pickle
import os
import sys
import re
import datetime
import hashlib
import time
import random
from twilio.rest import TwilioRestClient
from NessiWrapper import Nessi
from ml import Svm

def idToint(x):
    hash_object = hashlib.md5(x)
    return int(hash_object.hexdigest(), 16)


class FraudAlert(object):

    def __init__(self, debug):
       
        self.runs = 0
        self.debug = debug
        self.oldPurchases = []
        self.badPurchases = []
        self.accounts = []
        self.svm = Svm('svm.pkl')

        # Load config
        with open('secret.json') as json_data:
            config = json.load(json_data)
            self.apiKey = config['nessi_key']
            self.customerId = config['customer_id']
            self.twilioSid = config['twilio']['sid']
            self.twilioToken = config['twilio']['token']
            self.twilioNumber = config['twilio']['number']
            self.number = config['number']

        # load twilio
        self.twilio = TwilioRestClient(self.twilioSid, self.twilioToken)

        # setup Nessi
        self.nessi = Nessi('customer', self.apiKey)

        # Restore state
        if os.path.isfile('purchases.pkl'):
            with open('purchases.pkl', 'rb') as handle:
                self.oldPurchases = pickle.load(handle)

        if os.path.isfile('badpurchases.pkl'):
            with open('badpurchases.pkl', 'rb') as handle:
                self.badPurchases = pickle.load(handle)

        # Get accounts
        resp = self.nessi.getAccountsByCustomerId(self.customerId)
        for acc in resp:
            self.accounts.append(acc['_id'])


        # refit
        self.refit()
    
    def run(self):
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
                if (not purchase['_id'] in self.oldPurchases) and (not purchase['_id'] in self.badPurchases):
                    newPurchases.append(purchase)
        return newPurchases

    def getInputsFromPurchases(self, purchases):
        inputs = []
        for i, purc in enumerate(purchases):
            if self.debug:
                print('parsing purchases: {}/{}'.format(i, len(purchases)))
            merchant = self.nessi.getMerchant(purc['merchant_id'])
            if merchant == None:
                print('err no merchant')
                sys.exit()
            dateParts = re.findall('(\d{4})-(\d{1,2})-(\d{1,2})', purc['purchase_date'])
            if len(dateParts) == 0:
                print('failed to split date. date was: {}'.format(purc['purchase_date']))
                sys.exit()
            else:
                dateParts = dateParts[0]
            date = datetime.date(int(dateParts[0]), int(dateParts[1]), int(dateParts[2]))
            amount = float(purc['amount']) / 1000
            if amount > 1:
                amount = 1
            inp = [
                (float(merchant['geocode']['lat']) + 90)/180,
                (float(merchant['geocode']['lng'] + 180)/360),
                #idToint(purc['merchant_id']),
                #date.weekday(),
                #int(dateParts[1]) - 1,
                #int(dateParts[0]),
                amount
            ]
            if self.debug:
                print('got input:\n{}'.format(inp))

            inputs.append(inp)

        return inputs

    def refit(self):
        purchases = []
        for acc in self.accounts:
            purchases += self.nessi.getPurchasesByAccount(acc)
        inputs = self.getInputsFromPurchases(purchases)
        if (self.debug):
            print("going to refit")
        self.svm.refit(inputs)
        if (self.debug):
            print("finished refitting")
        
    def classifyPurchases(self):

        purchases = self.getNewPurchases()
        if len(purchases) == 0:
            return
        if (self.debug):
            print("found these purchases")
            print(purchases)

        inputs = self.getInputsFromPurchases(purchases)
        if (self.debug):
            print("got these inputs")
            print(inputs)

        # Classify
        results = self.svm.classify_new(inputs)
        frauds = []
        for i, res in enumerate(results):
            if res == -1:
                self.badPurchases.append(purchases[i]['_id'])
                frauds.append(purchases[i])
            else:
                self.oldPurchases.append(purchases[i]['_id'])
        
        if self.debug:
            print("Fraudulent charges:")
            for f in frauds:
                print(f)
            print("Done")

        if len(frauds) > 0:
            self.notifyUser(frauds)
        
        # write out checked purchases
        with open('purchases.pkl', 'wb') as handle:
            pickle.dump(self.oldPurchases, handle)
        with open('badpurchases.pkl', 'wb') as handle:
            pickle.dump(self.badPurchases, handle)


    def send_message(self, body):
        self.twilio.messages.create(body=body, to=self.number, from_=self.twilioNumber)

    def notifyUser(self, frauds):
        print('numfrauds: {}'.format(len(frauds)))
        if (len(frauds) > 5):
            print('too many')
            return
        body = 'We have detected suspicious purchases on your account.\n\n'
        i = 1
        for fraud in frauds:
            merchant = self.nessi.getMerchant(fraud['merchant_id'])
            body = "{}{}:\n\tMerchant name: {}\n\tDate: {}\n\tDescription: {}\n\tAmount: {}\n\tAt: {}, {}\n\n".format(body, i, merchant['name'], fraud['purchase_date'], fraud['description'], fraud['amount'], merchant['address']['city'], merchant['address']['state'])

        self.send_message(body)
    
        
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
