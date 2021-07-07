export interface NavigationAnswer {
  actionToTake: string
}

export interface CoinChoice {
  name: string
  value: string
}

export interface CryptoTrackerConfig {
  coins: Coin[]
  applicationSettings: ApplicationSettings
}

export interface Coin {
  name: string
  symbol: string
  imagePath?: string
  blackImagePath?: string
  contractAddress: string
  tradingPair: string
  hasReflections: boolean
  walletAddresses: string[]
  tracker: Tracker
}

interface Tracker {
  name: string
  url: string
  instructions?: string
  requiresAPI: boolean
  coinMultiplier?: number
  apiKey: string
}

export interface WalletAddressData {
  newCoin: Coin | String
  apiKey?: String
}

export interface ApplicationSettings {
  localCurrency: string
  localCurrencyChar: string
  displayWidth: number
  displayHeight: number
  typeOfDisplay: string
  currencyConverterAPIKey: string
  leftButtonPin: number
  rightButtonPin: number
  configButtonPin: number
  rotateScreen: boolean
  runOnSchedule: boolean
  typeOfSchedule?: string
  showProgressBar?: boolean
  schedule?: frequencyDuration | startEnd
}

interface frequencyDuration {
  frequency: number
  duration: number
}

interface startEnd {
  startTime: string
  endTime: string
}
