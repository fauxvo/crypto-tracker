import chalk from 'chalk'
import {
  mainMenuQuestion,
  addCoinQuestion,
  applicationSettingsQuestion,
} from './questions'
import { NavigationAnswer, Coin, ApplicationSettings } from './types'
import ConfigSettings from './models/configSettings'

const configSettings = new ConfigSettings()

async function cryptoTrackerConfigProcess(): Promise<void> {
  const mainMenuAnswer: NavigationAnswer = await mainMenuQuestion()

  switch (mainMenuAnswer.actionToTake) {
    case 'addNewCoin':
      const newCoin: Coin | string = await addCoinQuestion(configSettings)

      if (typeof newCoin === 'string') {
        if (newCoin === 'back') {
          console.log(`\n\n`)
          return await cryptoTrackerConfig()
        }
      } else {
        configSettings.addPersonalCoin(newCoin)
        console.log(`\n\n`)
        return await cryptoTrackerConfig()
      }

    case 'applicationSettingsConfig':
      const applicationSettings: ApplicationSettings =
        await applicationSettingsQuestion(
          configSettings.getCryptoTrackerConfig().applicationSettings
        )
      configSettings.updateApplicationSettings(applicationSettings)
      return await cryptoTrackerConfig()

    case 'output':
      configSettings.outputCryptoTrackerConfig()
      return await cryptoTrackerConfig()

    case 'save':
      await configSettings.saveCryptoTrackerConfig()
      return await cryptoTrackerConfig()

    default:
    case 'quit':
      await quit()
  }
}

export async function cryptoTrackerConfig(): Promise<any> {
  try {
    await cryptoTrackerConfigProcess()
  } catch (error) {
    console.log(chalk.red(`*** main error: ${error}`))
  }
}

async function quit() {
  console.log(
    chalk.yellow(
      `Config CLI Terminated.  Reset your PI to update the application settings`
    )
  )
}

// Catches ctrl+c event
process.on('SIGINT', quit.bind(null, { exit: true }))
