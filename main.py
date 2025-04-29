# main.py
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, HttpUrl
from typing import List, Dict, Any, Optional
import requests
from bs4 import BeautifulSoup
import asyncio
from concurrent.futures import ThreadPoolExecutor
import logging
import time

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Website Scraper API",
    description="An API that scrapes content from websites",
    version="1.0.0"
)

class ScrapingRequest(BaseModel):
    urls: List[HttpUrl]
    selectors: Optional[Dict[str, str]] = None
    timeout: Optional[int] = 10
    headers: Optional[Dict[str, str]] = None

class ScrapingResponse(BaseModel):
    url: str
    status: str
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None
    time_taken: float

@app.post("/scrape", response_model=List[ScrapingResponse])
async def scrape_websites(request: ScrapingRequest):
    """
    Scrape multiple websites based on the provided URLs and optional CSS selectors.
    
    If selectors are provided, only the specified elements will be extracted.
    If no selectors are provided, the full HTML content will be returned.
    """
    if not request.urls:
        raise HTTPException(status_code=400, detail="No URLs provided")
    
    # Use default headers if none provided
    headers = request.headers or {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    
    # Create a thread pool for concurrent scraping
    with ThreadPoolExecutor(max_workers=min(10, len(request.urls))) as executor:
        # Create a list of tasks for asyncio to gather
        tasks = [
            asyncio.to_thread(
                scrape_single_website, 
                url, 
                request.selectors, 
                request.timeout, 
                headers
            ) 
            for url in request.urls
        ]
        
        # Gather results from all tasks
        results = await asyncio.gather(*tasks)
    
    return results

def scrape_single_website(url: str, selectors: Optional[Dict[str, str]], timeout: int, headers: Dict[str, str]) -> ScrapingResponse:
    """
    Scrape a single website and return the result.
    """
    start_time = time.time()
    try:
        logger.info(f"Scraping URL: {url}")
        response = requests.get(url, headers=headers, timeout=timeout)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extract data based on selectors if provided, otherwise return full HTML
        if selectors:
            data = {}
            for key, selector in selectors.items():
                elements = soup.select(selector)
                data[key] = [element.get_text(strip=True) for element in elements]
        else:
            # If no selectors, return basic page info
            data = {
                "title": soup.title.string if soup.title else None,
                "meta_description": soup.find("meta", attrs={"name": "description"}).get("content", "") if soup.find("meta", attrs={"name": "description"}) else None,
                "h1_tags": [h1.get_text(strip=True) for h1 in soup.find_all("h1")],
                "links": [{"text": a.get_text(strip=True), "href": a.get("href")} for a in soup.find_all("a", href=True)][:50]  # Limit to 50 links
            }
        
        time_taken = time.time() - start_time
        return ScrapingResponse(
            url=str(url),
            status="success",
            data=data,
            time_taken=time_taken
        )
    
    except requests.exceptions.RequestException as e:
        logger.error(f"Error scraping {url}: {str(e)}")
        time_taken = time.time() - start_time
        return ScrapingResponse(
            url=str(url),
            status="error",
            error=str(e),
            time_taken=time_taken
        )
    except Exception as e:
        logger.error(f"Unexpected error scraping {url}: {str(e)}")
        time_taken = time.time() - start_time
        return ScrapingResponse(
            url=str(url),
            status="error",
            error=f"Unexpected error: {str(e)}",
            time_taken=time_taken
        )

@app.get("/")
def read_root():
    return {"message": "Welcome to the Website Scraper API", "usage": "Send a POST request to /scrape with a list of URLs"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)