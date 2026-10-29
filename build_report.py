from pathlib import Path
import json,html,re
from collections import Counter
from reportlab.pdfgen import canvas
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,KeepTogether,Image
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib.pagesizes import A4

ROOT=Path(__file__).parent; OUT=ROOT/'output'/'pdf';OUT.mkdir(parents=True,exist_ok=True)
D=ROOT/'dowody'; M=json.loads((D/'metrics.json').read_text(encoding='utf-8'))
F=[]
def finding(id,priority,title,status,evidence,impact,action,accept,owner,effort):
 F.append(dict(id=id,priority=priority,title=title,status=status,evidence=evidence,impact=impact,action=action,accept=accept,owner=owner,effort=effort))

finding('SEC-01','P1','Brak wymuszenia HTTPS','Potwierdzone',
 'GET http://www.building4you.pl/ zwraca 200 i treść strony bez przekierowania. Wariant http://building4you.pl/ przekierowuje na www, ale pozostaje przy HTTP. Odpowiedzi HTTPS nie zawierają Strict-Transport-Security. Dowód: pages.json, rekordy czterech wariantów domeny; headers-home.txt.',
 'Pierwsze wejście przez HTTP pozostaje nieszyfrowane. Osoba kontrolująca połączenie może odczytać lub zmienić pobieraną stronę. Sam działający certyfikat tego nie eliminuje. Nie stwierdzono przechwycenia danych ani włamania.',
 'Ustawić na CDN/serwerze stałe przekierowanie 301 lub 308 z obu wariantów HTTP na https://www.building4you.pl/, z zachowaniem ścieżki i parametrów. Po sprawdzeniu wszystkich usług wdrożyć HSTS na odpowiedziach HTTPS; includeSubDomains dopiero po przeglądzie subdomen.',
 'Oba adresy HTTP prowadzą do HTTPS; żadna treść HTML nie jest serwowana po HTTP. Przekierowania działają również dla /kontakt/ i parametrów kampanii. Nagłówek HSTS jest widoczny na HTTPS.', 'Administrator hostingu / CDN','2-4 h')
finding('MKT-01','P1*','Niepotwierdzony pomiar skuteczności reklam','Brak wykrytej integracji; priorytet warunkowy',
 'W HTML 72 podstron i w 9 skryptach aplikacji nie wykryto sygnatur GTM, gtag, Google Analytics, Google Ads ani Meta Pixel. DOM strony głównej także nie pokazał skryptów tych dostawców. Nie był to pełny zapis ruchu sieciowego ani kontrola integracji serwerowych. Dowód: metrics.json i all-code.json.',
 'Jeśli kampanie są aktywne, brak potwierdzonego pomiaru utrudnia ocenę kosztu pozyskania zapytania i optymalizację budżetu. Zewnętrzna inspekcja nie rozstrzyga, czy istnieją importy offline, pomiar połączeń lub integracje serwerowe.',
 'Sprawdzić konta Ads/GA4/GTM/Meta i uzgodnić plan pomiaru. Rozróżnić kliknięcie telefonu lub e-maila od faktycznego leada. Wdrożyć tylko potrzebne integracje, z deduplikacją, zarządzaniem zgodami oraz powiązaniem wyników z CRM, jeśli jest używany.',
 'Próbne zdarzenie trafia raz do właściwej usługi. Lead jest rejestrowany po faktycznym skutecznym kontakcie, a nie po samym kliknięciu. Testy zgód i atrybucji są udokumentowane. P1 obowiązuje przed wydatkami reklamowymi; bez kampanii P2.', 'Marketing / analityk / programista','4-12 h + dostęp do kont')
finding('UX-01','P2','Stopka powoduje poziome przewijanie przy 320 px','Potwierdzone',
 'Na /hale-przemyslowe/ przy viewport 320 px: clientWidth=305 px, scrollWidth=329 px. Elementy .b4y-footer-company i .b4y-footer-connect kończą się około x=328,8 px. Przy 390 px na stronie głównej, kontakcie i ofercie nie wykryto takiego przepełnienia. Dowód: browser-320.json; zrzut 06-footer-320.png.',
 'Na wąskich ekranach stopka wykracza poza obszar treści. To utrudnia odczyt i korzystanie ze strony; problem może być bardziej widoczny po powiększeniu tekstu.',
 'W footer-gallery.css usunąć ograniczenia wynikające z minimalnej szerokości zawartości siatki. Sprawdzić minmax(0,1fr), min-width:0 dla dzieci, zawijanie długich podpisów oraz układ newslettera. Naprawić źródło przepełnienia zamiast maskować je overflow-x:hidden.',
 'Przy 320, 360, 390 i 768 px scrollWidth nie przekracza clientWidth; treść i przyciski pozostają czytelne. Powtórzyć kontrolę z tekstem powiększonym do 200%.', 'Frontend','2-4 h')
