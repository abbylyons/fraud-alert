# notfraud.py

from NessiWrapper import Nessi
import json

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
clothing = {
    "merchant_id": "asdf"
    "medium": "balance",
    "purchase_date": "2016-05-10",
    "amount": round(random.uniform(20.0, 100.0), 2),
    "description": "clothing"
}

# send good charge
response = nessi.createPurchase(accounts[0], clothing)
if response["code"] != 201:
    print "good purchase failed"