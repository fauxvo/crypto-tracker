import inquirer from 'inquirer'
import { NavigationAnswer } from '../types'

export async function mainMenuQuestion(): Promise<NavigationAnswer> {
  return inquirer.prompt([
    {
      type: 'list',
      name: 'actionToTake',
      message: 'Which action would you like to take?',
      choices: [
        {
          name: 'Add a new coin / token',
          value: 'addNewCoin',
        },
        {
          name: 'Configure Crypto Tracker Application Settings',
          value: 'applicationSettingsConfig',
        },
        new inquirer.Separator(),
        {
          name: 'Output Config',
          value: 'output',
        },
        {
          name: 'Save Config',
          value: 'save',
        },
        {
          name: 'Quit',
          value: 'quit',
        },
      ],
    },
  ])
}
