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

purcs = []
for acc in accounts:
    nessi.deleteAccount(acc)

