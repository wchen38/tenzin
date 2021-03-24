# from crypto_lib.api_interface import ApiInterface
import crypto_lib.cbpro_api_utils as utils
import copy

class CbproWeightedApi():
    def __init__(self, public_client, auth_client):
        self.__public_client = public_client
        self.__auth_client = auth_client
        self.workbook = {} 

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
            start = 0 # start index of buy trasaction
            crypto_balance = 0 # reset balance with a new crypto
            for index, fill_order in enumerate(fill_orders):
                side = fill_order["side"]
                # calcuate the gain/loss once client makes a sale, else added up the
                # accumulated crypto.
                if side == "sell":
                    utils.write_to_json(fill_orders, "fill_orders.json")
                    expected_return = self.__calc_realized_gain(crypto_balance, fill_orders[start:index+1])
                    if product_id not in self.workbook:
                        self.workbook[product_id] = {fill_order["created_at"]: {"realized": expected_return}}
                    else:
                        self.workbook[product_id].update({fill_order["created_at"]: {"realized": expected_return}})
                    start = index+1 # start index of buy trasaction
                    crypto_balance = 0 # reset balance after each sale
                else:
                    crypto_balance += float(fill_order["size"])

    def get_avg_profit(self):
        print("get average profit...")
        if self.workbook == {}:
            print("Error: Needs to caluate the realized gain first!")
            return

        for product_id, profit_records in self.workbook.items():
            profit_sum = 0
            loss_sum = 0
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
                        profit_prob = 1
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
                        profit_records[date]["average_loss"] = -gain
                        profit_records[date]["profit_probability"] = 0
                else:
                    if gain > 0:
                        num_profit += 1
                        profit_sum += gain
                        avg_profit = profit_sum / num_profit
                    else:
                        loss_sum += gain
                        avg_loss = loss_sum / (total_sales - num_profit)
                    profit_records[date]["average_profit"] = avg_profit
                    profit_records[date]["average_loss"] = avg_loss
                    profit_records[date]["profit_probability"] = num_profit / total_sales
                profit_prob = profit_records[date]["profit_probability"]
                profit_records[date]["appt"] = avg_profit * profit_prob + avg_loss *(1 - profit_prob)
        print(self.workbook)

    def get_crypto_tax(self):
        print("get crypto tax info...")

    # calculate the unrealized gain/loss once client makes a sale
    def __calc_realized_gain(self, crypto_balance, sub_fills):
        total_expected_return = 0
        sell_info = sub_fills[-1]
        sell_price = float(sell_info["price"])
        sell_fee = float(sell_info["fee"])
        try:
            sell_amount = float(sell_info["usd_volume"]) + sell_fee
        except Exception:
            print("Error: unhandled key in fill order: {}".format(sell_info))

        for fill_order in sub_fills[:-1]:
            size = float(fill_order["size"]) # the amount of crypto you purchased or sold
            buy_fee = float(fill_order["fee"])
            try:
                buy_amount = float(fill_order["usd_volume"]) + buy_fee # amount of USD you spend to buy crypto
            except Exception:
                print("Error: unhandled key in fill order: {}".format(fill_order))
            weight = size / crypto_balance
            expected_return = size * sell_price / buy_amount - 1 # percentage of individual return
            total_expected_return += (weight * expected_return)

        fee_percentage = sell_fee / sell_amount
        total_expected_return = total_expected_return - fee_percentage
        return total_expected_return