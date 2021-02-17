from crypto_lib.cbpro_fifo_api import CbproFifoApi
import cbpro
import os

class ApiManager:

    @staticmethod
    def create_api(type):
        public_client = cbpro.PublicClient()
        api_url="https://api-public.sandbox.pro.coinbase.com"
        auth_client = cbpro.AuthenticatedClient(os.environ["API_KEY"], os.environ["CLIENT_SECRET"], os.environ["PASSPHARSE"], api_url=api_url)
        # auth_client = cbpro.AuthenticatedClient(os.environ["API_KEY"], os.environ["CLIENT_SECRET"], os.environ["PASSPHARSE"])
        if type == "cbpro_fifo":
            return CbproFifoApi(public_client, auth_client)
        else:
            print("this {} does not exist yet".format(type))