from crypto_lib.api_manager import ApiManager
from crypto_lib.api_interface import ApiInterface

def main():
    print("hello world")
    apiMgr = ApiManager.create_api("cbpro")
    apiMgr.getRealizedGain()
    apiMgr.getUnrealizedGain()
    apiMgr.getCryptoTax() 
if __name__ == "__main__":
    main()