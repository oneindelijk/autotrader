from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import generic
from utils.at_exceptions import BalanceError, CurrencyError
import shutil
# Create your views here.

from .models import Wallet, Balance, Operation, Currency
from .graphs import  operations_graph_per_balance

def get_extra_content(active_id):
    pages = ['wallets', 'balance']
    Pages = []
    for i,p in enumerate(pages):
        Pages.append({'active': i + 1 == active_id,
                      'id': i + 1, 
                      'link':'portofolio:' + p,
                      'title': p[0].upper() + p[1:]
                      })
    return {'pages_list':Pages, 'app':'portofolio'}

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
    ActiveWallet = Wallet.objects.get(id=balance.wallet.id)
    operations = Operation.objects.filter(balance = balance)
    O = Operation()
    graph = operations_graph_per_balance(balance.pk)
    context = {'owner': balance.wallet.owner,'balance': balance, 'operations': operations, 'app': 'wallet','wallet': ActiveWallet, 'graph': graph}
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