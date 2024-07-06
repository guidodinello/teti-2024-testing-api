import requests
from iroha import SignedTransaction
from scalecodec import ScaleBytes
from scalecodec.types import Vec

"""

Pending Transactions

    Protocol: HTTP
    Method: GET
    Encoding: SCALE
    Endpoint: /pending_transactions

Requests

A GET request to the endpoint.
Responses
Code	Response	Description
200	OK	Returns a list of pending transactions as SignedTransaction objects encoded with SCALE; must be decoded by the client.

https://hyperledger.github.io/iroha-2-docs/reference/data-model-schema.html#signedtransaction

SignedTransaction
Type: Enum
Variants:
Variant name	Variant value	Discriminant
V1	SignedTransactionV1	1

"""


def get_pending_transactions(url):
    response = requests.get(f"{url}/pending_transactions")
    if response.status_code == 200:
        raw_data = response.content
        scale_bytes = ScaleBytes(raw_data)
        transactions = Vec(SignedTransaction).decode(scale_bytes)
        return transactions
    else:
        print(f"Error: Received status code {response.status_code}")
        return None


base_url = "http://localhost:8080"
pending_txs = get_pending_transactions(base_url)

if pending_txs is not None:
    print(f"Number of pending transactions: {len(pending_txs)}")
    for i, tx in enumerate(pending_txs, 1):
        print(f"Transaction {i}:")
        print(f"  Hash: {tx.transaction.hash}")
        print(f"  Creator: {tx.transaction.payload.account_id}")
