# Building4you.pl - analiza techniczna
Data: 27.10.2026. Audyt publiczny; szczegółowy zakres i ograniczenia w raporcie PDF.

72 różne podstrony HTTPS; 351 zasobów HEAD. Nie uzyskano wyniku PageSpeed (429).

## SEC-01 | P1 | Brak wymuszenia HTTPS
Potwierdzone

**Odpowiedzialność / nakład:** Administrator hostingu / CDN / 2-4 h

**Dowód:** GET http://www.building4you.pl/ zwraca 200 i treść strony bez przekierowania. Wariant http://building4you.pl/ przekierowuje na www, ale pozostaje przy HTTP. Odpowiedzi HTTPS nie zawierają Strict-Transport-Security. Dowód: pages.json, rekordy czterech wariantów domeny; headers-home.txt.

**Skutek:** Pierwsze wejście przez HTTP pozostaje nieszyfrowane. Osoba kontrolująca połączenie może odczytać lub zmienić pobieraną stronę. Sam działający certyfikat tego nie eliminuje. Nie stwierdzono przechwycenia danych ani włamania.

**Zalecenie:** Ustawić na CDN/serwerze stałe przekierowanie 301 lub 308 z obu wariantów HTTP na https://www.building4you.pl/, z zachowaniem ścieżki i parametrów. Po sprawdzeniu wszystkich usług wdrożyć HSTS na odpowiedziach HTTPS; includeSubDomains dopiero po przeglądzie subdomen.

**Kryterium odbioru:** Oba adresy HTTP prowadzą do HTTPS; żadna treść HTML nie jest serwowana po HTTP. Przekierowania działają również dla /kontakt/ i parametrów kampanii. Nagłówek HSTS jest widoczny na HTTPS.

## MKT-01 | P1* | Niepotwierdzony pomiar skuteczności reklam
Brak wykrytej integracji; priorytet warunkowy

**Odpowiedzialność / nakład:** Marketing / analityk / programista / 4-12 h + dostęp do kont

**Dowód:** W HTML 72 podstron i w 9 skryptach aplikacji nie wykryto sygnatur GTM, gtag, Google Analytics, Google Ads ani Meta Pixel. DOM strony głównej także nie pokazał skryptów tych dostawców. Nie był to pełny zapis ruchu sieciowego ani kontrola integracji serwerowych. Dowód: metrics.json i all-code.json.

**Skutek:** Jeśli kampanie są aktywne, brak potwierdzonego pomiaru utrudnia ocenę kosztu pozyskania zapytania i optymalizację budżetu. Zewnętrzna inspekcja nie rozstrzyga, czy istnieją importy offline, pomiar połączeń lub integracje serwerowe.

**Zalecenie:** Sprawdzić konta Ads/GA4/GTM/Meta i uzgodnić plan pomiaru. Rozróżnić kliknięcie telefonu lub e-maila od faktycznego leada. Wdrożyć tylko potrzebne integracje, z deduplikacją, zarządzaniem zgodami oraz powiązaniem wyników z CRM, jeśli jest używany.

**Kryterium odbioru:** Próbne zdarzenie trafia raz do właściwej usługi. Lead jest rejestrowany po faktycznym skutecznym kontakcie, a nie po samym kliknięciu. Testy zgód i atrybucji są udokumentowane. P1 obowiązuje przed wydatkami reklamowymi; bez kampanii P2.

## UX-01 | P2 | Stopka powoduje poziome przewijanie przy 320 px
Potwierdzone

**Odpowiedzialność / nakład:** Frontend / 2-4 h

**Dowód:** Na /hale-przemyslowe/ przy viewport 320 px: clientWidth=305 px, scrollWidth=329 px. Elementy .b4y-footer-company i .b4y-footer-connect kończą się około x=328,8 px. Przy 390 px na stronie głównej, kontakcie i ofercie nie wykryto takiego przepełnienia. Dowód: browser-320.json; zrzut 06-footer-320.png.

**Skutek:** Na wąskich ekranach stopka wykracza poza obszar treści. To utrudnia odczyt i korzystanie ze strony; problem może być bardziej widoczny po powiększeniu tekstu.

**Zalecenie:** W footer-gallery.css usunąć ograniczenia wynikające z minimalnej szerokości zawartości siatki. Sprawdzić minmax(0,1fr), min-width:0 dla dzieci, zawijanie długich podpisów oraz układ newslettera. Naprawić źródło przepełnienia zamiast maskować je overflow-x:hidden.

