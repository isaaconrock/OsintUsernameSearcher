import requests

# Function to read URLs from a file and insert the username
def read_urls_from_file(username):
    with open('websites.txt', 'r') as file:
        base_urls = file.readlines()
    # Insert the username into each URL
    urls = [url.strip().format(username=username) for url in base_urls]
    return urls

# Function to search username across websites listed in the file
def search_username(username):
    print(f'Searching for username: {username}')
    websites = read_urls_from_file(username)
    matches_found = 0

    for url in websites:
        try:
            response = requests.get(url, timeout=10)
            if response.status_code == 200:
                print(f'Found {username} at {url}')
                matches_found += 1
        except Exception as e:
            print(f'Error accessing {url}: {e}')

    print(f'Finished: A total of {matches_found} matches found out of {len(websites)} websites.')

if __name__ == '__main__':
    username = input('Enter username to search: ')
    search_username(username)
