# stellar-sdk >= 2.0.0 required
# create a completely new and unique pair of keys
# see more about KeyPair objects: https://stellar-sdk.readthedocs.io/en/latest/api.html#keypair
from stellar_sdk.keypair import Keypair
import json



fileName = 'accounts.json'
users = ['Alice', 'Bob']

def users_info(users):
    data=[]
    for user in users:
        pair = Keypair.random()
        data.append({'name': user, 'secret': pair.secret, 'publicKey': pair.public_key})
    return data

with open(fileName, 'w+') as f:
    json.dump(users_info(users), f)
