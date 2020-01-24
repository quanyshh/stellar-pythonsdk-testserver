import json
import requests


fileName = 'accounts.json'

with open(fileName) as r:
    accounts = json.load(r)

for user in accounts:
    response = requests.get(f"https://friendbot.stellar.org?addr={user['publicKey']}")
    if response.status_code == 200:
        print("SUCCESS! You have a new account :)")
    else:
        print("ERROR!")
