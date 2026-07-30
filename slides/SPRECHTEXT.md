# Sprechtext — jede Folie, jedes Wort

**Kickoff 30. Juli · dein Block 15:02–15:20 · 16 Folien**

| | |
|---|---|
| **18 Min** | dein Block |
| **16** | Folien |
| **3** | Bildschirmwechsel |
| **4 Min** | Live-Bau |

> ⚠️ **Wenn du in Verzug bist:** Folie 8 (Prompt-Aufbau) überspringen, steht im Infoblatt.
> Danach Folie 14 (Azure DevOps) auf einen Satz kürzen.
> **Folie 9 nie streichen** — der FEHLT-Satz ist der wertvollste Inhalt.

---

# DER EINSATZ

## Woran du anknüpfst

Auf Lisas Folie 2 sagst du nichts. Nur zuhören. Sie endet mit:

> *„Wir wollen herausfinden, welche Agent-Lösungen unseren Arbeitsalltag wirklich erleichtern
> können — und was heute schon machbar ist."*

**🖥 JETZT UMSCHALTEN** — Lisa beendet ihre Freigabe, du teilst dein Deck-Fenster (Vollbild, Folie 1).

> ⚠️ **Lisas Folie 3 entfällt.** Dein Block ersetzt sie vollständig. Das muss sie vorher wissen,
> sonst klickt sie weiter.

---

# TEIL 1 — DER ÜBERBLICK · 15:02–15:06

## Folie 1 · Titel — 40 Sekunden

**Auf der Leinwand:** „Was heute wirklich geht. Und wo genau die Grenze liegt."

> Genau da mache ich weiter — **was ist heute schon machbar**. Ich hab das in den letzten
> Tagen nachgeprüft, nicht aus dem Gedächtnis.
>
> Vier Themen in zwanzig Minuten: die drei Wege, einen Agenten zu bauen. Was der Agent
> Builder wirklich kann und wo er aufhört. Wie ihr in fünf Minuten selbst einen baut.
> Und zwei Beispiele, die laufen.

*Warum „nachgeprüft, nicht aus dem Gedächtnis": Im Raum sitzen Leute, die selbst mit Copilot
arbeiten. Der Halbsatz sagt ihnen, dass sie keine Marketing-Folien bekommen.*

---

## Folie 2 · Drei Wege, einen Agenten zu bauen — 2 Minuten

**Die wichtigste Folie des Blocks.**

> Es gibt drei Wege, und sie werden ständig verwechselt, weil alle drei „Copilot Agent" heißen.
>
> **Der Agent Builder** steckt direkt in M365 Copilot. Ohne Code, jede und jeder mit Lizenz.
> Wissensquellen anbinden, Dateien und Diagramme erzeugen — das alles geht. **Was er heute
> nicht hat, sind Actions**: also selbst etwas schreiben oder eine API rufen. Das ist euer
> Weg heute.
>
> **Der Entwicklerweg** geht über ein Manifest. Der kann tatsächlich schreiben — Mails
> triagieren, Termine anlegen, eigene APIs und Power-Platform-Connectoren einbinden. Braucht
> aber eine Entwicklerin, ein Repo und einen Deploy-Prozess. **Nicht an einem Nachmittag.**
>
> **Copilot Studio** kann alles davon plus Trigger. Ist bei uns aber noch kaum ausgerollt.

> 🔴 **Sag nicht „M365 kann nicht schreiben".** Das stimmt so nicht und jemand im Raum weiß das.
> Richtig ist: **der Agent Builder hat heute keine Actions.** Die Plattform kann es, der
> No-Code-Weg nicht.

*Beleg: Microsoft Learn, „Agent Builder in Microsoft 365 Copilot" und „Agents, Actions, and
Connectors in the Microsoft 365 Ecosystem", abgerufen 30.07.2026. Steht als Quellenzeile auf der Folie.*

---

## Folie 3 · Die harten Zahlen — 90 Sekunden

> Konkret, damit ihr nicht raten müsst: Der Name darf **30 Zeichen** haben, die Beschreibung
> **1.000**, und die Instructions — das eigentliche Gehirn des Agenten — **8.000 Zeichen**.
> Dazu bis zu **20 Wissensquellen**.
>
> 8.000 Zeichen sind viel. Unsere sechs fertigen Prompts im Repo brauchen zwischen 6.100 und
> 6.800 Zeichen. **Ihr habt also noch gut anderthalbtausend Zeichen für eure eigenen Regeln**,
> wenn ihr einen davon als Startpunkt nehmt.
>
> Der **Code-Interpreter** kann rechnen, Daten analysieren und Dateien und Diagramme erzeugen.
> Was er nicht kann: nach außen greifen oder APIs rufen. Das ist eine Sandbox zum Rechnen,
> keine Automatisierungsmaschine.

