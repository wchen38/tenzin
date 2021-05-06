import cbpro
import os
from crypto_lib.cbpro_weighted_api import CbproWeightedApi

def main():
    print("hello world")
    public_client = cbpro.PublicClient()
    api_url="https://api-public.sandbox.pro.coinbase.com"
    auth_client = cbpro.AuthenticatedClient(os.environ["API_KEY"], os.environ["CLIENT_SECRET"], os.environ["PASSPHRASE"], api_url=api_url)

    weighted_api = CbproWeightedApi(public_client, auth_client)
    weighted_api.get_realized_gain()
    weighted_api.get_avg_profit()

if __name__ == "__main__":
    main()