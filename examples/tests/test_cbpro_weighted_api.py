from crypto_lib.cbpro_weighted_api import CbproWeightedApi
import pytest

# buy, sell
fills1 = [{'created_at': '2021-03-02T06:21:08.79Z', 'trade_id': 25298423, 'product_id': 'BTC-USD', 'order_id': '502b3160-bc7e-4ee2-b261-d472311a682f', 'user_id': '5e16bbd6ec45e904d35370e5', 'profile_id': '744f9c7a-859e-4df8-9e61-62200ada11f5', 'liquidity': 'T', 'price': '34233', 'size': '0.145', 'fee': '25', 'side': 'buy', 'settled': True, 'usd_volume': '5000'}, {'created_at': '2021-03-01T05:43:05.399Z', 'trade_id': 25217298, 'product_id': 'BTC-USD', 'order_id': 'ed26f8f9-d75b-4758-8281-f9172090f3c3', 'user_id': '5e16bbd6ec45e904d35370e5', 'profile_id': '744f9c7a-859e-4df8-9e61-62200ada11f5', 'liquidity': 'T', 'price': '41017', 'size': '0.145', 'fee': '29.74', 'side': 'sell', 'settled': True, 'usd_volume': '5947.47'}]

# buy, buy, sell
fills2 = [{'created_at': '2021-03-02T06:21:08.79Z', 'trade_id': 25298423, 'product_id': 'BTC-USD', 'order_id': '502b3160-bc7e-4ee2-b261-d472311a682f', 'user_id': '5e16bbd6ec45e904d35370e5', 'profile_id': '744f9c7a-859e-4df8-9e61-62200ada11f5', 'liquidity': 'T', 'price': '33262', 'size': '0.177', 'fee': '29.59', 'side': 'buy', 'settled': True, 'usd_volume': '5917.73'}, {'created_at': '2021-03-02T06:21:08.79Z', 'trade_id': 25298423, 'product_id': 'BTC-USD', 'order_id': '502b3160-bc7e-4ee2-b261-d472311a682f', 'user_id': '5e16bbd6ec45e904d35370e5', 'profile_id': '744f9c7a-859e-4df8-9e61-62200ada11f5', 'liquidity': 'T', 'price': '34345', 'size': '0.290', 'fee': '50', 'side': 'buy', 'settled': True, 'usd_volume': '10000'},{'created_at': '2021-03-01T05:43:05.399Z', 'trade_id': 25217298, 'product_id': 'BTC-USD', 'order_id': 'ed26f8f9-d75b-4758-8281-f9172090f3c3', 'user_id': '5e16bbd6ec45e904d35370e5', 'profile_id': '744f9c7a-859e-4df8-9e61-62200ada11f5', 'liquidity': 'T', 'price': '39220', 'size': '0.467', 'fee': '91.53', 'side': 'sell', 'settled': True, 'usd_volume': '18305.17'}]

@pytest.mark.parametrize("balance, fills, result",
                            [
                                (0.145, fills1, 0.1894),
                                (0.467, fills2, 0.1453)
                            ])
def test_calc_realized_gain(balance, fills, result):
    fake_public_clent = ""
    fake_auth_client = ""
    api = CbproWeightedApi(fake_public_clent, fake_auth_client)

    res = api._CbproWeightedApi__calc_realized_gain(balance, fills)
    assert res == pytest.approx(res, 0.1)