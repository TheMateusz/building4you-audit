import requests,json,re,time,hashlib,ssl,socket
from pathlib import Path
from bs4 import BeautifulSoup
from urllib.parse import urlsplit,urljoin,urldefrag
from concurrent.futures import ThreadPoolExecutor
OUT=Path('dowody'); pages=json.loads((OUT/'pages.json').read_text(encoding='utf-8'))
known={x.get('requested') for x in pages}|{x.get('url') for x in pages}
links=list(dict.fromkeys(urldefrag(a['url'])[0] for x in pages for a in x.get('links',[]) if urlsplit(a['url']).netloc=='www.building4you.pl' and not re.search(r'\.(?:jpe?g|png|pdf|svg|webp)$',urlsplit(a['url']).path,re.I)))
new=[u for u in links if u not in known][:70]
def get(u):
 try:
  t=time.perf_counter();r=requests.get(u,timeout=20);s=BeautifulSoup(r.content,'html.parser'); name=hashlib.sha256(u.encode()).hexdigest()[:12]+'.txt';(OUT/name).write_bytes(r.content)
  return {'requested':u,'url':r.url,'status':r.status_code,'headers':dict(r.headers),'seconds':round(time.perf_counter()-t,3),'bytes':len(r.content),'file':name,'title':s.title.get_text(' ',strip=True) if s.title else '', 'description':[x.get('content') for x in s.select('meta[name="description"]')],'canonical':[x.get('href') for x in s.select('link[rel="canonical"]')],'h1':[x.get_text(' ',strip=True) for x in s.select('h1')],'images':[dict(x.attrs) for x in s.select('img')],'scripts':[urljoin(r.url,x['src']) for x in s.select('script[src]')],'styles':[urljoin(r.url,x['href']) for x in s.select('link[rel="stylesheet"]')],'links':[{'url':urljoin(r.url,x.get('href','')),'text':x.get_text(' ',strip=True)} for x in s.select('a[href]')],'text':s.get_text(' ',strip=True),'forms':[str(x) for x in s.select('form')],'iframes':[dict(x.attrs) for x in s.select('iframe')],'jsonld':[x.get_text() for x in s.select('script[type="application/ld+json"]')]}
 except Exception as e:return {'requested':u,'error':str(e)}
with ThreadPoolExecutor(max_workers=3) as ex: second=list(ex.map(get,new))
(OUT/'pages-secondary.json').write_text(json.dumps(second,ensure_ascii=False,indent=2),encoding='utf-8')
allpages=pages+second
assets=[]
for p in allpages:
 if p.get('status')!=200 or not p.get('title'):continue
 for i in p.get('images',[]):
  if i.get('src') and not i['src'].startswith('data:'): assets.append(urljoin(p['url'],i['src']))
 assets+=p.get('scripts',[])+p.get('styles',[])
# HEAD only: inspect presence, types and declared sizes without downloading full galleries/video.
assets=list(dict.fromkeys(assets))
assets=assets[:350]
assets.append('https://www.building4you.pl/wp-content/themes/building4you-wp/b4y-home/movie_720.mp4')
def head(u):
 try:
  r=requests.head(u,timeout=15,allow_redirects=True)
  return {'url':u,'final':r.url,'status':r.status_code,'headers':dict(r.headers)}
 except Exception as e:return {'url':u,'error':str(e)}
with ThreadPoolExecutor(max_workers=3) as ex: ar=list(ex.map(head,assets))
(OUT/'resources.json').write_text(json.dumps(ar,ensure_ascii=False,indent=2),encoding='utf-8')
try:
 ctx=ssl.create_default_context()
 with socket.create_connection(('www.building4you.pl',443),timeout=15) as sock:
  with ctx.wrap_socket(sock,server_hostname='www.building4you.pl') as ss:
   tls={'version':ss.version(),'cipher':ss.cipher(),'certificate':ss.getpeercert()}
 (OUT/'tls.json').write_text(json.dumps(tls,indent=2),encoding='utf-8')
except Exception as e:(OUT/'tls.json').write_text(json.dumps({'error':str(e)}),encoding='utf-8')
print('SECONDARY',len(second),'ASSETS',len(ar),'NON200',[(x['url'],x.get('status')) for x in ar if x.get('status')!=200])
