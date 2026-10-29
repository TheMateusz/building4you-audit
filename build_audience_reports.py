from pathlib import Path
import json,html
from reportlab.platypus import SimpleDocTemplate,Paragraph,Spacer,Table,TableStyle,PageBreak,Image
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from PIL import Image as PILImage
from pypdf import PdfReader

R=Path(__file__).parent; O=R/'output'/'pdf'; O.mkdir(parents=True,exist_ok=True)
F=json.loads((R/'ustalenia.json').read_text(encoding='utf-8'))
review=json.loads((R/'verification/verification-summary.json').read_text(encoding='utf-8'))
for name,file in [('Body','arial.ttf'),('Bold','arialbd.ttf')]:pdfmetrics.registerFont(TTFont(name,'C:/Windows/Fonts/'+file))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='Bold',italic='Body',boldItalic='Bold')
ink=colors.HexColor('#172b45');accent=colors.HexColor('#b9213b');light=colors.HexColor('#eef3f8');gray=colors.HexColor('#536174')
class Report:
 def __init__(self,audience,client=False):
  self.audience=audience;self.flow=[];self.client=client
  self.styles={k:ParagraphStyle(k,fontName='Bold' if k.startswith('h') else 'Body',fontSize=fs,leading=ld,textColor=ink,spaceAfter=sp) for k,fs,ld,sp in [('body',11 if client else 9.4,16 if client else 14,10),('small',9 if client else 8,13 if client else 11.5,7),('h1',26,31,19),('h2',15 if client else 13.5,20 if client else 18,11)]}
 def p(self,t,k='body'):
  return Paragraph(html.escape(t.replace('–','-').replace('—','-')),self.styles[k])
 def add(self,t,k='body'):self.flow.append(self.p(t,k))
 def field(self,label,t):self.flow.append(Paragraph('<b>'+html.escape(label)+':</b> '+html.escape(t.replace('–','-').replace('—','-')),self.styles['body']))
 def page(self):self.flow.append(PageBreak())
 def table(self,rows,widths):
  t=Table([[self.p(str(c),'small') for c in row] for row in rows],colWidths=widths,hAlign='LEFT',repeatRows=1)
  t.setStyle(TableStyle([('VALIGN',(0,0),(-1,-1),'TOP'),('BACKGROUND',(0,0),(-1,0),light),('LINEBELOW',(0,0),(-1,0),.8,ink),('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#d8e1e9')),('LEFTPADDING',(0,0),(-1,-1),8),('RIGHTPADDING',(0,0),(-1,-1),8),('TOPPADDING',(0,0),(-1,-1),8),('BOTTOMPADDING',(0,0),(-1,-1),8)]));self.flow.append(t)
 def footer(self,c,d):
  c.saveState();w,h=A4;c.setStrokeColor(accent);c.setLineWidth(2);c.line(50,h-35,w-50,h-35);c.setFont('Body',7);c.setFillColor(gray);c.drawString(50,27,'BUILDING4YOU | '+self.audience+' | 27.10.2026 | v2.1 - po weryfikacji');c.drawRightString(w-50,27,str(d.page));c.restoreState()
 def build(self,name):
  path=O/name;SimpleDocTemplate(str(path),pagesize=A4,leftMargin=50,rightMargin=50,topMargin=53,bottomMargin=48,title='Building4you - '+self.audience,author='Audyt publicznej strony').build(self.flow,onFirstPage=self.footer,onLaterPages=self.footer);return path

# CLIENT: plain language, grouped by decisions and effects rather than technologies.
C=Report('Raport dla klienta',True)
C.add('Ocena strony Building4you','h1')
C.add('Raport dla klienta | 27 października 2026 | Po ponownej weryfikacji','small')
C.add('Strona działa, ale wymaga poprawek w nawigacji, zabezpieczeniu połączenia i przygotowaniu do reklam.','h2')
C.add('Odwiedzający mogą przeglądać ofertę, realizacje i dane kontaktowe. Potwierdziliśmy jednak konkretne utrudnienia: zmienione menu, powtarzające się fragmenty oferty i elementy stopki, które wychodzą poza ekran małego telefonu.')
C.add('Od czego zacząć','h2')
for title,desc in [ ('1. Zapewnić zawsze szyfrowane połączenie','Strona ma certyfikat, ale wejście przez starszy, nieszyfrowany adres nie przełącza automatycznie na bezpieczne połączenie. To najpilniejsza potwierdzona poprawka.'),('2. Uporządkować menu i drogę do wyceny','W porównaniu ze starszą wersją z menu zniknęły dwa odnośniki, w tym Szybka wycena. Trzeba ustalić, czy była to zamierzona zmiana, i przywrócić potrzebne funkcje.'),('3. Potwierdzić pomiar zapytań przed reklamami','Nie wykryliśmy widocznego podłączenia popularnych narzędzi analitycznych. Bez sprawdzenia kont nie wiadomo, czy firma może rzetelnie oceniać skuteczność kampanii.')]:
 C.add(title,'h2');C.add(desc)
