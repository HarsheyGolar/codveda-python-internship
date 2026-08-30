from data_scraper import extract_data, fetch_page, parse_data, save_to_csv


# Run the scraper for a user-provided URL and display the results.
def main():
    url = input("Enter Your URL: ").strip()
    if not url:
        print("No URL entered.")
        return

    try:
        response = fetch_page(url)
        soup = parse_data(response)
        news_items = extract_data(soup)

        file_name = save_to_csv(news_items)

        print(f"Total News Items Extracted: {len(news_items)}")
        print(f"Saved data to: {file_name}\n")

        for index, item in enumerate(news_items[:5], 1):
            print(f"[{index}] {item['title']}")
            print(f"   type:   {item['type']}")
            print(f"   source: {item['source']}")
            print(f"   Date:   {item['pub_date']}")
            print(f"   link:   {item['link']}\n")
    except Exception as exc:
        print(f"Error while scraping: {exc}")


if __name__ == "__main__":
    main()
