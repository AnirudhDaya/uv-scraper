# Web Scraper API

A robust web scraping API built with FastAPI that can scrape multiple websites concurrently and return structured data in JSON format.

## Features

- Scrape multiple websites concurrently
- Extract specific elements using CSS selectors
- Configurable timeout and headers
- Error handling and logging
- Response includes scraping time measurements
- Docker support for easy deployment

## Installation

### Using uv (recommended)

This project was initialized with `uv`, a fast Python package installer and resolver.

```bash
# Clone the repository
git clone https://github.com/yourusername/web-scraper-api.git
cd web-scraper-api

# Create a virtual environment and install dependencies with uv
uv venv
uv pip install -r requirements.txt
```

### Using pip

```bash
# Clone the repository
git clone https://github.com/yourusername/web-scraper-api.git
cd web-scraper-api

# Create a virtual environment and install dependencies
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### Using Docker

```bash
# Build the Docker image
docker build -t web-scraper-api .

# Run the Docker container
docker run -p 8000:8000 web-scraper-api
```

## Usage

### Starting the API Server

```bash
uvicorn main:app --reload
```

The API will be available at http://localhost:8000.

### API Documentation

Once the server is running, you can access the automatically generated API documentation:

- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

### API Endpoints

#### POST /scrape

Scrapes websites based on the provided URLs and optional CSS selectors.

**Request Body:**

```json
{
  "urls": [
    "https://example.com",
    "https://another-example.com"
  ],
  "selectors": {
    "headlines": "h1, h2, h3",
    "content": "article p",
    "links": "a[href]"
  },
  "timeout": 10,
  "headers": {
    "User-Agent": "Custom User Agent"
  }
}
```

**Response:**

```json
[
  {
    "url": "https://example.com",
    "status": "success",
    "data": {
      "headlines": ["Headline 1", "Headline 2"],
      "content": ["Paragraph 1", "Paragraph 2"],
      "links": ["Link Text 1", "Link Text 2"]
    },
    "time_taken": 0.923
  },
  {
    "url": "https://another-example.com",
    "status": "error",
    "error": "Connection timeout",
    "time_taken": 10.053
  }
]
```

## Responsible Usage

Please use this tool responsibly:

1. Respect robots.txt files
2. Set reasonable delays between requests
3. Avoid scraping sensitive or personal information
4. Check the website's terms of service before scraping
5. Don't overload servers with too many requests

## License

[MIT License](LICENSE)