finding('CODE-01','P2','Powielone bloki treści na stronach oferty','Potwierdzone',
 'Na /hale-przemyslowe/ po FAQ ponownie wyświetlają się akapity wprowadzające i sekcje opisu budowy. W kodzie dwa długie akapity występują identycznie po dwa razy. Identyczne powtórzenia akapitów znaleziono także na /projekty-i-budowa-hal-magazynowych/ oraz /budowa-hali-pod-klucz/. Dowód: metrics.json -> duplicate_paragraphs; zrzut 04-service-mobile.png.',
 'Strona jest niepotrzebnie długa, szczególnie na telefonie. Trudniej dotrzeć do dalszych informacji. Kopie treści zwiększają ryzyko niespójności przy aktualizacji; nie jest to samo w sobie dowód kary SEO.',
 'Sprawdzić źródło treści w WordPressie oraz sposób łączenia importowanych sekcji z treścią wpisu. Zostawić jedną wersję każdego bloku, zachowując unikalne FAQ i potrzebne informacje. Przejrzeć pozostałe szablony usług.',
 'Każdy wskazany akapit występuje raz w renderowanym main. Nie znika treść unikalna. Kontrola mobilna potwierdza prawidłową kolejność sekcji.', 'WordPress / redaktor','2-6 h')
finding('SEC-02','P2','Brak dodatkowych nagłówków zabezpieczających','Potwierdzone braki konfiguracji',
 'Na stronie głównej, /kontakt/ i /hale-przemyslowe/ brak CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy i Permissions-Policy. Nie wykryto również CSP w meta. Brak HSTS opisano w SEC-01. Dowód: pages.json, metrics.json.',
 'Przeglądarka nie otrzymuje jawnych ograniczeń osadzania strony i źródeł zasobów. Zmniejsza to ochronę warstwową. Nie potwierdza istnienia XSS, clickjackingu z istotnym skutkiem ani innej podatności możliwej do wykorzystania.',
 'Dodać nosniff i politykę referrera, ustalić potrzebne uprawnienia. Zablokować niepotrzebne osadzanie przez frame-ancestors w CSP i zgodny X-Frame-Options. CSP wdrażać najpierw jako Report-Only; uwzględnić inline JS/CSS, obrazy data:, wideo i ewentualne przyszłe tagi.',
 'Nagłówki są obecne na odpowiedziach strony i kluczowych podstron. Egzekwowanie CSP nie blokuje wymaganych funkcji. Test osadzania potwierdza uzgodnioną politykę.', 'Hosting / frontend','4-8 h')
finding('PERF-01','P2','Film w tle o rozmiarze 8,56 MB także na telefonie','Potwierdzony rozmiar i odtwarzanie',
 'movie_720.mp4 ma Content-Length 8 555 220 bajtów. W DOM przy 390 px był aktywnym źródłem odtwarzanego wideo. Element ma autoplay, loop i preload=metadata, a home.js wywołuje play(). Dowód: resources.json, browser-home-mobile.json, all-code.json.',
 'Film może istotnie zwiększać transfer i zużycie energii. Rozmiar pliku nie oznacza, że całość została pobrana przy każdym wejściu. Bez pomiaru terenowego nie określam wpływu na LCP ani współczynnik konwersji.',
 'Dla telefonów, ograniczonego transferu i preferencji ograniczonego ruchu rozważyć statyczny poster. Skrócić i ponownie skompresować film, przygotować właściwe warianty rozdzielczości. Nie pobierać ani nie uruchamiać dużego pliku, jeśli zostaje wybrany wariant statyczny.',
 'Na uzgodnionych profilach mobilnych start strony nie wymaga odtwarzania filmu. Porównać transfer, LCP i płynność przed i po zmianie na tym samym profilu testowym.', 'Frontend / multimedia','3-6 h')
