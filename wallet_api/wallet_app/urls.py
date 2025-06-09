from django.urls import path
from .views import WalletView, WalletOperation, WalletGen

urlpatterns = [
    path('wallets/<uuid:wallet_uuid>/', WalletView.as_view()),
    path('wallets/<uuid:wallet_uuid>/operation/', WalletOperation.as_view()),
    path('walletgen/', WalletGen.as_view())
]