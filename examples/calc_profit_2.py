from crypto_lib.api_manager import ApiManager
from crypto_lib.api_interface import ApiInterface

def main():
    print("hello world")
    apiMgr = ApiManager.create_api("cbpro_fifo")
    apiMgr.get_realized_gain()
    apiMgr.get_unrealized_gain()
    apiMgr.get_crypto_tax() 
if __name__ == "__main__":
    main()