C.add('Badanie obejmowało 72 podstrony oraz próbkę 351 plików strony. Wszystkie badane podstrony z treścią były dostępne przez bezpieczny adres. Nie potwierdzono włamania; przegląd publicznej strony nie obejmuje pełnego bezpieczeństwa serwera.','small')
C.page()
C.add('Co potwierdziła ponowna kontrola','h1')
C.add('Podmenu O nas rzeczywiście wygląda na puste','h2')
C.add('Na górze strony napisy O firmie i Referencje są białe na białym tle. Odnośniki istnieją, ale ich nie widać. Po przewinięciu strony zmieniają się na ciemne i stają się czytelne. To konkretny błąd wyglądu wymagający naprawy.')
C.flow.append(Image(str(R/'verification/menu-open.png'),width=495,height=279))
C.add('Pozostałe potwierdzone problemy','h2')
C.add('Ponowny przegląd potwierdził nieszyfrowane wejście bez automatycznego przełączenia na bezpieczne, powielone akapity w ofercie, brak opisów stron oraz stopkę wychodzącą poza ekran małego telefonu.')
C.add('Co jest zaleceniem, a nie dowiedzioną awarią','h2')
C.add('Brak formularza kontaktowego nie oznacza, że formularz się zepsuł. Niewykrycie narzędzi analitycznych w kodzie nie dowodzi braku pomiaru na kontach reklamowych. Zmiany względem maja nie dowodzą awarii z ostatniego tygodnia. Takie rozróżnienia zachowano w tym raporcie.','small')
C.page()
C.add('Co zmieniło się w menu','h1')
C.add('Porównaliśmy obecną stronę ze znalezioną kopią z 13 maja 2026. Zmiany w strukturze menu można potwierdzić mimo braków części archiwalnych plików wyglądu.')
C.table([['Element','Starsza wersja','Obecna wersja'],['Menu główne','8 pozycji, w tym Szybka wycena i Rekrutacja.','6 pozycji; brakuje obu wymienionych odnośników.'],['Oferta w menu','Rozwijana lista 9 usług.','Odnośnik do oferty bez rozwijanej listy usług.'],['Menu na telefonie','Przewidziano otwierany panel menu.','Linki są stale widoczne i układają się w dwóch rzędach.'],['Wygląd napisów','Inny krój i rozmiar liter w zachowanych plikach projektu.','Mniejsze napisy, inne odstępy i sposób ułożenia.']],[105,195,195])
C.add('Tak wygląda obecne menu telefonu','h2')
im=PILImage.open(R/'porownanie'/'current-mobile.png'); im.crop((0,0,im.width,210)).save(R/'porownanie'/'menu-client-crop.png')
C.flow.append(Image(str(R/'porownanie'/'menu-client-crop.png'),width=300,height=300*210/im.width))
C.add('Ważne ograniczenie porównania','h2')
C.add('Nie znaleźliśmy publicznej kopii z ostatniego miesiąca, czyli z 27 września-20 października. Kopia majowa jest starsza, a część jej plików wyglądu nie jest dostępna. Nie można więc rzetelnie ustalić, kiedy zmieniono menu ani odtworzyć całego dawnego wyglądu na podstawie samego archiwum. Najlepszym wzorcem będzie kopia strony z hostingu sprzed zmian.','small')
C.page()
C.add('Zalecane zmiany: kolejność prac','h1')
C.add('Pilne','h2')
C.table([['Co zrobić','Dlaczego'],['Zawsze kierować na szyfrowaną stronę.','Każdy odwiedzający powinien od początku korzystać z chronionego połączenia.'],['Naprawić nieczytelne podmenu O nas i uzgodnić dostęp do wyceny.','Białe napisy na białym tle to potwierdzony błąd. Przywrócenie usuniętych pozycji wymaga ustalenia, czy były potrzebne i usunięto je niezamierzenie.'],['Potwierdzić pomiar zapytań, jeśli działają lub ruszają reklamy.','Firma powinna wiedzieć, które działania przynoszą rzeczywiste kontakty. Samo kliknięcie numeru telefonu nie oznacza rozmowy.']],[250,245])
C.add('W następnym etapie','h2')
C.table([['Co zrobić','Oczekiwany efekt'],['Poprawić menu i stopkę na małych ekranach.','Czytelne linki i przyciski mieszczące się na ekranie.'],['Usunąć powtarzające się fragmenty oferty.','Krótsza, spójna i łatwiejsza do przeczytania oferta.'],['Dodać wyraźne zaproszenie do kontaktu przy usługach.','Użytkownik po przeczytaniu oferty wie, co zrobić dalej. Formularz jest opcją do uzgodnienia.'],['Uzupełnić opisy stron w wyszukiwarce i uporządkować ich adresy.','Spójniejsza prezentacja oferty w wynikach wyszukiwania. Nie jest to gwarancja wzrostu pozycji.'],['Uzupełnić zabezpieczenia przeglądarki.','Dodatkowa warstwa ochrony odwiedzających. Nie stwierdzono wykorzystania tych braków do ataku.']],[250,245])
C.page()
C.add('Szybkość i wygoda korzystania','h1')
C.add('Powtórzyliśmy test Google i wykonaliśmy niezależne pomiary. Szybkość można zbadać, choć Google nadal nie wyznacza pełnego wyniku strony głównej w swojej konfiguracji.')
C.table([['Obszar','Wynik','Co to oznacza'],['Wydajność strony głównej','Google: brak; lokalnie: 73-75/100','Dwa lokalne pomiary Lighthouse wyznaczyły wynik. Google nie zarejestrował chwili pojawienia się największej treści.'],['Wydajność strony kontaktowej','Google: 98/100','Test kontrolny zadziałał. Problem pomiaru nie obejmuje wszystkich podstron.'],['Dostępność strony głównej','96/100','Część testów automatycznych. Nadal potrzebne są poprawki i sprawdzenie ręczne.'],['Dobre praktyki techniczne','100/100','Wynik ograniczonego zestawu testów, bez gwarancji pełnego bezpieczeństwa.'],['Podstawy widoczności w Google','92/100','Test wskazał brak opisów stron. Ocena nie określa pozycji w wyszukiwarce.']],[140,95,260])
C.add('Co warto poprawić','h2')
C.add('Strona główna pobrała w testach około 10 megabajtów danych. Znaczną część stanowią zdjęcia i film w tle. Warto ograniczyć ich rozmiary i przygotować lżejszy widok telefonu. Dokładnego wpływu na liczbę zapytań nie zmierzono.')
C.add('Lokalny test w warunkach symulowanego wolniejszego połączenia wskazał około 8,3 sekundy do pojawienia się największej treści. To wynik jednego rodzaju testu, nie czas każdego użytkownika. Różnica między narzędziami zależy od konfiguracji przeglądarki; nie udało się przypisać błędu Google konkretnej instrukcji w kodzie.')
C.add('Należy poprawić czytelność napisów, umożliwić zatrzymanie ciągłych animacji i zadbać o stabilne ułożenie obrazów. Strona już ukrywa film dla osób z włączonym systemowym ograniczeniem animacji; ta ochrona wymaga uzupełnienia, a nie wdrożenia od zera.','small')
C.add('Pozostałe sprawy do zaplanowania','h2')
C.add('Newsletter jest obecnie jawnie wyłączony. Trzeba zdecydować, czy go uruchomić, czy usunąć nieaktywny element. Przed dodaniem narzędzi reklamowych, newslettera lub formularza należy sprawdzić zgodność informacji o prywatności z faktycznym działaniem strony. W dalszej kolejności warto uporządkować kod i dodatkowe opisy strony dla wyszukiwarek.')
C.page()
C.add('Jak odebrać wykonane poprawki','h1')
C.add('Proponowany podział prac','h2')
C.table([['Etap','Zakres'],['Najpierw','Szyfrowane połączenie, decyzja o menu i wycenie, sprawdzenie pomiaru reklam.'],['Następnie','Telefony, treść oferty, kontakt, opisy w Google i dodatkowe zabezpieczenia.'],['Po poprawkach','Ograniczenie ciężaru strony, wygoda korzystania, pomiar kontrolny oraz decyzja o newsletterze.']],[115,380])
C.add('Lista kontrolna dla klienta','h2')
for t in ['Na telefonie i komputerze widać wszystkie uzgodnione pozycje menu; przyciski nie wychodzą poza ekran.', 'Z każdej ważnej oferty łatwo przejść do kontaktu lub wyceny. Numery telefonu i adres e-mail są poprawne.', 'W ofercie nie ma przypadkowo powtórzonych fragmentów. Teksty są czytelne i można zatrzymać animacje.', 'Wykonawca pokazuje wynik testu po poprawkach i potwierdza działanie zabezpieczenia połączenia.', 'Jeśli działają reklamy, osoba odpowiedzialna za marketing pokazuje kontrolowany test rejestracji rzeczywistego zapytania.']:
 C.add('• '+t)
