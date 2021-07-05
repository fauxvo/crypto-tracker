import inquirer from 'inquirer'
import { coinList } from '../data/coinList'
import ConfigSettings from '../models/configSettings'
import { CoinChoice, Coin } from '../types'

export async function addCoinQuestion(
  configSettings: ConfigSettings
): Promise<Coin | string> {
  const separator = new inquirer.Separator()
  const listOfCoins: (CoinChoice | typeof separator)[] = coinList.map(
    (coin) => {
      return { name: coin.name, value: coin.name }
    }
  )

  listOfCoins.push(separator)
  listOfCoins.push({ name: 'Back', value: 'back' })

  return inquirer
    .prompt([
      {
        type: 'list',
        name: 'whichCoin',
        message: 'Which coin would you like to add?',
        choices: listOfCoins,
      },
    ])
    .then((answer) => {
      if (answer.whichCoin === 'back') return 'back'

      // Find the coin the user wanted to add
      return coinList.find((coin) => coin.name === answer.whichCoin) || 'back'
    })
    .then(async (currentCoin) => {
      if (currentCoin === 'back') return 'back'

      // Find out if the newCoin currently exists and if the API is already set
      const foundCoin = configSettings
        .getCryptoTrackerConfig()
        .coins.find((coin) => coin.name === currentCoin.name)

      let apiKey: string | undefined
      if (foundCoin) {
        apiKey = foundCoin.tracker.apiKey
      }

      await addWalletAddress(currentCoin, apiKey)
      return currentCoin
    })
}

function addWalletAddress(currentCoin: Coin, apiKey?: string) {
  return inquirer
    .prompt([
      {
        type: 'input',
        name: 'coinWalletAddress',
        message: `What is the wallet ${currentCoin.name} address you'd like to include?`,
      },
      {
        type: 'input',
        name: 'apiKey',
        message: currentCoin.tracker.instructions,
        when:
          currentCoin.tracker.requiresAPI &&
          !currentCoin.tracker.apiKey &&
          !apiKey,
      },
      {
        type: 'confirm',
        name: 'addAnotherAddress',
        message: `Would you like to add another ${currentCoin.name} address?`,
      },
    ])
    .then(async (answer) => {
      currentCoin.walletAddresses.push(answer.coinWalletAddress)
      if (answer.apiKey) {
        currentCoin.tracker.apiKey = answer.apiKey
      }

      if (answer.addAnotherAddress) {
        await addWalletAddress(currentCoin)
      }
    })
}
