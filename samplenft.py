# Connect ----------------------------------------------------------------------
import xrpl
testnet_url = "https://s.altnet.rippletest.net:51234"
client = xrpl.clients.JsonRpcClient(testnet_url)

# Address
# rEzp7civgsK3X9sEFTr7s2t6uT27NmNSm2
# Secret
# sp5KtuzzRteeCCTu6JsurowZWZjEM
# Balance
# 1,000 XRP
# Sequence Number
# 21580734

# Get credentials from the Testnet Faucet --------------------------------------
# For production, instead create a Wallet instance
faucet_url = "https://faucet.altnet.rippletest.net/accounts"
print("Getting 2 new accounts from the Testnet faucet...")
from xrpl.wallet import generate_faucet_wallet
cold_wallet = generate_faucet_wallet(client, debug=True)
hot_wallet = generate_faucet_wallet(client, debug=True)


# Configure issuer (cold address) settings -------------------------------------
cold_settings_tx = xrpl.models.transactions.AccountSet(
    account=cold_wallet.classic_address,
    transfer_rate=0,
    set_flag=xrpl.models.transactions.AccountSetFlag.ASF_DEFAULT_RIPPLE,
)

cst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=cold_settings_tx,
    wallet=cold_wallet,
    client=client,
)
print("Sending cold address AccountSet transaction...")
response = xrpl.transaction.send_reliable_submission(cst_prepared, client)
print(response)


# Configure hot address settings -----------------------------------------------
hot_settings_tx = xrpl.models.transactions.AccountSet(
    account=hot_wallet.classic_address,
    set_flag=xrpl.models.transactions.AccountSetFlag.ASF_REQUIRE_AUTH,
)
hst_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=hot_settings_tx,
    wallet=hot_wallet,
    client=client,
)
print("Sending hot address AccountSet transaction...")
response = xrpl.transaction.send_reliable_submission(hst_prepared, client)
print(response)


# Create trust line from hot to cold address -----------------------------------
currency_code = "64656E6163687477616368740000000000000000"
trust_set_tx = xrpl.models.transactions.TrustSet(
    account=hot_wallet.classic_address,
    limit_amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
        currency=currency_code,
        issuer=cold_wallet.classic_address,
        value="1000000000000000e-96", # Large limit, arbitrarily chosen
    )
)

ts_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=trust_set_tx,
    wallet=hot_wallet,
    client=client,
)

print("Creating trust line from hot address to issuer...")
response = xrpl.transaction.send_reliable_submission(ts_prepared, client)
print(response)


# Send token -------------------------------------------------------------------
issue_quantity = "1000000000000000e-96"
send_token_tx = xrpl.models.transactions.Payment(
    account=cold_wallet.classic_address,
    destination=hot_wallet.classic_address,
    amount=xrpl.models.amounts.issued_currency_amount.IssuedCurrencyAmount(
        currency=currency_code,
        issuer=cold_wallet.classic_address,
        value=issue_quantity
    ),
    memos=[xrpl.models.transactions.Memo(memo_data="72656e74", memo_type="687474703a2f2f6578616d706c652e636f6d2f6d656d6f2f67656e65726963")]
)

pay_prepared = xrpl.transaction.safe_sign_and_autofill_transaction(
    transaction=send_token_tx,
    wallet=cold_wallet,
    client=client,
)
print(f"Sending {issue_quantity} {currency_code} to {hot_wallet.classic_address}...")
response = xrpl.transaction.send_reliable_submission(pay_prepared, client)
print(response)


# Check balances ---------------------------------------------------------------
print("Getting hot address balances...")
response = client.request(xrpl.models.requests.AccountLines(
    account=hot_wallet.classic_address,
    ledger_index="validated",
))
print(response)

print("Getting cold address balances...")
response = client.request(xrpl.models.requests.GatewayBalances(
    account=cold_wallet.classic_address,
    ledger_index="validated",
    hotwallet=[hot_wallet.classic_address]
))
print(response)
