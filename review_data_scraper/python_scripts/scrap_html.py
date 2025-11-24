import requests
import os

def download_raw_htmls(base_url, out_dir="review_html", max_pages=100):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/126.0.0.0 Safari/537.36'
    }
    os.makedirs(out_dir, exist_ok=True)

    for page_num in range(1, max_pages + 1):
        # Replace the page value in the URL
        url = base_url.replace("page=1", f"page={page_num}")
        filename = os.path.join(out_dir, f"review_html_{page_num}.html")
        print(f"Fetching page {page_num}: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(response.text)
            print(f"✅ Saved HTML to {filename}")
        except requests.exceptions.RequestException as e:
            print(f"❌ Error on page {page_num}: {e}")

# Base URL with "page=1" as placeholder
base_url = "https://www.flipkart.com/samsung-galaxy-s24-5g-snapdragon-amber-yellow-128-gb/product-reviews/itmd4baa945a78ef?pid=MOBHDVFKSZNEZGXW&lid=LSTMOBHDVFKSZNEZGXWFNGEN2&marketplace=FLIPKART&page=1"
download_raw_htmls(base_url)
