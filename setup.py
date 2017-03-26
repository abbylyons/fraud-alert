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
acc = {
    'type': 'Credit Card',
    'nickname' : 'new CC',
    'rewards' : 300,
    'balance' : 678123,
    'account_number' : '4040034488881881'
}
nessi.createAccount(customerId, acc)
resp = nessi.getAccountsByCustomerId(customerId)
for acc in resp:
    accounts.append(acc['_id'])

def setup():
    # put api calls here
    # monthly bill (same day of month, amount varies)
    biller = {"name": "biller", "category": ["bill"], "address": { "street_number": "1", "street_name": "Mass Ave", "city": "Cambridge", "state": "MA", "zip": "02138"}, "geocode": {"lat": 42.3636629, "lng": -71.0558767}}
    response = nessi.createMerchant(biller)
    if response["code"] != 201:
        print "Biller failed"
        return
    bill = {
        "merchant_id": response["objectCreated"]["_id"],
        "medium": "balance",
        "purchase_date": "TODO",
        "amount": 200.00,
        "description": "bill"
    }
    for month in range(1, 13):
        if month < 10:
            bill["purchase_date"] = "2016-0" + str(month) + "-05"
        else:
            bill["purchase_date"] = "2016-" + str(month) + "-05"
        response = nessi.createPurchase(accounts[0], bill)
        if response["code"] != 201:
            print "Bill " + str(month) + " failed"
            return

    # weekly grocery shopping (same day of week)
    grocer = {
        "name": "grocer",
        "category": [
            "groceries"
        ],
        "address": {
            "street_number": "2",
            "street_name": "Mass Ave",
            "city": "Cambridge",
            "state": "MA",
            "zip": "02138"
        },
        "geocode": {
            "lat": 42.3582389,
            "lng": -71.1164017
        }
    }
    response = nessi.createMerchant(grocer)
    if response["code"] != 201:
        print "Grocer failed"
        return
    print('merch id: {}'.format(response["objectCreated"]["_id"]))
    groceries = {
        "merchant_id": response["objectCreated"]["_id"],
        "medium": "balance",
        "purchase_date": "TODO",
        "amount": round(random.uniform(10.0, 40.0), 2),
        "description": "groceries"
    }
    month = 1
    date = 1
    for day in range(0, 365):
        date += 1
        if day == 31:
            month = "02"
            date = 1
        if day == 60:
            month = "03"
            date = 1
        if day == 91:
            month = "04"
            date = 1
        if day == 121:
            month = "05"
            date = 1
        if day == 152:
            month = "06"
            date = 1
        if day == 182:
            month = "07"
            date = 1
        if day == 213:
            month = "08"
            date = 1
        if day == 244:
            month = "09"
            date = 1
        if day == 274:
            month = "10"
            date = 1
        if day == 305:
            month = "11"
            date = 1
        if day == 335:
            month = "12"
            date = 1

        if (day + 3) % 7 == 0:
            if date < 10:
                groceries["purchase_date"] = "2016-{}-0{}".format(month, date)
            else:
                groceries["purchase_date"] = "2016-{}-{}".format(month, date)
            groceries['amount'] = round(random.uniform(10.0, 40.0), 2)
            response = nessi.createPurchase(accounts[0], groceries)
            if response["code"] != 201:
                print "Grocery " + str(day) + " failed"
                return

    # clothing (four times a year, weekend)
    store1 = {
        "name": "store",
        "category": [
            "clothing"
        ],
        "address": {
            "street_number": "3",
            "street_name": "Mass Ave",
            "city": "Cambridge",
            "state": "MA",
            "zip": "02138"
        },
        "geocode": {
            "lat": 42.3679418,
            "lng": -71.0786522
        }
    }
    response = nessi.createMerchant(store1)
    if response["code"] != 201:
        print "Store1 failed"
        return
    clothing = {
        "merchant_id": response["objectCreated"]["_id"],
        "medium": "balance",
        "purchase_date": "TODO",
        "amount": round(random.uniform(20.0, 80.0), 2),
        "description": "clothing"
    }
    clothing["purchase_date"] = "2016-01-03"
    clothing["amount"] = round(random.uniform(20.0, 80.0), 2)
    response = nessi.createPurchase(accounts[0], clothing)
    if response["code"] != 201:
        print "Clothing 1 failed"
        return
    clothing["purchase_date"] = "2016-05-28"
    clothing["amount"] = round(random.uniform(20.0, 80.0), 2)
    response = nessi.createPurchase(accounts[0], clothing)
    if response["code"] != 201:
        print "Clothing 2 failed"
        return
    clothing["purchase_date"] = "2016-11-29"
    clothing["amount"] = round(random.uniform(20.0, 80.0), 2)
    response = nessi.createPurchase(accounts[0], clothing)
    if response["code"] != 201:
        print "Clothing 3 failed"
        return
    clothing["purchase_date"] = "2016-12-18"
    clothing["amount"] = round(random.uniform(20.0, 80.0), 2)
    response = nessi.createPurchase(accounts[0], clothing)
    if response["code"] != 201:
        print "Clothing 4 failed"
        return

    # luxury goods (two times a year, weekend, larger than clothing amount)
    store2 = {
        "name": "luxury",
        "category": [
            "stuff"
        ],
        "address": {
            "street_number": "4",
            "street_name": "Mass Ave",
            "city": "Cambridge",
            "state": "MA",
            "zip": "02138"
        },
        "geocode": {
            "lat": 42.391272,
            "lng": -71.1046068
        }
    }
    response = nessi.createMerchant(store2)
    if response["code"] != 201:
        print "Store2 failed"
        return
    luxury = {
        "merchant_id": response["objectCreated"]["_id"],
        "medium": "balance",
        "purchase_date": "TODO",
        "amount": round(random.uniform(200.0, 1000.0), 2),
        "description": "luxury"
    }
    luxury["purchase_date"] = "2016-05-18"
    luxury["amount"] = round(random.uniform(200.0, 1000.0), 2)
    response = nessi.createPurchase(accounts[0], luxury)
    if response["code"] != 201:
        print "Luxury 1 failed"
        return
    luxury["purchase_date"] = "2016-10-20"
    luxury["amount"] = round(random.uniform(200.0, 1000.0), 2)
    response = nessi.createPurchase(accounts[0], luxury)
    if response["code"] != 201:
        print "Luxury 2 failed"
        return

    # education (twice a year, large amount)
    harvard = {
        "name": "harvard",
        "category": [
            "education"
        ],
        "address": {
            "street_number": "5",
            "street_name": "Mass Ave",
            "city": "Cambridge",
            "state": "MA",
            "zip": "02138"
        },
        "geocode": {
            "lat": 42.3770068,
            "lng": -71.1188488
        }
    }
    response = nessi.createMerchant(harvard)
    if response["code"] != 201:
        print "harvard failed"
        return
    education = {
        "merchant_id": response["objectCreated"]["_id"],
        "medium": "balance",
        "purchase_date": "TODO",
        "amount": 15000.00,
        "description": "education"
    }
    education["purchase_date"] = "2016-01-12"
    response = nessi.createPurchase(accounts[0], education)
    if response["code"] != 201:
        print "Education 1 failed"
        return
    education["purchase_date"] = "2016-08-22"
    response = nessi.createPurchase(accounts[0], education)
    if response["code"] != 201:
        print "Education 2 failed"
        return

    # taxes (once a year, 62400 * 0.25)
    government = {
        "name": "us federal government",
        "category": [
            "government"
        ],
        "address": {
            "street_number": "6",
            "street_name": "Mass Ave",
            "city": "Cambridge",
            "state": "MA",
            "zip": "02138"
        },
        "geocode": {
            "lat": 38.8995322,
            "lng": -77.1546522
        }
    }
    response = nessi.createMerchant(government)
    if response["code"] != 201:
        print "government failed"
        return
    taxes = {
        "merchant_id": response["objectCreated"]["_id"],
        "medium": "balance",
        "purchase_date": "TODO",
        "amount": 15600.00,
        "description": "taxes"
    }
    taxes["purchase_date"] = "2016-04-15"
    response = nessi.createPurchase(accounts[0], taxes)
    if response["code"] != 201:
        print "Taxes failed"
        return


setup()
