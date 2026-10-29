from pathlib import Path
import sys
from bs4 import BeautifulSoup
import json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from pypdf import PdfReader,PdfWriter

R=Path(__file__).parent; P=R/'porownanie'; O=R/'output'/'pdf'
for name,file in [('PL','arial.ttf'),('PLB','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('PL',normal='PL',bold='PLB',italic='PL',boldItalic='PLB')
navy=colors.HexColor('#16263d');red=colors.HexColor('#b9213b')
S={k:ParagraphStyle(k,fontName='PLB' if k.startswith('h') else 'PL',fontSize=size,leading=leading,textColor=navy,spaceAfter=space) for k,size,leading,space in [('body',9.5,14,9),('small',8,11,7),('h1',23,28,17),('h2',13,18,10)]}
def text(t,k='body'):return Paragraph(html.escape(t.replace('–','-').replace('—','-')),S[k])
story=[]
def add(t,k='body'):story.append(text(t,k))
def page():story.append(PageBreak())
def table(rows,widths):
 t=Table([[text(str(c),'small') for c in row] for row in rows],colWidths=widths,repeatRows=1,hAlign='LEFT')
 t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),colors.HexColor('#eef2f6')),('LINEBELOW',(0,0),(-1,0),.8,navy),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#dce2e9')),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8)]));story.append(t)