finding('PERF-02','P2','Duże obrazy i skany referencji','Potwierdzony potencjał optymalizacji',
 'W próbce: fotografia Fortuna PNG 3 161 117 B; skan 9_Novmax.png 2 408 987 B; 5_Stalgast_I_etap.png 2 083 136 B. Są to rozmiary wskazanych oryginałów z HEAD. Część innych grafik jest już przetwarzana przez mod_pagespeed do WebP. Dowód: resources.json.',
 'Wyświetlanie oryginałów w miniaturach może zwiększać transfer. Plik otwierany świadomie jako pełny dokument może zasadnie być większy. Nie należy utożsamiać sumy rozmiarów plików z transferem pojedynczej wizyty.',
 'Oddzielić miniaturę od pełnego dokumentu. Użyć responsywnych obrazów srcset/sizes, WebP lub AVIF dla zdjęć i lazy loading poza pierwszym ekranem. Skany optymalizować z zachowaniem czytelności; oryginał udostępniać po kliknięciu.',
 'Telefon pobiera miniaturę dopasowaną do szerokości, a nie wielomegabajtowy oryginał. Tekst referencji jest czytelny. Zmierzyć transfer rzeczywistej wizyty, w tym warianty optymalizowane przez CDN.', 'Frontend / redaktor','4-10 h')
finding('SEO-01','P2','Brak meta description w badanych podstronach','Potwierdzone: 72/72',
 'W kodzie 72 różnych podstron HTTPS nie ma meta name=description, w tym na stronie głównej, kontakcie, ofertach, blogu i realizacjach. Tytuły stron są obecne. Dowód: metrics.json oraz zapisane HTML.',
 'Google musi wybrać opis z treści strony. Ogranicza to kontrolę nad komunikatem w wynikach wyszukiwania; nie blokuje indeksowania i nie stanowi automatycznie przyczyny spadku pozycji.',
 'Przygotować unikalne opisy dla strony głównej i kluczowych usług, potem realizacji i artykułów. Powiązać opis z konkretną intencją i treścią; unikać jednego opisu na wszystkich stronach. Google może użyć innego fragmentu mimo wdrożenia.',
 'Kluczowe podstrony mają pojedynczy, sensowny opis w head. Kontrola crawlem wyklucza braki i masowe duplikaty w uzgodnionej grupie stron.', 'SEO / redaktor / WordPress','4-12 h dla kluczowych stron')
finding('SEO-02','P2','Niespójna deklaracja adresów kanonicznych','Potwierdzone: 10 stron bez canonical',
 'Brak canonical na stronie głównej, /realizacje/, /aktualnosci/, /oferta/, /blog/ i pięciu stronach paginacji. Zwykłe strony i wpisy zazwyczaj mają canonical. Dodatkowo strona główna jest dostępna jako HTTP 200. Dowód: metrics.json -> missing_canonical.',
 'Niejednolite sygnały zwiększają niepewność wyboru preferowanego URL. Sam brak canonical nie oznacza błędnej indeksacji; trzeba ją potwierdzić w Search Console.',
 'Po naprawie HTTPS ustawić spójne canonical dla strony głównej i archiwów. Każda użyteczna strona paginacji powinna wskazywać właściwy własny URL, a nie automatycznie stronę pierwszą. Sprawdzić adresy z parametrami.',
 'Preferowane adresy HTTPS są spójne w canonical, mapie strony i linkowaniu. Search Console potwierdza właściwy adres wybrany przez Google dla reprezentatywnych podstron.', 'SEO / WordPress','2-4 h')
finding('UX-02','P2','Ścieżka zapytania wymaga wzmocnienia','Rekomendacja konwersji',
 'Na badanej stronie /hale-przemyslowe/ w treści main nie ma przycisku zapytania, telefonu ani formularza; kontakt jest dostępny w menu i stopce. /kontakt/ oferuje tel: i mailto:, ale nie ma formularza WWW. Brak formularza jest wyborem funkcjonalnym, nie dowodem awarii.',
 'Użytkownik po przeczytaniu oferty musi znaleźć kontakt, a mailto: wymaga skonfigurowanego programu pocztowego. Dodatkowy krok może ograniczać liczbę zapytań, zwłaszcza z reklam. Wielkości wpływu nie zmierzono.',
 'Dodać jasne CTA przy ofercie i na jej końcu, np. Zapytaj o wycenę, wraz z telefonem. Rozważyć krótki formularz, jeśli firma zapewni obsługę zgłoszeń. Przed publikacją ustalić dostarczanie, ochronę antyspamową, walidację i informację o przetwarzaniu danych.',
 'Z oferty da się przejść do kontaktu jednym jednoznacznym działaniem. Jeśli powstanie formularz, kontrolowany test potwierdza odbiór zgłoszenia, komunikaty błędów i pomiar faktycznej wysyłki.', 'Marketing / UX / WordPress','2-4 h CTA; formularz dodatkowo 6-12 h')