C.add('Co wymaga dodatkowego dostępu','h2')
C.add('Przegląd obejmował stronę widoczną publicznie. Do oceny serwera, kopii zapasowych, działania poczty i kont reklamowych potrzebny jest dostęp do odpowiednich systemów. Nie wysyłaliśmy wiadomości ani zgłoszeń. Nie wprowadziliśmy zmian na stronie.','small')
C.add('Szczegółowe dowody, wskazówki dla wykonawcy i warunki technicznego odbioru znajdują się w osobnym raporcie dla programisty. Orientacyjna kolejność nie jest wyceną ani gwarantowanym terminem wykonania.','small')
client=C.build('Building4you-raport-dla-klienta-2026-10-27-v2.1.pdf')

# DEVELOPER: one coherent current document, without superseded limitations.
extra=[
 dict(id='REG-01',priority='P1*',title='Brakujące pozycje menu i podmenu Oferta',status='Potwierdzona różnica historyczna; intencja zmiany nieustalona',evidence='Archiwalny HTML z 13.05.2026: 8 pozycji głównych; Szybka Wycena i Rekrutacja. Oferta ma 9 odnośników w .dj-subwrap. Obecny header ma 6 pozycji, a Oferta nie ma dzieci. Źródło: porownanie/comparison.json oraz oba HTML.',impact='Możliwa utrata istotnej ścieżki zapytania i łatwego wyboru usług. Zmiany mogą być celowe; sam zakres różnic nie dowodzi błędu migracji ani daty wdrożenia.',action='Uzgodnić docelowy model nawigacji, potem odtworzyć potrzebne pozycje w menu WordPress. Wycena powinna prowadzić do zaakceptowanego procesu, a nie obiecywać nieistniejącej funkcji. Nie instalować starego pluginu Joomla w WordPressie.',accept='Lista i kolejność pozycji, cele CTA oraz komplet usług zaakceptowane; wszystkie cele działają. P1 tylko przy potwierdzonej niezamierzonej regresji lub istotnym wpływie na zapytania.',owner='UX / właściciel / WordPress',effort='3-8 h po ustaleniu zakresu'),
 dict(id='REG-02',priority='P2',title='Zmiana mobilnej nawigacji z offcanvas na zawijane linki',status='Potwierdzona różnica struktury',evidence='Dawny HTML zawiera .dj-mobile-open-btn, .dj-offcanvas i menu mobilne. Obecny header nie ma przycisku ani panelu. Przy 390 px linki są w dwóch rzędach; header ma ok. 155 px. Dowód: current-header-mobile.json.',impact='Większy nagłówek zajmuje część ekranu i nie zachowuje dawnego modelu obsługi. Nie oznacza to, że wszystkie linki przestały działać.',action='Jeśli celem jest odtworzenie dawnej obsługi, zbudować panel z button, aria-expanded, aria-controls, zamykaniem Escape i sensownym zarządzaniem fokusem. Zapewnić dostęp do podmenu bez hover.',accept='320/390/768 px, klawiatura i dotyk: wszystkie linki dostępne, panel można otworzyć i zamknąć, brak nakładania na treść. Przywracany jest uzgodniony model, nie tylko wygląd.',owner='Frontend',effort='4-10 h'),
 dict(id='REG-03',priority='P2',title='Typografia i odstępy nagłówka nie odpowiadają starszemu projektowi',status='Potwierdzone różnice; wzorzec archiwalny niekompletny',evidence='Computed style obecnego menu: Arial/Helvetica, 12 px, weight 750, padding 17 px 14 px. Zachowany arkusz DJ deklaruje proxima_nova_condensedSBd 16 px. Archiwum CSS tego pliku pochodzi z 2023 r.; custom.css użyty w HTML majowym jest niedostępny.',impact='Krój i rozmiar liter, wysokość i układ menu wyglądają inaczej. Bez kompletnego wzorca nie można dowieść dokładnej dawnej geometrii.',action='Pozyskać projekt lub backup sprzed zmian. Ujednolicić font-face, rozmiary, odstępy, breakpointy i stan nagłówka po scrollu. Nie podmieniać całego CSS na archiwalne pliki bez kontroli zgodności DOM.',accept='Zaakceptowane porównania 320/390/768/1280 px oraz stany: początek strony, scroll, dropdown, fokus. Sprawdzone ładowanie fontów i brak regresji w podstronach.',owner='Frontend / projektant',effort='4-10 h'),
 dict(id='PSI-01',priority='P2',title='Powtarzalny NO_LCP uniemożliwia pełny wynik wydajności',status='Potwierdzony błąd pomiaru; przyczyna nieustalona',evidence='PageSpeed A i B, telefon oraz komputer: LCP i TBT mają NO_LCP; brak wyniku performance. Inne kategorie zwracają 96/100/92. Dowód: porownanie/pagespeed-*-dom.txt.',impact='Nie można ocenić pełnej wydajności ani uznać Core Web Vitals za zaliczone. Nie jest to dowód awarii dla każdego użytkownika ani wynik 0/100.',action='Przeanalizować trace Lighthouse/DevTools oraz stan widoczności elementów hero. Na stagingu porównać statyczny hero, ograniczone animacje i wideo. Oddzielić problem strony od konfiguracji narzędzia. Nie wyłączać funkcji produkcyjnych wyłącznie w celu poprawienia wyniku.',accept='Kompletny pomiar LCP/TBT/performance dla obu profili; powtórzenia przy porównywalnych warunkach. Jeśli problem narzędzia się utrzymuje, udokumentować przyczynę i niezależny pomiar.',owner='Frontend / wydajność',effort='3-8 h diagnostyki'),
 dict(id='PSI-02',priority='P2',title='Uzupełnienie audytu o transfer, kontrast i wymiary obrazów',status='Sygnały z testu; szczegóły wymagają kontroli elementów',evidence='Transfer 9 239-10 621 KiB. Szacunek redukcji obrazów mobile: 1781 i 459 KiB; desktop: 1610 KiB. PSI wskazuje kontrast oraz brak jawnych width/height; część innych audytów ma błąd pomiaru.',impact='Duże multimedia mogą utrudniać korzystanie przy wolnym połączeniu. Zły kontrast zmniejsza czytelność. Sam brak width/height nie dowodzi przesunięć, gdy miejsce rezerwuje poprawny CSS.',action='Rozszerzyć PERF-01/02 o dane PSI. Zidentyfikować konkretne węzły z audytu kontrastu i sprawdzić je ręcznie. Ustawić wymiary lub aspect-ratio tam, gdzie brakuje rezerwacji miejsca. Błędów wykonania audytu nie oznaczać jako potwierdzonych wad minifikacji.',accept='Kontrola transferu przed/po, mniejszy payload, naprawione wskazane kontrasty i stabilny layout; pełny retest po wyjaśnieniu NO_LCP.',owner='Frontend / dostępność',effort='2-6 h dodatkowo; bez podwójnego liczenia PERF-01/02')]
