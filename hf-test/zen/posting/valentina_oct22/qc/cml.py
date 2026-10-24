from playwright.sync_api import sync_playwright
import sys
with sync_playwright() as p:
    b=p.chromium.launch(); pg=b.new_page(viewport={'width':1400,'height':1000})
    for name,url in [('cml_search','https://ads.tiktok.com/business/creativecenter/music/pc/en?searchKey=DIP%20ON%20EM'),('cml_trending','https://ads.tiktok.com/business/creativecenter/inspiration/popular/music/pc/en?countryCode=US&period=7&rank_type=commercial')]:
        try:
            pg.goto(url,timeout=45000); pg.wait_for_timeout(8000)
            pg.screenshot(path=name+'.png',full_page=False)
            open(name+'.txt','w').write(pg.inner_text('body')[:6000])
        except Exception as e: print(name,e)
    b.close()
