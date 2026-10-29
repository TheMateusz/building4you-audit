from pathlib import Path
from concurrent.futures import ThreadPoolExecutor
from bs4 import BeautifulSoup
import requests,json,hashlib,re
P=Path('porownanie');P.mkdir(exist_ok=True)
urls=json.loads((P/'archive-css-urls.json').read_text())
def get(u):
 a='https://web.archive.org/web/20260513010843id_/'+u
 try:
  r=requests.get(a,timeout=25);fn='archive-'+hashlib.sha256(u.encode()).hexdigest()[:10]+'.css';(P/fn).write_bytes(r.content)
  return {'original':u,'requested':a,'final':r.url,'status':r.status_code,'type':r.headers.get('Content-Type'),'bytes':len(r.content),'file':fn}
 except Exception as e:return {'original':u,'error':str(e)}
with ThreadPoolExecutor(max_workers=3) as ex:r=list(ex.map(get,urls))
(P/'archive-css-results.json').write_text(json.dumps(r,indent=2),encoding='utf-8')
print(json.dumps(r,indent=2))
