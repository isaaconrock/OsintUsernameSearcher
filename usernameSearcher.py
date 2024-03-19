import urllib.request
from threading import Thread
from queue import Queue

DEFAULT_NUM_THREADS = 999

q = Queue()

def scan_sites(username):
    while True:
        site = q.get()
        url = f"{site}{username}"
        try:
            urllib.request.urlopen(url)
        except urllib.request.HTTPError as e:
            print(f"[-] No user found or error on site: {url} (Error: {e.code})")
        except urllib.request.URLError as e:
            print(f"[!] Connection refused or error on site: {url} (Error: {e.reason})")
        else:
            print(f"[+] User found in: {url}")
        q.task_done()


def load_sites_from_file(filename):
    with open(filename, 'r') as file:
        sites = [line.strip() for line in file.readlines()]
    return sites

def main(username, sites_file='sites.txt', n_threads=DEFAULT_NUM_THREADS):
    sites = load_sites_from_file(sites_file)
    for site in sites:
        q.put(site)

    for _ in range(n_threads):
        worker = Thread(target=scan_sites, args=(username,))
        worker.daemon = True
        worker.start()

if __name__ == "__main__":
    import sys
    if len(sys.argv) != 2:
        print("Usage: ./spy <username>")
        sys.exit(1)

    username = sys.argv[1]
    main(username)
    q.join()
