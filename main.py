import json
import os
import smtplib
import sys

import openai
from dotenv import load_dotenv

from biometrics import BiometricCalculator
from meal_planner import generate_meal_plan
from email_sender import send_meal_plan_email, send_alert_email

# Resolve paths relative to this script (for cron compatibility)
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))


def _fail(recipient, message):
    """Print error, attempt to send an alert email, then exit."""
    print(f"Error: {message}")
    try:
        send_alert_email(recipient, message)
    except Exception:
        print("Warning: Could not send alert email.")
    sys.exit(1)


def main():
    # Load environment variables
    load_dotenv(os.path.join(SCRIPT_DIR, ".env"))

    if not os.environ.get("OPENAI_API_KEY"):
        sys.exit("Error: OPENAI_API_KEY not set. Check your .env file.")

    # Load configuration
    config_path = os.path.join(SCRIPT_DIR, "config.json")
    try:
        with open(config_path) as f:
            config = json.load(f)
    except FileNotFoundError:
        sys.exit(f"Error: {config_path} not found. Run ./setup.sh first.")
    except json.JSONDecodeError as e:
        sys.exit(f"Error: config.json is not valid JSON — {e}")

    # Calculate biometrics
    bio = config["biometrics"]
    try:
        calc = BiometricCalculator(
            age=bio["age"],
            gender=bio["gender"],
            height_cm=bio["height_cm"],
            current_weight_lbs=bio["current_weight_lbs"],
            activity_level=bio["activity_level"],
            goal_weight_lbs=bio["goal_weight_lbs"],
            target_date=bio["target_date"],
        )
    except KeyError as e:
        sys.exit(f"Error: Missing field in config.json biometrics — {e}")
    print(f"Biometrics: {calc.summary()}")

    # Generate meal plan
    recipient = config["email_recipient"]
    print("Generating meal plan...")
    preferences = config["preferences"]
    try:
        meal_plan = generate_meal_plan(calc.summary(), preferences)
    except openai.AuthenticationError:
        _fail(recipient, "Invalid OpenAI API key. Check OPENAI_API_KEY in your .env file.")
    except openai.RateLimitError as e:
        if "insufficient_quota" in str(e):
            _fail(recipient, "OpenAI quota exceeded. Check your billing at https://platform.openai.com/account/billing")
        _fail(recipient, "OpenAI rate limit hit. Try again in a few minutes.")
    except (openai.APITimeoutError, openai.APIConnectionError):
        _fail(recipient, "Could not reach OpenAI API. Check your internet connection.")
    except openai.APIError as e:
        _fail(recipient, f"OpenAI API error — {e}")
    print("Meal plan generated.")

    # Send email
    print(f"Sending email to {recipient}...")
    try:
        send_meal_plan_email(recipient, meal_plan)
    except smtplib.SMTPAuthenticationError:
        sys.exit("Error: SMTP login failed. Check SMTP_EMAIL and SMTP_PASSWORD in your .env file.")
    except smtplib.SMTPException as e:
        sys.exit(f"Error: Failed to send email — {e}")
    except ConnectionError:
        sys.exit(f"Error: Could not connect to SMTP server. Check SMTP_SERVER and SMTP_PORT in your .env file.")

    print("Done!")


if __name__ == "__main__":
    main()
