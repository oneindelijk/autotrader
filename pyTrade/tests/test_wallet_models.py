import unittest
from django.test import TestCase
from wallet.models import Wallet, Currency, Balance, Operation
from utils.at_exceptions import CurrencyError, BalanceError
import random

class TestWalletModels(TestCase):

    def setUp(self):

        ''' test create currencies '''

        USD = Currency(symbol='$', name='US Dollar', abbreviation = 'USD', rate=1)
        USD.save()
        BRL = Currency(symbol='R$', name='Brazilian Pesos', abbreviation = 'BRL', rate=1)
        BRL.save()
        ''' create test wallet '''
        W = Wallet(owner = 'TestCase : Owner', baseCurrency = USD)
        W.save()
        ''' create balances with for currencies '''
        for curr in [W.baseCurrency, BRL]:
            B = Balance(wallet = W, currency = curr)
            B.amount = random.random() * random.randint(1,10000000)
            B.save()

        self.O = Operation(wallet = W)
    
    def test_addToBalance_baseCurrency(self):

        ''' add an amount without stating a currency '''

        bal = Balance.objects.filter(currency = self.O.wallet.baseCurrency)
        basis_amount = bal[0].amount
        add_amount = random.random() * random.randint(1,10000000)
        self.O.addToBalance(add_amount)
        self.assertEqual(bal[0].amount, add_amount + basis_amount)

    def test_addToBalance_definedCurrency(self):

        ''' add an amount stating the currency '''

        testCurrencyABB = 'BRL'
        testCurrency = Currency.objects.get(abbreviation = 'BRL')
        bal = Balance.objects.filter(currency = testCurrency)
        basis_amount = bal[0].amount
        add_amount = random.random() * random.randint(1,10000000)
        self.O.addToBalance(add_amount, testCurrencyABB)
        self.assertEqual(bal[0].amount, add_amount + basis_amount)
        
    def test_addToBalance_missingCurrency(self):

        ''' try adding an amount with a non existing currency '''

        add_amount = random.random() * random.randint(1,10000000)
        with self.assertRaises(CurrencyError):
            self.O.addToBalance(add_amount, 'TRK')
        

    def tearDown(self):
        pass
