from crypto_lib.cbpro_fifo_api import CbproFifoApi
from crypto_lib.cbpro_weighted_api import CbproWeightedApi
import cbpro
import os

class ApiManager:

    @staticmethod
    def create_api(method):
        public_client = cbpro.PublicClient()
        api_url="https://api-public.sandbox.pro.coinbase.com"
        auth_client = cbpro.AuthenticatedClient(os.environ["API_KEY"], os.environ["CLIENT_SECRET"], os.environ["PASSPHRASE"], api_url=api_url)
        # auth_client = cbpro.AuthenticatedClient(os.environ["API_KEY"], os.environ["CLIENT_SECRET"], os.environ["PASSPHARSE"])
        if method == "cbpro_fifo":
            return CbproFifoApi(public_client, auth_client)
        elif method == "cbpro_weighted":
            return CbproWeightedApi(public_client, auth_client)
        else:
            print("this {} does not exist yet".format(method))