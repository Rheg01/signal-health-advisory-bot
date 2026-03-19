import requests
from bs4 import BeautifulSoup
import subprocess
import os
import json
from datetime import datetime

# Env vars from Railway
PHONE = os.getenv("SIGNAL_PHONE")                    # e.g. +639xxxxxxxxx
RECIPIENTS = os.getenv("RECIPIENTS", "").split(",")  # comma-separated phones/groups
CONFIG_DIR = "/signal-data"

os.environ["PATH"] = f"/app/signal-cli/bin:{os.environ.get('PATH', '')}"

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "Accept-Language": "en-US,en;q=0.5",
    "Referer": "https://www.google.com/",
}

STATE_FILE = os.path.join(CONFIG_DIR, "last_seen.json")

def load_state():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return json.load(f)
    return {}

def save_state(state):
    os.makedirs(CONFIG_DIR, exist_ok=True)
    with open(STATE_FILE, "w") as f:
        json.dump(state, f)

def fetch_articles():
    articles = []
    sources = {
        "DOH": "https://doh.gov.ph/news-and-updates/",
        "WHO": "https://www.who.int/news",  # or use RSS: https://www.who.int/feeds/entity/csr/don/en/rss.xml
        # Add: PhilHealth press -> "https://www.philhealth.gov.ph/news/",
        # FDA alerts -> "https://www.fda.gov.ph/category/advisories/",
        # UNICEF PH -> "https://www.unicef.org/philippines/press-releases"
    }

    state = load_state()

    for site, base_url in sources.items():
        try:
            resp = requests.get(base_url, headers=HEADERS, timeout=15)
            resp.raise_for_status()
            soup = BeautifulSoup(resp.text, "lxml")

            # Customize selectors per site — examples below are starters
            items = soup.select("article, .news-item, .post, .media-release")[:6]  # latest few

            for item in items:
                title_tag = item.select_one("h2, h3, .title, a")
                title = title_tag.get_text(strip=True) if title_tag else "Untitled"

                link_tag = item.select_one("a")
                link = link_tag["href"] if link_tag else base_url
                if not link.startswith("http"):
                    link = base_url.rstrip("/") + "/" + link.lstrip("/")

                summary_tag = item.select_one("p, .summary, .excerpt")
                summary = (summary_tag.get_text(strip=True)[:220] + "...") if summary_tag else ""

                key = f"{site}:{title[:80]}"
                if key not in state:
                    articles.append(f"**{title}**\n{summary}\nFull article: {link}")
                    state[key] = link
        except Exception as e:
            print(f"Fetch error {site}: {e}")

    save_state(state)
    return articles

def send_message(msg):
    for rec in [r.strip() for r in RECIPIENTS if r.strip()]:
        try:
            cmd = [
                "signal-cli", "-c", CONFIG_DIR,
                "--account", PHONE,
                "send", "-m", msg
            ]
            if rec.startswith("+"):  # phone
                cmd += [rec]
            else:  # assume group-id if not phone
                cmd += ["--group-id", rec]

            subprocess.run(cmd, check=True, timeout=40, capture_output=True)
            print(f"Sent to {rec}")
        except Exception as e:
            print(f"Send fail to {rec}: {e}")

if __name__ == "__main__":
    print(f"Run started: {datetime.now()}")
    new_msgs = fetch_articles()
    for m in new_msgs:
        send_message(m)
    print(f"Done — {len(new_msgs)} new advisories sent.")
