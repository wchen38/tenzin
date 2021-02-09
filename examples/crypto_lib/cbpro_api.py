from crypto_lib.api_interface import ApiInterface

class CbproApi(ApiInterface):
    def getRealizedGain(self):
        print("get realized gain...")

    def getUnrealizedGain(self):
        print("get unrealized gain...")

    def getCryptoTax(self):
        print("get crypto tax info...")