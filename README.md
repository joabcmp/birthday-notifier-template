#🎉 Birthday Notifier Serverless for Telegram

A simple and reproducible birthday notification system using:

Python
GitHub Actions
Telegram Bot API

No server required. Runs automatically every day.

#💡 Why use this?
No server required
Runs automatically every day
Easy to customize for any group
Free using GitHub Actions
#⚙️ How it works
GitHub Actions runs daily
The script reads a JSON file with birthdays
It checks who has a birthday today
Sends a message to Telegram
Saves a log to avoid duplicate notifications
#📁 Project structure
.github/workflows/birthday.yml
data/aniversariantes.json
data/notification_log.json
scripts/send_daily_birthdays.py
README.md
LICENSE
#🚀 How to reproduce
###Step 1
Create a repository from this template

###Step 2
Edit the file:

data/aniversariantes.json

Add your group birthdays.

###Step 3

Create GitHub Secrets:

TELEGRAM_BOT_TOKEN
TELEGRAM_CHAT_ID
###Step 4

Enable GitHub Actions in your repository

Step 5 (Test)
Edit `data/aniversariantes.json` and set one entry to today (e.g. the Bot entry).Go to Actions
Click Run workflow

#📌 Where to insert your data

Example:
```JSON
[
  {
    "id": 1,
    "name": "Erick A",
    "day": 26,
    "month": 1,
    "description": "Lider PB",
    "active": true
  }
]
```

Fields:
*id: unique identifier
*name: name displayed in the message
*day: birthday day
*month: birthday month
*description: optional text
*active: enable/disable notifications

#🤖 How to create a Telegram Bot
Open Telegram
Search for BotFather
Send /newbot
choose a name for your bot
choose a username ending in bot

BotFather will return a token like this:

`123456789:ABCDEF...`

This will be your TELEGRAM_BOT_TOKEN.

#💬 How to get Chat ID
In BotFather, disable privacy mode so the bot can receive group messages:

`/setprivacy`

Select your bot and choose Disable.
Add your bot to the group and send a message.

Then open this URL in your browser, replacing YOUR_BOT_TOKEN with your real token:

https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates

Look for a block like this:
```JSON
"chat": {
  "id": -1001234567890,
  "title": "Your Group Name",
  "type": "supergroup"
}
```
The value in id is your TELEGRAM_CHAT_ID.
#⚠️ Common mistakes
Missing GitHub Secrets
Wrong Chat ID
Testing without changing date
Already notified today (check notification_log.json)

#⏱️ Schedule

The workflow runs daily using cron:

5 11 * * *

This corresponds to 11:05 UTC, which is 08:05 in Fortaleza (UTC-3).

⚠️ Note: GitHub Actions schedules are based on UTC time.

Due to platform load and shared infrastructure, scheduled workflows may not run exactly at the specified time.
It is normal for executions to be delayed by up to ~1 hour.

#🧪 Manual test

Go to the Actions tab
Select the workflow
Click Run workflow

This is useful to test the notifier without waiting for the scheduled time.

⚠️ Free tier may delay execution by a few seconds.

#📜 License

MIT
