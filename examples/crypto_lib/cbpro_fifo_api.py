from crypto_lib.api_interface import ApiInterface
import crypto_lib.cbpro_api_utils as utils

class CbproFifoApi(ApiInterface):
    def __init__(self, public_client, auth_client):
        self.__public_client = public_client
        self.__auth_client = auth_client

    def get_unrealized_gain(self):
        print("get unrealized gain...")

    def get_realized_gain(self):
        print("get realized gain...")
        res = {}
        acc_ids = utils.get_acount_ids(self.__auth_client)
        order_ids = utils.get_order_ids(self.__auth_client, acc_ids)
        # utils.get_order_details(self.__auth_client, order_ids)
        fills = utils.get_fills_order_details(self.__auth_client, order_ids)
        res = self.__get_unrealized_gain(fills)
        print(res)

    def get_crypto_tax(self):
        print("get crypto tax info...")
    '''
        {
            "BTC_USD": {date: expected return} 
        }
    '''
    def __get_unrealized_gain(self, fills):
        res = {}
        index = 0
        for product_id, fill_orders in fills.items():
            crypto_balance = 0
            for fill_order in fill_orders:
                try:
                    side = fill_order["side"]
                except:
                    import pdb; pdb.set_trace()
                # calcuate the gain/loss once client makes a sale, else added up the
                # accumulated crypto.
                if side == "sell":
                    expected_return = self.__calc_unrealized_gain(crypto_balance, fill_orders[:index+1])
                    if product_id not in res:
                        res[product_id] = {fill_order["created_at"]: expected_return}
                else:
                    crypto_balance += float(fill_order["size"])
                index += 1
        return res

    # calculate the unrealized gain/loss once client makes a sale
    def __calc_unrealized_gain(self, crypto_balance, sub_fills):
        total_expected_return = 0
        for fill_order in sub_fills:
            size = float(fill_order["size"]) # the amount of crypto you purchased or sold
            settle_price = float(fill_order["price"]) # the price of the crypto
            try:
                volume = float(fill_order["usd_volume"]) # amount of USD you spend to buy crypto
            except:
                print("Error: unhandled key in fill order: {}".format(fill_order))
            weight = size / crypto_balance
            expected_return = size * settle_price / volume - 1 # percentage of individual return
            total_expected_return += (weight * expected_return)

        fee_percentage = float(fill_order["fee"]) / volume
        total_expected_return = total_expected_return - fee_percentage
        return total_expected_return
