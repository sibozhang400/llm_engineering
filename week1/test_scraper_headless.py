"""
Test script to check if headless mode works with stealth
"""
import asyncio
from scraper_new import scrape_website

async def main():
    print("Testing Playwright scraper with headless=True (stealth mode)...")
    print("This runs in the background without showing a browser window.\n")
    
    url = "https://www.coles.com.au/"
    
    try:
        content = await scrape_website(url, headless=True)
        print(f"✅ Successfully scraped {len(content)} characters")
        print(f"\nFirst 500 characters:")
        print(content[:500])
        print("\n" + "="*60)
        
        # Check if we got blocked
        if "Incapsula" in content or "Request unsuccessful" in content:
            print("❌ Blocked by Incapsula with headless=True")
            print("   Recommendation: Use headless=False instead")
            return False
        else:
            print("✅ No Incapsula block detected!")
            
            # Check for Coles-specific content
            if "coles" in content.lower() and ("special" in content.lower() or "price" in content.lower()):
                print("✅ Headless mode works! You can use headless=True")
                return True
            else:
                print("⚠️  Got content but might not be the full page")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(main())