**Kryterium odbioru:** Przy 320, 360, 390 i 768 px scrollWidth nie przekracza clientWidth; treść i przyciski pozostają czytelne. Powtórzyć kontrolę z tekstem powiększonym do 200%.

## CODE-01 | P2 | Powielone bloki treści na stronach oferty
Potwierdzone

**Odpowiedzialność / nakład:** WordPress / redaktor / 2-6 h

**Dowód:** Na /hale-przemyslowe/ po FAQ ponownie wyświetlają się akapity wprowadzające i sekcje opisu budowy. W kodzie dwa długie akapity występują identycznie po dwa razy. Identyczne powtórzenia akapitów znaleziono także na /projekty-i-budowa-hal-magazynowych/ oraz /budowa-hali-pod-klucz/. Dowód: metrics.json -> duplicate_paragraphs; zrzut 04-service-mobile.png.

**Skutek:** Strona jest niepotrzebnie długa, szczególnie na telefonie. Trudniej dotrzeć do dalszych informacji. Kopie treści zwiększają ryzyko niespójności przy aktualizacji; nie jest to samo w sobie dowód kary SEO.

**Zalecenie:** Sprawdzić źródło treści w WordPressie oraz sposób łączenia importowanych sekcji z treścią wpisu. Zostawić jedną wersję każdego bloku, zachowując unikalne FAQ i potrzebne informacje. Przejrzeć pozostałe szablony usług.

**Kryterium odbioru:** Każdy wskazany akapit występuje raz w renderowanym main. Nie znika treść unikalna. Kontrola mobilna potwierdza prawidłową kolejność sekcji.

## SEC-02 | P2 | Brak dodatkowych nagłówków zabezpieczających
Potwierdzone braki konfiguracji

**Odpowiedzialność / nakład:** Hosting / frontend / 4-8 h

**Dowód:** Na stronie głównej, /kontakt/ i /hale-przemyslowe/ brak CSP, X-Frame-Options, X-Content-Type-Options, Referrer-Policy i Permissions-Policy. Nie wykryto również CSP w meta. Brak HSTS opisano w SEC-01. Dowód: pages.json, metrics.json.

**Skutek:** Przeglądarka nie otrzymuje jawnych ograniczeń osadzania strony i źródeł zasobów. Zmniejsza to ochronę warstwową. Nie potwierdza istnienia XSS, clickjackingu z istotnym skutkiem ani innej podatności możliwej do wykorzystania.

**Zalecenie:** Dodać nosniff i politykę referrera, ustalić potrzebne uprawnienia. Zablokować niepotrzebne osadzanie przez frame-ancestors w CSP i zgodny X-Frame-Options. CSP wdrażać najpierw jako Report-Only; uwzględnić inline JS/CSS, obrazy data:, wideo i ewentualne przyszłe tagi.

**Kryterium odbioru:** Nagłówki są obecne na odpowiedziach strony i kluczowych podstron. Egzekwowanie CSP nie blokuje wymaganych funkcji. Test osadzania potwierdza uzgodnioną politykę.

## PERF-01 | P2 | Film w tle o rozmiarze 8,56 MB także na telefonie
Potwierdzony rozmiar i odtwarzanie

**Odpowiedzialność / nakład:** Frontend / multimedia / 3-6 h

**Dowód:** movie_720.mp4 ma Content-Length 8 555 220 bajtów. W DOM przy 390 px był aktywnym źródłem odtwarzanego wideo. Element ma autoplay, loop i preload=metadata, a home.js wywołuje play(). Dowód: resources.json, browser-home-mobile.json, all-code.json.

**Skutek:** Film może istotnie zwiększać transfer i zużycie energii. Rozmiar pliku nie oznacza, że całość została pobrana przy każdym wejściu. Bez pomiaru terenowego nie określam wpływu na LCP ani współczynnik konwersji.

**Zalecenie:** Dla telefonów, ograniczonego transferu i preferencji ograniczonego ruchu rozważyć statyczny poster. Skrócić i ponownie skompresować film, przygotować właściwe warianty rozdzielczości. Nie pobierać ani nie uruchamiać dużego pliku, jeśli zostaje wybrany wariant statyczny.

**Kryterium odbioru:** Na uzgodnionych profilach mobilnych start strony nie wymaga odtwarzania filmu. Porównać transfer, LCP i płynność przed i po zmianie na tym samym profilu testowym.

