from django.test import TestCase
from rest_framework.test import APIClient
from .models import Wallet

class WalletAPITest(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.wallet = Wallet.objects.create()

    def test_get_balance(self):
        response = self.client.get(f"/api/v1/wallets/{self.wallet.uuid}/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["balance"], "0.00")

    def test_deposit(self):
        data = {"operation_type": "DEPOSIT", "amount": 500}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["balance"], "500.00")

    def test_withdraw(self):
        data = {"operation_type": "DEPOSIT", "amount": 500}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        data = {"operation_type": "WITHDRAW", "amount": 500}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data["balance"], "0.00")

    def test_deposit_too_much(self):
        data = {"operation_type": "DEPOSIT", "amount": 1000000000}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_withdraw_insufficient_funds(self):
        data = {"operation_type": "WITHDRAW", "amount": 2000}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_withdraw_invalid_amount(self):
        data = {"operation_type": "WITHDRAW", "amount": -2}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_withdraw_invalid_datatype(self):
        data = {"operation_type": "WITHDRAW", "amount": "MONEY"}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        self.assertEqual(response.status_code, 400)

    def test_wrong_opetarion_type(self):
        data = {"operation_type": "gibberish", "amount": 13}
        response = self.client.post(f"/api/v1/wallets/{self.wallet.uuid}/operation/", data, format="json")
        self.assertEqual(response.status_code, 400)