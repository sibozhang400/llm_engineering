"""
Quick test script to verify the Playwright scraper works
"""
import asyncio
from scraper_new import scrape_website

async def main():
    print("Testing Playwright scraper with headless=False...")
    print("A browser window will appear - this is normal!\n")
    
    url = "https://www.coles.com.au/"
    
    try:
        content = await scrape_website(url, headless=False)
        print(f"✅ Successfully scraped {len(content)} characters")
        print(f"\nFirst 500 characters:")
        print(content[:500])
        print("\n" + "="*60)
        
        # Check if we got blocked
        if "Incapsula" in content or "Request unsuccessful" in content:
            print("❌ Still blocked by Incapsula")
            return False
        else:
            print("✅ No Incapsula block detected!")
            
            # Check for Coles-specific content
            if "coles" in content.lower() and ("special" in content.lower() or "price" in content.lower()):
                print("✅ Looks like we got real Coles content!")
                return True
            else:
                print("⚠️  Got content but might not be the full page")
                return False
                
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

if __name__ == "__main__":
    asyncio.run(main())
