import requests
from bs4 import BeautifulSoup
import os
import time

# Home loan URL only
URLS = [
    "https://bankofmaharashtra.bank.in/personal-banking/loans/home-loan",
]

OUTPUT_FILE = "C:/Ro1/Test/loan-product-assistant/data/raw/scraped_data.html"


def scrape_bom_loans():
    print("🔄 Scraping Bank of Maharashtra loan data...")

    # Enhanced headers to mimic a real browser more closely
    headers = {
        "User-Agent": (
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
            "AppleWebKit/537.36 (KHTML, like Gecko) "
            "Chrome/120.0.0.0 Safari/537.36"
        ),
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9",
        "Accept-Encoding": "gzip, deflate, br",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Cache-Control": "max-age=0",
    }

    # Create a session to maintain cookies
    session = requests.Session()
    session.headers.update(headers)

    all_content = ""
    successful_scrapes = 0

    for idx, url in enumerate(URLS):
        print(f"📌 Scraping ({idx + 1}/{len(URLS)}): {url}")

        try:
            # Add a delay between requests to avoid rate limiting
            if idx > 0:
                time.sleep(2)
            
            response = session.get(url, timeout=15, allow_redirects=True)
            
            # Check response
            print(f"   Status Code: {response.status_code}")
            print(f"   Content Length: {len(response.content)} bytes")
            
        except requests.Timeout:
            print(f"❌ Timeout error for {url}")
            continue
        except requests.RequestException as e:
            print(f"❌ Request error for {url}: {e}")
            continue

        if response.status_code != 200:
            print(f"❌ Failed: {url} | Status: {response.status_code}")
            continue

        # Check if we got actual content
        if len(response.content) < 100:
            print(f"⚠️  Warning: Very small response from {url}")
            continue

        soup = BeautifulSoup(response.text, "html.parser")

        # Remove script and style elements for cleaner text
        for script in soup(["script", "style", "noscript"]):
            script.decompose()

        # Try to find main content areas (common patterns for bank websites)
        main_content = ""
        
        # Try different selectors that banks commonly use
        content_selectors = [
            {"class": ["main-content", "content", "page-content", "loan-content"]},
            {"id": ["main", "content", "main-content"]},
            {"role": "main"},
        ]
        
        found_content = False
        for selector in content_selectors:
            elements = soup.find_all(attrs=selector)
            if elements:
                main_content = "\n".join([elem.get_text(separator="\n", strip=True) for elem in elements])
                if len(main_content) > 500:  # Reasonable content length
                    found_content = True
                    break
        
        # Fallback to body if specific selectors don't work
        if not found_content:
            body = soup.find("body")
            if body:
                main_content = body.get_text(separator="\n", strip=True)
            else:
                main_content = soup.get_text(separator="\n", strip=True)

        # Check if we got meaningful content
        if len(main_content) > 200:
            all_content += f"\n\n{'=' * 80}\n"
            all_content += f"URL: {url}\n"
            all_content += f"{'=' * 80}\n\n"
            all_content += main_content
            successful_scrapes += 1
            print(f"✅ Successfully scraped {len(main_content)} characters")
        else:
            print(f"⚠️  Warning: Insufficient content from {url} (only {len(main_content)} chars)")

    # Save results
    if all_content:
        # Write directly to file in current directory
        try:
            with open(OUTPUT_FILE, "w", encoding="utf-8") as f:
                f.write(all_content)
            
            # Verify file was created
            if os.path.exists(OUTPUT_FILE):
                file_size = os.path.getsize(OUTPUT_FILE)
                abs_path = os.path.abspath(OUTPUT_FILE)
                print(f"\n✅ Scraped data saved to: {abs_path}")
                print(f"📊 Successfully scraped {successful_scrapes}/{len(URLS)} pages")
                print(f"📁 File size: {file_size:,} bytes ({file_size/1024:.2f} KB)")
            else:
                print(f"\n⚠️ File was not created at {OUTPUT_FILE}")
        except Exception as e:
            print(f"\n❌ Error saving file: {e}")
    else:
        print("\n❌ No content was scraped. Possible issues:")
        print("   - Website may require JavaScript rendering")
        print("   - IP may be blocked")
        print("   - URLs may have changed")
        print("   - Website may use anti-scraping protection")
        print("\n💡 Consider using Selenium or Playwright for JavaScript-heavy sites")


if __name__ == "__main__":
    scrape_bom_loans()