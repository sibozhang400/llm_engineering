# Coles Website Scraper - Implementation Summary

## Problem Solved

The original `fetch_website_contents()` function using `requests` and BeautifulSoup wasn't working for the Coles website because:

1. **JavaScript Rendering**: Coles is a modern Single Page Application (SPA) that loads product data dynamically via JavaScript
2. **Bot Protection**: The site uses Incapsula WAF (Web Application Firewall) to block automated scrapers

## Solution Implemented

### 1. Playwright with Stealth Mode

Created `scraper_new.py` with:
- **Playwright async API** - Runs a real Chrome browser that executes JavaScript
- **playwright-stealth** - Patches browser fingerprints to avoid bot detection
- **Realistic browser settings**:
  - Custom user agent
  - Proper viewport size (1920x1080)
  - Browser args to disable automation flags
  - Wait strategies for dynamic content

### 2. Key Features

- **Headless mode works!** - Can run without showing browser window
- **Bypasses Incapsula** - Successfully gets past bot protection
- **Gets full rendered content** - ~500KB of HTML with all dynamic content loaded
- **Configurable wait time** - 5 second delay for JavaScript to finish rendering

## Files Updated

1. **`scraper_new.py`** - New async Playwright scraper with stealth mode
2. **`day1_grocery_deal_search.ipynb`** - Updated to use new scraper
3. **`test_scraper.py`** - Test script for headless=False mode
4. **`test_scraper_headless.py`** - Test script for headless=True mode

## How to Use

### In Jupyter Notebook

```python
from scraper_new import scrape_website

# Scrape with headless mode (recommended)
website_contents = await scrape_website(url, headless=True)

# Or with visible browser (for debugging)
website_contents = await scrape_website(url, headless=False)
```

### In Python Script

```python
import asyncio
from scraper_new import scrape_website

async def main():
    content = await scrape_website("https://www.coles.com.au/", headless=True)
    print(f"Got {len(content)} characters")

asyncio.run(main())
```

## Dependencies Installed

```bash
uv pip install playwright playwright-stealth
playwright install chromium
```

## Current Status

✅ **Working**: Scraper successfully bypasses Incapsula and gets full page content
✅ **Tested**: Both headless=True and headless=False modes work
✅ **Clean text extraction**: BeautifulSoup extracts text from HTML

## Next Steps

1. **Run the notebook cells** to test the scraper
2. **Add LLM integration** to parse deals and prices from the clean text
3. **Consider targeting specific pages** like `https://www.coles.com.au/on-special` for better deal listings
4. **Investigate API endpoints** (optional) - Check browser DevTools Network tab for JSON endpoints

## Performance Notes

- **Scraping time**: ~10-13 seconds per page
- **Content size**: ~500KB HTML, ~50-100KB clean text
- **Rate limiting**: Be respectful - add delays between requests if scraping multiple pages

## Ethical Considerations

- This is for learning/personal use only
- Don't hammer the server with rapid requests
- Respect robots.txt
- For production use, consider official APIs or contact Coles

## Troubleshooting

If you get blocked again:
1. Try `headless=False` to see if it helps
2. Increase wait time in the scraper (currently 5 seconds)
3. Check if your IP has been rate-limited (try from different network)
4. Consider rotating user agents or using proxy services
