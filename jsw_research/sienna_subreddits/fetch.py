import asyncio,sys
from playwright.async_api import async_playwright
subs=sys.argv[1:]
async def main():
  async with async_playwright() as p:
    b=await p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=False,args=['--no-sandbox'])
    pg=await b.new_page()
    for s in subs:
      for kind,url in [('rules',f'https://www.reddit.com/r/{s}/about/rules.json'),('about',f'https://www.reddit.com/r/{s}/about.json')]:
        try:
          r=await pg.goto(url,timeout=30000); t=await r.text()
        except Exception as e: t='ERR '+str(e)
        open(f'raw_{s}_{kind}.json','w').write(t); print(s,kind,t[:80].replace('\n',' '))
        await asyncio.sleep(2)
    await b.close()
asyncio.run(main())
