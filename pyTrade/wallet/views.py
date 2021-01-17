from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from utils.at_exceptions import BalanceError, CurrencyError
import shutil
# Create your views here.

from .models import Wallet, Balance, Operation, Currency

def index(request):
    Wallets = Wallet.objects.all()
    context = {'Wallets': Wallets, 'app': 'wallet'}
    return render(request, 'wallet/index.html', context)
 
def detail(request, wallet_id, message=''):
    ActiveWallet = Wallet.objects.get(pk=wallet_id)
    B = Balance.objects.filter(wallet = ActiveWallet)
    C = Currency.objects.all()
    balances = [{'id': bal.id, 
                'currency': bal.currency,
                'amount': bal.amount,
                'amount_str': '{:0.2f}'.format(bal.amount),
                'converted': '{:0.2f}'.format(bal.converted_balance()) } for bal in B]
    total = '{:0.2f}'.format(sum([bal.converted_balance() for bal in B]) *  ActiveWallet.baseCurrency.rate)
    context = {'owner': ActiveWallet.owner,
                'wallet': ActiveWallet,
                'balances': balances,
                'total': total,
                'currency': C,
                'message': message, 
                'app': 'wallet'
    }
    return render(request, 'wallet/detail.html', context)

def balance_detail(request, balance_id):
    balance = Balance.objects.get(pk = balance_id)
    operations = Operation.objects.filter(balance = balance)
    context = {'owner': balance.wallet.owner,'balance': balance, 'operations': operations, 'app': 'wallet'}
    return render(request, 'wallet/balance_detail.html', context)

def add_valuta(request, wallet_id):
    wallet = get_object_or_404(Wallet, pk=wallet_id)
    try:
        amount = float(request.POST['amount'])
    except ValueError:
        return detail(request,wallet_id,'You must enter an amount')
    else:
        currency_abb = request.POST['currency']
        if request.POST['operation'] == 'deposit':
            wallet.addToBalance(amount, currency_abb)
        else:
            try:
                wallet.subtractFromBalance(amount, currency_abb)
            except (CurrencyError, BalanceError):
                errmsg = shutil.sys.exc_info()[1].args[0]
                return detail(request,wallet_id, errmsg)
            except:
                return detail(request,wallet_id,shutil.sys.exc_info())
            
        return HttpResponseRedirect(reverse('wallet:detail', args=(wallet_id,)))