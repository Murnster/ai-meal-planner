#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
cd "$SCRIPT_DIR"

echo "========================================="
echo "  AI Meal Planner — Setup"
echo "========================================="
echo

# --- Virtual environment & dependencies ---
if [ ! -d "meals" ]; then
    echo "Creating virtual environment..."
    python3 -m venv meals
fi

echo "Installing dependencies..."
meals/bin/pip install -q -r requirements.txt
echo "Dependencies installed."
echo

# --- Helper functions ---
ask() {
    local prompt="$1" default="$2" var
    if [ -n "$default" ]; then
        read -rp "$prompt [$default]: " var
        echo "${var:-$default}"
    else
        while [ -z "$var" ]; do
            read -rp "$prompt: " var
        done
        echo "$var"
    fi
}

ask_secret() {
    local prompt="$1" var
    while [ -z "$var" ]; do
        read -rsp "$prompt: " var
        echo >&2
    done
    echo "$var"
}

# --- config.json ---
echo "--- Personal Configuration ---"
echo

age=$(ask "Age" "")
echo
echo "Gender options: male, female"
gender=$(ask "Gender" "male")
height_cm=$(ask "Height in cm" "")
current_weight=$(ask "Current weight in lbs" "")
echo
echo "Activity levels:"
echo "  sedentary, lightly_active, moderately_active, very_active, extra_active"
activity=$(ask "Activity level" "moderately_active")
goal_weight=$(ask "Goal weight in lbs" "")
target_date=$(ask "Target date (YYYY-MM-DD)" "")

echo
echo "--- Meal Preferences ---"
echo
locale=$(ask "Locale (e.g. en-US, en-CA, en-GB)" "en-CA")
dietary=$(ask "Dietary restrictions / preferences (free text)" "No specific restrictions")
echo
read -rp "Use a consistent meal-prep lunch Mon-Fri? (y/n) [y]: " lunch_input
if [ "${lunch_input,,}" = "n" ]; then
    consistent_lunch="false"
else
    consistent_lunch="true"
fi

echo
email_recipient=$(ask "Email address to receive meal plans" "")

# Write config.json safely via Python (handles special characters in user input)
meals/bin/python3 - "$age" "$gender" "$height_cm" "$current_weight" \
    "$activity" "$goal_weight" "$target_date" "$locale" "$dietary" \
    "$consistent_lunch" "$email_recipient" <<'PYEOF'
import json, sys

_, age, gender, height_cm, current_weight, activity, goal_weight, \
    target_date, locale, dietary, consistent_lunch, email_recipient = sys.argv

config = {
    "biometrics": {
        "age": int(age),
        "gender": gender,
        "height_cm": int(height_cm),
        "current_weight_lbs": int(current_weight),
        "activity_level": activity,
        "goal_weight_lbs": int(goal_weight),
        "target_date": target_date,
    },
    "preferences": {
        "locale": locale,
        "dietary_blob": dietary,
        "consistent_lunch": consistent_lunch == "true",
    },
    "email_recipient": email_recipient,
}

with open("config.json", "w") as f:
    json.dump(config, f, indent=2)
PYEOF

echo
echo "config.json saved."

# --- .env ---
echo
echo "--- API & Email Credentials ---"
echo

openai_key=$(ask_secret "OpenAI API key")
echo
smtp_server=$(ask "SMTP server" "smtp.gmail.com")
smtp_port=$(ask "SMTP port" "587")
smtp_email=$(ask "SMTP email address" "")
smtp_password=$(ask_secret "SMTP password (Gmail app password)")

# Write .env safely via Python (handles special characters in credentials)
meals/bin/python3 - "$openai_key" "$smtp_server" "$smtp_port" \
    "$smtp_email" "$smtp_password" <<'PYEOF'
import sys, os, stat

_, openai_key, smtp_server, smtp_port, smtp_email, smtp_password = sys.argv

lines = [
    f"OPENAI_API_KEY={openai_key}",
    f"SMTP_SERVER={smtp_server}",
    f"SMTP_PORT={smtp_port}",
    f"SMTP_EMAIL={smtp_email}",
    f"SMTP_PASSWORD={smtp_password}",
]

with open(".env", "w") as f:
    f.write("\n".join(lines) + "\n")

os.chmod(".env", stat.S_IRUSR | stat.S_IWUSR)
PYEOF

echo
echo ".env saved (permissions set to 600)."

# --- Cron job ---
echo
read -rp "Install weekly cron job (Saturday 11:59 PM)? (y/n) [y]: " cron_input
if [ "${cron_input,,}" != "n" ]; then
    bash "$SCRIPT_DIR/install-cron.sh"
fi

# --- Done ---
echo
echo "========================================="
echo "  Setup complete!"
echo "========================================="
echo
echo "Run the meal planner:"
echo "  meals/bin/python main.py"