> ▸ **Der wichtigste Tipp der Folie:** Der „Try it"-Tab, aktiv sobald Name, Beschreibung und
> Instructions stehen. Sag ausdrücklich: **testet früh.** Teams, die erst am Ende testen,
> verlieren zwei Stunden.

---

# TEIL 2 — WAS DAS FÜR DIE TEAMS HEISST · 15:06–15:08

## Folie 4 · Wissensquellen — 75 Sekunden

> Wissensquellen: SharePoint-Inhalte, hochgeladene Dateien, öffentliche Websites — und bei uns
> auch direkt **eure Outlook-Mails und Teams-Chats**. Dafür müsst ihr nichts extra beantragen.
>
> Die Grenze zieht **nicht die Lizenz, sondern die Berechtigung**: Der Agent sieht genau das,
> was ihr selbst sehen dürft. Er umgeht keine Rechte.
>
> Und jetzt der Punkt, der heute Nachmittag die meisten Teams kostet: **Wenn euer Use Case an
> einer Quelle hängt, an die ihr nicht drankommt, ist er tot — und zwar leise.** Ihr merkt es
> erst um 17 Uhr, wenn die Zeit weg ist.
>
> Deshalb: **Prüft in den ersten zehn Minuten, ob ihr die Daten überhaupt öffnen könnt.**
> Wenn nicht — Datei exportieren und direkt an den Agenten hängen. Das ist kein Notbehelf,
> das ist der übliche Weg.

*Die Folie mit dem höchsten praktischen Wert. Sie verhindert genau den Fall, den du sonst beim
Coaching dreimal reparieren musst.*

---

## Folie 5 · Der Agent legt vor — 60 Sekunden

> Daraus folgt der Bauplan für heute: **Der Agent legt vor, ein Mensch schickt ab.**
>
> Das ist keine Notlösung. Der Agent macht die Arbeit, die weh tut — lesen, strukturieren,
> formulieren, Akzeptanzkriterien ableiten, Randfälle finden. Das Einfügen dauert dreißig
> Sekunden. **Der Nutzen liegt zu fünfundneunzig Prozent vor dem letzten Klick.**
>
> Und es ist zukunftssicher: Wenn Actions kommen — im Entwicklerweg gibt es sie ja heute schon
> — schaltet ihr genau diesen einen Schritt durch. Instructions, Wissensquellen und Prüflogik
> bleiben unverändert. **Ihr baut nichts weg.**

> ▸ Auf den orangenen Kasten zeigen. Wenn heute Abend nur eine Folie erinnert wird, dann diese.

---

# TEIL 3 — LIVE BAUEN · 15:08–15:12

## Folie 6 · Agent im M365 Copilot bauen — 4 Minuten, harte Grenze

**🖥 ZU TAB 1 WECHSELN** — M365 Copilot. Erst die Folie kurz stehen lassen, damit alle die
sieben Schritte mitlesen, dann rüber.

> Ich zeig euch das einmal komplett, dann könnt ihr es nachmachen.
>
> **Neuer Agent** — und jetzt der wichtige Trick: Ihr müsst nichts konfigurieren. Ihr
> **beschreibt in normalem Deutsch**, was er tun soll, und Name, Beschreibung und Instructions
> füllen sich von selbst. Er schlägt sogar Wissensquellen und Fähigkeiten vor.
>
> Dann wechsle ich auf **Configure** und ersetze die generierten Instructions durch unseren
> fertigen Prompt aus dem Repo. Wissensquelle dazu über das Plus. Und dann sofort auf **Try it**.
>
> Rechnet mit **drei bis vier Durchläufen**, bis der Agent sitzt. Das ist normal, und das ist
> die eigentliche Arbeit heute Nachmittag — nicht das Anlegen.

**Beschreibungstext (auf der Folie mit Kopieren-Knopf):**

```
Du hilfst mir, aus einer Anforderung Testfälle abzuleiten. Ich gebe dir eine
User Story mit Akzeptanzkriterien, du erzeugst eine Tabelle mit Testfällen für
Happy Path, Fehlerfälle, Grenzwerte und Berechtigungen.
```

