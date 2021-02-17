from crypto_lib.api_interface import ApiInterface
import crypto_lib.cbpro_api_utils as utils

class CbproFifoApi(ApiInterface):
    def __init__(self, public_client, auth_client):
        self.__public_client = public_client
        self.__auth_client = auth_client

    def getUnrealizedGain(self):
        print("get unrealized gain...")
        acc_ids = utils.get_acount_ids(self.__auth_client)
        order_ids = utils.get_order_ids(self.__auth_client, acc_ids)
        utils.get_fills_order_details(self.__auth_client)

    def getRealizedGain(self):
        print("get realized gain...")

    def getCryptoTax(self):
        print("get crypto tax info...")