import chalk from 'chalk'
import util from 'util'
import { promises as pfs } from 'fs'
import fs from 'fs'
import path from 'path'

import { ADA_SSD1306 } from '../consts'
import { CryptoTrackerConfig, Coin, ApplicationSettings } from '../types'

const fileName = '../../cryptoTrackerConfig.json'
const configPath = path.resolve(__dirname, fileName)

export default class ConfigSettings {
  private cryptoTrackerConfig: CryptoTrackerConfig

  constructor() {
    if (fs.existsSync(configPath)) {
      this.cryptoTrackerConfig = require(fileName)
    } else {
      this.cryptoTrackerConfig = {
        coins: [],
        applicationSettings: {
          localCurrency: 'USD',
          localCurrencyChar: '$',
          displayWidth: 128,
          displayHeight: 64,
          typeOfDisplay: ADA_SSD1306,
          currencyConverterAPIKey: '',
          leftButtonPin: 5,
          rightButtonPin: 6,
          configButtonPin: 4,
          rotateScreen: false,
          runOnSchedule: false,
        },
      }
    }
  }

  getCryptoTrackerConfig(): CryptoTrackerConfig {
    return this.cryptoTrackerConfig
  }

  outputCryptoTrackerConfig(): void {
    console.log(
      util.inspect(this.cryptoTrackerConfig, { showHidden: false, depth: null })
    )
    console.log(`\n\n`)
  }

  async saveCryptoTrackerConfig(): Promise<void> {
    return pfs
      .writeFile(
        'cryptoTrackerConfig.json',
        JSON.stringify(this.cryptoTrackerConfig, null, 2)
      )
      .then(() => {
        console.log(chalk.green('Saved the Config File'))
        console.log(`\n`)
      })
      .catch((error) => {
        console.error(chalk.red(error))
      })
  }

  addPersonalCoin(newCoin: Coin) {
    // Check to see if this coin already exists.  If so, add it to the existing stack
    const foundCoinIndex = this.cryptoTrackerConfig.coins.findIndex(
      (coin) => coin.name === newCoin.name
    )

    if (foundCoinIndex != -1) {
      this.cryptoTrackerConfig.coins[foundCoinIndex].walletAddresses.push(
        ...newCoin.walletAddresses
      )
      this.cryptoTrackerConfig.coins[foundCoinIndex].tracker.apiKey =
        newCoin.tracker.apiKey
    } else {
      this.cryptoTrackerConfig.coins.push(newCoin)
    }
  }

  updateApplicationSettings(applicationSettings: ApplicationSettings) {
    this.cryptoTrackerConfig.applicationSettings = applicationSettings
  }
}