finding('A11Y-01','P2','Ciągłe animacje bez widocznego sterowania pauzą','Potwierdzone w zbadanym widoku',
 'Film na stronie głównej jest odtwarzany w pętli bez controls. Dostępne przyciski dotyczą karuzeli, nie pauzy filmu. home.js uruchamia także pętlę Typed.js bez sprawdzenia prefers-reduced-motion. sections.js uwzględnia tę preferencję tylko dla własnych animacji.',
 'Ciągły ruch i zmieniający się nagłówek mogą utrudniać korzystanie osobom wrażliwym na animacje. To ustalenie cząstkowe, nie pełny audyt zgodności WCAG.',
 'Dodać łatwo dostępne sterowanie pauzą i wznowieniem. Dla prefers-reduced-motion wyłączyć automatyczny film i pisanie tekstu, pozostawiając czytelny statyczny nagłówek. Skontrolować obsługę klawiatury i nazwy przycisków.',
 'Pauzę można włączyć klawiaturą i czytnikiem ekranu. Przy ograniczeniu ruchu w systemie strona nie rozpoczyna tych animacji, a treść pozostaje dostępna.', 'Frontend / dostępność','3-6 h')
finding('PRIV-01','P2','Polityka prywatności wymaga przeglądu przed uruchomieniem tagów','Potwierdzony zakres treści; ocena prawna nieprzeprowadzona',
 'Polityka opisuje głównie marketing na podstawie zgody. W badanym tekście nie ma opisu cookies/analityki; końcowa sekcja Klauzula informacyjna zawiera tylko dane administratora. Nie wykryto banera zgód w zbadanych widokach. Dowód: zapis /polityka-prywatnosci/ w pages.json.',
 'Treść może nie odzwierciedlać wszystkich rzeczywistych procesów, szczególnie po dodaniu formularza, newslettera lub tagów. Sam brak banera nie dowodzi naruszenia, jeśli strona nie uruchamia technologii wymagających zgody.',
 'Zestawić politykę z rzeczywistymi usługami hostingu, poczty, analityki i marketingu. Uzupełnienie zakresu, podstaw, odbiorców i retencji uzgodnić z osobą odpowiedzialną za ochronę danych. Przed dodaniem tagów przygotować właściwą obsługę zgód.',
 'Dokument i konfiguracja odpowiadają faktycznie uruchomionym procesom. Zgoda, odmowa i wycofanie działają zgodnie z zatwierdzonym scenariuszem. Ocena prawna należy do uprawnionej osoby.', 'Właściciel procesów / IOD / programista','2-6 h technicznie + przegląd treści')
finding('UX-03','P3','Newsletter jest widoczny, ale nieaktywny','Potwierdzone; jawnie oznaczone',
 'W stopce pole e-mail i przycisk ZAMAWIAM mają disabled. Obok jest informacja, że zapisy ruszą po podłączeniu systemu wysyłkowego. To świadomie wyłączona funkcja, nie błąd walidacji. Dowód: HTML strony głównej oraz zrzut kontaktu.',
 'Interfejs zajmuje miejsce i sugeruje przyszłą funkcję, ale obecnie nie pozyskuje zapisów. Nie stwierdzono utraty przesłanych zgłoszeń, ponieważ wysyłka jest wyłączona.',
 'Podjąć decyzję produktową: ukryć sekcję do uruchomienia albo wdrożyć pełną integrację z potwierdzeniem zapisu i obsługą rezygnacji. Nie aktywować samego przycisku bez zaplecza.',
 'Sekcja jest usunięta z publicznego widoku albo kontrolowany zapis przechodzi cały proces, z komunikatem rezultatu i obsługą zgód.', 'Marketing / WordPress','1 h ukrycie; 4-8 h integracja')
finding('CODE-02','P3','Nawarstwione poprawki CSS zwiększają koszt zmian','Obserwacja kodu frontendowego',
 'style.css zawiera kolejne reguły dla .b4y-brand > a o szerokościach 230 px, 140 px i wariantach mobilnych oraz wiele !important. Są też odrębne arkusze home, sections i footer-gallery oraz warstwy service-fix/service-tune. Dowód: all-code.json i zapis arkusza 6ec5923ea9a3.txt.',
 'Zależność od kolejności ładowania utrudnia przewidzenie wyniku i sprzyja regresjom, takim jak przepełnienie stopki. Sama liczba plików lub !important nie jest podatnością bezpieczeństwa.',
 'Po naprawach funkcjonalnych uporządkować komponenty nagłówka, stopki i oferty. Usunąć dopiero potwierdzone duplikaty reguł, zdefiniować breakpointy i ograniczyć nadpisywanie. Potrzebny jest dostęp do źródeł, aby ocenić pełną architekturę.',
 'Zmiany przechodzą porównanie wizualne strony głównej, kontaktu, usługi i realizacji dla 320/390/768/1280 px. Oczyszczony kod zachowuje dotychczasowe funkcje.', 'Frontend','6-16 h po przeglądzie źródeł')
