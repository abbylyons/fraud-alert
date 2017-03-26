# notfraud.py

from NessiWrapper import Nessi
import json
import random

# setup Nessi
with open('secret.json') as json_data:
    config = json.load(json_data)
    apiKey = config['nessi_key']
    customerId = config['customer_id']
nessi = Nessi('customer', apiKey)
accounts = []
resp = nessi.getAccountsByCustomerId(customerId)
for acc in resp:
    accounts.append(acc['_id'])

# make good charge
groceries = {
    "merchant_id": "58d728b01756fc834d906dfe",
    "medium": "balance",
    "purchase_date": "2016-05-10",
    "amount": round(random.uniform(10.0, 40.0), 2),
    "description": "food"
}

# send good charge
response = nessi.createPurchase(accounts[0], groceries)
if response["code"] != 201:
    print "good purchase failed"
