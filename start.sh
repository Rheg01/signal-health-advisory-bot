#!/usr/bin/env bash
set -e

# Ensure signal-cli is discoverable
export PATH="/app/signal-cli/bin:$PATH"

# Optional: verify it's working (logs only)
signal-cli --version || echo "signal-cli not found in PATH!"

python scraper.py

exit 0   # Critical for cron — clean exit
