import sys,asyncio
from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(executable_path='/usr/bin/google-chrome',headless=True,args=['--no-sandbox'])
    pg=b.new_page(viewport={'width':1100,'height':1400},user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/130.0 Safari/537.36')
    for url,out in zip(sys.argv[1::2],sys.argv[2::2]):
        pg.goto(url,wait_until='domcontentloaded',timeout=45000); pg.wait_for_timeout(4000)
        pg.screenshot(path=out,full_page=True); open(out+'.txt','w').write(pg.inner_text('body'))
        print(out,pg.title())
    b.close()