for f in F:
 if f['id']=='A11Y-01':
  f['evidence']='Film ma autoplay/loop bez controls; brak przycisku pauzy. home.js uruchamia Typed.js bez kontroli prefers-reduced-motion. Korekta: home.css już zawiera @media (prefers-reduced-motion:reduce), które ukrywa element wideo. JS nadal próbuje wywołać play(); wpływu na transfer w tym trybie nie zmierzono.'
  f['action']='Zachować istniejącą regułę ukrywającą wideo. Dodać pauzę/wznowienie, ograniczyć animację Typed.js i sprawdzić, czy ukryty film jest nadal pobierany lub odtwarzany. Przetestować klawiaturę i ustawienia ruchu systemu.'
 if f['id']=='CODE-02':
  f['impact']='Warstwy nadpisań utrudniają utrzymanie. Nowy UX-04 potwierdza konkretny konflikt kolorów. Nie wykazano, że każde nadpisanie jest błędem, ani że sama liczba !important stanowi podatność.'
for f in extra:
 if f['id']=='PSI-01':
  f['title']='NO_LCP w PageSpeed; lokalny pomiar wydajności działa'
  f['evidence']='Ponowny PSI strony głównej: NO_LCP. Kontakt PSI: 98/100, LCP 1,6 s. Lokalny Lighthouse 13.5.0 + Chrome 156: 73 i 75/100, LCP ok. 8,3 s. Chrome-headless-shell 153.0.8010.36: główna NO_LCP, kontakt 100/100. verification/verification-summary.json oraz raporty i trace.'
  f['impact']='PSI nie otrzymuje użytecznego LCP w swojej konfiguracji, więc nie oblicza pełnej oceny. Nie oznacza to, że strony nie da się zmierzyć. Lokalny wynik jest odrębnym benchmarkiem, nie wynikiem Google ani terenowym CWV.'
  f['action']='Porównać zapis zdarzeń LCP w wersjach i konfiguracjach Chromium. Nie przypisywać winy wyłącznie filmowi lub Typed.js: lokalne blokowanie każdego osobno i razem nie usunęło NO_LCP na Chrome153. Dalsza izolacja wymaga kontrolowanych zmian renderowania na stagingu.'
  f['accept']='Utrzymać powtarzalny pomiar lokalny i docelowo uzyskać poprawny PSI. Każdy wynik opisać wersją silnika, profilem i warunkami. Naprawa przyczyny ma być potwierdzona testem, nie tylko wyższą punktacją.'
  f['status']='Pomiar zaktualizowany; dokładna przyczyna w kodzie nieustalona'
