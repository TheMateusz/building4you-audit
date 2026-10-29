from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from urllib.parse import urljoin
from collections import Counter
from bs4 import BeautifulSoup
import requests,json,re,hashlib,time
R=Path(__file__).parent;O=R/'verification';O.mkdir(exist_ok=True)
m=json.loads((R/'dowody/metrics.json').read_text(encoding='utf-8'))
def get(u):
 try:
  r=requests.get(u,timeout=20);name=hashlib.sha256(u.encode()).hexdigest()[:12]+'.html';(O/name).write_bytes(r.content);s=BeautifulSoup(r.content,'html.parser')
  paragraphs=Counter(x.get_text(' ',strip=True) for x in s.select('main p') if len(x.get_text())>130)
  return {'requested':u,'url':r.url,'status':r.status_code,'headers':dict(r.headers),'redirects':[{'url':x.url,'status':x.status_code,'location':x.headers.get('Location')} for x in r.history],'file':name,'sha256':hashlib.sha256(r.content).hexdigest(),'description':[x.get('content') for x in s.select('meta[name="description"]')],'canonical':[x.get('href') for x in s.select('link[rel="canonical"]')],'jsonld':len(s.select('script[type="application/ld+json"]')),'forms':len(s.select('form')),'duplicates':[(p,c) for p,c in paragraphs.items() if c>1],'disabled':[(x.name,x.get('type'),x.get('aria-label'),x.get_text(strip=True)) for x in s.select('[disabled]')],'tracking':re.findall(r'googletagmanager|google-analytics|gtag\s*\(|fbq\s*\(|connect\.facebook',r.text,re.I),'main_cta':[{'text':x.get_text(' ',strip=True),'href':x.get('href')} for x in s.select('main a[href]') if any(t in x.get('href','') for t in ['kontakt','tel:','mailto:','wycena'])]}
 except Exception as e:return {'requested':u,'error':str(e)}
urls=[x['url'] for x in m['page_inventory']]+['http://www.building4you.pl/','http://building4you.pl/','https://building4you.pl/']
with ThreadPoolExecutor(max_workers=3) as ex:p=list(ex.map(get,urls))
(O/'pages-recheck.json').write_text(json.dumps(p,ensure_ascii=False,indent=2),encoding='utf-8')
assets=json.loads((R/'dowody/resources.json').read_text(encoding='utf-8'))
def head(x):
 try:
  r=requests.head(x['url'],timeout=15,allow_redirects=True);return {'url':x['url'],'status':r.status_code,'headers':dict(r.headers)}
 except Exception as e:return {'url':x['url'],'error':str(e)}
with ThreadPoolExecutor(max_workers=3) as ex:a=list(ex.map(head,assets))
(O/'assets-recheck.json').write_text(json.dumps(a,ensure_ascii=False,indent=2),encoding='utf-8')
print('PAGES',Counter(x.get('status') for x in p),'ASSETS',Counter(x.get('status') for x in a))
print('DESCRIPTIONS',sum(bool(x.get('description')) for x in p[:72]),'CANONICAL MISSING',sum(not x.get('canonical') for x in p[:72]),'JSONLD',sum(x.get('jsonld',0) for x in p[:72]))
print('DUPLICATES',[(x['url'],len(x['duplicates'])) for x in p if x.get('duplicates')]);print('TRACKING',[(x['url'],x['tracking']) for x in p if x.get('tracking')])
