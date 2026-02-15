# AI Meal Planner

A Raspberry Pi automation script that generates a personalized, zero-waste weekly meal plan using OpenAI GPT-4o and emails it to you every Saturday night.

## Features

- Calculates your daily calorie target using the Mifflin-St Jeor equation
- Generates a full weekly meal plan with grocery list and cost estimate
- Zero-waste policy — all perishable ingredients are used across the week
- Optional consistent meal-prep lunch for workdays
- Sends a styled HTML email via SMTP

## Quick Setup

Run the interactive setup script — it creates the virtual environment, installs dependencies, and walks you through all the configuration:

```bash
./setup.sh
```

You'll need your OpenAI API key and a Gmail app password ready.

### Getting a Gmail App Password

1. Enable 2-Step Verification on your Google account
2. Go to [App Passwords](https://myaccount.google.com/apppasswords)
3. Select **Mail** and your device, then click **Generate**
4. Use the 16-character password when the setup script asks for it

### Manual Setup

If you prefer to configure things manually:

1. `python3 -m venv meals && meals/bin/pip install -r requirements.txt`
2. Edit `config.json` with your biometrics, preferences, and email
3. `cp .env.example .env` and fill in your API key and SMTP credentials

## Usage

```bash
source meals/bin/activate
python main.py
```

## Cron Job (Weekly on Saturday at 11:59 PM)

```bash
crontab -e
```

Add this line (adjust paths to your setup):

```
59 23 * * 6 cd /home/pi/ai-meal-planner && /home/pi/ai-meal-planner/meals/bin/python main.py >> cron.log 2>&1
```

Note: `* * * 6` = Saturday in cron (0=Sunday, 6=Saturday). If you want Sunday night, use `59 23 * * 0`.
