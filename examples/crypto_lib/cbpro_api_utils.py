import time

# helping with debug the api
def print_json(data):
    print(json.dumps(data, indent=4, sort_keys=True))

def get_acount_ids(client):
    print("get account ids...", flush=True)
    accounts = client.get_accounts()
    id_info = []
    # write_to_json(accounts)
    for account in accounts:
        id_info.append(account["id"])
    # print_json(id_info)
    return id_info

# get the order ids from each account id
def get_order_ids(client, acc_ids):
    print("get order ids...", flush=True)
    orders = []
    for acc_id in acc_ids:
        time.sleep(1)
        his = client.get_account_history(acc_id)
        his_list = list(his)
        invested = 0
        for item in his_list:
            # type transfer don't have order id
            if "order_id" in item["details"].keys():
                order_id = item["details"]["order_id"]
                if order_id not in orders:
                    orders.append(order_id)
    return orders


def get_order_details(client, order_ids):
    print("get_order_details...", flush=True)
    orders = {}
    first_time = True
    for order_id in order_ids:
        time.sleep(0.5)
        order_info = client.get_order(order_id)
        # write_to_json(order_info, "get_order.json")
        try:
            product_id = order_info["product_id"]
        except:
            pdb.set_trace()
        invested = float(order_info["executed_value"])
        coins = float(order_info["filled_size"])
        if product_id not in orders.keys():
            orders[product_id] = {"invested": invested, "coins": coins}
        else:
            orders[product_id]["invested"] += invested
            orders[product_id]["coins"] += coins

    # print_json(orders)
    return orders

def get_fills_order_details(client):
    import pdb; pdb.set_trace()
    time.sleep(0.5)
    # btc_fills = client.get_fills("BTC-USD")
    btc_fills = client.get_fills("5d98cd72-ee60-454d-acd1-2276d11983fb")
    print(list(btc_fills))
    return orders