finding('SEO-03','P3','Linkowanie wewnętrzne prowadzi przez stare adresy','Potwierdzone; przekierowania działają',
 'Menu używa ?page_id=1020, ?cat=5 i podobnych adresów, które przekierowują na nowe ścieżki. W treści są oferta.html, o-nas/referencje.html i szybka-wycena.html?view=article&id=86. Badane cele kończą się poprawnie kodem 200. Dowód: pages.json -> redirects.',
 'Dodatkowe przekierowania są zbędnym etapem i komplikują utrzymanie. Nie wykryto tu niedziałających głównych linków; zachowanie przekierowań jest ważne dla dawnych odnośników zewnętrznych.',
 'W menu i treści zastąpić linki bezpośrednimi docelowymi adresami HTTPS. Zachować przekierowania ze starych adresów dla użytkowników i wyszukiwarek. Skontrolować zachowanie parametrów atrybucji przy migracji.',
 'Crawl linków z menu i kluczowych sekcji nie wykazuje niepotrzebnych 3xx. Dawne publiczne URL nadal prowadzą do poprawnych treści.', 'WordPress / SEO','2-4 h')
finding('SEO-04','P3','Brak danych strukturalnych JSON-LD','Potwierdzony brak formatu JSON-LD',
 'W 72 badanych podstronach nie wykryto script type=application/ld+json. To sprawdzenie dotyczyło JSON-LD, a nie pełnej walidacji wszystkich możliwych formatów danych strukturalnych. Dowód: metrics.json -> jsonld_pages=0.',
 'Niewykorzystana możliwość jednoznacznego opisania organizacji i struktury treści. Brak JSON-LD nie blokuje indeksowania. Wdrożenie nie gwarantuje rozszerzonych wyników ani wzrostu pozycji.',
 'Dodać zgodne z treścią dane Organization, BreadcrumbList i odpowiedni typ artykułów tam, gdzie mają zastosowanie. Uzgodnić spójne dane firmy i identyfikatory; nie dodawać fikcyjnych ocen lub usług.',
 'Walidator danych strukturalnych nie wykazuje błędów. Oznaczenia odpowiadają widocznej treści, a ich obecność sprawdzono po renderowaniu.', 'SEO / WordPress','3-6 h')

(ROOT/'ustalenia.json').write_text(json.dumps(F,ensure_ascii=False,indent=2),encoding='utf-8')
navy=colors.HexColor('#16263d');red=colors.HexColor('#b9213b');gray=colors.HexColor('#5b6573');light=colors.HexColor('#eef2f6')
fontdir=Path('C:/Windows/Fonts')
pdfmetrics.registerFont(TTFont('ArialPL',str(fontdir/'arial.ttf')))
pdfmetrics.registerFont(TTFont('ArialPL-Bold',str(fontdir/'arialbd.ttf')))
pdfmetrics.registerFontFamily('ArialPL',normal='ArialPL',bold='ArialPL-Bold',italic='ArialPL',boldItalic='ArialPL-Bold')
styles={
 'body':ParagraphStyle('body',fontName='ArialPL',fontSize=9.1,leading=13.6,textColor=navy,spaceAfter=8),
 'small':ParagraphStyle('small',fontName='ArialPL',fontSize=7.5,leading=10.5,textColor=gray,spaceAfter=6),
 'h1':ParagraphStyle('h1',fontName='ArialPL-Bold',fontSize=22,leading=27,textColor=navy,spaceAfter=17),
 'h2':ParagraphStyle('h2',fontName='ArialPL-Bold',fontSize=13,leading=17,textColor=navy,spaceBefore=12,spaceAfter=9),
 'label':ParagraphStyle('label',fontName='ArialPL-Bold',fontSize=8.1,leading=11,textColor=red,spaceAfter=7),
 'cover':ParagraphStyle('cover',fontName='ArialPL-Bold',fontSize=34,leading=40,textColor=navy,spaceAfter=20),
}
def clean(t):return t.replace('–','-').replace('—','-').replace('‑','-')
def para(t,style='body'):return Paragraph(html.escape(clean(t)),styles[style])
story=[]
def add(t,style='body'):story.append(para(t,style))
def table(rows,widths=None):
 data=[[para(str(c),'small') for c in row] for row in rows]
 t=Table(data,colWidths=widths or [90,405],hAlign='LEFT',repeatRows=1)
 t.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),light),('VALIGN',(0,0),(-1,-1),'TOP'),('LINEBELOW',(0,0),(-1,0),.8,navy),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#dce2e9')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7)]))
 story.append(t)
