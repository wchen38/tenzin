from crypto_lib.cbpro_api import CbproApi
class ApiManager:

    @staticmethod
    def create_api(type):
        if type == "cbpro":
            return CbproApi()
        else:
            print("this {} does not exist yet".format(type))