from pathlib import Path
import json
R=Path(__file__).resolve().parent.parent;V=R/'verification'
sources=['lighthouse-home.report.json','lighthouse-home-repeat.json','lighthouse-home-chrome153.json','lighthouse-153-no-typed.json','lighthouse-153-no-video.json','lighthouse-153-static-hero.json','lighthouse-153-contact.json']
runs=[]
for n in sources:
 p=json.loads((V/n).read_text(encoding='utf-8'));a=p['audits'];m=a['metrics'].get('details',{}).get('items',[{}])[0]
 runs.append({'file':n,'url':p['finalDisplayedUrl'],'fetchTime':p['fetchTime'],'lighthouse':p['lighthouseVersion'],'userAgent':p['userAgent'],'performance':p['categories']['performance']['score'],'lcpMs':a['largest-contentful-paint'].get('numericValue'),'lcpError':a['largest-contentful-paint'].get('errorMessage'),'fcpMs':a['first-contentful-paint'].get('numericValue'),'tbtMs':a['total-blocking-time'].get('numericValue'),'cls':a['cumulative-layout-shift'].get('numericValue'),'speedIndexMs':a['speed-index'].get('numericValue'),'observedLcpMs':m.get('observedLargestContentfulPaint'),'blockedUrlPatterns':p.get('configSettings',{}).get('blockedUrlPatterns',[]),'runtimeError':p.get('runtimeError')})
matrix={
 'SEC-01':('Potwierdzony problem konfiguracji','HTTP ponownie 200 bez przejścia na HTTPS.'),
 'MKT-01':('Do weryfikacji na kontach','Brak tagów w publicznym kodzie potwierdzony; brak skutecznego pomiaru nie został dowiedziony.'),
 'REG-01':('Różnica historyczna','6 zamiast 8 pozycji i brak dzieci Oferta potwierdzone. Zmiana względem maja, nie potwierdzona regresja z ostatniego tygodnia.'),
 'UX-01':('Potwierdzony błąd układu','320 px: client 305, scrollWidth 329; powtórzono w przeglądarce.'),
 'CODE-01':('Potwierdzony błąd treści','Duplikaty długich akapitów ponownie wykryte na trzech wskazanych stronach.'),
 'SEC-02':('Potwierdzone braki ochrony dodatkowej','Nagłówki nadal nieobecne; nie potwierdzono możliwego do wykorzystania ataku.'),
 'PERF-01':('Potwierdzony rozmiar i zachowanie','Film ma 8555220 B i autoplay; koszt oraz wpływ na biznes nie zostały zmierzone.'),
 'PERF-02':('Potwierdzony potencjał optymalizacji','Rozmiary oryginałów potwierdzone; nie każda wizyta pobiera te same oryginały.'),
 'SEO-01':('Potwierdzony brak metadanych','72/72 ponownie bez meta description. Nie dowodzi to spadku pozycji.'),
 'SEO-02':('Potwierdzona niespójność deklaracji','10/72 ponownie bez canonical. Nie potwierdzono błędnego wyboru URL przez Google.'),
 'UX-02':('Rekomendacja biznesowa','Brak formularza i CTA w treści badanej usługi potwierdzony; nie jest to awaria formularza.'),
 'A11Y-01':('Częściowo wymagał doprecyzowania','Brak sterowania pauzą i nieobsłużona animacja tekstu pozostają; CSS już ukrywa wideo przy prefers-reduced-motion.'),
 'PRIV-01':('Rekomendacja przeglądu','Zakres tekstu potwierdzony; nie przeprowadzono oceny zgodności prawnej i nie stwierdzono naruszenia.'),
 'REG-02':('Różnica / rekomendacja','Mobilny układ linków działa, lecz różni się od archiwalnego panelu. Brak hamburgera nie jest samodzielnym dowodem awarii.'),
 'REG-03':('Różnica / rekomendacja','Bieżąca typografia potwierdzona; stary wzorzec CSS niekompletny.'),
 'PSI-01':('Zaktualizowana diagnoza','PSI głównej NO_LCP, kontakt PSI 98; lokalny Lighthouse Chrome156: 73/75, Chrome153: NO_LCP. Przyczyna na poziomie konkretnej linii kodu nieustalona.'),
 'PSI-02':('Rekomendacja oparta na diagnostyce','Transfer i sygnały PSI potwierdzone; konkretny kontrast podmenu potwierdzony jako nowy UX-04.'),
 'UX-03':('Potwierdzona nieaktywna funkcja','Newsletter nadal jawnie disabled. Nie dowodzi utraty wysłanych zapisów.'),
 'CODE-02':('Obserwacja utrzymaniowa','Nadpisania CSS potwierdzone; konflikt kolorów menu pokazuje konkretny skutek.'),
 'SEO-03':('Rekomendacja porządkowa','Linki przekierowują prawidłowo; nie klasyfikować ich jako niedziałające.'),
 'SEO-04':('Potwierdzony brak JSON-LD / rekomendacja','0/72 JSON-LD; nie blokuje indeksowania.'),
 'UX-04':('Nowy potwierdzony błąd','Podmenu O nas: #fff na #fff przed scroll; #222 na #fff po scroll. Błąd konkretnej reguły CSS.')}
summary={'date':'2026-10-27','scope':{'html_pages':72,'assets_head':351,'all_page_recheck_statuses':200,'all_asset_recheck_statuses':200},'new_pagespeed':{'home':'https://pagespeed.web.dev/analysis/https-www-building4you-pl/hdu8rg4pxd?form_factor=mobile','contact':'https://pagespeed.web.dev/analysis/https-www-building4you-pl-kontakt/ub4l0psvu6?form_factor=mobile','contact_performance':98,'contact_lcp_s':1.6,'contact_tbt_ms':90},'local_runs':runs,'review':[{'id':k,'classification':a,'result':b} for k,(a,b) in matrix.items()]}
(V/'verification-summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print('Wrote verification summary:',len(runs),'runs;',len(matrix),'reviewed items')
