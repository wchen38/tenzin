from tenzin.crypto_lib.cbpro_weighted_api import CbproWeightedApi
import pytest
from unittest import mock

# buy, sell
fill_1 = [{'created_at': '2021-03-01T06:21:08', 'trade_id': 1, 'product_id': 'BTC-USD', 'order_id': 'xxxx', 'user_id': 'xxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '34233', 'size': '0.145', 'fee': '25', 'side': 'buy', 'settled': True, 'usd_volume': '4975'}, {'created_at': '2021-03-02T05:43:05.399Z', 'trade_id': 2, 'product_id': 'BTC-USD', 'order_id': 'xxx', 'user_id': 'xxxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '41017', 'size': '0.145', 'fee': '29.74', 'side': 'sell', 'settled': True, 'usd_volume': '5917.73'}]

# buy, buy, sell
fill_2 = [{'created_at': '2021-03-03T06:21:08', 'trade_id': 3, 'product_id': 'BTC-USD', 'order_id': 'xxx', 'user_id': 'xxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '33262', 'size': '0.177', 'fee': '29.59', 'side': 'buy', 'settled': True, 'usd_volume': '5888.14'}, {'created_at': '2021-04-02T06:21:08.79Z', 'trade_id': 4, 'product_id': 'BTC-USD', 'order_id': 'xxx', 'user_id': 'xxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '34345', 'size': '0.290', 'fee': '50', 'side': 'buy', 'settled': True, 'usd_volume': '9950'},{'created_at': '2021-03-05T05:43:05.399Z', 'trade_id': 5, 'product_id': 'BTC-USD', 'order_id': 'xxx', 'user_id': 'xxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '39220', 'size': '0.467', 'fee': '91.53', 'side': 'sell', 'settled': True, 'usd_volume': '15213.64'}]

fill_3 = [{'created_at': '2021-03-06T06:21:08', 'trade_id': 6, 'product_id': 'BTC-USD', 'order_id': 'xxxx', 'user_id': 'xxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '34866', 'size': '0.519', 'fee': '90.92', 'side': 'buy', 'settled': True, 'usd_volume': '18092.41'}, {'created_at': '2021-03-07T07:43:05.399Z', 'trade_id': 7, 'product_id': 'BTC-USD', 'order_id': 'xxx', 'user_id': 'xxxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '33706', 'size': '0.519', 'fee': '87.45', 'side': 'sell', 'settled': True, 'usd_volume': '17315.57'}]

fill_4 = [{'created_at': '2021-03-08T06:21:08', 'trade_id': 6, 'product_id': 'BTC-USD', 'order_id': 'xxxx', 'user_id': 'xxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '29010', 'size': '0.598', 'fee': '87.22', 'side': 'buy', 'settled': True, 'usd_volume': '17357.05'}, {'created_at': '2021-03-09T07:43:05.399Z', 'trade_id': 7, 'product_id': 'BTC-USD', 'order_id': 'xxx', 'user_id': 'xxxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '35978', 'size': '0.598', 'fee': '107.63', 'side': 'sell', 'settled': True, 'usd_volume': '21418.46'}]

fill_5 = [{'created_at': '2021-03-10T06:21:08', 'trade_id': 6, 'product_id': 'BTC-USD', 'order_id': 'xxxx', 'user_id': 'xxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '33819', 'size': '0.63', 'fee': '107.09', 'side': 'buy', 'settled': True, 'usd_volume': '21311.37'}, {'created_at': '2021-03-11T07:43:05.399Z', 'trade_id': 7, 'product_id': 'BTC-USD', 'order_id': 'xxx', 'user_id': 'xxxx', 'profile_id': 'xxx', 'liquidity': 'T', 'price': '37912', 'size': '0.4', 'fee': '43.63', 'side': 'sell', 'settled': True, 'usd_volume': '15121.17'}]
fills = {}
fills["BTC-USD"] = []
fills["BTC-USD"].extend(fill_1)
fills["BTC-USD"].extend(fill_2)
fills["BTC-USD"].extend(fill_3)
fills["BTC-USD"].extend(fill_4)
fills["BTC-USD"].extend(fill_5)


@mock.patch(
    "tenzin.crypto_lib.cbpro_weighted_api.utils.get_fills_order_details"
)
@mock.patch("tenzin.crypto_lib.cbpro_weighted_api.utils.get_acount_ids")
@mock.patch("tenzin.crypto_lib.cbpro_weighted_api.utils.get_order_ids")
def test_get_realized_gain(
    mock_get_order_ids,
    mock_get_account_ids,
    mock_get_fills
):
    mock_get_fills.return_value = fills
    mock_get_account_ids = ""
    mock_get_order_ids = ""
    fake_public_clent = ""
    fake_auth_client = ""
    api = CbproWeightedApi(fake_public_clent, fake_auth_client)

    api.get_realized_gain()
    api.get_appt()
    assert api.workbook["BTC-USD"]['2021-03-09T07:43:05']['appt'] == pytest.approx(0.1279, 0.1)


@pytest.mark.parametrize(
    "balance, fills, result",
    [
        (0.145, fill_1, 0.19),
        (0.467, fill_2, 0.145)
    ])
def test_calc_realized_gain(balance, fills, result):
    fake_public_clent = ""
    fake_auth_client = ""
    api = CbproWeightedApi(fake_public_clent, fake_auth_client)

    res = api._CbproWeightedApi__calc_realized_gain(balance, fills)
    assert res == pytest.approx(result, 0.1)

@pytest.mark.parametrize(
    "account_ids, result",
    [
        ([], True),
        ({}, False)
    ]
)
@mock.patch("tenzin.crypto_lib.cbpro_weighted_api.utils.get_acount_ids")
def test_is_valid_account(mock_get_account_id, account_ids, result):
    mock_get_account_id.return_value = account_ids
    api = CbproWeightedApi("", "")
    is_valid = api.is_valid_account()
    assert is_valid is result