def page():story.append(PageBreak())

add('BUILDING4YOU.PL | AUDYT ZEWNĘTRZNY','label');story.append(Spacer(1,22))
add('Raport techniczny\nstrony internetowej'.replace('\n',' '),'cover')
add('Bezpieczeństwo, kod frontendowy, SEO, wydajność i gotowość do reklam','h2')
add('Data badania: 27 października 2026 | Strefa czasu: Europe/Warsaw\nWersja: 1.0 | Stan publicznej strony w czasie przeglądu'.replace('\n',' '),'small')
story.append(Spacer(1,20))
table([['Zakres','Wynik przeglądu'],['72','Różne publiczne podstrony HTTPS sprawdzone po końcowym URL.'],['351','Zasoby sprawdzone metodą HEAD; wszystkie odpowiedziały 200 i miały właściwy typ zasobu.'],['16','Ustaleń i zaleceń: 1 pilne potwierdzone, 1 pilne warunkowo, 10 średnich i 4 niskie.']],[70,425])
story.append(Spacer(1,17))
add('Najważniejszy wniosek','h2')
add('Strona ponownie działa, ale wymaga wymuszenia HTTPS. Przed zwiększeniem wydatków reklamowych należy potwierdzić pomiar leadów. Najbardziej konkretne błędy użytkowe to powielona treść usług i przepełnienie stopki na wąskim ekranie.')
add('Nie potwierdzono włamania ani krytycznej podatności. Audyt publicznej strony nie daje podstaw do uznania backendu i serwera za w pełni bezpieczne. Nie nadano pozornej oceny bezpieczeństwa w skali 0-100.','small')
page()
add('Zakres i wiarygodność wyników','h1')
add('Metoda','h2')
add('Przegląd publicznego HTML, nagłówków HTTP, przekierowań, certyfikatu TLS, 9 skryptów aplikacji i arkuszy strony głównej. Dwie warstwy linkowania: strona główna oraz odnośniki znalezione w podstronach. Zapisano 84 odpowiedzi stron i adresów kontrolnych. Różne adresy wejściowe prowadzące do tego samego URL nie są liczone ponownie w grupie 72 podstron HTTPS.')
add('Przegląd przeglądarkowy obejmował stronę główną, kontakt, ofertę hal przemysłowych i referencje. Sprawdzono układ 390 x 844 px i dodatkowo usługę przy 320 x 740 px; widok komputerowy miał około 1280 px szerokości. Zweryfikowano kliknięcie kontaktu i rozwinięcie działu ofertowania. Nie wysyłano wiadomości, zgłoszeń ani zapisów newslettera.')
add('Co działa poprawnie','h2')
for t in ['Strona główna i wszystkie badane podstrony treści HTTPS zwracają 200. Wcześniejszego 403 nie odtworzono; przyczyna tamtej blokady pozostaje nieustalona.', 'Certyfikat został poprawnie zweryfikowany, obejmuje domenę i www, a połączenie negocjowało TLS 1.3. Data końca ważności: 4 grudnia 2026. Należy potwierdzić automatyczne odnowienie; certyfikat nie jest obecnie nieważny.', 'robots.txt wskazuje działającą mapę wp-sitemap.xml. Nieistniejący adres kontrolny zwraca prawidłowe 404. Brak sitemap_index.xml nie jest błędem, skoro działa inna mapa.', 'Główne stare odnośniki .html przekierowują do właściwych treści. tel: i mailto: mają poprawną strukturę. Akordeon działu ofertowania działa.', 'W badanych widokach nie zarejestrowano ostrzeżeń ani błędów konsoli. Na kontakcie i badanej usłudze nie wykryto zakończonych ładowaniem uszkodzonych obrazów. To wynik próbki, nie gwarancja dla każdej przeglądarki.']:
 add('• '+t)
