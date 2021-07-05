import { Coin } from '../types'

export const coinList: Coin[] = [
  {
    symbol: 'SAFEMOON',
    name: 'Safemoon',
    imagePath: '../src/images/safe_logo.bmp',
    blackImagePath: '../src/images/safe_logo_invert.bmp',
    contractAddress: '0x8076c74c5e3f5852037f31ff0093eeb8c8add8d3',
    tradingPair: 'SAFEMOON/USDT',
    tracker: {
      name: 'BSCScan',
      requiresAPI: true,
      coinMultiplier: 0.000000001,
      url: `https://api.bscscan.com/api?module=account&action=tokenbalance&contractaddress={0}&address={1}&tag=latest&apikey={2}`,
      apiKey: '',
      instructions:
        'To track Safemoon, obtain an API key from BSCscan.com https://bscscan.com/register and enter the API key',
    },
    walletAddresses: [],
  },
  {
    symbol: 'BTC',
    name: 'Bitcoin',
    imagePath: '../src/images/btc.png',
    blackImagePath: '../src/images/btc_invert.png',
    contractAddress: '',
    tradingPair: 'BTC/USDT',
    tracker: {
      name: 'Blockcypher',
      requiresAPI: false,
      coinMultiplier: 0.00000001,
      url: `https://api.blockcypher.com/v1/btc/main/addrs/{0}`,
      apiKey: '',
    },
    walletAddresses: [],
  },
  {
    symbol: 'ETH',
    name: 'Ethereum',
    imagePath: '../src/images/eth.png',
    blackImagePath: '../src/images/eth_invert.png',
    contractAddress: '',
    tradingPair: 'ETH/USDT',
    tracker: {
      name: 'EthScan',
      requiresAPI: true,
      coinMultiplier: 0.000000000000000001,
      url: `https://api.etherscan.io/api?module=account&action=balancemulti&address={0}&tag=latest&apikey={1}`,
      apiKey: '',
      instructions:
        'To track Ethereum, obtain an API key from Etherscan.io https://etherscan.io/register and enter the API key',
    },
    walletAddresses: [],
  },
  {
    symbol: 'DOGE',
    name: 'Dogecoin',
    imagePath: '../src/images/doge.png',
    blackImagePath: '../src/images/doge_invert.png',
    contractAddress: '',
    tradingPair: 'DOGE/USDT',
    tracker: {
      name: 'DogeChain',
      requiresAPI: false,
      coinMultiplier: 0.00000001,
      url: `https://dogechain.info/api/v1/address/balance/{0}`,
      apiKey: '',
    },
    walletAddresses: [],
  },
]
