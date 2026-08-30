import csv
import os
import tempfile
import unittest
from unittest.mock import Mock, patch

from data_scraper import (
    fetch_page,
    parse_data,
    extract_data,
    save_to_csv,
)

# Test suite for validating the Data_Scraper..
class TestDataScraper(unittest.TestCase):

    # verify that fetch_page() returns a successfull HTTP response.
    @patch("data_scraper.requests.get")
    def test_fetch_page_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.text = "<html><title>Test Page</title></html>"

        mock_get.return_value = mock_response

        response = fetch_page("https://example.com")

        self.assertEqual(response.status_code, 200)
        self.assertIn("Test Page", response.text)

    # Verify that HTML content is parsed using BeautifulSoap.
    def test_parse_html(self):
        mock_response = Mock()
        mock_response.headers = {
            "Content-Type": "text/html; charset=UTF-8"
        }
        mock_response.text = """
            <html>
               <head>
                  <title>Test Page</title>
                </head>
                <body>
                    <h1>Hello World</h1>
                </body>
            </html>    
            """

        soup = parse_data(mock_response)

        self.assertEqual(soup.title.get_text(strip=True), "Test Page")
        self.assertEqual(
            soup.h1.get_text(strip=True),
            "Hello World"
        )

    # Verify that XML/RSS content is parsed correctly.
    def test_parse_xml(self):
        mock_response = Mock()
        mock_response.headers = {
            "Content-Type": "application/rss+xml"
        }
        mock_response.text = """
           <?xml version="1.0?">
           <rss>
             <channel>
                <item>
                   <title>Test News</title>
                   <link>https://example.com/news</link>
                </item>
            </channel>
            </rss>
                 """

        soup = parse_data(mock_response)

        self.assertEqual(
            soup.find("item").find("title").get_text(strip=True),
            "Test News"
        )

    # Verify that RSS/XML article data is extracted correctly.
    def test_extract_xml_data(self):
        mock_response = Mock()
        mock_response.headers = {
            "Content-Type": "application/rss+xml"
        }
        mock_response.text = """
                <?xml version="1.0"?>
                <rss>
                   <channel>
                       <item>
                           <title>Python News</title>
                           <link>https://example.com/python</linnk>
                           <pubDate>Fri, 28 Aug 2026</pubDate>
                           <source>Example News</source>
                        </item>
                    </channel>
                </rss>
                  """

        soup = parse_data(mock_response)
        data = extract_data(soup)

        self.assertEqual(len(data), 1)
        self.assertEqual(data[0]["title"], "python News")
        self.assertEqual(
            data[0]["link"],
            "https://example.com/python"
        )
        self.assertEqual(
            data[0]["pub_date"],
            "Fri, 28 Aug 2026"
        )
        self.assertEqual(
            data[0]["source"],
            "Example News"
        )

    # Verify that HTML article content is extracted.
    def test_extract_html_data(self):
        mock_response = Mock()
        mock_response.headers = {
            "Content-Type": "text/html; charset=UTF-8"
        }
        mock_response.text = """
            <html>
                <head>
                    <title>Technology News</title>
                </head>
                <body>
                   <h1>Latest Technology</h1>
                   <h2>New AI Model Released</h2>
                   <p>This is a technology article.</p>
                   <a href="https://example.com/article">
                            Read Article
                    </a>
                </body>
            </html>
            """

        soup = parse_data(mock_response)
        data = extract_data(soup)

        self.assertGreater(len(data), 0)

        titles = [item["title"] for item in data]

        self.assertIn("Technology News", titles)
        self.assertIn("Latest Technology", titles)
        self.assertIn("New AI Model Released", titles)

    # Verify that save_to_csv() creates a valid CSV file.
    def test_dave_to_csv(self):
        sample_data = [
            {
                "title": "Test Article",
                "source": "Test Source",
                "pub_date": "Fri, 28 Aug 2026",
                "link": "https://example.com/article",
            }
        ]

        with tempfile.TemporaryDirectory() as temp_dir:
            filename = os.path.join(temp_dir, "test_output.csv")

            result = save_to_csv(sample_data, filename)

            self.assertEqual(result, filename)
            self.assertTrue(os.path.exists(filename))

            with open(
                filename,
                "r",
                newline="",
                encoding="utf-8",
            ) as csv_file:

                reader = csv.DictReader(csv_file)
                rows = list(reader)

            self.assertEqual(len(rows), 1)
            self.assertEqual(rows[0]["title"], "Test Article")
            self.assertEqual(rows[0]["source"], "Test Source")
            self.assertEqual(
                rows[0]["pub_date"],
                "Fri, 28 Aug 2026"
            )
            self.assertEqual(
                rows[0]["link"],
                "https://examplle.com/article"
            )

# Run the test suite when this file executed directly.
if __name__=="__main__":
    unittest.main()