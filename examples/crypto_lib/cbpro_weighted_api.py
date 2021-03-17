# from crypto_lib.api_interface import ApiInterface
import crypto_lib.cbpro_api_utils as utils
import copy

class CbproWeightedApi():
    def __init__(self, public_client, auth_client):
        self.__public_client = public_client
        self.__auth_client = auth_client
        self.__workbook = {} 

    def get_unrealized_gain(self):
        print("get unrealized gain...")

    '''
        {
            "BTC_USD": {date: expected return} 
        }
    '''
    def get_realized_gain(self):
        print("get realized gain...")
        res = {}
        acc_ids = utils.get_acount_ids(self.__auth_client)
        order_ids = utils.get_order_ids(self.__auth_client, acc_ids)
        # utils.get_order_details(self.__auth_client, order_ids)
        fills = utils.get_fills_order_details(self.__auth_client, order_ids)

        for product_id, fill_orders in fills.items():
            crypto_balance = 0
            for index, fill_order in enumerate(fill_orders):
                side = fill_order["side"]
                # calcuate the gain/loss once client makes a sale, else added up the
                # accumulated crypto.
                if side == "sell":
                    expected_return = self.__calc_unrealized_gain(crypto_balance, fill_orders[:index+1])
                    if product_id not in self.__workbook:
                        self.__workbook[product_id] = {fill_order["created_at"]: {"realized": expected_return}}
                    else:
                        self.__workbook[product_id].update({fill_order["created_at"]: {"realized": expected_return}})
                else:
                    crypto_balance += float(fill_order["size"])
        print("realized gain:\n{}".format(self.__workbook))
    
    def get_avg_profit(self):
        print("get average profit...")
        if self.__workbook == {}:
            print("Error: Needs to caluate the realized gain first!")
            return
        
        for product_id, profit_records in self.__workbook.items():
            profit_sum = 0
            loss_sum = 0
            profit_prob = 0
            avg_profit = 0
            avg_loss = 0
            num_profit = 0
            total_sales = 0
            records_copy = copy.deepcopy(profit_records)
            for date, record in records_copy.items():
                gain = record["realized"]
                total_sales += 1
                if total_sales == 1:
                    if gain > 0:
                        num_profit = 1
                        profit_sum = gain
                        avg_profit = gain
                        profit_records[date]["average_profit"] = gain
                        profit_records[date]["average_loss"] = 0
                        profit_records[date]["profit_probability"] = 1
                    else:
                        profit_loss = gain
                        avg_loss = gain
                        profit_records[date]["average_profit"] = 0
                        profit_records[date]["average_loss"] = gain
                        profit_records[date]["profit_probability"] = 0
                else:
                    if gain > 0:
                        num_profit += 1
                        profit_sum += gain
                        avg_profit = profit_sum / num_profit
                    else:
                        loss_sum -= gain
                        avg_loss = loss_sum / (total_sales - num_profit)
                    profit_records["average_profit"] = avg_profit
                    profit_records["average_loss"] = avg_loss
                    profit_records["profit_probability"] = num_profit / total_sales
        print(self.__workbook)


    def get_crypto_tax(self):
        print("get crypto tax info...")

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