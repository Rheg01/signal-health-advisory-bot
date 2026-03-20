import subprocess
import schedule
import time
import os
from fetch_news import get_latest_article

PHONE = os.getenv("+639102406985")
RECIPIENTS = os.getenv("+639952746595", "+639606570195")
RECIPIENT_LIST = [r.strip() for r in RECIPIENTS.split(",") if r.strip()]

# Persistent file
LAST_FILE = "last_sent.txt"

def already_sent(link):
    if not os.path.exists(LAST_FILE):
        return False
    with open(LAST_FILE, "r") as f:
        return link in f.read()

def save_sent(link):
    with open(LAST_FILE, "w") as f:
        f.write(link)

def clean_summary(text):
    return text.replace("<p>", "").replace("</p>", "")[:300]

def format_message(article):
    return f"""🩺 {article['title']}

📌 Summary:
{clean_summary(article['summary'])}...

🔗 Read more:
{article['link']}
"""

def send_signal(msg):
    result = subprocess.run([
        "./signal-cli/bin/signal-cli",
        "-u", PHONE,
        "send",
        "-m", msg,
        RECIPIENT
    ], capture_output=True, text=True)

    print("STDOUT:", result.stdout)
    print("STDERR:", result.stderr)

    if result.returncode != 0:
        raise Exception("Signal send failed")

def job():
    print("=== JOB STARTED ===")
    print("PHONE:", PHONE)
    print("RECIPIENT:", RECIPIENT)

    article = get_latest_article()

    if not article:
        print("No article found")
        return

    if already_sent(article["link"]):
        print("Already sent, skipping...")
        return

    msg = format_message(article)
    print("Message:\n", msg)

    try:
        send_signal(msg)
        save_sent(article["link"])
        print("Message sent successfully!")
    except Exception as e:
        print("Error sending message:", e)

# 🔥 TEST MODE (runs immediately)
job()

# ⏰ RUN EVERY 1 MINUTE (change to daily later)
schedule.every(1).minutes.do(job)

print("Health bot running...")

while True:
    schedule.run_pending()
    time.sleep(60)
