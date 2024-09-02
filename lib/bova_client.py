import requests
import hashlib
import json
from typing import Any, Dict, Optional

class BovaClient:
    def __init__(self, api_host: str, api_secret: str, api_token: str = None):
        self.api_host = api_host
        self.api_secret = api_secret
        self.api_token = api_token

    def _generate_signature(self, payload: dict) -> str:
        combined_string = f"{self.api_secret}{json.dumps(payload, separators=(',', ':'))}"
        signature = hashlib.sha1(combined_string.encode()).hexdigest()
        return signature

    def _headers(self, signature: str = None) -> Dict[str, str]:
        headers = {
            "Content-Type": "application/json",
        }
        if signature:
            headers["Signature"] = signature
        if self.api_token:
            headers["Authorization"] = f"Bearer {self.api_token}"
        return headers


    def create_payment(self, payload: dict) -> dict:
        url = f"{self.api_host}/v1/p2p_transactions"
        signature = self._generate_signature(payload)
        headers = self._headers(signature)
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()
        return response_data

    def mark_payment_as_paid(self, tx_id: str) -> Dict[str, Any]:
        url = f"{self.api_host}/v1/p2p_transactions/{tx_id}/paid"
        headers = self._headers()
        response = requests.put(url, headers=headers)
        return response.json()

    def cancel_payment(self, tx_id: str) -> Dict[str, Any]:
        url = f"{self.api_host}/v1/p2p_transactions/{tx_id}/cancel"
        headers = self._headers()
        response = requests.put(url, headers=headers)
        return response.json()

    def get_payment_by_id(self, payment_id: str) -> Dict[str, Any]:
        url = f"{self.api_host}/v1/p2p_transactions/{payment_id}"
        headers = self._headers()
        response = requests.get(url, headers=headers)
        return response.json()

    def create_dispute(self, transaction_id: str, amount: int, proof_images: Optional[list[str]] = None) -> Dict[str, Any]: # add changes for photo
        url = f"{self.api_host}/v1/p2p_disputes/from_client"
        data = {
            "transaction_id": transaction_id,
            "p2p_dispute[amount]": str(amount),
        }
        files = {}
        if proof_images is not None:
            for i, proof_image in enumerate(proof_images):
                if i == 0:
                    files['p2p_dispute[proof_image]'] = proof_image
                else:
                    files[f'p2p_dispute[proof_image{i+1}]'] = proof_image
        
        headers = self._headers()
        response = requests.post(url, headers=headers, data=data, files=files)
        return response.json()


    def create_mass_transaction(self, mass_transaction_request: Dict[str, Any]) -> Dict[str, Any]:
        url = f"{self.api_host}/v1/mass_transactions"
        payload = mass_transaction_request
        signature = self._generate_signature(payload)
        headers = self._headers(signature)
        response = requests.post(url, headers=headers, data=payload)
        return response.json()

    def get_mass_transaction_by_id(self, transaction_id: str) -> Dict[str, Any]:
        url = f"{self.api_host}/v1/mass_transactions/{transaction_id}"
        headers = self._headers()
        response = requests.get(url, headers=headers)
        return response.json()


    def get_account_balances(self) -> Dict[str, Any]:
        url = f"{self.api_host}/v1/merchant/accounts"
        headers = self._headers()
        response = requests.get(url, headers=headers)
        return response.json()


    def get_merchant_rates(self) -> Dict[str, Any]:
        url = f"{self.api_host}/v1/merchant/rates"
        headers = self._headers()
        response = requests.get(url, headers=headers)
        return response.json()

    
    def get_merchant_deposits(self, payload: dict) -> dict:
        url = f"{self.api_host}/merchant/v1/deposits"
        signature = self._generate_signature(payload)
        headers = self._headers(signature)
        response = requests.post(url, headers=headers, data=payload)
        response_data = response.json()
        return response_data
