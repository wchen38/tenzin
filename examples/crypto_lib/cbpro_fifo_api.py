from crypto_lib.api_interface import ApiInterface
import crypto_lib.cbpro_api_utils as utils

class CbproFifoApi(ApiInterface):
    def __init__(self, public_client, auth_client):
        self.__public_client = public_client
        self.__auth_client = auth_client

    def get_unrealized_gain(self):
        pass

    def get_realized_gain(self):
        pass

    def get_crypto_tax(self):
        pass