allf=F+extra
allf.append(dict(id='UX-04',priority='P2',title='Białe napisy na białym tle podmenu O nas',status='Potwierdzony błąd w przeglądarce',evidence='Na początku strony: podmenu widoczne, linki O firmie i Referencje mają rgb(255,255,255), tło również rgb(255,255,255), kontrast 1:1. Po scrollY=419 px napisy zmieniają się na rgb(34,34,34). Zapis verification/menu-open.json, menu-after-scroll.json i screenshot menu-open.png.',impact='Rozwinięta lista wygląda na pustą; odwiedzający nie widzi, jakie odnośniki ma wybrać. To rzeczywisty błąd niezależny od niekompletnego porównania archiwalnego.',action='W b4y-home/home.css reguła body.home:not(.b4y-home-scrolled) .b4y-menu a nadaje #fff !important wszystkim potomnym linkom. Zawęzić ją do linków najwyższego poziomu, np. .b4y-menu > li > a, i ustawić kolory dropdownu jawnie. Sprawdzić także hover/focus i wersję mobilną.',accept='Przed i po scrollu linki podmenu mają czytelny kontrast. Klawiatura i dotyk pozwalają wybrać oba cele. Stan hover/focus jest czytelny. Dowód odbioru: screenshot i computed styles.',owner='Frontend',effort='1-2 h + test regresji'))
classifications={x['id']:x for x in review['review']}
for f in allf:f['verification']=classifications[f['id']]
order={'P1':0,'P1*':1,'P2':2,'P3':3}
allf=sorted(allf,key=lambda x:order[x['priority']])
(R/'ustalenia-techniczne-v2.1.json').write_text(json.dumps(allf,ensure_ascii=False,indent=2),encoding='utf-8')
T=Report('Raport dla programisty')
T.add('Audyt techniczny Building4you','h1')
T.add('Raport dla programisty | 27.10.2026 | Wersja 2.1 po weryfikacji','small')
T.add('Zakres i główne wnioski','h2')
T.add('Sprawdzono 72 różne końcowe podstrony HTTPS, 351 zasobów metodą HEAD, publiczny HTML, nagłówki HTTP/TLS, 9 skryptów aplikacji i wybrane CSS. Testy przeglądarkowe obejmowały stronę główną, kontakt, usługę oraz referencje. Dokument łączy audyt, porównanie archiwalne i dwa przebiegi PageSpeed bez odsyłania do wcześniejszych wersji.')
T.add('22 pozycje backlogu: 1 P1, 2 P1 warunkowo, 15 P2 i 4 P3. Lista łączy potwierdzone błędy, braki konfiguracji, zalecenia i różnice historyczne. Nie są to 22 dowiedzione awarie. Najpierw SEC-01, potem UX-04 i warunkowe MKT-01/REG-01. Priorytet jest oceną operacyjną, nie CVSS; nakładów zadań wspólnych nie sumować mechanicznie.')
T.add('Stan pozytywny','h2')
T.add('Badane podstrony treści: 200. Próbka 351 zasobów: 200 i właściwe typy. Główne stare .html mają działające przekierowania. robots.txt wskazuje wp-sitemap.xml; adres kontrolny zwraca 404. Certyfikat poprawny, TLS 1.3, koniec ważności 4.12.2026 - potwierdzić automatyczne odnowienie. Nie odtworzono wcześniejszego 403; przyczyna pozostaje nieustalona.')
T.add('Granice weryfikacji','h2')
T.add('Bez repozytorium, PHP, bazy, hostingu, panelu WordPress, Search Console i kont reklamowych. Nie wykonano testów penetracyjnych, logowania, wysyłek ani testów obciążeniowych. Brak błędów konsoli w próbce nie jest gwarancją dla całej witryny. Nie potwierdzono włamania ani kompletności zabezpieczeń backendu.')
T.add('Archiwum: 27.09-20.10.2026 bez znalezionej kopii. Porównanie z 13.05.2026 jest starszym punktem odniesienia; custom.css archiwum zwraca 404. Pozostałe pobrane CSS są odtwarzane z kopii 2023. Nie wykonano wiarygodnego porównania piksel w piksel i nie ustalono daty migracji.','small')
T.page()
T.add('Wynik ponownej weryfikacji','h1')
T.table([['Zakres','Wynik / klasyfikacja'],['72 podstrony i 351 HEAD','Wszystkie ponownie 200. HTML głównej identyczny bajtowo z poprzednim zapisem. HEAD nie potwierdza integralności całej zawartości pliku.'],['Metadane i treść','72 bez description, 10 bez canonical, 0 JSON-LD. Duplikaty ponownie na 3 wskazanych stronach.'],['HTTP i nagłówki','HTTP nadal 200 bez wymuszenia HTTPS; wskazane nagłówki ochronne nadal nieobecne.'],['Menu O nas','Nowy potwierdzony UX-04: biały tekst na białym tle, po scrollu tekst ciemny. Konkretna reguła CSS zbyt szeroko obejmuje potomków.'],['Stopka 320 px','Ponownie clientWidth 305, scrollWidth 329. To realne przepełnienie.'],['Reklamy / formularz / archiwum','Brak tagów publicznych nie dowodzi braku pomiaru. Brak formularza to wybór funkcjonalny. Zmiana względem maja nie datuje regresji na ostatni tydzień.'],['Ograniczenie animacji','Korekta A11Y-01: CSS już ukrywa film dla prefers-reduced-motion. Nadal brak pauzy i ograniczenia Typed.js.'],['Wydajność','PSI głównej NO_LCP; PSI kontakt 98. Dwa lokalne pomiary głównej Chrome156: 73/75, LCP ok. 8,3 s.']],[130,365])
T.add('Macierz każdej pozycji znajduje się w verification/verification-summary.json oraz ustalenia-techniczne-v2.1.json. Status dowodu nie jest tożsamy z priorytetem biznesowym.','small')
T.page()
T.add('Backlog według priorytetu','h1')
T.add('P1: pilne. P1*: pilne tylko po potwierdzeniu warunku. P2: następny cykl. P3: planowe usprawnienie. Dla każdej pozycji dalej podano dowód, skutek, zmianę i kryterium odbioru.','small')
T.table([['ID','Priorytet','Zadanie']]+[[x['id'],x['priority'],x['title']] for x in allf],[75,60,360])
T.page()
for i in range(0,len(allf),2):
 T.add('Ustalenia i wskazówki do wdrożenia','small')
 for f in allf[i:i+2]:
  T.add(f['id']+' | '+f['priority']+' | '+f['title'],'h2')
  T.add(f['status']+' | '+f['owner']+' | Nakład orientacyjny: '+f['effort'],'small')
  T.add('Po weryfikacji: '+f['verification']['classification'],'small')
  for label,key in [('Dowód','evidence'),('Skutek','impact'),('Zmiana','action'),('Odbiór','accept')]:T.field(label,f[key])
  T.flow.append(Spacer(1,11))
 T.page()
