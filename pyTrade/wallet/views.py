from django.shortcuts import render

# Create your views here.

from .models import Wallet, Balance

def index(request):
    Wallets = Wallet.objects.all()
    context = {'Wallets': Wallets}
    return render(request, 'wallet/index.html', context)
    

def detail(request, wallet_id):
    ActiveWallet = Wallet.objects.get(pk=wallet_id)
    Balances = Balance.objects.filter(wallet = ActiveWallet)
    context = {'owner': ActiveWallet.owner,
                'wallet_id': ActiveWallet.id,
                'balances': Balances
    }
    return render(request, 'wallet/detail.html', context)

def balance_detail(request, balance_id):
    Balances = Balance.objects.get(pk = balance_id)
    context = {'balances': Balances}
    return render(request, 'wallet/balance_detail.html', context)