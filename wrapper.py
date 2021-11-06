from typing import List, Any
import json
from utils.requests_retry_session import requests_retry_session
from utils.parsers import parse_datetime


class PaystackAPI(object):
    def __init__(self, api_key: str):
        self._session = requests_retry_session()
        self._headers = {"Authorization": f"Bearer {api_key}"}
        self._BASE_URL = "https://api.paystack.co"

    def create_customer(self, data):
        """Create a customer account on paystack_api

        Parameters:
        data (dict): payload containing email, first_name, metadata (dict)

        Returns:
        dict: Payload of created customer on paystack_api
        """
        response = self._session.post(
            f"{self._BASE_URL}/customer", data=data, headers=self._headers
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", None)

    def fetch_customer(self, email_or_customer_code):
        """Fetch a customer account on paystack_api

        Parameters:
        email_or_customer_code (string): customer's email or customer_code on paystack_api

        Returns:
        dict: Payload of a customer on paystack_api
        """
        response = self._session.get(
            f"{self._BASE_URL}/customer/{email_or_customer_code}", headers=self._headers
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", None)

    def create_subaccount(self, data):
        """Create a subaccount on paystack_api

        Parameters:
        data (dict): business_name, settlement_bank, account_number, percentage_charge, primary_contact_email, primary_contact_name, primary_contact_phone, settlement_schedule

        Returns:
        dict: Payload of a created subaccount on paystack_api
        """
        response = self._session.post(
            f"{self._BASE_URL}/subaccount", data=data, headers=self._headers
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", None)

    def fetch_subaccounts(self, page: int = 1, limit: int = 50):
        """Fetch all subaccounts on paystack_api

        Parameters:
        page (int):
        limit (int):

        Returns:
        dict: List of subaccounts on paystack_api
        """
        response = self._session.get(
            f"{self._BASE_URL}/subaccount?page={page}&perPage={limit}",
            headers=self._headers,
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", [])

    def fetch_subaccount(self, data):
        pass

    def fetch_plans(self, page: int = 1, limit: int = 50):
        """Fetch all plans on paystack_api

        Parameters:
        page (int):
        perPage (int):

        Returns:
        dict: List of plans on paystack_api
        """

        response = self._session.get(
            f"{self._BASE_URL}/plan?page={page}&perPage={limit}", headers=self._headers
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", [])

    def fetch_plan(self, plan_id_or_code):
        response = self._session.get(
            f"{self._BASE_URL}/plan/{plan_id_or_code}", headers=self._headers
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", [])

    def create_subscription(
        self, customer_code, plan_code, authorization=None, start_date=None
    ):
        data = {
            "customer": customer_code,
            "plan": plan_code,
            "start_date": start_date,
            "authorization": authorization,
        }
        response = self._session.post(
            f"{self._BASE_URL}/subsciption", data=data, headers=self._headers
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", [])

    def fetch_subscriptions(self, page: int = 1, limit: int = 50):
        """Fetch all subscriptions on paystack_api

        Parameters:
        page (int):
        perPage (int):

        Returns:
        dict: List of subscriptions on paystack_api
        """

        response = self._session.get(
            f"{self._BASE_URL}/subscription?page={page}&perPage={limit}",
            headers=self._headers,
        )
        response.raise_for_status()
        content = response.json()
        return content.get("data", [])

    def fetch_subscription(self, subscription_code):
        pass

    def disable_subscription(self, code, token):
        pass

    def enable_subscription(self):
        pass

    def fetch_banks(self, currency="GHS"):
        response = self._session.get(
            f"{self._BASE_URL}/bank?currency={currency}", headers=self._headers
        )
        response.raise_for_status()
        return response.json().get("data", [])

    def resolve_account_number(self, account_number, bank_code):
        try:
            response = self._session.get(
                f"{self._BASE_URL}/bank/resolve?account_number={account_number}&bank_code={bank_code}",
                headers=self._headers,
            )
            response.raise_for_status()
            return response.json()["data"]
        except Exception as e:
            raise e

    def create_transfer_recipient(
        self, _type, name, account_number, bank_code, currency="GHS"
    ):
        payload = {
            "type": _type,
            "name": name,
            "account_number": account_number,
            "bank_code": bank_code,
            "currency": currency,
        }
        response = self._session.post(
            f"{self._BASE_URL}/transferrecipient",
            data=json.dumps(payload),
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()["data"]

    def transfer_funds(
        self, recipient_code, amount, reason=None, source="balance", currency="GHS"
    ):
        payload = {
            "recipient": recipient_code,
            "amount": amount,
            "reason": reason,
            "source": source,
            "currency": currency,
        }
        response = self._session.post(
            f"{self._BASE_URL}/transfer", data=json.dumps(payload), headers=self._headers
        )
        response.raise_for_status()
        return response.json()["data"]

    def initialize_transaction(self, customer_email, amount, sub_account=None):
        payload = {"email": customer_email, "amount": amount}
        if sub_account:
            payload["subaccount"] = sub_account

        response = self._session.post(
            f"{self._BASE_URL}/transaction/initialize",
            data=json.dumps(payload),
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()["data"]

    def _charge(
        self,
        customer_email,
        channel,
        amount,
        sub_account=None,
        currency="GHS",
        authorization_code=None,
        mobile_money=None,
    ):
        payload = {
            "email": customer_email,
            "amount": amount,
            "currency": currency,
        }
        if sub_account:
            payload["subaccount"] = sub_account
        url = "charge"

        if channel == "authorization_code":
            payload["authorization_code"] = authorization_code
            url = "transaction/charge_authorization"
        elif channel == "mobile_money":
            payload["mobile_money"] = mobile_money
            url = "charge"

        response = self._session.post(
            f"{self._BASE_URL}/{url}", data=json.dumps(payload), headers=self._headers
        )
        response.raise_for_status()
        return response.json()

    def charge_authorization_code(
        self, customer_email, amount, payment_token, currency="GHS", sub_account=None
    ):
        return self._charge(
            customer_email=customer_email,
            channel="authorization_code",
            amount=amount,
            currency=currency,
            sub_account=sub_account,
            authorization_code=payment_token,
        )

    def charge_momo(self, customer_email, amount, payment_token, currency="GHS", sub_account=None):
        return self._charge(
            customer_email=customer_email,
            channel="mobile_money",
            amount=amount,
            currency=currency,
            sub_account=sub_account,
            mobile_money=payment_token,
        )

    def verify_transaction(self, reference):
        response = self._session.get(
            f"{self._BASE_URL}/transaction/verify/{reference}", headers=self._headers
        )
        response.raise_for_status()
        data = response.json()
        return data["data"]

    def submit_otp(self, otp, reference):
        payload = {"otp": otp, "reference": reference}
        response = self._session.post(
            f"{self._BASE_URL}/charge/submit_otp",
            data=json.dumps(payload),
            headers=self._headers,
        )
        response.raise_for_status()
        return response.json()["data"]

    def check_charge(self, reference: str):
        response = self._session.get(
            f"{self._BASE_URL}/charge/{reference}", headers=self._headers
        )
        response.raise_for_status()
        data = response.json()
        return data["data"]

    def fetch_settlements(self, page: int = 1, limit: int = 25) -> List[dict[str, Any]]:
        settlements = []
        response = self._session.get(
            f"{self._BASE_URL}/settlement?page={page}&perPage={limit}",
            headers=self._headers,
        )
        response.raise_for_status()
        content = response.json()
        data = content["data"]
        pagination = content["meta"]

        settlements.extend(
            [
                {
                    "id": s["id"],
                    "date": parse_datetime(s["settlement_date"]).date(),
                    "status": s["status"],
                    "total_amount": s["total_amount"],
                }
                for s in data
            ]
        )

        total = pagination["total"]
        if page <= total:
            next_page = int(page) + 1
            settlements += self.fetch_settlements(page=next_page)

        return settlements

    def fetch_settled_transaction_references(self, settlement_id: int, page: int = 1, limit: int = 25) -> List[str]:
        references = []
        response = self._session.get(
            f"{self._BASE_URL}/settlement/{settlement_id}/transactions?page={page}&perPage={limit}",
            headers=self._headers,
        )
        response.raise_for_status()
        content = response.json()
        data = content["data"]
        pagination = content["meta"]

        references.extend([t["reference"] for t in data])

        total = pagination["total"]
        if page <= total:
            next_page = int(page) + 1
            references += self.fetch_settled_transaction_references(
                settlement_id, page=next_page
            )

        return references
