from pathlib import Path
from urllib.parse import urljoin, urlsplit, urldefrag
from concurrent.futures import ThreadPoolExecutor
import requests, json, time, re, hashlib
from bs4 import BeautifulSoup

ROOT=Path(__file__).parent
OUT=ROOT/'dowody'; OUT.mkdir(exist_ok=True)
BASE='https://www.building4you.pl/'
def fetch(url, head=False):
    start=time.perf_counter()
    try:
        r=requests.request('HEAD' if head else 'GET',url,timeout=20,allow_redirects=True,headers={'User-Agent':'B4U-Public-Audit/1.0 (read-only)'})
        item={'requested':url,'url':r.url,'status':r.status_code,'seconds':round(time.perf_counter()-start,3),'headers':dict(r.headers),'redirects':[{'status':x.status_code,'url':x.url,'location':x.headers.get('Location')} for x in r.history]}
        if not head:
            r.encoding=r.encoding or 'utf-8'
            item['bytes']=len(r.content)
            name=hashlib.sha256(url.encode()).hexdigest()[:12]
            (OUT/(name+'.txt')).write_text(r.text,encoding='utf-8')
            item['file']=name+'.txt'
            if 'text/html' in r.headers.get('Content-Type',''):
                s=BeautifulSoup(r.content,'html.parser')
                item.update(title=s.title.get_text(' ',strip=True) if s.title else '',description=[x.get('content') for x in s.select('meta[name="description"]')],canonical=[x.get('href') for x in s.select('link[rel="canonical"]')],robots=[x.get('content') for x in s.select('meta[name="robots"]')],h1=[x.get_text(' ',strip=True) for x in s.select('h1')],headings=[(x.name,x.get_text(' ',strip=True)) for x in s.select('h1,h2,h3,h4')],links=[{'url':urljoin(r.url,x.get('href','')),'text':x.get_text(' ',strip=True)} for x in s.select('a[href]')],scripts=[urljoin(r.url,x['src']) for x in s.select('script[src]')],styles=[urljoin(r.url,x['href']) for x in s.select('link[rel="stylesheet"]')],images=[dict(x.attrs) for x in s.select('img')],forms=[str(x) for x in s.select('form')],iframes=[dict(x.attrs) for x in s.select('iframe')],text=s.get_text(' ',strip=True),jsonld=[x.get_text() for x in s.select('script[type="application/ld+json"]')])
        return item
    except Exception as e:return {'requested':url,'error':str(e)}

home=fetch(BASE)
links=[]
for a in home.get('links',[]):
    u=urldefrag(a['url'])[0]
    if urlsplit(u).netloc=='www.building4you.pl' and u not in links and not re.search(r'\.(pdf|jpe?g|png|mp4|webp)$',u,re.I):links.append(u)
urls=list(dict.fromkeys([BASE]+links+['http://www.building4you.pl/','http://building4you.pl/','https://building4you.pl/','https://www.building4you.pl/robots.txt','https://www.building4you.pl/wp-sitemap.xml','https://www.building4you.pl/sitemap_index.xml','https://www.building4you.pl/audyt-nieistniejaca-strona-20261027/']))
with ThreadPoolExecutor(max_workers=3) as ex: results=list(ex.map(fetch,urls))
(OUT/'pages.json').write_text(json.dumps(results,ensure_ascii=False,indent=2),encoding='utf-8')
assets=list(dict.fromkeys(home.get('scripts',[])+home.get('styles',[])))
with ThreadPoolExecutor(max_workers=3) as ex: ar=list(ex.map(fetch,assets))
(OUT/'code-assets.json').write_text(json.dumps(ar,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps([{'url':x.get('requested'),'final':x.get('url'),'status':x.get('status'),'title':x.get('title'),'h1':x.get('h1'),'desc':x.get('description'),'canonical':x.get('canonical'),'forms':len(x.get('forms',[])),'error':x.get('error')} for x in results],ensure_ascii=False,indent=2))
