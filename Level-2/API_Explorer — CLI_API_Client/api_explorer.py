import requests
import json

def get_url(url):
    
    if url.startswith("https://"):
        response = requests.get(url)
        if response.status_code == 200:
            return "Success"
        else:
            return "Failed"

def fetch_data(url):
    # url = "https://api.github.com/users/HarsheyGolar"
    response = requests.get(url, timeout=10)
    return response

def parse_data(response):
    return response.json()

def format_data(data):
    return json.dumps(data, indent=4)

if __name__ == "__main__":
    response = fetch_data()
    data = parse_data(response)
    print(format_data(data))