old=BeautifulSoup((R/'archive-home-20260513.html').read_text(encoding='utf-8'),'html.parser')
new=BeautifulSoup((R/'home.html').read_text(encoding='utf-8'),'html.parser')
oldnav=[x.find('a').get_text(' ',strip=True) for x in old.select('#dj-megamenu175 > li')]
newnav=[x.find('a').get_text(' ',strip=True) for x in new.select('header nav > ul > li')]
diff={'archive_timestamp':'20260513010843','archive_url':'https://web.archive.org/web/20260513010843/https://www.building4you.pl/','old_menu':oldnav,'new_menu':newnav,'old_offer_children':len(old.select('#dj-megamenu175 > li.itemid305 .dj-submenu > li')),'new_offer_children':len(new.select('header nav > ul > li:nth-child(4) li')),'old_mobile_toggle':bool(old.select('.dj-mobile-open-btn')),'new_mobile_toggle':bool(new.select('header button,[aria-label="Open mobile menu"]')),'old_description':bool(old.select('meta[name="description"]')),'new_description':bool(new.select('meta[name="description"]')),'old_analytics_script':[x['src'] for x in old.select('script[src]') if 'googletagmanager' in x['src']]}
(P/'comparison.json').write_text(json.dumps(diff,ensure_ascii=False,indent=2),encoding='utf-8')
speeds=[{'run':'A','device':'Telefon','FCP':'1,2 s','LCP':'NO_LCP','TBT':'NO_LCP','CLS':'0,054','SI':'2,4 s','payload_kib':10524,'performance':None,'accessibility':96,'best_practices':100,'seo':92}, {'run':'A','device':'Komputer','FCP':'0,3 s','LCP':'NO_LCP','TBT':'NO_LCP','CLS':'0,081','SI':'0,3 s','payload_kib':10621,'performance':None,'accessibility':96,'best_practices':100,'seo':92}, {'run':'B','device':'Telefon','FCP':'1,2 s','LCP':'NO_LCP','TBT':'NO_LCP','CLS':'0,070','SI':'1,2 s','payload_kib':9239,'performance':None,'accessibility':96,'best_practices':100,'seo':92}, {'run':'B','device':'Komputer','FCP':'0,3 s','LCP':'NO_LCP','TBT':'NO_LCP','CLS':'0,081','SI':'0,4 s','payload_kib':10621,'performance':None,'accessibility':96,'best_practices':100,'seo':92}]
(P/'pagespeed-summary.json').write_text(json.dumps(speeds,ensure_ascii=False,indent=2),encoding='utf-8')
add('BUILDING4YOU.PL | AKTUALIZACJA AUDYTU','small')
add('Porównanie archiwalne i PageSpeed','h1')
add('27 października 2026 | Wersja zbiorcza 1.1','small')
add('Wniosek: struktura i mechanizm menu zostały zmienione','h2')
add('Potwierdzam różnice wykraczające poza sam wygląd: dawny nagłówek Joomla/DJ-MegaMenu został zastąpiony nagłówkiem motywu WordPress. Obecnie brakuje dwóch głównych pozycji menu i podmenu oferty. Na telefonie zamiast panelu otwieranego przyciskiem są stale widoczne linki zawijane do dwóch rzędów. To wyjaśnia część wrażenia, że menu i style się rozsypały.')
add('Nie można ustalić z publicznego archiwum, czy zmiany były zamierzone, kiedy dokładnie je wdrożono ani kto je wprowadził. Wniosek o niepełnym odtworzeniu dawnej nawigacji jest hipotezą opartą na różnicach HTML i CSS; wymaga porównania ze specyfikacją migracji.','small')
add('Jaką datę porównano','h2')
add('Warunek: wersja z 20.10.2026 lub wcześniejsza, czyli co najmniej tydzień przed badaniem. W zapytaniu CDX dla strony głównej najnowsza znaleziona poprawna kopia sprzed tej daty pochodzi z 13.05.2026, godz. 01:08:43 UTC. Nie znaleziono kopii z dokładnie poprzedniego tygodnia. Porównanie obejmuje 13.05.2026 i stan z 27.10.2026.')
add('Po doprecyzowaniu limitu do miesiąca sprawdzono 27.09-20.10.2026. Wayback CDX dla całej domeny zwrócił pustą listę. Common Crawl, indeks październikowy z 5-18.10, nie znalazł kopii www.building4you.pl/; szersze zapytanie domenowe zwróciło 504. Archive.today zwróciło 429. Nie znaleziono publicznej kopii spełniającej ten warunek. Kopia majowa go nie spełnia i służy wyłącznie jako starszy punkt odniesienia.','small')
add('Zastrzeżenie odtwarzania archiwum','h2')
add('Archiwalny HTML jest dostępny, ale kluczowy plik A.custom.css...wUmjz9RfMQ.css zwraca w archiwum 404. Inne arkusze pod tymi samymi adresami są odtwarzane z kopii z 2023 r. Z tego powodu nie traktuję zrzutu archiwum jako wiernego obrazu dawnej strony i nie wykonuję pozornego porównania piksel w piksel. Potwierdzone różnice pochodzą przede wszystkim z HTML i zachowanych reguł CSS.')
add('Aktualizacja poprzedniego raportu','h2')
add('Niniejsza część aktualizuje wcześniejszą informację o braku wyników PageSpeed. API nadal zwracało 429, ale interfejs PageSpeed Insights wykonał dwa przebiegi dla telefonu i komputera. Nie uzyskano pełnej oceny wydajności, ponieważ oba przebiegi zwróciły NO_LCP. Raport pierwotny pozostaje dalej w pakiecie jako część bazowa z 16 ustaleniami.')
page()
add('Co zmieniło się w menu','h1')
table([['Element','Archiwum 13.05.2026','Obecnie 27.10.2026'],['Technologia','Generator Joomla; menu DJ-MegaMenu, skrypty desktop/mobile.','WordPress; HTML .b4y-header / .b4y-menu.'],['Pozycje główne','8: O nas, Realizacje, Aktualności, Oferta, Szybka Wycena, Kontakt, Blog, Rekrutacja.','6: O nas, Realizacje, Aktualności, Oferta, Blog, Kontakt.'],['Wycena i rekrutacja','Bezpośrednie pozycje menu. Szybka wycena ma klasę kontakt-red.','Obie pozycje zniknęły z głównego menu. Odnośnik dawnej wyceny prowadzi obecnie do kontaktu.'],['Podmenu Oferta','9 odnośników do usług w układzie wielokolumnowym.','Brak dzieci pozycji Oferta. Lista usług istnieje gdzie indziej, ale nie jako podmenu nagłówka.'],['Telefon','W HTML jest przycisk otwarcia i zamknięcia panelu offcanvas, podmenu i obsługa mobilna.','Brak takiego przycisku/panelu. Przy 390 px linki są w 2 rzędach; nagłówek ma ok. 155 px.'],['Języki i social w nagłówku','W HTML PL/EN i linki społecznościowe.','Nie ma ich w obecnym nagłówku; social nadal są w stopce.'],['Typografia','Zachowany arkusz DJ deklaruje proxima_nova_condensedSBd, 16 px. Uwaga: kopia arkusza jest z 2023 r.','Pomiar computed style: Arial/Helvetica/sans-serif, 12 px, font-weight 750.'],['Rozmiary i odstępy','Arkusz DJ zawiera inne paddingi, wysokości i pozycje dropdownów. Brak kompletnego custom.css uniemożliwia pełną rekonstrukcję.','W głównych linkach padding 17 px 14 px; inny layout flex, szerokości i breakpointy.']],[78,207,210])
add('Zmiana fontu i struktury HTML jest potwierdzona. Nie ma podstaw, by sprowadzić naprawę do ponownego wczytania jednego arkusza. Trzeba ustalić docelowe funkcje menu i odtworzyć je w obecnej technologii.','small')
page()
add('Obecne menu na telefonie','h1')
add('Widok z 27.10.2026, viewport 390 x 844 px. Linki pozostają na ekranie i zawijają się do dwóch rzędów. W dawnym HTML w tym miejscu przewidziano osobny przycisk menu oraz panel offcanvas.','body')
story.append(Image(str(P/'current-mobile.png'),width=205,height=461))
add('Różnice powiązane z migracją','h2')
add('Strona archiwalna zawierała meta description i metadane Open Graph; obecna strona główna nie zawiera meta description. To potwierdza regresję tego elementu SEO. W archiwum jest też formularz AcyMailing z checkboxem i przyciskiem, podczas gdy obecny newsletter ma disabled. Nie testowano, czy historyczny formularz rzeczywiście dostarczał zapisy.')
add('Archiwalny HTML zawiera wywołanie gtag z identyfikatorem UA-152616077-1; w obecnej próbce integracji nie wykryto. Historyczna obecność kodu nie potwierdza dawnego skutecznego pomiaru i nie uzasadnia przywracania starego identyfikatora zamiast zaprojektowania aktualnego pomiaru.','small')
page()
add('PageSpeed Insights: wyniki','h1')
add('Przebieg A: 27.10.2026, 11:06 CET. Przebieg B: 11:08 CET. Strona główna HTTPS, Lighthouse 13.5.0; telefon emulowany jako Moto G Power z ograniczeniem 4G. Oba przebiegi wykonane przez publiczny interfejs Google. API: 429, niezależnie od wyników interfejsu.','small')
table([['Kategoria','Telefon A / B','Komputer A / B'],['Wydajność','Brak wyniku: NO_LCP','Brak wyniku: NO_LCP'],['Dostępność','96 / 96','96 / 96'],['Sprawdzone metody','100 / 100','100 / 100'],['SEO','92 / 92','92 / 92'],['Dane użytkowników CrUX','Brak danych','Brak danych']],[165,165,165])
story.append(Spacer(1,12))
table([['Metryka','Telefon A','Telefon B','Komputer A','Komputer B'],['FCP','1,2 s','1,2 s','0,3 s','0,3 s'],['LCP','NO_LCP','NO_LCP','NO_LCP','NO_LCP'],['TBT','NO_LCP','NO_LCP','NO_LCP','NO_LCP'],['CLS','0,054','0,070','0,081','0,081'],['Speed Index','2,4 s','1,2 s','0,3 s','0,4 s'],['Ładunek sieciowy','10 524 KiB','9 239 KiB','10 621 KiB','10 621 KiB']],[115,95,95,95,95])
add('Jak interpretować wynik','h2')
add('To nie jest wynik wydajności 0/100 ani 100/100. Lighthouse nie wyznaczył LCP i wynikających z niego elementów oceny. Błędy NO_LCP powtórzyły się na obu profilach i w drugim przebiegu. Przyczyna nie została rozstrzygnięta. Wymaga kontroli śladu renderowania i konfiguracji strony/testu; nie można automatycznie uznać tego za awarię strony u wszystkich użytkowników.')
add('FCP i Speed Index nie zastępują LCP. CLS jest pojedynczym pomiarem laboratoryjnym, a nie potwierdzeniem zaliczenia terenowych Core Web Vitals. Wynik 100 za sprawdzone metody nie jest certyfikatem bezpieczeństwa i nie unieważnia ustaleń o HTTP oraz nagłówkach zabezpieczających.')
page()
add('Co wykazał PageSpeed i co naprawić','h1')
add('Potwierdzone sygnały z testu','h2')
for t in ['Duży transfer strony głównej: 9 239-10 621 KiB, czyli ok. 9,0-10,4 MiB. W pierwszym mobilnym przebiegu oszacowano 1 781 KiB możliwej redukcji obrazów, w powtórnym 459 KiB; na komputerze 1 610 KiB. Rozrzut potwierdza zmienność badania, a nie stałą gwarantowaną oszczędność.', 'Brak metaopisu został ponownie wskazany przez Google. To jest zgodne z własną analizą HTML i różnicą względem archiwum.', 'Test wskazuje niewystarczający kontrast oraz obrazy bez jawnych width/height. Dokładne elementy wymagają kontroli szczegółów audytu i testu ręcznego. Nie wszystkie pozycje widoczne w sekcji dostępności są automatycznie błędami.', 'Lighthouse sygnalizuje możliwości poprawy cache, blokowanie renderowania i wyświetlanie fontów. Audyty minifikacji, nieużywanego kodu i długich zadań mają błąd pomiaru - nie należy ich przepisywać jako potwierdzonych wad kodu.']:
 add('• '+t)
