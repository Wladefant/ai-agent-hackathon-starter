# Stufe 2 — Excel und CSV

**Wofür:** viele Work Items auf einmal exportieren, von einem Agenten anreichern lassen und
zurück nach Azure DevOps schreiben.
**Für wen:** alle, die Dateien herunterladen und hochladen dürfen. Kein Skript, kein Terminal.

**Das ist der stärkste Weg für Fachbereiche.** Ein Agent, der 40 Test Cases auf einmal mit
Testdaten füllt, ist in der Demo deutlich beeindruckender als einer, der eine Story schreibt.

---

## Der Ablauf

```
Query in ADO  →  Export to CSV  →  CSV in den Agenten  →  gefülltes CSV zurück
                                                                   ↓
                        Work Items aktualisiert  ←  Import Work Items
```

---

## Schritt 1 — Exportieren

1. **Boards → Queries** → Query bauen (siehe [01-ohne-technik.md](01-ohne-technik.md)).
2. Über **Column options** genau die Spalten einblenden, die du brauchst.
   **Der Export enthält exakt die sichtbaren Spalten.** Blende `ID` und `Work Item Type`
   unbedingt ein — ohne die beiden kommst du nicht zurück.
3. Rechts oben **…** → **Export to CSV**.

Ergebnis: eine `.csv`-Datei mit einer Kopfzeile aus Spaltennamen und einer Zeile je Work Item.

---

## Schritt 2 — Der Agent füllt die Datei

Lade die CSV in deinen M365-Agenten hoch (oder füge sie als Text ein, wenn sie klein ist).

**Prompt-Vorlage:**

```
Anbei eine CSV-Datei aus Azure DevOps. Eine Zeile = ein Work Item.

Aufgabe: Fülle für jede Zeile die Spalte "Acceptance Criteria".
Leite die Kriterien aus Title und Description ab. 3 bis 5 Kriterien je Zeile.

Regeln — bitte genau einhalten:
1. Ändere KEINE bestehende Spalte außer "Acceptance Criteria".
2. Ändere KEINE Werte in der Spalte "ID". Lösche keine Zeile.
3. Behalte die Kopfzeile und die Spaltenreihenfolge unverändert bei.
4. Gib die vollständige CSV zurück, nicht nur die geänderten Zeilen.
5. Felder mit Komma, Anführungszeichen oder Zeilenumbruch in doppelte
   Anführungszeichen setzen. Ein " im Text wird zu "".
6. Reiner Text, kein Markdown, kein HTML.
```

Regel 5 ist die wichtigste. Ohne sie zerlegt dir der erste Kommatext die halbe Tabelle.

**Prüfe die Antwort, bevor du importierst:**
- Gleiche Zeilenzahl wie vorher?
- Kopfzeile unverändert?
- Alle IDs noch da und unverändert?

---

## Schritt 3 — Zurück importieren

**Boards → Work Items** → in der Toolbar **Import Work Items** → Datei wählen → prüfen →
**Save Items**.

Der Import zeigt die Zeilen erst als ungespeicherte Vorschau. **Bis du auf Save Items
klickst, ist nichts passiert.** Das ist dein Sicherheitsnetz — schau dir die Vorschau an.

---

## Die Regeln des CSV-Imports

**Diese gelten verlässlich:**

| Regel | Bedeutung |
|---|---|
| Spalte `ID` gefüllt | Das bestehende Work Item mit dieser ID wird **aktualisiert**. |
| Spalte `ID` leer | Ein **neues** Work Item wird angelegt. |
| Spalte `Work Item Type` | Beim Anlegen **Pflicht** — sonst weiß Azure DevOps nicht, was es erzeugen soll. |
| Spalte `Title` | Beim Anlegen **Pflicht**. |
| Spaltennamen | Müssen den Anzeigenamen der Felder entsprechen, so wie sie im Export stehen. Tippfehler = Spalte wird ignoriert oder der Import scheitert. |
| Trennzeichen | **Komma**. Nicht Semikolon. |
| Anführungszeichen | Felder mit Komma, `"` oder Zeilenumbruch gehören in `"…"`. Ein `"` im Text wird zu `""`. |
| Kodierung | **UTF-8**, sonst werden Umlaute zu `Ã¤`. |

