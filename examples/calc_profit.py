import cbpro
import os
import json
import copy
import time
import pdb

'''
How to calculate crypto gains?
    To find your total profits, multiply the sale price 
    of your crypto by how much of the coin you bought. 
    If you bought 2 bitcoin and the selling price is $10,000, 
    then the total sale amount is $10,000 x 2 = $20,000. 
    Next, subtract how much you paid for the crypto plus any fees 
    you paid to sell it.

overall algorithm
    get every account id
    get every order id from each account id
    get the buy orders, (excuted value and fill size)
        sum up the executed value (USD invested)
        sum up the fill size (coin amount you bought)

    total profit for each crypto currency
    (total fill size * total executed value) - total executed value
'''

public_client = cbpro.PublicClient()

api_url="https://api-public.sandbox.pro.coinbase.com" 
auth_client = cbpro.AuthenticatedClient(os.environ["API_KEY"], os.environ["CLIENT_SECRET"], os.environ["PASSPHARSE"], api_url=api_url)

def print_json(data):
    print(json.dumps(data, indent=4, sort_keys=True))

def write_to_json(data, filename):
    with open('outputs/{}'.format(filename), 'w') as out:
        json.dump(data, out, indent=4, sort_keys=True)

def get_acount_ids():
    accounts = auth_client.get_accounts()
    id_info = {}
    # write_to_json(accounts)
    for account in accounts:
        if float(account["balance"]) == 0.0:
            continue
        id_info[account["id"]] = {account["currency"]: float(account["balance"])}

    # print_json(id_info)
    return id_info

def get_order_ids(acc_info):
    orders = []
    for acc_id, balance in acc_info.items():
        time.sleep(1)
        his = auth_client.get_account_history(acc_id)
        his_list = list(his)
        invested = 0
        for item in his_list:
            # type transfer don't have order id
            if "order_id" in item["details"].keys():
                order_id = item["details"]["order_id"]
                if order_id not in orders:
                    orders.append(order_id)
    return orders
'''
{
    "BTC_USD": {
                    "invested": 5000
                    "coins": 0.01 
                }
}
'''
def get_order_details(order_ids):
    orders = {}
    first_time = True
    for order_id in order_ids:
        order_info = auth_client.get_order(order_id)
        # write_to_json(order_info, "get_order.json")
        product_id = order_info["product_id"]
        invested = float(order_info["executed_value"])
        coins = float(order_info["filled_size"])
        if product_id not in orders.keys():
            orders[product_id] = {"invested": invested, "coins": coins}
        else:
            orders[product_id]["invested"] += invested
            orders[product_id]["coins"] += coins

    # print_json(orders)
    return orders

def calcuate_profit(order_details):
    res = {}
    for product_id, detail in order_details.items():
        res[product_id] = {}
        time.sleep(1)
        stats = public_client.get_product_24hr_stats(product_id)
        if "last" in stats.keys():
            last = float(stats["last"])
            value_as_of_today = detail["coins"] * last
            invested = detail["invested"]
            profit = value_as_of_today - invested

            res[product_id]["value_of_today"] = value_as_of_today
            res[product_id]["total_invested"] = invested
            res[product_id]["profit"] = profit
            res[product_id]["percent_gain_or_loss"] = (profit/invested) * 100
    return res


def main():
    if not os.path.exists('outputs'):
        os.makedirs('outputs')
    acc_id = get_acount_ids()
    order_ids = get_order_ids(acc_id)
    order_details = get_order_details(order_ids)
    profits = calcuate_profit(order_details)
    print_json(profits)
if __name__ == "__main__":
    main()