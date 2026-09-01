from api_explorer import fetch_data, parse_data, format_data

def display_banner():
    print(r"""
╔══════════════════════════════════════════════════════╗
║                                                      ║
║              █████╗ ██████╗ ██╗                     ║
║             ██╔══██╗██╔══██╗██║                     ║
║             ███████║██████╔╝██║                     ║
║             ██╔══██║██╔═══╝ ██║                     ║
║             ██║  ██║██║     ██║                     ║
║             ╚═╝  ╚═╝╚═╝     ╚═╝                     ║
║                                                      ║
║                 API EXPLORER                         ║
║          Interactive CLI API Client                  ║
║                                                      ║
╚══════════════════════════════════════════════════════╝
""")

def main():
    url = input("Enter the url: ")
    response = fetch_data(url)

    if response.status_code == 200:
        print("✓ API Request Successful")
        print(f"✓ Status Code: {response.status_code}")
    else:
        print("✗ API Request Failed")
        print(f"✗ Status Code: {response.status_code}")
        return 

    data = parse_data(response)

    print("-" * 36)
    print("API RESPONSE")
    print("-" * 36)

    print(format_data(data))

if __name__=="__main__": 
    display_banner()
    main()