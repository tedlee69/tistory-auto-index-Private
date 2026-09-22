import feedparser
import datetime
from google.oauth2 import service_account
from googleapiclient.discovery import build

RSS_URL  = "https://myblog08565.tistory.com/rss"
SCOPES   = ["https://www.googleapis.com/auth/indexing"]
KEY_FILE = "service_account.json"
DAYS     = 1

def get_recent_urls():
    feed   = feedparser.parse(RSS_URL)
    cutoff = datetime.datetime.now() - datetime.timedelta(days=DAYS)
    urls   = []
    for entry in feed.entries:
        pub = datetime.datetime(*entry.published_parsed[:6])
        if pub >= cutoff:
            urls.append(entry.link)
    return urls

def request_indexing(urls):
    creds   = service_account.Credentials.from_service_account_file(KEY_FILE, scopes=SCOPES)
    service = build("indexing", "v3", credentials=creds)
    for url in urls:
        body = {"url": url, "type": "URL_UPDATED"}
        res  = service.urlNotifications().publish(body=body).execute()
        print(f"✓ {url}  →  {res}")

if __name__ == "__main__":
    urls = get_recent_urls()
    if urls:
        print(f"→ {len(urls)}개 URL 색인 요청")
        request_indexing(urls)
    else:
        print("→ 최근 24시간 내 새 포스트 없음. 스킵.")