add('Ograniczenia','h2')
add('Bez logowania do WordPressa, repozytorium, hostingu, bazy danych, Search Console i kont reklamowych. Nie badano kodu PHP, haseł, uprawnień, kopii zapasowych, aktualizacji, dostarczania poczty ani zabezpieczeń formularza, którego w próbce nie ma. Nie przeprowadzono testów penetracyjnych, prób SQLi/XSS, logowania ani testów obciążeniowych.')
add('API PageSpeed zwróciło 429 z powodu limitu usługi. Nie uzyskano wyniku Lighthouse ani Core Web Vitals; nie podaje się ich szacunkowych wartości. Rozmiary plików nie są pomiarem czasu ładowania. Test HEAD nie potwierdza integralności każdego pliku ani wszystkich zasobów tła CSS.','small')
page()
add('Lista zmian według priorytetów','h1')
add('P1: pilne, przed skalowaniem ruchu. P2: następny cykl wdrożeniowy. P3: planowe usprawnienia. P1* jest warunkowe: dotyczy aktywnych lub planowanych kampanii. Priorytet operacyjny nie jest oceną CVSS.','small')
table([['ID / priorytet','Zmiana / odpowiedzialność']]+[[f[ 'id']+' / '+f['priority'],f['title']+' | '+f['owner']] for f in F],[95,400])
add('Nakłady są orientacyjną pracą specjalisty, nie wyceną. Część zadań współdzieli wdrożenie i testy; nie należy sumować ich mechanicznie. Wymagany dostęp i stan źródeł mogą zmienić nakład.','small')
page()
for index in range(0,len(F),2):
 add('Ustalenia szczegółowe','label')
 for f in F[index:index+2]:
  add(f['id']+' | '+f['priority']+' | '+f['title'],'h2')
  add(f['status']+' | '+f['owner']+' | Szacunkowo: '+f['effort'],'small')
  for label,key in [('Dowód','evidence'),('Skutek','impact'),('Zalecana zmiana','action'),('Kryterium odbioru','accept')]:
   story.append(Paragraph('<b>'+label+':</b> '+html.escape(clean(f[key])),styles['body']))
  story.append(Spacer(1,9))
 page()
add('Plan wdrożenia i odbioru','h1')
table([['Etap','Zakres i kolejność'],['0-2 dni','SEC-01: HTTP -> HTTPS, następnie HSTS po sprawdzeniu usług. MKT-01: potwierdzenie kampanii i planu pomiaru; dostęp tylko do potrzebnych kont.'],['3-7 dni roboczych','UX-01 i CODE-01: stopka oraz powielona treść. SEC-02: zabezpieczenia przeglądarkowe. UX-02: jasne CTA. PRIV-01 przed uruchomieniem nowych procesów i tagów.'],['Następne 1-2 tygodnie','PERF-01/02: media. SEO-01/02: opisy i canonical. A11Y-01: pauza i ograniczenie animacji. Pomiar kontrolny wydajności.'],['Planowo','Decyzja o newsletterze; bezpośrednie linkowanie; porządkowanie CSS i dane strukturalne. Potwierdzenie odnowienia TLS przed 4.12.2026.']],[95,400])
add('Warunki wspólne dla wdrożenia','h2')
add('Przed zmianami przygotować sprawdzoną kopię oraz możliwość wycofania. Zmiany kodu i konfiguracji zweryfikować najpierw w środowisku testowym, jeśli jest dostępne. Po publikacji wyczyścić odpowiednie cache CDN/WordPressa i sprawdzić publiczne odpowiedzi.')
for t in ['Dostępność: HTTP, HTTPS, www, podstrony i 404; zachowanie parametrów UTM/gclid przy wymaganych przekierowaniach.', 'Funkcjonalność: menu, CTA, telefony, e-mail, akordeony, galerie oraz ewentualny nowy formularz od wysyłki do odbioru.', 'Układ: 320/360/390/768/1280 px, klawiatura, powiększenie tekstu i prefers-reduced-motion.', 'Reklamy: brak duplikacji zdarzeń, test zgód, odróżnienie kliknięcia od rzeczywistego leada.', 'SEO: crawl metadanych, canonical i linków oraz kontrola reprezentatywnych adresów w Search Console.', 'Wydajność: porównanie przed/po na tym samym urządzeniu i profilu sieci; użyć danych terenowych, gdy są dostępne.']:
 add('• '+t)
add('Dalsza kontrola wymagająca dostępu','h2')
add('Repozytorium: przegląd PHP, szablonów, zależności i mechanizmu budowania. WordPress/hosting: wersje i aktualizacje, role, MFA, backup z próbą odtworzenia, logi CDN/WAF/serwera wyjaśniające 403. Marketing: GA4/Ads/Meta, definicje leadów i koszty. Search Console: indeksacja, przekierowania i historia po zmianach. Są to zadania do wykonania, nie potwierdzone usterki.')
page()
add('Dowody i dokumentacja','h1')
add('Materiały lokalne przekazane z raportem','h2')
for t in ['dowody/pages.json + pages-secondary.json: odpowiedzi, nagłówki, przekierowania i analiza HTML.', 'dowody/metrics.json: zbiorcze wyniki oraz lista 72 podstron i plików źródłowych.', 'dowody/resources.json: statusy, typy i zadeklarowane rozmiary 351 zasobów.', 'dowody/all-code.json: indeks pobranych skryptów i CSS. Pliki o nazwach skrótów SHA-256 zawierają zapisane odpowiedzi.', 'dowody/tls.json: wynik weryfikacji certyfikatu i połączenia; pagespeed-mobile.json: odpowiedź 429.', 'dowody/browser-*.json i zrzuty 01-06: obserwacje DOM, testy przeglądarkowe i widoki. ustalenia.json: lista zmian z kryteriami odbioru.']:
 add('• '+t)
