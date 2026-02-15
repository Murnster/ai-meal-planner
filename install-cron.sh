#!/usr/bin/env bash
set -e

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PYTHON="$SCRIPT_DIR/meals/bin/python"
MAIN="$SCRIPT_DIR/main.py"
LOG="$SCRIPT_DIR/cron.log"
CRON_CMD="59 23 * * 6 cd $SCRIPT_DIR && $PYTHON $MAIN >> $LOG 2>&1"

# Check if the job already exists
if crontab -l 2>/dev/null | grep -qF "$MAIN"; then
    echo "Cron job already installed. Skipping."
    echo
    echo "Current entry:"
    crontab -l | grep -F "$MAIN"
    exit 0
fi

# Append to existing crontab
(crontab -l 2>/dev/null; echo "$CRON_CMD") | crontab -

echo "Cron job installed — runs every Saturday at 11:59 PM."
echo
echo "  $CRON_CMD"
echo
echo "To remove it later: crontab -e"
