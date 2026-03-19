import subprocess
import schedule
import time
import os
from fetch_news import get_latest_article

# Environment variables
PHONE = os.getenv("+639102406985")
RECIPIENT = os.getenv("+639952746595")

# Persistent file path (use Railway volume path)
LAST_FILE = "/root/health-bot-data/last_sent.txt"  # <-- make sure your volume is mounted here

# Check if link already sent
def already_sent(link):
    if not os.path.exists(LAST_FILE):
        return False
    with open(LAST_FILE, "r") as f:
        return link in f.read()

# Save the sent link
def save_sent(link):
    with open(LAST_FILE, "w") as f:
        f.write(link)

# Clean up summary for message
def clean_summary(text):
    return text.replace("<p>", "").replace("</p>", "")[:300]

# Format message
def format_message(article):
    return f"""🩺 {article['title']}

📌 Summary:
{clean_summary(article['summary'])}...

🔗 Read more:
{article['link']}
"""

# Send via signal-cli
def send_signal(msg):
    subprocess.run([
        "./signal-cli/bin/signal-cli",
        "-u", PHONE,
        "send",
        "-m", msg,
        RECIPIENT
    ], check=True)

# Job executed daily
def job():
    print("Job started...")
    article = get_latest_article()
    if not article:
        print("No article found")
        return

    if already_sent(article["link"]):
        print("Already sent, skipping...")
        return

    msg = format_message(article)
    print("Message to send:\n", msg)

    try:
        send_signal(msg)
        save_sent(article["link"])
        print("Message sent successfully!")
    except Exception as e:
        print("Failed to send message:", e)

# Schedule the job
schedule.every().day.at("01:00").do(job)  # 9AM PH time = 1AM UTC

print("Health bot running 24/7...")

# Main loop
while True:
    schedule.run_pending()
    time.sleep(60)
