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

### Example Client

An example client script is provided in `example_client.py`:

```bash
python example_client.py
```

### Sample Request and Response

#### Sample Request

```bash
curl -X 'POST' \
  'https://scrape.raisevcfund.com/scrape' \
  -H 'Content-Type: application/json' \
  -d '{
  "urls": [
    "https://softservedweb.com"
  ]
}'
```

#### Sample Response

```json
[
  {
    "url": "https://softservedweb.com/",
    "status": "success",
    "data": {
      "title": "Soft Served Web",
      "meta_description": "Soft Served Web is a web development agency that specializes in building custom websites and web applications.",
      "h1_tags": [
        "EmpoweringYourBusinesswithTechnologyExcellence",
        "Services",
        "Not Convinced?",
        "For the needy !"
      ],
      "links": [
        {"text": "", "href": "/"},
        {"text": "About", "href": "/about"},
        {"text": "Services", "href": "/#services"},
        {"text": "Projects", "href": "/projects"},
        {"text": "Blogs", "href": "/blogs"},
        {"text": "IntroducingAgents as a Service", "href": "/projects"},
        {"text": "Talk to Us", "href": "/contact"},
        {"text": "projects", "href": "/projects"},
        {"text": "AR Social\" Never expected an easy toi deploy treasurehunt application that too in AR would be out there, Believe me when I say ZERO setup time \"Raghav V SCollege Fest Coordinator, Cult", "href": "/projects/ar-social"},
        {"text": "Kuppayam\" A game changer for my wardrobe , picking up my OOTD has never been easier. A must use for all fashionistas \"Ton GeorgeThrissur", "href": "/projects/kuppayam"},
        {"text": "TinkerSpace VR\" Mindblowing, immersive and exactly as we expected, They delivered right in the nick of time \"MuadTinkerspace", "href": "/projects/tinker-space"},
        {"text": "Connect with us!", "href": "/contact"},
        {"text": "want to meet us ?", "href": "/about"},
        {"text": "Book a Call", "href": "/contact"},
        {"text": "", "href": "/projects/neura-query"},
        {"text": "", "href": "/projects/dialgen-ai"},
        {"text": "", "href": "/projects/daya-hr-automation"},
        {"text": "Book a Call", "href": "/contact"},
        {"text": "Projects", "href": "/projects"},
        {"text": "Contact us", "href": "/contact"},
        {"text": "Contact us", "href": "/contact"},
        {"text": "Contact us", "href": "/contact"},
        {"text": "Talk to Us", "href": "/contact"},
        {"text": "", "href": "/contact"},
        {"text": "Twitter", "href": "https://x.com/softservedweb"},
        {"text": "Linkedin", "href": "https://www.linkedin.com/company/softservedweb/"},
        {"text": "Instagram", "href": "https://www.instagram.com/softservedweb/"},
        {"text": "Privacy Policy", "href": "/privacy-policy"},
        {"text": "Terms and Conditions", "href": "/terms-and-condition"},
        {"text": "Refund Policy", "href": "/refund-policy"}
      ]
    },
    "error": null,
    "time_taken": 0.3171391487121582
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