**Beispiel für korrektes Quoting:**

```csv
ID,Work Item Type,Title,Acceptance Criteria
4711,User Story,Kontoauszug als PDF,"- Download sichtbar
- PDF enthält Zeitraum, Saldo und Kontonummer
- Dateiname enthält das Datum"
,User Story,"Filter ""Nur offene"" in der Übersicht",- Filter merkt sich den Zustand
```

Zeile 1 aktualisiert Work Item 4711 mit einem mehrzeiligen Feld. Zeile 2 hat eine leere ID
und legt deshalb ein neues Work Item an; die inneren Anführungszeichen sind verdoppelt.

---

## ⚠️ Die zwei Excel-Fallen

**1. Semikolon statt Komma.** Deutsches Excel speichert CSV standardmäßig mit Semikolon als
Trennzeichen. Azure DevOps erwartet Komma.
**Prüfen:** Datei mit Rechtsklick → *Öffnen mit* → *Editor / Notepad*. Steht dort
`ID;Work Item Type;…`, ist sie falsch.
**Lösung:** In Excel *Speichern unter* → Dateityp **CSV UTF-8 (durch Trennzeichen getrennt)**.
Bleibt es beim Semikolon, im Editor per *Suchen und Ersetzen* korrigieren — aber nur, wenn in
den Textfeldern selbst keine Semikola vorkommen.

**2. Excel zerstört Werte still.** Führende Nullen verschwinden, `2024-01-05` wird zu einem
Datumsformat, lange Zahlen werden zu `1,23E+11`.
**Lösung:** Wenn du nur Text anreichern willst, öffne die CSV gar nicht erst in Excel. Gib sie
direkt dem Agenten und importiere die Antwort. Excel ist der Umweg, nicht der Weg.

---

## Vor dem großen Lauf: 2-Zeilen-Test

Es gibt Verhaltensweisen, die je nach Projektvorlage und Prozess (Agile, Scrum, CMMI) und je
nach ADO-Version unterschiedlich sind. Rate nicht. Teste sie in zwei Minuten mit einer
Mini-CSV aus zwei Zeilen und schau in der Import-Vorschau nach:

| Zu prüfen | Wie du es prüfst |
|---|---|
| **HTML-Felder** — kommen `Description` und `Acceptance Criteria` als Text oder mit `<div>`/`<p>`-Markup zurück? | Ein Work Item mit formatierter Beschreibung exportieren und die CSV im Editor ansehen. |
| **Formatierung beim Import** — überlebt eine mehrzeilige Beschreibung? | Testzeile importieren, Work Item öffnen, hinsehen. |
| **Pflichtfelder deines Prozesses** — verlangt euer Template z. B. `Area Path` oder `Iteration Path`? | Import-Vorschau zeigt Fehler pro Zeile an. |
| **Zeilenlimit** — wie viele Zeilen nimmt der Import? | Mit deinem echten Umfang testen. Bei Problemen in Blöcke à 100 Zeilen teilen. |
| **Verknüpfungen (Parent/Child)** — lassen sie sich per CSV setzen? | Im Export-Header nachsehen, ob es überhaupt eine Link-Spalte gibt. Verlass dich nicht darauf. Hierarchien setzt man schneller per Hand oder mit [`ado-create.mjs --parent`](scripts/). |

Wenn die Import-Vorschau Fehler meldet, meldet sie sie **pro Zeile mit Grund**. Das ist die
schnellste Fehlersuche, die du bekommst — lies sie, statt zu raten.

---

## Merksatz

> Exportiere wenige Spalten. Lass den Agenten genau **eine** Spalte füllen.
> Importiere zuerst zwei Zeilen, dann alle.

Drei getrennte Durchläufe mit je einer gefüllten Spalte sind schneller als ein Durchlauf, bei
dem der Agent fünf Spalten gleichzeitig durcheinanderbringt.