add('Dodatkowe zadania według priorytetu','h2')
table([['ID / priorytet','Zadanie i odbiór'],['REG-01 / P1*','Uzgodnić i przywrócić brakujące funkcje nagłówka: CTA wyceny, ewentualną rekrutację i podmenu usług. P1, jeśli zmiany były niezamierzone lub ograniczają pozyskiwanie zapytań. Odbiór: zgodna lista linków i właściwe cele.'],['REG-02 / P2','Odtworzyć mobilną nawigację z przyciskiem i panelem, obsługą dotyku, klawiatury i aria-expanded. Odbiór: 320/390/768 px, bez nakładania na treść i utraty linków.'],['REG-03 / P2','Ujednolicić fonty, odstępy i breakpointy na podstawie projektu lub kopii źródłowej. Nie kopiować w ciemno starego pluginu Joomla do WordPressa. Odbiór: zaakceptowane widoki desktop i mobile.'],['PSI-01 / P2','Wyjaśnić powtarzalne NO_LCP na środowisku testowym i uzyskać kompletny pomiar. Porównać wariant statycznego hero i wyłączone animacje wyłącznie testowo. Odbiór: pełne LCP/TBT i powtarzalny wynik.'],['PSI-02 / P2','Rozszerzyć PERF-01/02 i A11Y-01 o transfer, kontrast oraz wymiary obrazów wskazane przez PSI. Odbiór: mniejszy zmierzony transfer, naprawione wskazane kontrasty i ponowny pomiar.']],[105,390])
page()
add('Źródła i sposób odtworzenia','h1')
refs=[('Archiwum strony głównej, 13.05.2026','https://web.archive.org/web/20260513010843/https://www.building4you.pl/'),('PageSpeed, przebieg A - telefon','https://pagespeed.web.dev/analysis/https-www-building4you-pl/cwhaza3pkp?form_factor=mobile'),('PageSpeed, przebieg A - komputer','https://pagespeed.web.dev/analysis/https-www-building4you-pl/cwhaza3pkp?form_factor=desktop'),('PageSpeed, przebieg B - telefon','https://pagespeed.web.dev/analysis/https-www-building4you-pl/uesitxr2mj?form_factor=mobile'),('PageSpeed, przebieg B - komputer','https://pagespeed.web.dev/analysis/https-www-building4you-pl/uesitxr2mj?form_factor=desktop')]
for title,url in refs:
 story.append(Paragraph('<b>'+html.escape(title)+'</b><br/><link href="'+url+'" color="#245c96">'+url+'</link>',S['small']))