> 🔴 **Harte Grenze: 4 Minuten.** Wenn etwas hakt — abbrechen, „das zeig ich euch beim
> Coaching", zurück zum Deck. Nicht reparieren, nicht erklären warum.

---

# TEIL 4 — DAS HANDWERK · 15:12–15:14

## Folie 7 · Agent oder Chatbot — 45 Sekunden

**🖥 ZURÜCK ZUM DECK**

> Kurz die gemeinsame Sprache. **Ein Chatbot antwortet** — ihr fragt, es kommt was zurück, den
> nächsten Schritt macht ihr. **Ein Agent bekommt ein Ziel** und feste Regeln, zerlegt selbst
> in Schritte und prüft sein Ergebnis gegen diese Regeln. Und, das ist der praktische
> Unterschied: **Er ist wiederverwendbar.** Zwanzig Leute benutzen denselben Agenten.
>
> Zwei Bedingungen, und **beide** müssen erfüllt sein. Erstens: mehrere Schritte. Bei einem
> Schritt reicht ein guter Prompt, baut keinen Agenten drumherum. Zweitens: **prüfbares
> Ergebnis** — ihr müsst sagen können, woran man erkennt, dass die Ausgabe gut ist.

*Deine wichtigste Coaching-Folie. Teams, die Bedingung 2 nicht beantworten können, bauen vier
Stunden und haben um 18:15 nichts zu zeigen.*

---

## Folie 8 · Prompt-Aufbau — 45 Sekunden · *als erstes streichbar*

> Der häufigste Fehler heute Nachmittag wird ein zu kurzer Auftrag sein. Ein Prompt, der trägt,
> hat vier Teile: **Rolle, Aufgabe, Regeln, Format.**
>
> Rolle und Aufgabe liefern die meisten mit. **Regeln und Format werden fast immer vergessen**
> — und genau daran scheitern die Agenten am Ende des Tages.
>
> Ohne Format kommt Fließtext zurück, und ihr sortiert von Hand nach — das kostet mehr Zeit,
> als der Agent gespart hat. Ohne Regeln bewertet das Modell nach Gefühl, und zwar **jedes Mal
> anders**. Zwei Durchläufe, zwei Ergebnisse, kein Vertrauen.

---

## Folie 9 · Der FEHLT-Satz — 45 Sekunden · **nie streichen**

```
Erfinde nichts. Fehlt eine Angabe, schreib FEHLT
und formuliere die Rückfrage.
```

> Und dann der eine Satz, der in **jeden** Prompt gehört, egal welcher Use Case: „Erfinde
> nichts. Fehlt eine Angabe, schreib FEHLT und formuliere die Rückfrage."
>
> Warum das nötig ist: **Ein Modell antwortet lieber plausibel als gar nicht.** Es erfindet
> einen Feldnamen, eine Frist, eine Zuständigkeit — und man sieht dem Ergebnis nicht an, was
> echt war und was erfunden. Das ist der gefährlichste Fehlermodus überhaupt, **weil das
> Ergebnis dabei gut aussieht.**
>
> Mit dem Satz bekommt ihr statt einer erfundenen Antwort eine ehrliche Lücke und eine
> Rückfrage, die ihr weiterleiten könnt. **Ein Ergebnis mit drei FEHLT-Markern ist ein
> besseres Ergebnis als eines ohne.**

*In einer Bank ist das der Unterschied zwischen brauchbar und gefährlich. Der Satz steht in
allen sechs Prompts im Repo — das kannst du dazusagen.*

---

# TEIL 5 — DIE DEMOS · 15:14–15:17

## Folie 10 · Der Prompt hinter Demo 1 — 60 Sekunden

**Erst der Auftrag, dann das Ergebnis.** Noch nicht umschalten.

> Bevor ich das laufen lasse, zeig ich euch den Auftrag. Denn genau das ist der Teil, den ihr
> nachher selbst schreibt — und den ihr kopieren könnt.
>
> Das ist **kein Zauberspruch**. Das sind sechs klar benannte Blöcke: Rolle, Aufgabe,
> Quellenpriorität, Bewahren, Verboten, Ausgabeformat.
>
> Drei Stellen sind entscheidend. Erstens: **„Sie handeln nicht autonom"** steht ganz oben —
> der Agent weiß, dass ein Mensch das Ergebnis prüft. Zweitens die **Quellenpriorität**: erst
> das Glossar, dann eigenes Urteil, damit die Fachbegriffe stabil bleiben statt jedes Mal
> anders zu klingen. Drittens das **Ausgabeformat** — das erzwingt das Audit-Log. Ohne Format
> kein Prüfschritt.