add('Źródła zaleceń technicznych','h2')
refs=[('MDN: Strict-Transport-Security','https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security'),('MDN: Content Security Policy','https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP'),('Google Search Central: opisy wyników i meta description','https://developers.google.com/search/docs/appearance/snippet'),('Google Search Central: adresy kanoniczne','https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls')]
for title,url in refs:
 story.append(Paragraph('<b>'+html.escape(title)+'</b><br/><link href="'+url+'" color="#245c96">'+url+'</link>',styles['small']))
add('Ustalenia dotyczące strony wynikają z bezpośredniego badania, a dokumentacja wyjaśnia sens zaleceń. Wnioski o przyczynach oraz wpływie biznesowym oznaczono jako potencjalne; nie są pomiarem utraconych przychodów.','small')
add('Przykład stanu strony głównej','h2')
im=Image(str(D/'01-home-desktop.png'),width=495,height=278);story.append(im)
page()
add('Dowody wizualne','h1')
add('Po lewej: przepełnienie stopki przy viewport 320 px (UX-01). Przycisk newslettera wychodzi poza prawą krawędź obszaru treści. Po prawej: film i animowany nagłówek na stronie głównej przy 390 px (PERF-01 / A11Y-01).','body')
visuals=Table([[Image(str(D/'06-footer-320.png'),width=220,height=534),Image(str(D/'02-home-mobile.png'),width=220,height=495)]],colWidths=[247.5,247.5],hAlign='LEFT')
visuals.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('LEFTPADDING',(0,0),(-1,-1),0),('TOPPADDING',(0,0),(-1,-1),8)]))
story.append(visuals)
page()
add('Indeks sprawdzonych podstron','h1')
add('72 końcowe adresy HTTPS z odpowiedzią 200. Lista stanowi zakres próbki, a nie pełną inwentaryzację całej witryny. Wszystkie te dokumenty HTML nie zawierały meta description.','small')
rows=[['Ścieżka URL','Tytuł']]
for x in M['page_inventory']:
 rows.append([x['url'].replace('https://www.building4you.pl','') or '/',x['title'].replace(' – Building4you','')])
table(rows,[260,235])

def footer(c,doc):
 c.saveState();w,h=A4
 c.setStrokeColor(red);c.setLineWidth(2);c.line(50,h-36,w-50,h-36)
 c.setFont('ArialPL',7);c.setFillColor(gray)
 c.drawString(50,27,'BUILDING4YOU.PL | Audyt zewnętrzny | 27.10.2026 | v1.0')
 c.drawRightString(w-50,27,str(doc.page));c.restoreState()
pdf=OUT/'Building4you-audyt-2026-10-27.pdf'
doc=SimpleDocTemplate(str(pdf),pagesize=A4,rightMargin=50,leftMargin=50,topMargin=54,bottomMargin=48,title='Building4you - audyt techniczny 27.10.2026',author='Raport audytu zewnętrznego')
doc.build(story,onFirstPage=footer,onLaterPages=footer)

# Editable companion, with the same findings and acceptance criteria.
md=['# Building4you.pl - analiza techniczna','Data: 27.10.2026. Audyt publiczny; szczegółowy zakres i ograniczenia w raporcie PDF.','', '72 różne podstrony HTTPS; 351 zasobów HEAD. Nie uzyskano wyniku PageSpeed (429).','']
for f in F:
 md += ['## '+f['id']+' | '+f['priority']+' | '+f['title'],f['status'],'', '**Odpowiedzialność / nakład:** '+f['owner']+' / '+f['effort'],'']
 for label,key in [('Dowód','evidence'),('Skutek','impact'),('Zalecenie','action'),('Kryterium odbioru','accept')]:md+=['**'+label+':** '+f[key],'']
(ROOT/'Lista-zmian-Building4you.md').write_text('\n'.join(md),encoding='utf-8')
print(pdf)