## PERF-02 | P2 | Duże obrazy i skany referencji
Potwierdzony potencjał optymalizacji

**Odpowiedzialność / nakład:** Frontend / redaktor / 4-10 h

**Dowód:** W próbce: fotografia Fortuna PNG 3 161 117 B; skan 9_Novmax.png 2 408 987 B; 5_Stalgast_I_etap.png 2 083 136 B. Są to rozmiary wskazanych oryginałów z HEAD. Część innych grafik jest już przetwarzana przez mod_pagespeed do WebP. Dowód: resources.json.

**Skutek:** Wyświetlanie oryginałów w miniaturach może zwiększać transfer. Plik otwierany świadomie jako pełny dokument może zasadnie być większy. Nie należy utożsamiać sumy rozmiarów plików z transferem pojedynczej wizyty.

**Zalecenie:** Oddzielić miniaturę od pełnego dokumentu. Użyć responsywnych obrazów srcset/sizes, WebP lub AVIF dla zdjęć i lazy loading poza pierwszym ekranem. Skany optymalizować z zachowaniem czytelności; oryginał udostępniać po kliknięciu.

**Kryterium odbioru:** Telefon pobiera miniaturę dopasowaną do szerokości, a nie wielomegabajtowy oryginał. Tekst referencji jest czytelny. Zmierzyć transfer rzeczywistej wizyty, w tym warianty optymalizowane przez CDN.

## SEO-01 | P2 | Brak meta description w badanych podstronach
Potwierdzone: 72/72

**Odpowiedzialność / nakład:** SEO / redaktor / WordPress / 4-12 h dla kluczowych stron

**Dowód:** W kodzie 72 różnych podstron HTTPS nie ma meta name=description, w tym na stronie głównej, kontakcie, ofertach, blogu i realizacjach. Tytuły stron są obecne. Dowód: metrics.json oraz zapisane HTML.

**Skutek:** Google musi wybrać opis z treści strony. Ogranicza to kontrolę nad komunikatem w wynikach wyszukiwania; nie blokuje indeksowania i nie stanowi automatycznie przyczyny spadku pozycji.

**Zalecenie:** Przygotować unikalne opisy dla strony głównej i kluczowych usług, potem realizacji i artykułów. Powiązać opis z konkretną intencją i treścią; unikać jednego opisu na wszystkich stronach. Google może użyć innego fragmentu mimo wdrożenia.

**Kryterium odbioru:** Kluczowe podstrony mają pojedynczy, sensowny opis w head. Kontrola crawlem wyklucza braki i masowe duplikaty w uzgodnionej grupie stron.

## SEO-02 | P2 | Niespójna deklaracja adresów kanonicznych
Potwierdzone: 10 stron bez canonical

**Odpowiedzialność / nakład:** SEO / WordPress / 2-4 h

**Dowód:** Brak canonical na stronie głównej, /realizacje/, /aktualnosci/, /oferta/, /blog/ i pięciu stronach paginacji. Zwykłe strony i wpisy zazwyczaj mają canonical. Dodatkowo strona główna jest dostępna jako HTTP 200. Dowód: metrics.json -> missing_canonical.

**Skutek:** Niejednolite sygnały zwiększają niepewność wyboru preferowanego URL. Sam brak canonical nie oznacza błędnej indeksacji; trzeba ją potwierdzić w Search Console.

**Zalecenie:** Po naprawie HTTPS ustawić spójne canonical dla strony głównej i archiwów. Każda użyteczna strona paginacji powinna wskazywać właściwy własny URL, a nie automatycznie stronę pierwszą. Sprawdzić adresy z parametrami.

**Kryterium odbioru:** Preferowane adresy HTTPS są spójne w canonical, mapie strony i linkowaniu. Search Console potwierdza właściwy adres wybrany przez Google dla reprezentatywnych podstron.

## UX-02 | P2 | Ścieżka zapytania wymaga wzmocnienia
Rekomendacja konwersji

**Odpowiedzialność / nakład:** Marketing / UX / WordPress / 2-4 h CTA; formularz dodatkowo 6-12 h

**Dowód:** Na badanej stronie /hale-przemyslowe/ w treści main nie ma przycisku zapytania, telefonu ani formularza; kontakt jest dostępny w menu i stopce. /kontakt/ oferuje tel: i mailto:, ale nie ma formularza WWW. Brak formularza jest wyborem funkcjonalnym, nie dowodem awarii.