> ▸ Nicht vorlesen. Auf die drei markierten Blöcke zeigen und den Satz dazu sagen.

---

## Folie 11 · Demo 1 — Übersetzungsagent — 2–3 Minuten

**🖥 ZU TAB 2** — der Agent ist offen und eingeloggt.

> Erstes Beispiel, und das ist bewusst keins von mir — **das hat ein Kollege gebaut, in M365,
> ohne eine Zeile Code.**
>
> Der Kundenservice schreibt auf Englisch, unsere Kundinnen und Kunden lesen Deutsch. Bisher
> übersetzt jemand von Hand und hofft, dass die Bankbegriffe stimmen. Ich geb ihm jetzt einen
> echten Satz aus dem Servicealltag …

**Input (auf der Folie mit Kopieren-Knopf):**

```
Thank you for the information. We need the notification. You can upload it
via the document upload in online banking or send it to us by email. Please
note that we currently cannot see your Extra account because it is a separate
account and you are logged into your joint account.
```

> … und was zurückkommt, ist nicht nur die Übersetzung. Darunter steht ein **Audit-Log**:
> welcher Fachbegriff aus dem Glossar gezogen wurde, welcher nicht gefunden wurde, in welche
> Richtung übersetzt wurde.
>
> **Das ist der Teil, auf den ich euch stoßen will.** Nicht die Übersetzung ist das Kunststück,
> das kann jedes Modell. Das Kunststück ist, dass ein Mensch **in fünf Sekunden prüfen kann,
> ob er dem Ergebnis trauen darf.** Genau das meinte ich vorhin mit „prüfbares Ergebnis".
> Baut das in euren Agenten ein — es kostet drei Zeilen Prompt.

**Zweiter Input, falls Zeit bleibt** (läuft DE→EN, zeigt die automatische Richtungserkennung):

```
Wir senden Ihnen einen Zwischenkontoauszug per Post-Box zu. Bitte reichen Sie
die Anzeige bis zum 15.08. ein, sonst müssen wir den Vorgang schließen.
```

---

## Folie 12 · Der Prompt hinter Demo 2 — 60 Sekunden

**🖥 ZURÜCK ZUM DECK**

> Auch hier erst der Auftrag. Der ist etwas länger, aber **der ganze Trick steht in einer
> Zeile: der Kategorienliste.**
>
> Vollständigkeit kommt nicht vom Modell, sie kommt vom Auftrag. Happy Path, Fehler, Grenze,
> Berechtigung, Zustand — weil das dort steht, vergisst der Agent es nie. Von Hand vergisst
> man unter Zeitdruck genau die letzten drei.
>
> Und **Schritt vier** verhindert den teuersten Fehler: „Fehlt die fachliche Grundlage, erzeuge
> KEINEN Testfall, sondern einen offenen Punkt." Ohne diesen Satz erfindet das Modell einen
> Grenzwerttest für ein Feld, das es gar nicht gibt — und das fällt beim Review nicht auf.

> ▸ Auf den fett gesetzten letzten Satz zeigen: das ist der FEHLT-Satz von vorhin, in echt.

---

## Folie 13 · Demo 2 — Testfall-Generator — 3 Minuten

**🖥 ZU TAB 3**

> Zweites Beispiel, aus meinem eigenen Bereich: Testautomatisierung. Aus einer Anforderung
> Testfälle zu schreiben ist bei uns Handarbeit — und passiert jede Woche wieder. Ich nehm
> eine **echte** Anforderung, kein hübsches Beispiel …

**Input (auf der Folie mit Kopieren-Knopf):**

```
Als Kundenbetreuer möchte ich beim Anlegen eines Gemeinschaftskontos sehen,
welche Vollmachten für die zweite kontoführende Person gelten, damit ich sie
im Gespräch korrekt beauskunften kann.

Akzeptanzkriterien:
- Die Vollmachten werden erst nach Auswahl beider Kontoinhaber angezeigt.
- Bei minderjährigen Kontoinhabern wird ein Hinweis auf die gesetzliche
  Vertretung eingeblendet.
- Ohne Berechtigung "Kontodaten erweitert" ist der Bereich nicht sichtbar.
```

