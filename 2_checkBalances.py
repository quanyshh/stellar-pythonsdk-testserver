from stellar_sdk.server import Server
import json

fileName = 'accounts.json'
with open(fileName) as r:
    accounts = json.load(r)

server = Server("https://horizon-testnet.stellar.org")

for user in accounts:
    account = server.accounts().account_id(user['publicKey']).call()
    for balance in account['balances']:
        print(f"User: {user['name']}, ID: {account['id']}")
        print(f"Type: {balance['asset_type']}, Balance: {balance['balance']}")
        print()