**Skutek:** Użytkownik po przeczytaniu oferty musi znaleźć kontakt, a mailto: wymaga skonfigurowanego programu pocztowego. Dodatkowy krok może ograniczać liczbę zapytań, zwłaszcza z reklam. Wielkości wpływu nie zmierzono.

**Zalecenie:** Dodać jasne CTA przy ofercie i na jej końcu, np. Zapytaj o wycenę, wraz z telefonem. Rozważyć krótki formularz, jeśli firma zapewni obsługę zgłoszeń. Przed publikacją ustalić dostarczanie, ochronę antyspamową, walidację i informację o przetwarzaniu danych.

**Kryterium odbioru:** Z oferty da się przejść do kontaktu jednym jednoznacznym działaniem. Jeśli powstanie formularz, kontrolowany test potwierdza odbiór zgłoszenia, komunikaty błędów i pomiar faktycznej wysyłki.

## A11Y-01 | P2 | Ciągłe animacje bez widocznego sterowania pauzą
Potwierdzone w zbadanym widoku

**Odpowiedzialność / nakład:** Frontend / dostępność / 3-6 h

**Dowód:** Film na stronie głównej jest odtwarzany w pętli bez controls. Dostępne przyciski dotyczą karuzeli, nie pauzy filmu. home.js uruchamia także pętlę Typed.js bez sprawdzenia prefers-reduced-motion. sections.js uwzględnia tę preferencję tylko dla własnych animacji.

**Skutek:** Ciągły ruch i zmieniający się nagłówek mogą utrudniać korzystanie osobom wrażliwym na animacje. To ustalenie cząstkowe, nie pełny audyt zgodności WCAG.

**Zalecenie:** Dodać łatwo dostępne sterowanie pauzą i wznowieniem. Dla prefers-reduced-motion wyłączyć automatyczny film i pisanie tekstu, pozostawiając czytelny statyczny nagłówek. Skontrolować obsługę klawiatury i nazwy przycisków.

**Kryterium odbioru:** Pauzę można włączyć klawiaturą i czytnikiem ekranu. Przy ograniczeniu ruchu w systemie strona nie rozpoczyna tych animacji, a treść pozostaje dostępna.

## PRIV-01 | P2 | Polityka prywatności wymaga przeglądu przed uruchomieniem tagów
Potwierdzony zakres treści; ocena prawna nieprzeprowadzona

**Odpowiedzialność / nakład:** Właściciel procesów / IOD / programista / 2-6 h technicznie + przegląd treści

**Dowód:** Polityka opisuje głównie marketing na podstawie zgody. W badanym tekście nie ma opisu cookies/analityki; końcowa sekcja Klauzula informacyjna zawiera tylko dane administratora. Nie wykryto banera zgód w zbadanych widokach. Dowód: zapis /polityka-prywatnosci/ w pages.json.

**Skutek:** Treść może nie odzwierciedlać wszystkich rzeczywistych procesów, szczególnie po dodaniu formularza, newslettera lub tagów. Sam brak banera nie dowodzi naruszenia, jeśli strona nie uruchamia technologii wymagających zgody.

**Zalecenie:** Zestawić politykę z rzeczywistymi usługami hostingu, poczty, analityki i marketingu. Uzupełnienie zakresu, podstaw, odbiorców i retencji uzgodnić z osobą odpowiedzialną za ochronę danych. Przed dodaniem tagów przygotować właściwą obsługę zgód.

**Kryterium odbioru:** Dokument i konfiguracja odpowiadają faktycznie uruchomionym procesom. Zgoda, odmowa i wycofanie działają zgodnie z zatwierdzonym scenariuszem. Ocena prawna należy do uprawnionej osoby.

## UX-03 | P3 | Newsletter jest widoczny, ale nieaktywny
Potwierdzone; jawnie oznaczone

**Odpowiedzialność / nakład:** Marketing / WordPress / 1 h ukrycie; 4-8 h integracja

**Dowód:** W stopce pole e-mail i przycisk ZAMAWIAM mają disabled. Obok jest informacja, że zapisy ruszą po podłączeniu systemu wysyłkowego. To świadomie wyłączona funkcja, nie błąd walidacji. Dowód: HTML strony głównej oraz zrzut kontaktu.

