
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAYPAL_BASE_URL = "https://api-m.sandbox.paypal.com"


def get_paypal_access_token():
    client_id = os.getenv("PAYPAL_CLIENT_ID")
    client_secret = os.getenv("PAYPAL_CLIENT_SECRET")

    if not client_id or not client_secret:
        return None, "PayPal Sandbox credentials are missing from .env"

    try:
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v1/oauth2/token",
            auth=(client_id, client_secret),
            headers={
                "Accept": "application/json",
                "Accept-Language": "en_US",
            },
            data={"grant_type": "client_credentials"},
            timeout=20,
        )

        if response.status_code != 200:
            return None, f"PayPal authentication failed: {response.text}"

        return response.json()["access_token"], None

    except requests.RequestException as error:
        return None, f"Could not connect to PayPal: {error}"


def create_order(amount, currency="USD"):
    token, error = get_paypal_access_token()

    if error:
        return None, error

    try:
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json={
                "intent": "CAPTURE",
                "purchase_units": [
                    {
                        "amount": {
                            "currency_code": currency,
                            "value": f"{float(amount):.2f}",
                        }
                    }
                ],
                "application_context": {
                    "brand_name": "PayPal AI SpendWise",
                    "user_action": "PAY_NOW",
                },
            },
            timeout=20,
        )

        if response.status_code not in (200, 201):
            return None, f"Order creation failed: {response.text}"

        order = response.json()
        approval_url = next(
            (
                link["href"]
                for link in order.get("links", [])
                if link.get("rel") == "approve"
            ),
            None,
        )

        return {
            "id": order["id"],
            "status": order["status"],
            "approval_url": approval_url,
        }, None

    except requests.RequestException as error:
        return None, f"Could not create PayPal order: {error}"


def capture_order(order_id):
    token, error = get_paypal_access_token()

    if error:
        return None, error

    try:
        response = requests.post(
            f"{PAYPAL_BASE_URL}/v2/checkout/orders/{order_id}/capture",
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {token}",
            },
            json={},
            timeout=20,
        )

        if response.status_code not in (200, 201):
            return None, f"Payment capture failed: {response.text}"

        return response.json(), None

    except requests.RequestException as error:
        return None, f"Could not capture payment: {error}"