> ▸ Laufen lassen. **Stille aushalten.** Das ist der Moment, in dem der Raum begreift, dass es echt ist.

> Was der Agent **zuverlässig** liefert, ist die Struktur und die Vollständigkeit über alle
> vier Kategorien. Grenzwerte und Berechtigungsfälle werden unter Zeitdruck als Erstes
> vergessen — der Agent vergisst sie nie, weil sie in der Aufgabe stehen.
>
> Und jetzt der ehrliche Teil: **Hier stimmt es nicht.** Der Agent kennt unsere Produktlogik
> nicht, und wo die Anforderung unscharf war, erzeugt er trotzdem etwas Plausibles. Deshalb
> steht hinter jedem meiner Agenten ein Prüfschritt — ein Mensch schaut drauf und sagt ja oder nein.
>
> Ich zeig euch das bewusst, weil ihr um halb sieben genau diesen Moment habt. Euer Agent wird
> nicht perfekt sein. Meiner ist es auch nicht. **Ein Agent mit einer bekannten Schwäche und
> einem Prüfschritt ist besser als einer, dem man blind glaubt.**

> 🔴 **Die Schwäche nicht wegmoderieren.** Sie ist das stärkste Coaching-Argument des Tages.
>
> 🔴 **Wenn eine Demo nicht lädt:** Nicht reparieren. „Das Netz will heute nicht, ich zeig's
> euch nachher am Tisch", dann Screenshots vom Desktop. Der Raum verzeiht eine kaputte Demo,
> aber keine fünf Minuten Herumklicken.

---

# TEIL 6 — ABSCHLUSS · 15:17–15:20

## Folie 14 · Azure DevOps in drei Stufen — 60 Sekunden

**🖥 ZURÜCK ZUM DECK**

> Ein Sonderthema, weil **vier der elf Use Cases** daran hängen: Azure DevOps. Es gibt drei
> Stufen, und ihr sucht euch die aus, die zu eurem Team passt.
>
> **Stufe eins** braucht nur den Browser: Query bauen, Text kopieren, Agenten-Ausgabe von Hand
> als Ticket anlegen. Null Setup. **Stufe zwei** über CSV-Export und Re-Import. **Stufe drei**
> über die REST-API mit eurem eigenen Login — **kein Personal Access Token**, das ist wichtig.
>
> Die Skripte für Stufe drei liegen fertig im Repo, und ich hab sie **heute gegen unsere echte
> Instanz getestet**: anmelden, ein Work Item lesen, eine Abfrage über 47 Test Cases, und einen
> Kommentar schreiben. Das läuft.

> ▸ **Diesen Satz unbedingt sagen:** „Für eine Demo reicht Stufe 1 oder 2, und es kostet euch
> keinen Punkt bei der Bewertung." Sonst verbringen drei Teams den Nachmittag mit
> Authentifizierung statt mit ihrem Use Case.

---

## Folie 15 · Die zwei technischen Stolpersteine — 45 Sekunden

> Zum Schluss die zwei Dinge, die euch heute wirklich aufhalten werden. Beide sind reparierbar,
> aber nur wenn ihr sie früh merkt.
>
> **Erstens: die Quelle, an die ihr nicht drankommt.** Der Agent soll etwas auswerten, das in
> einem System liegt, für das ihr keine Freigabe habt. Umbau: Daten einmal exportieren und als
> Datei anhängen. Für eine Demo völlig ausreichend.
>
> **Zweitens: der Use Case, der schreiben will.** „Und dann legt er das Ticket an" — das kann
> der Agent Builder heute nicht. Umbau: Der Agent erzeugt den fertigen Text, ein Mensch fügt
> ihn ein. Der Nutzen bleibt fast vollständig erhalten.
>
> Beides kostet fünf Minuten, wenn ihr es um 16 Uhr merkt. **Um halb sieben nicht mehr.** Also
> holt mich sofort, nicht am Ende.

*Bewusst keine Wiederholung von Lisas Spielregeln oder Jury-Kriterien — die hat sie auf ihren
Folien 5 und 7.*

---

## Folie 16 · Das Repo — 45 Sekunden

**🖥 KURZ ZU TAB 4** — das README zeigen, die zwei Einstiege, dann zurück.

