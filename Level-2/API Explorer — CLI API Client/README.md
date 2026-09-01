<div align="center">

# 🔎 API Explorer

### A Lightweight Python CLI for Testing and Exploring Public APIs

<p>
  <img src="https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python"/>
  <img src="https://img.shields.io/badge/Requests-HTTP%20Client-2CA5E0?style=for-the-badge&logo=python&logoColor=white" alt="Requests"/>
  <img src="https://img.shields.io/badge/JSON-Parser-4B8BBE?style=for-the-badge&logo=json&logoColor=white" alt="JSON"/>
  <img src="https://img.shields.io/badge/CLI-Terminal%20App-0A0A0A?style=for-the-badge&logo=terminal&logoColor=white" alt="CLI"/>
  <img src="https://img.shields.io/badge/Tests-Unittest-4B8BBE?style=for-the-badge&logo=githubactions&logoColor=white" alt="Tests"/>
  <img src="https://img.shields.io/badge/Status-Completed-success?style=for-the-badge&logo=checkmarx&logoColor=white" alt="Status"/>
</p>

<p>
  <strong>CodVeda Technologies · Python Development Internship · Level 2 · Task 2</strong>
</p>

</div>

---

## 📋 Table of Contents

- [Overview](#-overview)
- [Features](#-features)
- [Architecture](#-architecture)
- [Project Structure](#-project-structure)
- [How It Works](#-how-it-works)
- [Installation](#-installation)
- [Usage](#-usage)
- [Example Output](#-example-output)
- [Testing](#-testing)
- [Error Handling](#-error-handling)
- [Limitations](#-limitations)
- [Future Improvements](#-future-improvements)
- [Learning Outcomes](#-learning-outcomes)
- [Internship Context](#-internship-context)
- [Dependencies](#-dependencies)
- [License](#-license)
- [Author](#-author)

---

## ✨ Overview

**API Explorer** is a lightweight Python command-line application that accepts a public API URL from the user, sends a request to that endpoint, checks the HTTP status, parses the JSON response, and prints the data in a readable, well-formatted structure.

The project is designed to help beginners understand how real APIs behave in practice without relying on a browser or a frontend interface. It focuses on the fundamentals of request handling, response validation, JSON parsing, and terminal-based output.

### Core Pipeline

```text
User URL
   │
   ▼
fetch_data(url)
   │
   ▼
HTTP Response
   │
   ▼
parse_data(response)
   │
   ▼
format_data(data)
   │
   ▼
Pretty-Printed JSON Output
```

---

## ⚙️ Features

| Feature | Description |
|---|---|
| 🔗 **Runtime URL Input** | Accepts a target API URL directly from the terminal |
| 🌐 **HTTP Request Handling** | Sends GET requests using Python's `requests` library |
| ✅ **Status Validation** | Confirms whether the API response is successful or failed |
| 🧾 **JSON Parsing** | Converts API responses into Python-readable data structures |
| 🖨️ **Readable Output** | Formats JSON with indentation for terminal readability |
| 🧪 **Automated Testing** | Includes `unittest` coverage for validation and formatting logic |
| 🧱 **Modular Design** | Keeps fetching, parsing, and output formatting separated by function |

---

## 🏗️ Architecture

```text
User enters API URL
        │
        ▼
   fetch_data()
        │
        ▼
   HTTP Response
        │
        ▼
  Status code 200?
      /      \
     /        \
    Yes       No
     │         │
     ▼         ▼
parse_data()  Display Error Message
     │
     ▼
format_data()
     │
     ▼
Pretty JSON Output
```

---

## 📁 Project Structure

```text
API Explorer — CLI API Client/
│
├── api_explorer.py
│   ├── get_url()
│   ├── fetch_data()
│   ├── parse_data()
│   └── format_data()
│
├── main.py
│   └── CLI interface and request flow
│
├── test_api_explorer.py
│   └── Automated unit tests
│
├── README.md
│   └── Project documentation
│
└── .venv/
    └── Virtual environment
```

---

## 🔧 How It Works

### 1. `fetch_data(url)`

This function handles the API request.

It:

- receives the URL entered by the user
- sends an HTTP GET request
- uses a timeout to avoid indefinite hanging requests
- returns the response object for further processing

This allows the app to access both the response content and the HTTP status code.

---

### 2. `parse_data(response)`

Once the API call succeeds, the response is converted from raw HTTP content into usable Python data.

The function calls:

```python
response.json()
```

This makes the returned payload easy to inspect and print in a readable format.

---

### 3. `format_data(data)`

The JSON output is formatted using Python's `json.dumps(..., indent=4)` so it is easier to read in the terminal.

This is especially useful when the API response contains nested objects or arrays.

---

### 4. `main()`

The CLI flow is simple and beginner-friendly:

1. User enters an API URL
2. Request is sent
3. Response status is checked
4. Data is parsed
5. JSON is printed in a clean format

---

## 🚀 Installation

### Prerequisites

Python 3.x is required.

Check your version:

```bash
python --version
```

### Create a Virtual Environment

Windows PowerShell:

```powershell
python -m venv .venv
.venv\Scripts\activate
```

### Install Dependencies

```powershell
pip install requests
```

---

## ▶️ Usage

Run the application:

```powershell
python main.py
```

The terminal will ask for a URL:

```text
Enter the url: 
```

Example:

```text
Enter the url: https://api.github.com/users/octocat
```

The program then checks the response and prints the JSON payload in a structured format.

---

## 📤 Example Output

```text
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

✓ API Request Successful
✓ Status Code: 200
------------------------------------
API RESPONSE
------------------------------------
{
    "login": "octocat",
    "id": 583231,
    "node_id": "MDQ6VXNlcjU4MzIzMQ==",
    "avatar_url": "https://avatars.githubusercontent.com/u/583231?v=4",
    "name": "The Octocat",
    "company": null,
    "blog": "https://github.blog",
    "location": "San Francisco",
    "email": null
}
```

---

## 🧪 Testing

This project includes an automated test suite for the core logic.

Run tests with:

```powershell
python -m unittest test_api_explorer.py
```

### Covered Scenarios

- successful API requests
- HTTP error status handling
- request exceptions and connection failures
- JSON parsing
- nested JSON formatting
- list-based API output formatting

---

## ⚠️ Error Handling

The application includes basic safeguards for common runtime issues:

- invalid or unreachable URLs
- non-200 HTTP responses
- request timeouts
- malformed JSON payloads
- network-related exceptions

When a request fails, the app responds clearly instead of crashing unexpectedly.

---

## 🚧 Limitations

This project is intentionally minimal and is meant for learning and experimentation. Some limitations include:

- only supports GET requests for now
- no support for authentication headers or tokens
- no response filtering or search features
- no saving of fetched responses to disk
- not built for production-grade API client workflows

---

## 🔮 Future Improvements

This project can be extended in several useful directions:

- add support for POST, PUT, and DELETE methods
- include custom headers and API keys
- support query parameters and request bodies
- allow saving responses to JSON or CSV files
- add command-line flags for advanced usage
- build a richer terminal interface with colored output

---

## 🎯 Learning Outcomes

This project helps reinforce key programming skills such as:

- Python scripting and CLI development
- HTTP request/response fundamentals
- JSON parsing and serialization
- status code analysis and error handling
- unit testing and validation workflows

---

## 🏫 Internship Context

This project was developed as part of the **CodVeda Python Development Internship** to practice:

- real-world API interaction
- building user-friendly terminal tools
- writing clean, testable Python functions
- understanding the relationship between frontend/backend data exchange

---

## 📦 Dependencies

- Python 3.x
- `requests`
- `json`
- `unittest`

---

---

## 📄 License

<p>
  <img src="https://img.shields.io/badge/License-Open%20Source-orange?style=for-the-badge&logo=opensourceinitiative&logoColor=white" alt="License"/>
</p>

See the repository's <strong>LICENSE</strong> file for the applicable license.

---

## 👤 Author

<p align="center">
  <img src="https://img.shields.io/badge/Author-Harshey%20Golar-8A63D2?style=for-the-badge&logo=github&logoColor=white" alt="Author"/>
</p>

<h3 align="center">Harshey Golar</h3>

<p align="center">
  <strong>Python Developer · AI/ML Enthusiast</strong>
</p>

<p align="center">
  <a href="https://github.com/HarsheyGolar">
    <img src="https://img.shields.io/badge/GitHub-HarsheyGolar-181717?style=for-the-badge&logo=github&logoColor=white" alt="GitHub"/>
  </a>
</p>

---

<div align="center">

⭐ <strong>If you find this project useful, consider starring the repository.</strong>

Built with Python during the CodVeda Technologies Python Development Internship.

</div>

---

<p align="center">
  <img src="https://img.shields.io/badge/Made%20with-%E2%9D%A4-red?style=for-the-badge" alt="Made with love" />
  <img src="https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white" alt="Python" />
</p>
