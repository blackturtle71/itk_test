from django.shortcuts import get_object_or_404
from django.db.models import F
from django.db.utils import DataError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Wallet
from .serializers import WalletSerializer

class WalletView(APIView):
    def get(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        serialzier = WalletSerializer(wallet)
        return Response(serialzier.data)

# not sure if you really have to disallow posting outside of /operations/, but here we go
class WalletOperation(WalletView):
    def post(self, request, wallet_uuid):
        wallet = get_object_or_404(Wallet, uuid=wallet_uuid)
        operation_type = request.data.get('operation_type')
        amount = request.data.get('amount')

        # check op type
        if operation_type not in ['DEPOSIT', 'WITHDRAW']:
            return Response({"error" : "Invalid operation"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            amount = float(amount)
            if amount <= 0:
                raise ValueError
        except (TypeError, ValueError):
            return Response({"error" : "Value must be a positive number"}, status=status.HTTP_400_BAD_REQUEST)
        
        # perform op (with race condition prevention)
        if operation_type == "DEPOSIT":
            try:
                Wallet.objects.select_for_update().filter(uuid=wallet_uuid).update(balance=F('balance') + amount)
            except (DataError): # can explicitly check for numeric field overflow, but meh
                return Response({"error" : "You are too rich :("}, status=status.HTTP_400_BAD_REQUEST)
            
        elif operation_type == "WITHDRAW":
            if wallet.balance < amount:
                return Response({"error" : "Insufficient funds"}, status=status.HTTP_400_BAD_REQUEST)
            Wallet.objects.select_for_update().filter(uuid=wallet_uuid).update(balance=F('balance') - amount)
        
        wallet.refresh_from_db()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)

# tiny generator for manual testing    
class WalletGen(APIView):
    def get(self, request):
        wallet = Wallet.objects.create()
        serializer = WalletSerializer(wallet)
        return Response(serializer.data)
            


