import requests
import json

class Nessi(object):

    def __init__(self, permission, apiKey):
        self.baseUrl = 'http://api.reimaginebanking.com';
        self.enterprise = False;
        self.customer = False;
        if permission == 'customer':
            self.customer = True
        elif permission == 'enterprise':
            self.enterprise = True
        else:
            print("invalid permission for Nessi")
            return;
        self.apiKey = apiKey

    def __addIdUrl__(self, base, key, value):
        return '{}/{}/{}'.format(base,key,value)

    def __generateEndpointUrl__(self, endpoint, ids, params):
        params.append(('key', self.apiKey))
        retString = self.baseUrl
        for idPair in ids:
            retString = self.__addIdUrl__(retString, idPair[0], idPair[1])
        if (endpoint != ''):
            retString = '{}/{}'.format(retString, endpoint)
        for i, param in enumerate(params):
            if i == 0:
                retString = '{}?{}={}'.format(retString, param[0], param[1])
            else:
                retString = '{}&{}={}'.format(retString, param[0], param[1])
        return retString

    def __sendGetRequest__(self, url):
        resp = requests.get(url)
        if not resp.ok:
            print('nessi failed with code {}'.format(resp.status_code))
            print(resp.content)
            return None
        return json.loads(resp.content)

    def __sendDeleteRequest__(self, url):
        resp = requests.delete(url)
        if not resp.ok:
            print('nessi failed with code {}'.format(resp.status_code))
            print(resp.content)
            return None
        return json.loads(resp.content)

    def __sendPostRequest__(self, url, payload):
        resp = requests.post(url, data=json.dumps(payload), headers={'content-type':'application/json'})
        if not resp.ok:
            print('nessi failed with code {}'.format(resp.status_code))
            print(resp.content)
            return None
        return json.loads(resp.content)

    def __sendPutRequest__(self, url, payload):
        resp = requests.put(url, data=json.dumps(payload), headers={'content-type':'application/json'})
        if not resp.ok:
            print('nessi failed with code {}'.format(resp.status_code))
            print(resp.content)
            return None
        return json.loads(resp.content)


    ############
    # CUSTOMER #
    ############

    # ACCOUNTS

    def getAllAccounts(self, accType = ''):
        if accType == '':
            url = self.__generateEndpointUrl__('accounts', [], [])
        else:
            url = self.__generateEndpointUrl__('accounts', [], [('type', accType)])
        return self.__sendGetRequest__(url)

    def getAccount(self, accId):
        url = self.__generateEndpointUrl__('', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getAccountsByCustomerId(self, customerId):
        url = self.__generateEndpointUrl__('accounts', [('customers', customerId)], [])
        return self.__sendGetRequest__(url)

    def createAccount(self, customerId, account):
        url = self.__generateEndpointUrl__('accounts', [('customers', customerId)], [])
        return self.__sendPostRequest__(url, account)

    def updateAccount(self, accId, account):
        url = self.__generateEndpointUrl__('', [('accounts', accId)], [])
        return self.__sendPutRequest__(url, account)

    def deleteAccount(self, accId):
        url = self.__generateEndpointUrl__('', [('accounts', accId)], [])
        return self.__sendDeleteRequest__(url)

    # ATM

    def getAtms(self, lat='', lng='', rad=''):
        params = []
        if lat != '':
            params.append(('lat', lat))
        if lng != '':
            params.append(('lng', lng))
        if rad != '':
            params.append(('rad', rad))
        url = self.__generateEndpointUrl__('atms', [], params)
        return self.__sendGetRequest__(url)

    def getAtm(self, atmId):
        url = self.__generateEndpointUrl__('', [('atms', atmId)], [])
        return self.__sendGetRequest__(url)

    # Bill

    def getBillsByAccount(self, accId):
        url = self.__generateEndpointUrl__('bills', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getBill(self, billId):
        url = self.__generateEndpointUrl__('', [('bills', billId)], [])
        return self.__sendGetRequest__(url)

    def getBillsByCustomer(self, customerId):
        url = self.__generateEndpointUrl__('bills', [('customers', customerId)], [])
        return self.__sendGetRequest__(url)

    def createBill(self, accId, bill):
        url = self.__generateEndpointUrl__('bills', [('accounts', accId)], [])
        return self.__sendPostRequest__(url, bill)

    def updateBill(self, billId, bill):
        url = self.__generateEndpointUrl__('', [('bills', billId)], [])
        return self.__sendPutRequest__(url, bill)

    def deleteBill(self, billId):
        url = self.__generateEndpointUrl__('', [('bills', billId)], [])
        return self.__sendDeleteRequest__(url)


    # Branch

    def getBranches(self):
        url = self.__generateEndpointUrl__('branches', [], [])
        return self.__sendGetRequest__(url)

    def getBranch(self, branchId):
        url = self.__generateEndpointUrl__('', ['branches', branchId], [])
        return self.__sendGetRequest__(url)

    # Customer

    def getCustomerByAccount(self, accId):
        url = self.__generateEndpointUrl__('customer', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getCustomers(self):
        url = self.__generateEndpointUrl__('customers', [], [])
        return self.__sendGetRequest__(url)

    def getCustomer(self, customerId):
        url = self.__generateEndpointUrl__('', [('customers', customerId)], [])
        return self.__sendGetRequest__(url)

    def createCustomer(self, customer):
        url = self.__generateEndpointUrl__('customers', [], [])
        return self.__sendPostRequest__(url, customer)

    def updateCustomer(self, customerId, customer):
        url = self.__generateEndpointUrl__('', [('customers', customerId)], [])
        return self.__sendPutRequest__(url, customer)

    # Deposit

    def getDepositsByAccount(self, accId):
        url = self.__generateEndpointUrl__('deposits', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getDeposit(self, depositId):
        url = self.__generateEndpointUrl__('', ['deposits', depositId], [])
        return self.__sendGetRequest__(url)

    def createDeposit(self, accId, deposit):
        url = self.__generateEndpointUrl__('deposits', [('accounts', accId)], [])
        return self.__sendPostRequest__(url, deposit)

    def updateDeposit(self, depositId, deposit):
        url = self.__generateEndpointUrl__('', [('deposits', depositId)], [])
        return self.__sendPutRequest__(url, deposit)

    def deleteDeposit(self, depositId):
        url = self.__generateEndpointUrl__('', [('deposits', depositId)], [])
        return self.__sendDeleteRequest__(url)

    # Loan

    def getLoansByAccount(self, accId):
        url = self.__generateEndpointUrl__('loans', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getLoan(self, loanId):
        url = self.__generateEndpointUrl__('', ['loans', loanId], [])
        return self.__sendGetRequest__(url)

    def createLoan(self, accId, loan):
        url = self.__generateEndpointUrl__('loans', [('accounts', accId)], [])
        return self.__sendPostRequest__(url, loan)

    def updateLoan(self, loanId, loan):
        url = self.__generateEndpointUrl__('', [('loans', loanId)], [])
        return self.__sendPutRequest__(url, loan)

    def deleteLoan(self, loanId):
        url = self.__generateEndpointUrl__('', [('loans', loanId)], [])
        return self.__sendDeleteRequest__(url)


    # Merchant

    def getMerchants(self):
        url = self.__generateEndpointUrl__('merchants', [], [])
        return self.__sendGetRequest__(url)

    def getMerchant(self, merchantId):
        url = self.__generateEndpointUrl__('', ['merchants', merchantId], [])
        return self.__sendGetRequest__(url)

    def createMerchant(self, merchant):
        url = self.__generateEndpointUrl__('merchants', [], [])
        return self.__sendPostRequest__(url, merchant)

    def updateMerchant(self, merchantId, merchant):
        url = self.__generateEndpointUrl__('', [('merchants', merchantId)], [])
        return self.__sendPutRequest__(url, merchant)


    # Purchase

    def getPurchasesByAccount(self, accId):
        url = self.__generateEndpointUrl__('purchases', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getPurchaesByAccountAndMerchant(self, accId, merchantId):
        url = self.__generateEndpointUrl__('purchases', [('merchants', merchantId), ('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getPurchasesByMerchant(self, merchantId):
        url = self.__generateEndpointUrl__('purchases', [('merchants', merchantId)], [])
        return self.__sendGetRequest__(url)

    def getPurchase(self, purchaseId):
        url = self.__generateEndpointUrl__('', ['purchases', purchaseId], [])
        return self.__sendGetRequest__(url)

    def createPurchase(self, accId, purchase):
        url = self.__generateEndpointUrl__('purchases', [('accounts', accId)], [])
        return self.__sendPostRequest__(url, purchase)

    def updatePurchase(self, purchaseId, purchase):
        url = self.__generateEndpointUrl__('', [('purchases', purchaseId)], [])
        return self.__sendPutRequest__(url, purchase)

    def deletePurchase(self, purchaseId):
        url = self.__generateEndpointUrl__('', [('purchases', purchaseId)], [])
        return self.__sendDeleteRequest__(url)


    # Transfer

    def getTransfersByAccount(self, accId):
        url = self.__generateEndpointUrl__('transfers', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getTransfer(self, transferId):
        url = self.__generateEndpointUrl__('', ['transfers', transferId], [])
        return self.__sendGetRequest__(url)

    def createTransfer(self, accId, transfer):
        url = self.__generateEndpointUrl__('transfers', [('accounts', accId)], [])
        return self.__sendPostRequest__(url, transfer)

    def updateTransfer(self, transferId, transfer):
        url = self.__generateEndpointUrl__('', [('transfers', transferId)], [])
        return self.__sendPutRequest__(url, transfer)

    def deleteTransfer(self, transferId):
        url = self.__generateEndpointUrl__('', [('transfers', transferId)], [])
        return self.__sendDeleteRequest__(url)


    # Withdrawal

    def getWithdrawalsByAccount(self, accId):
        url = self.__generateEndpointUrl__('withdrawals', [('accounts', accId)], [])
        return self.__sendGetRequest__(url)

    def getWithdrawal(self, withdrawalId):
        url = self.__generateEndpointUrl__('', ['withdrawals', withdrawalId], [])
        return self.__sendGetRequest__(url)

    def createWithdrawal(self, accId, withdrawal):
        url = self.__generateEndpointUrl__('withdrawals', [('accounts', accId)], [])
        return self.__sendPostRequest__(url, withdrawal)

    def updateWithdrawal(self, withdrawalId, withdrawal):
        url = self.__generateEndpointUrl__('', [('withdrawals', withdrawalId)], [])
        return self.__sendPutRequest__(url, withdrawal)

    def deleteWithdrawal(self, withdrawalId):
        url = self.__generateEndpointUrl__('', [('withdrawals', withdrawalId)], [])
        return self.__sendDeleteRequest__(url)


    ##############
    # Enterprise #
    ##############

    # Account

    def enterpriseGetAccounts(self):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('/enterprise/accounts', [], [])
        return self.__sendGetRequest__(url)

    def enterpriseGetAccount(self, accId):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('', [('/enterprise/accounts', accId)], [])
        return self.__sendGetRequest__(url)


    # Bill

    def enterpriseGetBills(self):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('/enterprise/bills', [], [])
        return self.__sendGetRequest__(url)

    def enterpriseGetBill(self, billId):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('', [('/enterprise/bills', billId)], [])
        return self.__sendGetRequest__(url)

    # Customer

    def enterpriseGetCustomers(self):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('/enterprise/customers', [], [])
        return self.__sendGetRequest__(url)

    def enterpriseGetCustomer(self, customerId):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('', [('/enterprise/customers', customerId)], [])
        return self.__sendGetRequest__(url)

    # Deposit

    def enterpriseGetDeposits(self):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('/enterprise/deposits', [], [])
        return self.__sendGetRequest__(url)

    def enterpriseGetDeposit(self, depositId):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('', [('/enterprise/deposits', depositId)], [])
        return self.__sendGetRequest__(url)

    # Merchant

    def enterpriseGetMerchants(self):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('/enterprise/merchants', [], [])
        return self.__sendGetRequest__(url)

    def enterpriseGetMerchant(self, merchantId):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('', [('/enterprise/merchants', merchantId)], [])
        return self.__sendGetRequest__(url)

    # Transfer

    def enterpriseGetTransfers(self):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('/enterprise/transfers', [], [])
        return self.__sendGetRequest__(url)

    def enterpriseGetTransfer(self, transferId):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('', [('/enterprise/transfers', transferId)], [])
        return self.__sendGetRequest__(url)

    # Withdrawal

    def enterpriseGetWithdrawals(self):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('/enterprise/withdrawals', [], [])
        return self.__sendGetRequest__(url)

    def enterpriseGetWithdrawal(self, withdrawalId):
        if not self.enterprise:
            print('tried to access enterprise URL not in enterprise mode')
            return None
        url = self.__generateEndpointUrl__('', [('/enterprise/withdrawals', withdrawalId)], [])
        return self.__sendGetRequest__(url)
