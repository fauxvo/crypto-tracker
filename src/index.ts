import chalk from 'chalk'
import figlet from 'figlet'
import { cryptoTrackerConfig } from './cryptoTrackerConfig'

export async function index(): Promise<any> {
  return new Promise(() => {
    figlet(
      'Crypto Tracker',
      {
        font: 'Banner3',
        horizontalLayout: 'default',
        verticalLayout: 'default',
        width: 80,
        whitespaceBreak: true,
      },
      function (err, data) {
        if (err) {
          console.log(chalk.red('Something went wrong...'))
          console.dir(err)
          return
        }
        process.stdout.write('\u001b[2J\u001b[0;0H')
        console.log(chalk.cyan(data), `\n\n`)
        cryptoTrackerConfig()
      }
    )
  })
}

index()
