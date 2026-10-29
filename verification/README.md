# Ponowna weryfikacja - 27.10.2026

Aktualne dokumenty to raporty dla klienta i programisty z sufiksem `v2.1`. Zastępują wcześniejsze wersje w zakresie poniższych korekt.

## Potwierdzone ponownie

- 72 podstrony treści HTTPS i 351 zasobów HEAD ponownie zwracają 200.
- HTTP strony głównej nadal serwuje treść 200 bez wymuszenia HTTPS.
- 72/72 podstron bez meta description, 10 bez canonical, 0 z JSON-LD.
- Duplikaty akapitów na 3 wskazanych stronach; stopka przy 320 px ma scrollWidth 329 przy clientWidth 305.
- Nowy dowód UX-04: linki podmenu O nas są białe na białym tle przed przewinięciem, po przewinięciu zmieniają się na ciemne. Przyczyną jest za szeroka reguła CSS `body.home:not(.b4y-home-scrolled) .b4y-menu a`.

## Korekty interpretacji

Brak publicznych tagów nie dowodzi braku pomiaru na kontach. Brak formularza nie oznacza awarii formularza. Zmiany względem maja nie dowodzą regresji z ostatniego tygodnia. Brak dodatkowych nagłówków ochronnych nie dowodzi włamania. Kod już ukrywa film przy `prefers-reduced-motion`; nadal brakuje sterowania pauzą i ograniczenia animowanego tekstu.

## Dlaczego PageSpeed nie daje oceny głównej

Ponowny wynik Google dla głównej: NO_LCP. Kontakt w Google: 98/100, LCP ok. 1,6 s. Lokalny Lighthouse 13.5.0 z Chrome 156.0.8078.48 mierzy niezmienioną główną: 73 i 75/100, LCP ok. 8,26 s (standardowy mobilny profil z symulowanym spowolnieniem). Nie są to wyniki PageSpeed ani terenowe Core Web Vitals.

Lokalny `chrome-headless-shell` 153.0.8010.36, czyli ta sama wersja silnika co wskazana przez Google, odtwarza NO_LCP na głównej, a dla kontaktu daje 100/100. Blokowanie Typed.js, wideo oraz obu zasobów w lokalnych testach diagnostycznych nie usuwa NO_LCP. Warianty z blokadami nie oceniają niezmienionej strony.

Na poziomie pomiaru problemem jest brak użytecznego zdarzenia LCP. Zależność od konfiguracji Chromium jest odtworzona, ale nie przypisano przyczyny wyłącznie numerowi wersji lub pojedynczej instrukcji CSS/JS. Błąd NO_LCP nie oznacza niedostępności strony i nie jest tym samym co 429 API. Dokładna izolacja renderowania wymaga dalszego testu na stagingu.

## Pliki

- `verification-summary.json`: macierz 22 pozycji i 7 lokalnych pomiarów.
- `pages-recheck.json`, `assets-recheck.json`: ponowne odpowiedzi.
- `menu-open.json`, `menu-after-scroll.json`, `menu-open.png`: dowód konfliktu menu.
- `lighthouse-home.report.html`, `lighthouse-home.report.json`: pierwszy pełny lokalny wynik.
- `lighthouse-home-repeat.json`: powtórzenie; pozostałe JSON i trace: diagnostyka.
- `pagespeed-home-dom.txt`, `pagespeed-contact-dom.txt`: zapis nowego wyniku Google.

Żadnych zmian nie opublikowano na stronie. Automatyczna kontrola zablokowała usunięcie tymczasowej przeglądarki; jej pliki pozostają w `verification/browser153/` i nie są dołączane do pakietu. Zachowano metadane użytej wersji. Biblioteki narzędzia mogą pozostać w standardowej pamięci podręcznej npm.
