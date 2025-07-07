import os
import requests
from urllib.parse import urlparse
from duckduckgo_search import DDGS

# Install with: pip install duckduckgo-search requests

def is_pdf_url(url):
    return url.lower().endswith(".pdf") or ".pdf?" in url.lower()

def sanitize_filename(url):
    parsed = urlparse(url)
    name = os.path.basename(parsed.path)
    if not name.endswith(".pdf"):
        name += ".pdf"
    return name.replace("%", "_").replace("?", "_")

def download_pdf(url, folder="pdfs"):
    try:
        os.makedirs(folder, exist_ok=True)
        filename = sanitize_filename(url)
        filepath = os.path.join(folder, filename)

        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        }

        response = requests.get(url, headers=headers, timeout=15)

        if response.status_code == 200 and "application/pdf" in response.headers.get("Content-Type", ""):
            with open(filepath, "wb") as f:
                f.write(response.content)
            print(f"[+] Downloaded: {filename}")
        else:
            print(f"[-] Skipped (not a valid PDF): {url}")
    except Exception as e:
        print(f"[!] Error downloading {url}: {e}")

def search_and_download_pdfs(query, max_results=10):
    print(f"\n[i] Searching for: {query}\n")
    with DDGS() as ddgs:
        results = ddgs.text(f"{query} filetype:pdf", max_results=max_results)
        found = False
        for r in results:
            url = r.get("href")
            if url and is_pdf_url(url):
                found = True
                download_pdf(url)
        if not found:
            print("[-] No valid PDF links found.")

def main():
    while True:
        topic = input("\nEnter topic to search PDFs for: ")
        search_and_download_pdfs(topic, max_results=10)

        print("\nWhat do you want to do next?")
        print("1. 🔍 Download another PDF")
        print("2. ❌ Exit")

        choice = input("Enter choice [1/2]: ").strip()
        if choice != "1":
            print("\n[✔] Exiting... Have a great day!")
            break

if __name__ == "__main__":
    main()