T.add('PageSpeed: dane z dwóch przebiegów','h1')
T.add('A: 27.10.2026 ok. 11:06 CET; B: ok. 11:08 CET. Lighthouse 13.5.0, mobilnie Moto G Power / 4G. API zwracało 429, ale publiczny interfejs wykonał testy. Brak danych CrUX.','small')
T.table([['Metryka','Mobile A','Mobile B','Desktop A','Desktop B'],['Performance','brak','brak','brak','brak'],['FCP','1,2 s','1,2 s','0,3 s','0,3 s'],['LCP / TBT','NO_LCP','NO_LCP','NO_LCP','NO_LCP'],['CLS','0,054','0,070','0,081','0,081'],['Speed Index','2,4 s','1,2 s','0,3 s','0,4 s'],['Payload','10524 KiB','9239 KiB','10621 KiB','10621 KiB'],['Accessibility','96','96','96','96'],['Best practices','100','100','100','100'],['SEO','92','92','92','92']],[115,95,95,95,95])
T.add('Ograniczenia interpretacji','h2')
T.add('NO_LCP powtarza się w obu profilach i przebiegach. Nie obliczać performance samodzielnie z pozostałych liczb. FCP/SI nie zastępują LCP, a laboratoryjny CLS nie dowodzi zaliczenia terenowych CWV. Część audytów minifikacji i nieużywanego kodu ma błąd wykonania. Best practices 100 nie potwierdza kompletności ochrony HTTP/CSP/HSTS.')
T.add('Szacunek optymalizacji obrazów: mobile 1781/459 KiB, desktop 1610 KiB. Zmienność testu i optymalizacja CDN mają znaczenie; nie deklarować klientowi stałej oszczędności ani wzrostu konwersji bez pomiaru.')
T.page()
T.add('Dlaczego PageSpeed nie oblicza wyniku','h1')
T.add('Na poziomie pomiaru: brak użytecznego zdarzenia LCP','h2')
T.add('Lighthouse potrzebuje czasu wyrenderowania największej treści. W zapisie Chrome153 dla strony głównej brakuje observedLargestContentfulPaint, a analiza zgłasza NO_LCP. Strona odpowiada 200 i renderuje treść; nie jest to ten sam problem co wcześniejsze 403 ani limit 429 API.')
T.table([['Test','Wynik','Wniosek'],['PSI główna, kolejny przebieg','NO_LCP','Problem odtworzony w Google.'],['PSI kontakt, test kontrolny','98/100; LCP 1,6 s','Ten sam serwis Google mierzy inną podstronę.'],['Lighthouse 13.5 + Chrome156','73 i 75; LCP 8,26 s','Pełny wynik głównej jest możliwy w lokalnej konfiguracji.'],['Lighthouse 13.5 + headless153','Główna NO_LCP; kontakt 100','Odtworzono zależność od strony i konfiguracji silnika.'],['Headless153, blokady lokalne','Bez Typed.js, bez filmu i bez obu: nadal NO_LCP','Te próby nie uzasadniają wskazania jednego z tych skryptów jako wyłącznej przyczyny.']],[160,140,195])
T.add('Co ustalono, a czego nie','h2')
T.add('Potwierdzona jest zależność od sposobu rejestrowania/interpretacji LCP w konkretnej konfiguracji Chromium. Silniki 153 i 156 oraz otoczenie testu różnią się, dlatego nie przypisuje się przyczyny wyłącznie numerowi wersji. Nie wskazano potwierdzonej pojedynczej instrukcji CSS/JS odpowiedzialnej za NO_LCP. Jej ustalenie wymaga kontrolowanej izolacji renderowania na stagingu.')
T.add('Lokalne wyniki 73/75 są benchmarkiem laboratoryjnym na tym komputerze, ze standardową symulacją mobilną Lighthouse. Nie są wynikiem PSI, wynikiem desktopowym ani terenowym CWV. Wyników wariantów z blokadami zasobów nie wolno publikować jako oceny niezmienionej strony.','small')
T.page()
T.add('Menu: zmiany i kierunek naprawy','h1')
T.table([['Obszar','Starszy HTML / CSS','Stan bieżący'],['Mechanizm','Joomla + DJ-MegaMenu.','WordPress + .b4y-menu.'],['Główne menu','8 pozycji, w tym wycena i rekrutacja.','6 pozycji, bez tych dwóch odnośników.'],['Oferta','9 dzieci w wielokolumnowym podmenu.','Brak dzieci pozycji Oferta.'],['Mobile','Przycisk i panel offcanvas w HTML.','Zawijany flex, 2 rzędy przy 390 px, wysokość header ok. 155 px.'],['Typografia','Zachowany DJ CSS: proxima_nova_condensedSBd 16 px; kopia CSS z 2023.','Computed: Arial 12 px, weight 750, padding 17 px 14 px.'],['Metadane','Na głównej description i OG.','Brak description; regresja tego elementu potwierdzona.']],[85,205,205])
T.add('Wniosek implementacyjny','h2')
T.add('Obecnie nie brakuje wyłącznie stylowania starego DOM - zmieniła się również sama struktura HTML. Potrzebne jest uzgodnienie funkcji oraz odtworzenie nawigacji w aktualnej technologii. Powrót do przypadkowych arkuszy z archiwum może wprowadzić kolejne regresje.')
T.add('Dawny gtag UA-152616077-1 i formularz AcyMailing są obecne w HTML archiwalnym. Nie potwierdza to skuteczności ich historycznego działania. Obecny newsletter jest disabled, a popularnych integracji pomiarowych nie wykryto w próbce. Nie przywracać automatycznie starego identyfikatora pomiarowego.','small')
T.page()
T.add('Odbiór i źródła techniczne','h1')
T.add('Kolejność i zależności','h2')
T.add('Backup z próbą odtworzenia / rollback -> staging -> SEC-01 -> ustalenia CTA i pomiaru -> REG-01/02/03 oraz UX-01/CODE-01 -> zabezpieczenia, metadane i dostępność -> media -> pełny retest. Prywatność i zgody uzgodnić przed nowymi formularzami, newsletterem lub tagami. Po publikacji kontrolować publiczny cache CDN i WordPressa.')
T.add('Minimalna macierz regresji','h2')
T.add('Strona główna, kontakt, oferta i realizacja; szerokości 320/360/390/768/1280 px. Klawiatura i dotyk, fokus i Escape w menu, powiększenie tekstu 200%, prefers-reduced-motion, stany header przed/po scrollu. HTTP/HTTPS/www, 404, przekierowania starych URL z parametrami UTM/gclid. Formularz, jeśli powstanie: walidacja, antyspam, odbiór maila i jedno zdarzenie po skutecznej wysyłce.')
T.add('Indeks dowodów','h2')
for t in ['verification/pages-recheck.json i assets-recheck.json: ponowny odczyt 72 podstron i 351 zasobów. verification-summary.json: macierz weryfikacji 22 pozycji i wyniki 7 pomiarów lokalnych.', 'verification/menu-open.json, menu-after-scroll.json i menu-open.png: kolorystyka nieczytelnego podmenu. narrow-and-duplicate.json: powtórzony test układu i akapitów.', 'verification/lighthouse-*.json oraz pliki trace/devtoolslog: lokalne pomiary. pagespeed-home-dom.txt i pagespeed-contact-dom.txt: nowe wyniki Google.', 'dowody/ i porownanie/: pierwotne zapisy oraz archiwum. ustalenia-techniczne-v2.1.json: aktualny backlog 22 pozycji z klasyfikacją dowodu.']:
 T.add('• '+t,'small')
