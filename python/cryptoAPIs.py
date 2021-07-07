import requests
import ccxt
import sys
import debugpy

from functools import partial


def get_scan_balance(coin):
    symbol = coin.symbol
    url = coin.tracker.url
    wallet_addresses = coin.walletAddresses
    api_key = coin.tracker.apiKey
    contract_address = coin.contractAddress
    coin_multiplier = coin.tracker.coinMultiplier

    switcher = {
        'BTC': partial(get_bitcoin_balance, url, wallet_addresses, coin_multiplier),
        'SAFEMOON': partial(get_bscscan_balance, url, wallet_addresses, api_key, contract_address, coin_multiplier),
        'DOGE': partial(get_doge_balance, url, wallet_addresses, coin_multiplier),
        'ETH': partial(get_eth_balance, url, wallet_addresses, api_key, coin_multiplier)
    }

    func = switcher.get(symbol, lambda: 'Invalid Coin')
    return func()


def get_bscscan_balance(scan_url, wallet_addresses, api_key, contract_address, coin_multiplier):
    total = 0
    for wallet_address in wallet_addresses:
        url = scan_url.format(contract_address, wallet_address, api_key)
        total += (float)(requests.get(url).json()["result"]) * float(coin_multiplier)
    return total


def get_bitcoin_balance(scan_url, wallet_addresses, coin_multiplier):
    total = 0
    for wallet_address in wallet_addresses:
        url = scan_url.format(wallet_address)
        total += (float)(requests.get(url).json()["balance"]) * float(coin_multiplier)
    return total


def get_doge_balance(scan_url, wallet_addresses, coin_multiplier):
    total = 0
    for wallet_address in wallet_addresses:
        url = scan_url.format(wallet_address)
        total += (float)(requests.get(url).json()["balance"]) * float(coin_multiplier)
    return total


def get_eth_balance(scan_url, wallet_addresses, api_key, coin_multiplier):
    total = 0
    url = scan_url.format(",".join(wallet_addresses), api_key)
    results = (requests.get(url).json()['result'])
    for result in results:
        total += (float)(result['balance'])

    return (float)(total * float(coin_multiplier))


def get_exchange_rate(localCurrency, api_key):
    if localCurrency == 'USD':
        rate = 1.0
    else:
        url = "https://free.currconv.com/api/v7/convert?q=USD_{0}&compact=ultra&api_key={1}".format(
            localCurrency, api_key)
        rate = (float)(requests.get(url).json()["USD_{0}".format(localCurrency)])
    return rate


def update_data(financial_data_item, coin):
    global financialDataList
    exchange = ccxt.gateio()

    try:
        financial_data_item.previous_balance = financial_data_item.current_balance

        financial_data_item.current_balance = get_scan_balance(coin)
        ticker = exchange.fetch_ticker(coin.tradingPair)
        financial_data_item.previous_rate = financial_data_item.current_rate
        financial_data_item.current_rate = (float)(ticker['info']['last'])

        financial_data_item.previous_perc = financial_data_item.current_perc
        financial_data_item.current_perc = (float)(ticker['info']['percentChange'])

        financial_data_item.previous_balance_change = financial_data_item.current_balance_change

        if financial_data_item.current_balance != 0 and financial_data_item.previous_balance != 0:
            financial_data_item.current_balance_change = financial_data_item.current_balance_change + \
                (financial_data_item.current_balance - financial_data_item.previous_balance)
        else:
            # Initial setting
            financial_data_item.current_balance_change = 0

        return financial_data_item
    except:
        # Bit of a hack -- If CCXT timesout, just return the original object and hopefully it gets sorted next round
        return financial_data_item
