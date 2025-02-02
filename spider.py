#!/usr/bin/env python3
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin, urlparse
import sys
import time

def is_valid_url(url):
    """
    Basic check to see if a URL is valid.
    """
    parsed = urlparse(url)
    return bool(parsed.netloc) and bool(parsed.scheme)

def crawl_site(start_url):
    """
    Crawl the site starting from start_url, only following links
    on the same domain.
    """
    # Parse the domain of the starting URL for domain restriction.
    domain = urlparse(start_url).netloc
    print(f"Domain to crawl: {domain}")

    visited = set()
    to_visit = [start_url]
    live_urls = []

    while to_visit:
        url = to_visit.pop(0)
        if url in visited:
            continue
        visited.add(url)
        try:
            print(f"Visiting: {url}")
            response = requests.get(url, timeout=10)
        except requests.RequestException as e:
            print(f"Failed to fetch {url}: {e}")
            continue

        if response.status_code != 200:
            print(f"Non-200 response for {url}: {response.status_code}")
            continue

        # If it's a live page, add it to the list.
        live_urls.append(url)

        # Parse the page for links
        soup = BeautifulSoup(response.text, "html.parser")
        for a_tag in soup.find_all("a", href=True):
            href = a_tag.get("href")
            # Construct full URL from relative links
            full_url = urljoin(url, href)
            # Normalize the URL (remove URL fragments)
            parsed_full_url = urlparse(full_url)
            full_url = parsed_full_url._replace(fragment="").geturl()

            # Check if it is valid, on the same domain, and not already visited
            if is_valid_url(full_url) and urlparse(full_url).netloc == domain:
                if full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)
        # Optional delay to be polite to the server
        time.sleep(0.5)

    return live_urls

def write_to_file(urls, filename="live_urls.txt"):
    """
    Write the list of URLs to a text file.
    """
    with open(filename, "w") as file:
        for url in urls:
            file.write(url + "\n")
    print(f"Written {len(urls)} live URLs to {filename}")

def main():
    # Ask for the URL input from the user
    start_url = input("Enter the URL to crawl (include http:// or https://): ").strip()
    if not is_valid_url(start_url):
        print("Invalid URL. Please include the protocol (http:// or https://) and try again.")
        sys.exit(1)

    print("Starting the crawl. This might take a while depending on the size of the site...")
    live_urls = crawl_site(start_url)
    write_to_file(live_urls)

if __name__ == "__main__":
    main()