> Alles, was ihr braucht, liegt in einem Repo:
> **github.com/Wladefant/ai-agent-hackathon-starter** — der QR-Code ist auf der Folie und auf
> jeder Tischkarte.
>
> Wer nicht mit Git arbeitet, **klickt einfach drauf und kopiert den Text** — dafür ist es
> ausgelegt. Drin sind sechs fertige Agenten-Prompts mit Beispiel-Eingabe und erwarteter
> Ausgabe, das Azure-DevOps-Kit in drei Stufen, drei kleine Beispiele für die Teams mit
> Entwicklerin, und ein **komplettes Sechs-Agenten-System** aus einem anderen Team. Das müsst
> ihr heute nicht nachbauen — aber es zeigt euch, wo die Reise hingeht.
>
> Lisa, zurück zu dir — die Use Cases.

> ▸ Den Link **zehn Sekunden stehen lassen**, bis alle abfotografiert haben.

---

# DANACH — BEI LISAS USE-CASE-FOLIEN

**Ein Satz Machbarkeit pro Use Case. Kurz halten, das ist kein zweiter Vortrag.**

| Nr | Use Case | Werkzeug | Dein Satz |
|---|---|---|---|
| 01 | Incident Co-Pilot | M365 | Klassifizieren und ähnliche Fälle finden geht. Automatisch zuweisen nicht — baut den Vorschlag. |
| 02 | Technical Documentation | GitHub | Lebt an Pull Requests und Changes. Braucht Repo-Zugriff im Team. |
| 03 | Merak-Version Story | M365 | Release Notes lesen und Story vorbereiten: geht. Anlegen: Text vorlegen, Mensch legt an. |
| 04 | QBR Update | M365 | Excel lesen, Änderungsvorschläge erzeugen. Der Agent schlägt vor, ihr klickt. |
| 05 | Fachkonzept-Doku | M365 | User Stories rein, Word-Dokument raus. Standardfall, läuft sicher. |
| 06 | BDB Query | GitHub | Query erzeugen geht in beidem. Ausführen braucht Entwickler — Variante 1 ist realistisch. |
| 07 | OnePAM API | GitHub | Requests bauen: ja. Abrufen: braucht Zugang. Klärt das in den ersten zehn Minuten. |
| 08 | User Story & Change | M365 | Der dankbarste Use Case im Feld. In zwei Stunden vorführbar. |
| 09 | QBR Request Ersteller | M365 | Dialog führen, Pflichtfelder abfragen, Vorlage füllen. Klein und stark. |
| 10 | Testkonstellationen | M365 | Mein Heimatthema, fragt mich. Achtet auf den Prüfschritt. |
| 11 | Dokumentationsunterstützung | M365 | Verteilte Quellen zusammenziehen. Genau die Stärke von M365. |

> ▸ **Wenn ein Team Schreibzugriff braucht:** nicht abwürgen. „Baut ihn so, dass er am Ende
> einen fertigen Text vorlegt. Der letzte Klick ist heute ein Mensch — und das ist genau der
> Schritt, den man später durchschaltet."

---

## Dein Abschlusssatz nach Lisas Folie 20

> Ein Letztes von mir. **Ihr müsst heute nichts fertigstellen.** Was ihr am Abend zeigt, darf
> ein einziger Prompt sein, der funktioniert — Hauptsache, ihr könnt sagen, **welches Problem
> er löst und woran man erkennt, dass er es richtig gelöst hat.** Wer bei einem der beiden
> Punkte hängt, holt mich. Dafür bin ich da. Viel Spaß.

---

## Checkliste bis 14:30

| | |
|---|---|
| ☐ | Bildschirmübergabe einmal mit Lisa geübt |
| ☐ | Mit Lisa geklärt: **ihre Folie 3 entfällt**, sie macht nach dir bei Folie 4 weiter |
| ☐ | Nürnberg: sehen die Zugeschalteten den Wechsel? |
| ☐ | Deck im Vollbild getestet (Taste `F`) |
| ☐ | Tabs 1–4 offen und eingeloggt |
| ☐ | Beide Demos **vor Ort im dortigen Netz** einmal durchgelaufen |
| ☐ | Screenshot-Fallback auf dem Desktop |
| ☐ | Tischkarten ausgedruckt |

---

**Deck-Steuerung:** `←` `→` blättern · Knöpfe unten rechts · linkes Drittel klicken = zurück ·
`N` Sprechtext einblenden · `O` Übersicht · `D` dunkel · `F` Vollbild
