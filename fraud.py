# fraud.py

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

# make fraudulent charge
badstore = {
    "name": "badstore",
    "category": [
        "badstuff"
    ],
    "address": {
        "street_number": "10",
        "street_name": "Mass Ave",
        "city": "Cambridge",
        "state": "MA",
        "zip": "02138"
    },
    "geocode": {
        "lat": 37.757815,
        "lng": -122.5076404
    }
}
response = nessi.createMerchant(badstore)
if response["code"] != 201:
    print "badstore failed"

clothing = {
    "merchant_id": response["objectCreated"]["_id"],
    "medium": "balance",
    "purchase_date": "2016-12-10",
    "amount": round(random.uniform(1000.0, 5000.0), 2),
    "description": "clothing"
}

# send fraudulent charge
response = nessi.createPurchase(accounts[0], clothing)
if response["code"] != 201:
    print "bad purchase failed"