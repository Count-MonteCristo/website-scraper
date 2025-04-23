import requests

def fetch_html(url):
    try:
        headers = {
            "User-Agent": "Mozilla/5.0 (compatible; WebScraper/1.0)"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        return response.text
    except Exception as e:
        print(f"[ERROR] Could not fetch {url}: {e}")
        return None
