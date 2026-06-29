import asyncio
from playwright.async_api import async_playwright

async def main():
    async with async_playwright() as p:
        browser = await p.chromium.launch()
        page = await browser.new_page(viewport={"width": 1536, "height": 730})
        await page.goto("http://localhost:3000/")
        await page.wait_for_timeout(2000)
        await page.screenshot(path=r"C:\Users\xsush\.gemini\antigravity-ide\brain\cc18e36b-3b97-4924-8f2b-8277494bdaae\screenshot.png")
        await browser.close()

asyncio.run(main())
