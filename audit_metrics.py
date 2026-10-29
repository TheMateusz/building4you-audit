import requests,json,re,hashlib
from pathlib import Path
from bs4 import BeautifulSoup
from collections import Counter
OUT=Path('dowody')
p=json.loads((OUT/'pages.json').read_text(encoding='utf-8'))+json.loads((OUT/'pages-secondary.json').read_text(encoding='utf-8'))
u={x['url']:x for x in p if x.get('status')==200 and x.get('title') and x['url'].startswith('https:')}
all_scripts=sorted({s for x in u.values() for s in x.get('scripts',[])})
old=json.loads((OUT/'code-assets.json').read_text(encoding='utf-8'))
known={x['url'] for x in old}
for s in all_scripts:
 if s not in known:
  r=requests.get(s,timeout=20); name=hashlib.sha256(s.encode()).hexdigest()[:12]+'.txt';(OUT/name).write_bytes(r.content)
  old.append({'url':s,'requested':s,'status':r.status_code,'headers':dict(r.headers),'bytes':len(r.content),'file':name})
(OUT/'all-code.json').write_text(json.dumps(old,ensure_ascii=False,indent=2),encoding='utf-8')
dup=[];track=[];policies=[]
for x in u.values():
 html=(OUT/x['file']).read_text(encoding='utf-8');s=BeautifulSoup(html,'html.parser')
 c=Counter(z.get_text(' ',strip=True) for z in s.select('main p') if len(z.get_text())>130)
 d=[{'paragraph':t,'count':n} for t,n in c.items() if n>1]
 if d:dup.append({'url':x['url'],'duplicates':d})
 m=re.findall(r'googletagmanager|google-analytics|gtag\s*\(|fbq\s*\(|connect\.facebook|GTM-[A-Z0-9]+|AW-\d+',html,re.I)
 if m:track.append({'url':x['url'],'matches':m})
 if s.select('meta[http-equiv="Content-Security-Policy" i]'):policies.append(x['url'])
for x in old:
 t=(OUT/x['file']).read_text(encoding='utf-8')
 m=re.findall(r'googletagmanager|google-analytics|gtag\s*\(|fbq\s*\(|connect\.facebook|GTM-[A-Z0-9]+|AW-\d+',t,re.I)
 if m:track.append({'url':x['url'],'matches':m})
metrics={'unique_https_pages':len(u),'missing_description':sum(not x.get('description') for x in u.values()),'missing_canonical':[x['url'] for x in u.values() if not x.get('canonical')],'jsonld_pages':sum(bool(x.get('jsonld')) for x in u.values()),'forms':sum(len(x.get('forms',[])) for x in u.values()),'tracking_patterns':track,'csp_meta':policies,'duplicate_paragraphs':dup,'scripts':all_scripts,'page_inventory':[{'url':x['url'],'status':x['status'],'title':x['title'],'file':x['file']} for x in u.values()]}
(OUT/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in metrics.items() if k not in ['page_inventory','duplicate_paragraphs']},ensure_ascii=False,indent=2))
print('DUPLICATE PAGES',[(x['url'],len(x['duplicates'])) for x in dup])

