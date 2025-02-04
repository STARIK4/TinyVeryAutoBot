# Script on python for TinyVery stars collection and dust


Main advantages:
+ Automatic collection of rewards
+ Complete randomization of collection of rewards
+ Adding a large number of accounts
+ Convenient setup using a telegram bot

## Prerequisites

- Python 3.10+
- Required Python packages (listed below)

## Getting Started

Follow these steps to set up and use the bot:

### 1. Obtaining Your Session ID and GALAXY_ID

To get your `SESSION_ID`, follow these steps:

1. Open your browser and go to telegram.web
2. Press `F12` to open the Developer Tools
3. Go to the `Network` tab
4. Trigger a star collection request (perform the action that collects stars)
5. Find the `POST` request named `collect` in the network logs
6. In the `Payload` section of the `collect` request, you will find the `session` field. This is your `SESSION_ID`

To get your `GALAXY_ID`, follow these steps:
1. Open your browser and go to telegram.web
2. Press `F12` to open the Developer Tools
3. Go to the `Network` tab
4. Try to create stars
5. Find the `POST` request named `create` in the network logs
6. In the `Payload` section of the `create` request, you will find the `galaxy_id` field. This is your `GALAXY_ID`

## 2. Running the Bot
Run the bot:
'''bash     python run.py
    '''
Then go to the telegram bot and start registration there.
## Disclaimer
By using this software, you agree that you are responsible for any actions performed with it. I do not accept any responsibility for any damage or consequences resulting from using this bot or its components. Use at your own risk.
