from playwright.sync_api import sync_playwright
with sync_playwright() as p:
    b=p.chromium.launch(args=['--disable-dev-shm-usage']); pg=b.new_page(viewport={'width':1200,'height':1600})
    for s in ['aiArt','AIGirls','AIfashion','aiportraits']:
        try:
            pg.goto(f'https://www.reddit.com/r/{s}/about/rules/',timeout=45000); pg.wait_for_timeout(6000)
            pg.screenshot(path=f'{s}_rules.png',full_page=True)
            open(f'{s}_rules.txt','w').write(pg.inner_text('body')[:8000])
        except Exception as e: print(s,e)
    b.close()
