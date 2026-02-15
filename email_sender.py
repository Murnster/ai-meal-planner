import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

import markdown


def markdown_to_html(md_text):
    """Convert markdown to a styled HTML email."""
    body_html = markdown.markdown(md_text, extensions=["tables", "fenced_code"])

    return f"""\
<!DOCTYPE html>
<html>
<head>
<meta charset="utf-8">
<style>
  body {{ font-family: -apple-system, Helvetica, Arial, sans-serif; line-height: 1.6;
         color: #333; max-width: 700px; margin: 0 auto; padding: 20px; }}
  h1 {{ color: #2c5f2d; border-bottom: 2px solid #2c5f2d; padding-bottom: 8px; }}
  h2 {{ color: #2c5f2d; margin-top: 24px; }}
  h3 {{ color: #555; }}
  table {{ border-collapse: collapse; width: 100%; margin: 12px 0; }}
  th, td {{ border: 1px solid #ddd; padding: 8px; text-align: left; }}
  th {{ background: #2c5f2d; color: white; }}
  tr:nth-child(even) {{ background: #f9f9f9; }}
  strong {{ color: #2c5f2d; }}
  ul, ol {{ padding-left: 24px; }}
</style>
</head>
<body>
{body_html}
</body>
</html>"""


def send_alert_email(recipient, error_message):
    """Send a short alert email when the meal plan generation fails."""
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_email = os.environ["SMTP_EMAIL"]
    smtp_password = os.environ["SMTP_PASSWORD"]

    body = (
        f"Your weekly meal plan failed to generate.\n\n"
        f"Error: {error_message}\n\n"
        f"Check the logs on your device for more details."
    )

    msg = MIMEText(body, "plain")
    msg["Subject"] = "Meal Planner — Error"
    msg["From"] = smtp_email
    msg["To"] = recipient

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, recipient, msg.as_string())

    print(f"Alert email sent to {recipient}.")


def send_meal_plan_email(recipient, meal_plan_md):
    """Send the meal plan as a styled HTML email via SMTP."""
    smtp_server = os.environ["SMTP_SERVER"]
    smtp_port = int(os.environ["SMTP_PORT"])
    smtp_email = os.environ["SMTP_EMAIL"]
    smtp_password = os.environ["SMTP_PASSWORD"]

    html = markdown_to_html(meal_plan_md)

    msg = MIMEMultipart("alternative")
    msg["Subject"] = "Your Weekly Meal Plan"
    msg["From"] = smtp_email
    msg["To"] = recipient

    msg.attach(MIMEText(meal_plan_md, "plain"))
    msg.attach(MIMEText(html, "html"))

    with smtplib.SMTP(smtp_server, smtp_port) as server:
        server.starttls()
        server.login(smtp_email, smtp_password)
        server.sendmail(smtp_email, recipient, msg.as_string())

    print(f"Email sent to {recipient}.")
