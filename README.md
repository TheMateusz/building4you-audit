# Building4you — audyt strony internetowej

Studium audytu zewnętrznego strony Building4you.pl z 27 października 2026: analiza techniczna, UX, SEO i wydajności, priorytety zmian oraz raporty dla klienta i programisty. Skrypty Python zbierają publiczne odpowiedzi HTTP i zestawiają materiał dowodowy.

## Zacznij od raportów

- [Raport dla klienta — v2.1](output/pdf/Building4you-raport-dla-klienta-2026-10-27-v2.1.pdf)
- [Raport dla programisty — v2.1](output/pdf/Building4you-raport-dla-programisty-2026-10-27-v2.1.pdf)
- [Audyt zbiorczy — v1.1](output/pdf/Building4you-audyt-2026-10-27-v1.1.pdf)
- [Lista zmian i kryteria odbioru](Lista-zmian-Building4you.md)
- [Ustalenia techniczne w JSON — v2.1](ustalenia-techniczne-v2.1.json)

## Zakres i metoda

Zebrano 72 końcowe podstrony HTTPS oraz próbkę 351 zasobów sprawdzonych metodą HEAD. Materiał obejmuje nagłówki, HTML, pomiary DOM, zrzuty ekranu i weryfikację ustaleń. Wyniki są historycznym zapisem obserwacji; nie opisują automatycznie aktualnego stanu strony.

Raporty zachowują kolejne wersje. Dokumenty v2.1 oraz [opis weryfikacji](verification/README.md) zawierają późniejsze doprecyzowania; [aktualizacja v1.1](README-v1.1.md) uzupełnia raport bazowy o PageSpeed i porównanie archiwalne. Pełna ocena wydajności PageSpeed nie powstała z powodu NO_LCP — nie oznacza to wyniku 0/100.

Audyt był zewnętrzny i tylko do odczytu: bez dostępu do panelu, wysyłania formularzy i zmian w witrynie. Braki nagłówków nie są dowodem wykorzystania podatności. Nie ustalono autorstwa ani daty historycznych zmian. [Pierwotny opis pakietu](README-raport.md) dokumentuje pierwszą wersję i jej ograniczenia.

## Struktura

| Ścieżka | Zawartość |
| --- | --- |
| `output/pdf/` | Gotowe raporty PDF i ich wcześniejsze wersje |
| `dowody/` | Odpowiedzi publicznej strony, indeksy i pomiary |
| `porownanie/` | Materiał porównawczy i PageSpeed |
| `verification/` | Powtórna weryfikacja, zrzuty i podsumowanie |
| `audit_*.py`, `compare_collect.py`, `verify_findings.py` | Zbieranie i analiza danych |
| `build_*.py` | Generowanie raportów PDF |

## Narzędzia

Python 3.10+:

```powershell
python -m venv .venv
.venv\Scripts\python -m pip install -r requirements.txt
.venv\Scripts\python build_audience_reports.py
```

Generatory korzystają z fontów Arial w `C:/Windows/Fonts/`; na innych systemach trzeba wskazać własne pliki fontów obsługujących polskie znaki. Zapisane raporty można czytać bez instalowania zależności.

Ponowne uruchomienie skryptów zbierających dane wysyła żądania do publicznej witryny i zapisuje nowe wyniki. Do kolejnego audytu użyj osobnej kopii katalogu, aby zachować dowody historyczne. Lokalne pliki tymczasowe i pobrana przeglądarka nie należą do repozytorium.

## Autorstwo materiałów

Opracowanie audytu: Mateusz Matusiak ([TheMateusz](https://github.com/TheMateusz)). Treści, znaki i zrzuty audytowanej witryny pozostają materiałami ich właścicieli; zapisano je jako dowody analizy. Repozytorium nie deklaruje autorstwa audytowanej strony.