add('Dowody lokalne','h2')
for t in ['archive-latest.json: osiem ostatnich znalezionych zapisów strony głównej do 20.10.2026; archive-index.json: zapis wybranych kopii 2026.', 'archive-home-20260513.html: surowy HTML. porownanie/archive-css-results.json: statusy i rzeczywiste daty kopii CSS, w tym brak custom.css.', 'porownanie/comparison.json oraz current-header-desktop.json i current-header-mobile.json: różnice struktury oraz pomiar bieżących styli.', 'porownanie/pagespeed-*-dom.txt: zapis publicznego wyniku obu przebiegów i profili. pagespeed-summary.json: tabela wyników. Zrzuty pagespeed-mobile.png i pagespeed-desktop.png: stan interfejsu z przebiegu A.']:
 add('• '+t)
add('Poszukiwanie bliższej kopii: porownanie/archive-domain-recent.json, availability-20261020.json, commoncrawl-oct2026-home.jsonl i commoncrawl-collections.json. Wynik negatywny dotyczy sprawdzonych publicznych źródeł, nie prywatnych kopii hostingu.','small')
add('Zalecana kolejność','h2')
add('Zachować priorytet SEC-01 z raportu bazowego. Następnie uzgodnić docelowe funkcje menu i przywrócić utracone elementy, naprawić mobilny nagłówek i typografię, a równolegle wyjaśnić NO_LCP. Potem ograniczyć multimedia i przeprowadzić kontrolę porównawczą. Pełny wzorzec wyglądu najlepiej odtworzyć z kopii źródeł sprzed migracji; publiczne archiwum jest niekompletne.')
add('Porównanie nie zawiera wdrożonych zmian na stronie. Nie wykonano wysyłek formularzy ani testów starych formularzy archiwalnych. Nie sporządzano porównania szybkości obecnej strony z serwerem archiwum, ponieważ mierzyłoby ono również infrastrukturę Wayback Machine.','small')

