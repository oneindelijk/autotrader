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
        BRL = Currency(symbol='R$', name='Brazilian Pesos', abbreviation = 'BRL', rate=0.41)
        BRL.save()
        YEN = Currency(symbol='Y$', name='Japonese Yen', abbreviation = 'YEN', rate=1.4)
        YEN.save()
        ''' create test wallet '''
        self.W = Wallet(owner = 'TestCase : Owner', baseCurrency = USD)
        self.W.save()
        ''' create balances with for currencies '''
        for curr in [self.W.baseCurrency, BRL, YEN]:
            B = Balance(wallet = self.W, currency = curr)
            B.amount = random.random() * random.randint(1,10000000)
            B.save()

        self.O = Operation(wallet = self.W)
    
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
        
    def test_wallet_addToBalanceDirectly(self):

        ''' test amount added through wallet directly, omitting currency '''
        
        add_amount = random.random() * random.randint(1,10000000)
        orig_amount = self.W.total_balance()
        self.W.addToBalance(add_amount)
        self.assertAlmostEqual(self.W.total_balance(),add_amount + orig_amount)

        
    def test_wallet_subtractFromBalanceDirectly(self):

        ''' test amount subtract from wallet directly, omitting currency '''
        
        orig_amount = self.W.single_balance()
        del_amount = random.randint(1,int(orig_amount))
        self.W.subtractFromBalance(del_amount)
        self.assertAlmostEqual(self.W.single_balance(),orig_amount - del_amount)
        
    def test_wallet_subtractTooMuchFromBalanceDirectly(self):

        ''' test too big an amount subtract from wallet directly, omitting currency '''
        
        orig_amount = self.W.single_balance()
        del_amount = int(orig_amount) + 10
        with self.assertRaises(BalanceError):
            self.W.subtractFromBalance(del_amount)
        
    def test_wallet_addToBalanceWithCurrency(self):

        ''' test amount added through wallet With Currency '''
        
        currency = 'YEN'
        add_amount = random.random() * random.randint(1,10000000)
        orig_amount = self.W.single_balance(currency)
        self.W.addToBalance(add_amount, currency)
        self.assertAlmostEqual(self.W.single_balance(currency),add_amount + orig_amount)
        
    def test_wallet_addToBalanceWithFaultyCurrency(self):

        ''' test amount added through wallet With Non Existing Currency '''
        
        currency = 'YEP'
        add_amount = random.random() * random.randint(1,10000000)
        with self.assertRaises(CurrencyError):
            self.W.addToBalance(add_amount, currency)
        

        
    def test_wallet_subtractFromBalanceWithCurrency(self):

        ''' test amount subtract from wallet With Currency '''
        
        currency = 'YEN'
        orig_amount = self.W.single_balance(currency)
        del_amount = random.randint(1,int(orig_amount))
        self.W.subtractFromBalance(del_amount, currency)
        self.assertAlmostEqual(self.W.single_balance(currency),orig_amount - del_amount)
        
    def test_wallet_subtractTooMuchFromBalanceWithCurrency(self):

        ''' test too big an amount subtract from wallet With Currency '''
        
        currency = 'YEN'
        orig_amount = self.W.single_balance(currency)
        del_amount = int(orig_amount) + 10
        with self.assertRaises(BalanceError):
            self.W.subtractFromBalance(del_amount, currency)
        

    def tearDown(self):
        pass
