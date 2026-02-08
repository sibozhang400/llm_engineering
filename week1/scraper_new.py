from playwright.async_api import async_playwright
from playwright_stealth import Stealth

async def scrape_website(url, headless=False):
    """
    Scrape a website using Playwright with stealth mode to avoid bot detection.
    
    Args:
        url: The URL to scrape
        headless: If False, shows browser window (helps bypass detection)
    """
    async with async_playwright() as p:
        # Launch browser with stealth settings
        browser = await p.chromium.launch(
            headless=headless,
            args=[
                '--disable-blink-features=AutomationControlled',
                '--disable-dev-shm-usage',
                '--no-sandbox',
                '--disable-setuid-sandbox',
                '--disable-web-security',
                '--disable-features=IsolateOrigins,site-per-process'
            ]
        )
        
        # Create new page with realistic settings
        page = await browser.new_page(
            viewport={'width': 1920, 'height': 1080},
            user_agent='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        )
        
        # Apply stealth mode to avoid detection
        stealth = Stealth()
        await stealth.apply_stealth_async(page)
        
        # Navigate to the URL - use 'domcontentloaded' instead of 'networkidle' for faster loading
        # networkidle can hang on sites with continuous background requests
        await page.goto(url, wait_until='domcontentloaded', timeout=60000)
        
        # Wait a bit for any dynamic content to load
        await page.wait_for_timeout(5000)  # Increased to 5 seconds to let JS finish
        
        # Get the page content
        content = await page.content()
        
        await browser.close()
        return content