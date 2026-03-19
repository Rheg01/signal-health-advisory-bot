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
