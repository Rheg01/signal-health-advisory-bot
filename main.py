import subprocess
import schedule
import time
import os
from fetch_news import get_latest_article

PHONE = os.getenv("+639102406985")
RECIPIENT = os.getenv("+639952746595")

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

subprocess.run([
    "C:/signal-cli/bin/signal-cli",
    "-u", PHONE,
    "send",
    "-m", msg,
    RECIPIENT
], check=True)

def job():
    print("Fetching article...")
    article = get_latest_article()
    print("Article fetched:", article)

    if not article:
        print("No article found")
        return

    if already_sent(article["link"]):
        print("Already sent, skipping...")
        return

    msg = format_message(article)
    print("Formatted message:\n", msg)

    print("Sending message...")
    send_signal(msg)

    save_sent(article["link"])
    print("Message sent and saved!")

# Run daily (PH 9AM = UTC 1AM)
schedule.every().day.at("01:00").do(job)

print("Health bot running 24/7...")

while True:
    schedule.run_pending()
    time.sleep(60)
