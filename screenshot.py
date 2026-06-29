import asyncio
import os
from playwright.async_api import async_playwright

async def take_screenshots():
    out_dir = r"x:\Sentrix\screenshots"
    os.makedirs(out_dir, exist_ok=True)
    
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        context = await browser.new_context(viewport={"width": 1536, "height": 864})
        page = await context.new_page()
        
        try:
            print("Navigating to login page...")
            await page.goto("http://localhost:3000/login")
            await page.wait_for_timeout(2000)
            
            print("Logging in...")
            await page.fill('input[type="text"]', 'admin@sentrix.local')
            await page.fill('input[type="password"]', 'admin')
            await page.click('button[type="submit"]')
            await page.wait_for_timeout(3000)
            
            routes = {
                "dashboard": "/",
                "alerts": "/alerts",
                "cases": "/cases",
                "threat-intelligence": "/threat-intel",
                "malware-analysis": "/malware",
                "threat-hunting": "/threat-hunting",
                "soar": "/soar",
                "reports": "/reports"
            }
            
            for name, route in routes.items():
                print(f"Capturing {name}...")
                await page.goto(f"http://localhost:3000{route}")
                await page.wait_for_timeout(3000)
                await page.screenshot(path=os.path.join(out_dir, f"{name}.png"))
                
        except Exception as e:
            print(f"Error: {e}")
        finally:
            await browser.close()

if __name__ == "__main__":
    asyncio.run(take_screenshots())
