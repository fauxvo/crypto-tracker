import inquirer from 'inquirer'
import {
  ADA_SSD1306,
  frequencyDuration,
  SSD1305,
  SH1106,
  startEnd,
} from '../consts'
import { localCurrencies } from '../data/localCurrencies'
import { ApplicationSettings } from '../types'

export async function applicationSettingsQuestion(
  applicationSettings: ApplicationSettings
): Promise<ApplicationSettings> {
  return inquirer
    .prompt([
      {
        type: 'list',
        name: 'localCurrency',
        message: 'Which currency would you like to use?',
        default: applicationSettings.localCurrency,
        choices: localCurrencies.map((currency) => {
          return { name: currency, value: currency }
        }),
      },
      {
        type: 'list',
        name: 'typeOfDisplay',
        message: 'Which display are you using?',
        default: applicationSettings.typeOfDisplay,
        choices: [ADA_SSD1306, SH1106, SSD1305].map((display) => {
          return { name: display, value: display }
        }),
      },
      {
        type: 'number',
        name: 'rightButtonPin',
        message:
          'Which pin would you like to use for navigating to the next screen?',
        default: applicationSettings.rightButtonPin,
        when: (answers) =>
          [ADA_SSD1306, SH1106].includes(answers.typeOfDisplay),
      },
      {
        type: 'number',
        name: 'leftButtonPin',
        message:
          'Which pin would you like to use for navigating to the previous screen?',
        default: applicationSettings.leftButtonPin,
        when: (answers) =>
          [ADA_SSD1306, SH1106].includes(answers.typeOfDisplay),
      },
      {
        type: 'number',
        name: 'configButtonPin',
        message:
          'Which pin would you like to use for navigating to the config screen?',
        default: applicationSettings.configButtonPin,
        when: (answers) =>
          [ADA_SSD1306, SH1106].includes(answers.typeOfDisplay),
      },
      {
        type: 'confirm',
        name: 'rotateScreen',
        message:
          'Would you like to rotate the screen 180°? (probably want yes if using SH1106)',
        default: applicationSettings.rotateScreen,
      },
      {
        type: 'input',
        name: 'currencyConverterAPIKey',
        message:
          'To be able to convert currencies go to https://free.currencyconverterapi.com/free-api-key and enter the Currency Convert API Key',
        default: applicationSettings.currencyConverterAPIKey,
      },
      {
        type: 'confirm',
        name: 'runOnSchedule',
        message: 'Would you like to have the application run on a schedule?',
        default: applicationSettings.runOnSchedule,
      },
      {
        type: 'confirm',
        name: 'showProgressBar',
        message: 'Would you like to display the progress bar?',
        default: applicationSettings.showProgressBar,
      },
      {
        type: 'input',
        name: 'showProgressBar',
        message: 'Would you like to display the progress bar?',
        default: applicationSettings.showProgressBar,
      },
      {
        type: 'number',
        name: 'timeOnScreen',
        message: 'How long would you like to stay on each screen (in seconds)?',
        default: applicationSettings.timeOnScreen,
        validate: (timeOnScreen) => {
          return timeOnScreen > 3
        },
      },
      {
        type: 'confirm',
        name: 'showBalanceScreen',
        message: 'Would you like to display the balance screen?',
        default: applicationSettings.showBalanceScreen,
      },
      {
        type: 'confirm',
        name: 'showPriceScreen',
        message: 'Would you like to display the price screen?',
        default: applicationSettings.showPriceScreen,
      },
      {
        type: 'confirm',
        name: 'showReflectionScreen',
        message:
          'Would you like to display the reflection screen (when applicable)?',
        default: applicationSettings.showReflectionScreen,
      },
      {
        type: 'list',
        name: 'typeOfSchedule',
        message: 'What type of schedule would you like to run?',
        default: applicationSettings.typeOfSchedule,
        choices: [startEnd, frequencyDuration].map((schedule) => {
          return { name: schedule, value: schedule }
        }),
        when: (answers) => answers.runOnSchedule,
      },
      {
        type: 'input',
        name: 'schedule.startTime',
        message: 'What time would you like the app to start? (24 Hour Format)',
        default:
          applicationSettings.schedule &&
          applicationSettings.typeOfSchedule === startEnd &&
          'startTime' in applicationSettings.schedule
            ? applicationSettings.schedule.startTime
            : '09:00',
        when: (answers) =>
          answers.runOnSchedule && answers.typeOfSchedule === startEnd,
        validate: (input) => {
          return input.match(/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/).length
            ? true
            : false
        },
      },
      {
        type: 'input',
        name: 'schedule.endTime',
        message: 'What time would you like the app to end? (24 Hour Format)',
        default:
          applicationSettings.schedule &&
          applicationSettings.typeOfSchedule === startEnd &&
          'endTime' in applicationSettings.schedule
            ? applicationSettings.schedule.endTime
            : '17:00',
        when: (answers) =>
          answers.runOnSchedule && answers.typeOfSchedule === startEnd,
        validate: (input, answers) => {
          if (
            input.match(/^(0[0-9]|1[0-9]|2[0-3]):[0-5][0-9]$/).length &&
            answers.schedule.startTime < input
          ) {
            return true
          } else {
            return 'The end time must be later than the start time'
          }
        },
      },
      {
        type: 'input',
        name: 'schedule.duration',
        message:
          'How long would you like the application to run for? (in Minutes -- so if hours, multiply by 60!)',
        default:
          applicationSettings.schedule &&
          applicationSettings.typeOfSchedule === startEnd &&
          'duration' in applicationSettings.schedule
            ? applicationSettings.schedule.duration
            : 10,
        when: (answers) =>
          answers.runOnSchedule && answers.typeOfSchedule === frequencyDuration,
        validate: (input) => {
          input += ''
          return input.match(/^\d*$/).length ? true : false
        },
      },

      {
        type: 'input',
        name: 'schedule.frequency',
        message:
          'How frequent would you like the application? (in Minutes -- so if hours, multiply by 60!)',
        default:
          applicationSettings.schedule &&
          applicationSettings.typeOfSchedule === startEnd &&
          'frequency' in applicationSettings.schedule
            ? applicationSettings.schedule.frequency
            : 60,
        when: (answers) =>
          answers.runOnSchedule && answers.typeOfSchedule === frequencyDuration,
        validate: (input, answers) => {
          input += ''
          const digitalResult = input.match(/^\d*$/).length ? true : false
          if (digitalResult && input > answers.schedule.duration) {
            return true
          } else {
            return `The frequency must be greater than the duration value (current duration - ${answers.duration})`
          }
        },
      },
    ])
    .then((answer) => {
      console.log(`\n\nFinished Application Settings\n\n`)
      switch (answer.localCurrency) {
        case 'EUR':
          answer.localCurrencyChar = '€'
          break
        case 'GBP':
          answer.localCurrencyChar = '£'
          break
        default:
        case 'USD':
        case 'CAD':
          answer.localCurrencyChar = '$'
          break
      }
      switch (answer.typeOfDisplay) {
        case SSD1305:
          answer.displayWidth = 128
          answer.displayHeight = 32
          break
        default:
        case ADA_SSD1306:
        case SH1106:
          answer.displayWidth = 128
          answer.displayHeight = 64
          break
      }
      return answer
    })
}