def footer(c,d):
 c.saveState();w,h=A4;c.setStrokeColor(red);c.setLineWidth(2);c.line(50,h-36,w-50,h-36);c.setFont('PL',7);c.setFillColor(navy);c.drawString(50,27,'BUILDING4YOU.PL | Archiwum + PageSpeed | 27.10.2026 | v1.1');c.drawRightString(w-50,27,str(d.page));c.restoreState()
supp=O/'Building4you-porownanie-archiwum-PageSpeed-2026-10-27.pdf'
SimpleDocTemplate(str(supp),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=54,bottomMargin=48,title='Building4you - archiwum i PageSpeed',author='Audyt zewnętrzny').build(story,onFirstPage=footer,onLaterPages=footer)
full=O/'Building4you-audyt-2026-10-27-v1.1.pdf'
writer=PdfWriter();writer.append(str(supp),outline_item='Aktualizacja: archiwum i PageSpeed');writer.append(str(O/'Building4you-audyt-2026-10-27.pdf'),outline_item='Raport bazowy: 16 ustaleń');writer.add_metadata({'/Title':'Building4you - raport techniczny z porównaniem archiwalnym i PageSpeed - v1.1'});writer.write(str(full))

md=['# Building4you - uzupełnienie: archiwum i PageSpeed','27.10.2026. Najnowsza znaleziona kopia sprzed 20.10: 13.05.2026. Brak kompletnego CSS archiwum, bez porównania piksel w piksel.','', '## Menu','Dawniej: '+', '.join(oldnav)+'.','Obecnie: '+', '.join(newnav)+'.','Podmenu oferty: 9 odnośników -> 0. Mobilny panel offcanvas -> linki w dwóch rzędach. Obecna typografia menu: Arial 12 px; zachowany archiwalny CSS deklaruje Proxima Nova Condensed 16 px. Nie można datować zmiany ani rozstrzygnąć, czy była zamierzona.','', '## PageSpeed','Dwa przebiegi na telefonie i komputerze. Dostępność 96, sprawdzone metody 100, SEO 92. Wydajność: brak wyniku, powtarzalne NO_LCP. Nie oznacza to 0/100 ani 100/100. Transfer 9239-10621 KiB.','', '## Dodatkowe priorytety','- REG-01 P1 warunkowo: brakujące CTA wyceny, rekrutacja i podmenu oferty.','- REG-02 P2: mobilne menu z dostępnym przyciskiem i panelem.','- REG-03 P2: odtworzenie spójnej typografii i odstępów.','- PSI-01 P2: diagnostyka NO_LCP, pełny pomiar kontrolny.','- PSI-02 P2: optymalizacja transferu, wymiary obrazów i kontrast.','', '## Źródła']+[title+': '+url for title,url in refs]
(R/'Uzupelnienie-archiwum-PageSpeed.md').write_text('\n'.join(md),encoding='utf-8')
print('SUPPLEMENT',len(PdfReader(str(supp)).pages),'FULL',len(PdfReader(str(full)).pages));print(full)