T.add('Publiczne wyniki i dokumentacja','h2')
for title,url in [('PageSpeed - ponownie główna','https://pagespeed.web.dev/analysis/https-www-building4you-pl/hdu8rg4pxd?form_factor=mobile'),('PageSpeed - kontakt kontrolny','https://pagespeed.web.dev/analysis/https-www-building4you-pl-kontakt/ub4l0psvu6?form_factor=mobile'),('Wayback 13.05.2026','https://web.archive.org/web/20260513010843/https://www.building4you.pl/'),('Google: definicja i pomiar LCP','https://web.dev/articles/lcp'),('MDN HSTS','https://developer.mozilla.org/en-US/docs/Web/HTTP/Reference/Headers/Strict-Transport-Security'),('MDN CSP','https://developer.mozilla.org/en-US/docs/Web/HTTP/Guides/CSP'),('Google canonical','https://developers.google.com/search/docs/crawling-indexing/consolidate-duplicate-urls')]:
 T.flow.append(Paragraph('<b>'+html.escape(title)+'</b><br/><link href="'+url+'" color="#245c96">'+url+'</link>',T.styles['small']))
tech=T.build('Building4you-raport-dla-programisty-2026-10-27-v2.1.pdf')
print('CLIENT',len(PdfReader(str(client)).pages),'TECH',len(PdfReader(str(tech)).pages))