**Skutek:** Interfejs zajmuje miejsce i sugeruje przyszłą funkcję, ale obecnie nie pozyskuje zapisów. Nie stwierdzono utraty przesłanych zgłoszeń, ponieważ wysyłka jest wyłączona.

**Zalecenie:** Podjąć decyzję produktową: ukryć sekcję do uruchomienia albo wdrożyć pełną integrację z potwierdzeniem zapisu i obsługą rezygnacji. Nie aktywować samego przycisku bez zaplecza.

**Kryterium odbioru:** Sekcja jest usunięta z publicznego widoku albo kontrolowany zapis przechodzi cały proces, z komunikatem rezultatu i obsługą zgód.

## CODE-02 | P3 | Nawarstwione poprawki CSS zwiększają koszt zmian
Obserwacja kodu frontendowego

**Odpowiedzialność / nakład:** Frontend / 6-16 h po przeglądzie źródeł

**Dowód:** style.css zawiera kolejne reguły dla .b4y-brand > a o szerokościach 230 px, 140 px i wariantach mobilnych oraz wiele !important. Są też odrębne arkusze home, sections i footer-gallery oraz warstwy service-fix/service-tune. Dowód: all-code.json i zapis arkusza 6ec5923ea9a3.txt.

**Skutek:** Zależność od kolejności ładowania utrudnia przewidzenie wyniku i sprzyja regresjom, takim jak przepełnienie stopki. Sama liczba plików lub !important nie jest podatnością bezpieczeństwa.

**Zalecenie:** Po naprawach funkcjonalnych uporządkować komponenty nagłówka, stopki i oferty. Usunąć dopiero potwierdzone duplikaty reguł, zdefiniować breakpointy i ograniczyć nadpisywanie. Potrzebny jest dostęp do źródeł, aby ocenić pełną architekturę.

**Kryterium odbioru:** Zmiany przechodzą porównanie wizualne strony głównej, kontaktu, usługi i realizacji dla 320/390/768/1280 px. Oczyszczony kod zachowuje dotychczasowe funkcje.

## SEO-03 | P3 | Linkowanie wewnętrzne prowadzi przez stare adresy
Potwierdzone; przekierowania działają

**Odpowiedzialność / nakład:** WordPress / SEO / 2-4 h

**Dowód:** Menu używa ?page_id=1020, ?cat=5 i podobnych adresów, które przekierowują na nowe ścieżki. W treści są oferta.html, o-nas/referencje.html i szybka-wycena.html?view=article&id=86. Badane cele kończą się poprawnie kodem 200. Dowód: pages.json -> redirects.

**Skutek:** Dodatkowe przekierowania są zbędnym etapem i komplikują utrzymanie. Nie wykryto tu niedziałających głównych linków; zachowanie przekierowań jest ważne dla dawnych odnośników zewnętrznych.

**Zalecenie:** W menu i treści zastąpić linki bezpośrednimi docelowymi adresami HTTPS. Zachować przekierowania ze starych adresów dla użytkowników i wyszukiwarek. Skontrolować zachowanie parametrów atrybucji przy migracji.

**Kryterium odbioru:** Crawl linków z menu i kluczowych sekcji nie wykazuje niepotrzebnych 3xx. Dawne publiczne URL nadal prowadzą do poprawnych treści.

## SEO-04 | P3 | Brak danych strukturalnych JSON-LD
Potwierdzony brak formatu JSON-LD

**Odpowiedzialność / nakład:** SEO / WordPress / 3-6 h

**Dowód:** W 72 badanych podstronach nie wykryto script type=application/ld+json. To sprawdzenie dotyczyło JSON-LD, a nie pełnej walidacji wszystkich możliwych formatów danych strukturalnych. Dowód: metrics.json -> jsonld_pages=0.

**Skutek:** Niewykorzystana możliwość jednoznacznego opisania organizacji i struktury treści. Brak JSON-LD nie blokuje indeksowania. Wdrożenie nie gwarantuje rozszerzonych wyników ani wzrostu pozycji.

**Zalecenie:** Dodać zgodne z treścią dane Organization, BreadcrumbList i odpowiedni typ artykułów tam, gdzie mają zastosowanie. Uzgodnić spójne dane firmy i identyfikatory; nie dodawać fikcyjnych ocen lub usług.

**Kryterium odbioru:** Walidator danych strukturalnych nie wykazuje błędów. Oznaczenia odpowiadają widocznej treści, a ich obecność sprawdzono po renderowaniu.
