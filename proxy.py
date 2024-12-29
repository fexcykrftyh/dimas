import os
import urllib.request
import urllib.error
import re
import threading
import queue
from time import sleep

# Warna untuk output terminal
red = "\033[1;31m"
green = "\033[1;32m"
yellow = "\033[1;33m"
blue = "\033[1;34m"
defcol = "\033[0m"

# Fungsi untuk output warna
def error(msg):
    print(f"{red}[{yellow}!{red}] - {defcol}{msg}")

def action(msg):
    print(f"{red}[{green}+{red}] - {defcol}{msg}")

def display_progress(current, total):
    percent = int((current / total) * 100)
    bar = '-' * percent + ' ' * (100 - percent)
    print(f"\r[{bar}] {percent}%", end='', flush=True)

# Bagian 1: Scraper
def scrape_site(url, proxies, progress_callback, current, total):
    try:
        with urllib.request.urlopen(url) as response:
            html = response.read().decode('utf-8')
            found_proxies = re.findall(r'(?:\d{1,3}\.){3}\d{1,3}:\d{2,5}', html)
            action(f"{len(found_proxies)} proxies found on {url}")
            proxies.extend(found_proxies)
    except Exception as e:
        error(f"Error scraping {url}: {e}")
    finally:
        progress_callback(current, total)

def scrape_sites(sites_file, output_file):
    try:
        with open(sites_file, "r") as f:
            sites = [line.strip() for line in f]
    except FileNotFoundError:
        error(f"Unable to open file: {sites_file}")
        return []

    total_sites = len(sites)
    proxies = []
    threads = []
    thread_queue = queue.Queue()

    for i, site in enumerate(sites):
        t = threading.Thread(target=scrape_site, args=(site, proxies, display_progress, i + 1, total_sites))
        threads.append(t)
        thread_queue.put(t)
        t.start()

    while not thread_queue.empty():
        thread = thread_queue.get()
        thread.join()

    unique_proxies = list(set(proxies))
    with open(output_file, "w") as out_file:
        out_file.write("\n".join(unique_proxies))

    print("\nScraping completed.")
    action(f"Results saved in {output_file}.")
    return unique_proxies

# Bagian 2: Checker
def check_proxy(proxy, timeout):
    proxy_handler = urllib.request.ProxyHandler({'http': proxy})
    opener = urllib.request.build_opener(proxy_handler)
    urllib.request.install_opener(opener)
    try:
        urllib.request.urlopen('http://www.google.com', timeout=timeout)
        action(f"Proxy {proxy} is working.")
        return True
    except:
        error(f"Proxy {proxy} failed.")
        return False

def verify_proxies(proxy_list, output_file, timeout=5, threads=30):
    valid_proxies = []
    thread_queue = queue.Queue()

    def worker():
        while not thread_queue.empty():
            proxy = thread_queue.get()
            if check_proxy(proxy, timeout):
                valid_proxies.append(proxy)
            thread_queue.task_done()

    for proxy in proxy_list:
        thread_queue.put(proxy)

    for _ in range(threads):
        t = threading.Thread(target=worker)
        t.start()

    thread_queue.join()

    with open(output_file, "w") as out_file:
        out_file.write("\n".join(valid_proxies))

    action(f"Valid proxies saved to {output_file}")
    return valid_proxies

# Bagian 3: Integrasi
def main():
    sites_file = "sites.txt"
    scrape_output = "scraped_proxies.txt"
    check_output = "valid_proxies.txt"

    # Scrape Proxies
    action("Starting scraping process...")
    scraped_proxies = scrape_sites(sites_file, scrape_output)
    if not scraped_proxies:
        error("No proxies scraped. Exiting...")
        return

    # Check Proxies
    action("Starting proxy checking process...")
    valid_proxies = verify_proxies(scraped_proxies, check_output)

    # Clean Up
    if os.path.exists(scrape_output):
        os.remove(scrape_output)
        action(f"Temporary file {scrape_output} deleted.")

    if valid_proxies:
        action(f"{len(valid_proxies)} valid proxies found.")
    else:
        error("No valid proxies found.")

if __name__ == "__main__":
    main()
