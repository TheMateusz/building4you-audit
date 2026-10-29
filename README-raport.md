# Building4you.pl - pakiet audytu z 27.10.2026

- `output/pdf/Building4you-audyt-2026-10-27.pdf`: raport końcowy (17 stron), priorytety, dowody, kryteria odbioru i plan wdrożenia.
- `Lista-zmian-Building4you.md`: edytowalna lista 16 ustaleń i zaleceń.
- `ustalenia.json`: te same ustalenia w formacie do dalszego przetwarzania.
- `dowody/`: zapisane odpowiedzi publicznej strony, nagłówki, indeks kodu i zasobów, pomiary DOM oraz zrzuty ekranu.
- `narzedzia/`: skrypty użyte do zebrania i zestawienia danych. Wymagają Pythona oraz bibliotek requests i beautifulsoup4. Ich uruchomienie ponownie pobiera publiczne strony; wyniki opisują nowy stan, nie historyczny stan z dnia audytu.

Zakres: 72 końcowe podstrony HTTPS oraz próbka 351 zasobów sprawdzonych metodą HEAD. Odpowiedzi stron zebrano w plikach pages.json i pages-secondary.json. Dane te zawierają również przekierowania i dwa adresy kontrolne z 404. Nie jest to pełna inwentaryzacja całej witryny.

P1 oznacza zadanie pilne. P1* oznacza zadanie pilne warunkowo, jeśli kampanie reklamowe są aktywne lub mają zostać uruchomione. P2 oznacza kolejny cykl wdrożenia, a P3 planowe usprawnienia. Raport odróżnia usterki od rekomendacji i zadań wymagających dostępu.

Audyt miał charakter zewnętrzny i tylko do odczytu. Nie wykonano zmian na stronie, nie wysłano formularzy ani wiadomości. Bez dostępu do backendu i kont reklamowych nie można potwierdzić bezpieczeństwa serwera, dostarczania poczty i wyników kampanii. PageSpeed API zwróciło 429, dlatego raport nie podaje wyniku Lighthouse ani Core Web Vitals.

Pliki o nazwach złożonych z 12 znaków szesnastkowych to odpowiedzi pobranych adresów. Ich powiązanie z URL znajduje się w indeksach JSON. Rozszerzenie .txt nie oznacza, że odpowiedź była zwykłym tekstem; zapisy obejmują HTML, JS, CSS i XML.
