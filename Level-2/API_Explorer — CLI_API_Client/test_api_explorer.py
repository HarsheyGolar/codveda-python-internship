import json
import unittest
from unittest.mock import Mock, patch

from api_explorer import fetch_data, parse_data, format_data


class TestAPIExplorer(unittest.TestCase):

    # Verify that a successful API request returns the response object.
    @patch("api_explorer.requests.get")
    def test_fetch_data_success(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 200
        mock_response.json.return_value = {
            "name": "Harshey Golar",
            "followers": 10,
        }

        mock_get.return_value = mock_response

        response = fetch_data("https://api.example.com/user")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json(),
            {
                "name": "Harshey Golar",
                "followers": 10,
            },
        )

        mock_get.assert_called_once_with(
            "https://api.example.com/user",
            timeout=10,
        )

    # Verify that a failed HTTP response is still returned to the caller.
    @patch("api_explorer.requests.get")
    def test_fetch_data_http_error_response(self, mock_get):
        mock_response = Mock()
        mock_response.status_code = 404

        mock_get.return_value = mock_response

        response = fetch_data(
            "https://api.example.com/not-found"
        )

        self.assertEqual(response.status_code, 404)

    # Verify that network/request errors are propagated.
    @patch("api_explorer.requests.get")
    def test_fetch_data_request_error(self, mock_get):
        import requests

        mock_get.side_effect = requests.RequestException(
            "Connection failed"
        )

        with self.assertRaises(requests.RequestException):
            fetch_data("https://api.example.com")

    # Verify that parse_data returns the response it receives.
    def test_parse_data(self):
        mock_response = Mock()

        mock_response.json.return_value = {
            "name": "Harshey Golar",
            "followers": 10,
        }

        result = parse_data(mock_response)

        self.assertEqual(
            result,
            {
                "name": "Harshey Golar",
                "followers": 10,
            },
        )

        mock_response.json.assert_called_once()

    # Verify that JSON data is formatted into readable text.
    def test_format_data(self):
        data = {
            "name": "Harshey Golar",
            "followers": 10,
        }

        result = format_data(data)

        expected = json.dumps(data, indent=4)

        self.assertEqual(result, expected)

    # Verify that format_data handles nested JSON structures.
    def test_format_nested_data(self):
        data = {
            "user": {
                "name": "Harshey Golar",
                "stats": {
                    "followers": 10,
                    "repos": 12,
                },
            }
        }

        result = format_data(data)

        self.assertIn('"user"', result)
        self.assertIn('"name": "Harshey Golar"', result)
        self.assertIn('"followers": 10', result)
        self.assertIn('"repos": 12', result)

    # Verify that format_data handles lists returned by APIs.
    def test_format_list_data(self):
        data = [
            {"id": 1, "name": "Project One"},
            {"id": 2, "name": "Project Two"},
        ]

        result = format_data(data)

        self.assertIn('"Project One"', result)
        self.assertIn('"Project Two"', result)


if __name__ == "__main__":
    unittest.main()