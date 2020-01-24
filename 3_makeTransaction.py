from stellar_sdk.keypair import Keypair
from stellar_sdk.network import Network
from stellar_sdk.server import Server
from stellar_sdk.transaction_builder import TransactionBuilder
from stellar_sdk.exceptions import NotFoundError, BadResponseError, BadRequestError
import json
from stellar_base.builder import Builder


server = Server("https://horizon-testnet.stellar.org")

fileName = 'accounts.json'
with open(fileName) as r:
    accounts = json.load(r)

source_acc_key = accounts[0]['secret']
source_acc_id = accounts[0]['publicKey']
destination_acc_id = accounts[1]['publicKey']

try:
    server.load_account(destination_acc_id)
except NotFoundError:
    # If the account is not found, surface an error message for logging.
    raise Exception("The destination account does not exist!")

'''builder = Builder(secret=source_acc_key)
bob_address = destination_acc_id
builder.append_payment_op(bob_address, '10', 'XLM')
builder.add_text_memo('For beers') # string length <= 28 bytes
builder.sign()
builder.submit()'''

base_fee = server.fetch_base_fee()
source_account = server.load_account(source_acc_id)
# Start building the transaction.
transaction = (
    TransactionBuilder(
        source_account=source_account,
        network_passphrase='Test SDF Network ; September 2015',
        base_fee=base_fee,
    )
        # Because Stellar allows transaction in many currencies, you must specify the asset type.
        # Here we are sending Lumens.
        .append_payment_op(destination=destination_acc_id, amount="220", asset_code="XLM")
        # A memo allows you to add your own metadata to a transaction. It's
        # optional and does not affect how Stellar treats the transaction.
        .add_text_memo("Test Transaction")
        # Wait a maximum of three minutes for the transaction
        .set_timeout(10)
        .build()
)

# Sign the transaction to prove you are actually the person sending it.
transaction.sign(source_acc_key)

try:
    # And finally, send it off to Stellar!
    response = server.submit_transaction(transaction)
    print(f"Response: {response}")
except (BadRequestError, BadResponseError) as err:
    print(f"Something went wrong!\n{err}")