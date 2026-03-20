import feedparser
import random
import requests

SOURCES = [
    "https://www.who.int/rss-feeds/news-english.xml",
    "https://www.unicef.org/rss.xml",
    "https://rss.cnn.com/rss/edition_health.rss"
]

def get_feed(url):
    headers = {
        "User-Agent": "Mozilla/5.0"
    }
    response = requests.get(url, headers=headers, timeout=10)
    return feedparser.parse(response.content)

def get_latest_article():
    all_entries = []

    for url in SOURCES:
        try:
            feed = get_feed(url)

            print("Feed:", url)
            print("Entries found:", len(feed.entries))

            if feed.entries:
                all_entries.extend(feed.entries[:5])

        except Exception as e:
            print("Feed error:", e)

    if not all_entries:
        return None

    entry = random.choice(all_entries)

    return {
        "title": entry.title,
        "summary": getattr(entry, "summary", getattr(entry, "description", "No summary available")),
        "link": entry.link
    }
    
    import feedparser
    import random

SOURCES = [
    "https://www.who.int/rss-feeds/news-english.xml",
    "https://www.unicef.org/rss.xml",
]

def get_latest_article():
    all_entries = []

    for url in SOURCES:
        feed = feedparser.parse(url)
        if feed.entries:
            all_entries.extend(feed.entries[:5])  # get top 5

    if not all_entries:
        return None

    entry = random.choice(all_entries)

    return {
        "title": entry.title,
        "summary": entry.summary,
        "link": entry.link
    }
