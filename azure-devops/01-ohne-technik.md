# Stufe 1 — Azure DevOps ohne jede Technik

**Wofür:** Inhalte aus Azure DevOps in deinen Agenten holen und die Antwort wieder zurück
in ein Work Item bringen.
**Für wen:** Fachbereich, Test, Prozess, Doku. Du brauchst nur einen Browser und Copy-Paste.
Keine Installation, kein Entwickler, keine Berechtigung außer der, die du schon hast.

**Dauer:** 10 Minuten für den ersten Durchlauf.

---

## Das Muster

```
Work Item in ADO  →  Text kopieren  →  in den Agenten einfügen
                                              ↓
neues Work Item   ←  Text einfügen  ←  Antwort kopieren
```

Der Agent schreibt nicht selbst nach Azure DevOps. Du bist der letzte Schritt. Das ist heute
normal und völlig ausreichend für eine Demo.

---

## Schritt 1 — Die richtigen Work Items finden (Queries)

1. In Azure DevOps links auf **Boards → Queries**.
2. **New query**.
3. Filter zusammenklicken, typischerweise:
   - `Work Item Type` = `User Story` (oder `Test Case`, `Bug`)
   - `State` `<>` `Closed`
   - `Area Path` `Under` = dein Bereich
4. **Run query**.
5. Über **Column options** die Spalten wählen, die du wirklich brauchst. Weniger ist besser —
   du musst sie gleich kopieren.

Speichere die Query unter **My Queries**, wenn du sie mehrfach brauchst.

---

## Schritt 2 — Was du in den Agenten kopierst

Öffne ein Work Item und kopiere gezielt diese Felder. Nicht die halbe Seite, nicht die
Kommentare, nicht die Historie.

| Work-Item-Typ | Felder, die du kopierst |
|---|---|
| **User Story** | `Title` · `Description` · `Acceptance Criteria` |
| **Bug** | `Title` · `Repro Steps` · `System Info` |
| **Test Case** | `Title` · `Steps` (Action + Expected Result je Zeile) · `Preconditions` falls vorhanden |
| **Task** | `Title` · `Description` |

Am schnellsten geht es so: Feld anklicken, `Strg+A`, `Strg+C`.

**Bau daraus einen sauberen Block für den Agenten:**

```
Titel: Kontoauszug als PDF herunterladen

Beschreibung:
Als Kundin möchte ich meinen Kontoauszug als PDF speichern,
damit ich ihn meiner Steuerberatung geben kann.

Akzeptanzkriterien:
- Download-Button in der Auszugsübersicht sichtbar
- PDF enthält Kontonummer, Zeitraum und Saldo
```

Diese Beschriftungen (`Titel:`, `Beschreibung:`, `Akzeptanzkriterien:`) sind wichtig. Ohne sie
rät der Agent, was was ist.

---

## Schritt 3 — Der Prompt

Sag dem Agenten immer drei Dinge: **was er bekommt**, **was er liefern soll**, **in welchem
Format**.

```
Du bekommst eine User Story aus Azure DevOps.

Aufgabe: Schreibe 5 fachliche Testfälle dazu, inklusive Negativfällen.

Format je Testfall, als REINER TEXT ohne Markdown und ohne HTML:
Titel: <ein Satz>
Vorbedingung: <ein Satz>
Schritte:
1. <Aktion>
2. <Aktion>
Erwartetes Ergebnis: <ein Satz>

Hier ist die User Story:
<hier deinen Block aus Schritt 2 einfügen>
```

---

## ⚠️ Der eine Stolperstein: Azure DevOps speichert HTML

Die Felder **Description**, **Acceptance Criteria** und **Repro Steps** sind intern
HTML-Felder. Das hat zwei Folgen:

**Beim Herauskopieren:** Je nach Weg (Export, API, manchmal auch Copy-Paste) siehst du
Markup wie `<div><p>Text</p></div>`. Das ist kein Fehler. Entferne es entweder von Hand oder
schreib in den Prompt: *"Ignoriere HTML-Tags im folgenden Text."*

**Beim Hineinkopieren:** Markdown funktioniert dort **nicht**. Ein `**fett**` bleibt sichtbar
als `**fett**` stehen, eine `- Liste` bleibt eine Zeile mit Bindestrich.

**Deshalb in jeden Prompt schreiben:**

> „Antworte als reiner Text ohne Markdown-Formatierung. Keine `**`, keine `#`, keine
> Backticks. Wenn du eine Liste brauchst, benutze Zeilen, die mit einem Bindestrich beginnen."

Der Rich-Text-Editor in Azure DevOps macht aus solchen Zeilen beim Einfügen meist von selbst
eine ordentliche Liste. Alternativ formatierst du in 20 Sekunden mit der Editor-Toolbar nach.

---

## Schritt 4 — Die Antwort zurück in Azure DevOps

1. **Boards → Work Items → New Work Item** → Typ wählen.
2. **Title** aus der Agenten-Antwort einfügen (nur die Titelzeile, ohne „Titel:").
3. In **Description** klicken und den Rest einfügen.
4. Bei einem **Test Case**: auf den Tab **Steps** wechseln. Dort gibt es eine Tabelle mit
   *Action* und *Expected Result*. Jede Zeile einzeln einfügen — die Schritte-Tabelle nimmt
   keinen Textblock am Stück an.
5. **Save**.

**Tipp für die Nachvollziehbarkeit:** Setz im Feld **Tags** ein `agent-entwurf`. Dann könnt
ihr später mit einer Query zeigen, was der Agent an dem Tag produziert hat. Das ist in der
Demo ein starkes Argument.

---

## Wenn du viele Work Items auf einmal brauchst

Query ausführen → in der Ergebnisliste rechts oben auf **…** (drei Punkte) → **Export to CSV**.
Du bekommst eine Datei, die du in Excel öffnest.

Wenn das dein Fall ist, mach direkt bei [02-excel-und-csv.md](02-excel-und-csv.md) weiter —
dort steht auch, wie du die Datei wieder zurückspielst.

---

## Häufige Fragen

| Frage | Antwort |
|---|---|
| Kann ich den Agenten direkt auf Azure DevOps zugreifen lassen? | Heute in der Regel nicht. Plane mit Copy-Paste. |
| Der Agent erfindet Feldnamen. | Gib ihm im Prompt die exakte Feldliste vor und schreib dazu: „Benutze ausschließlich diese Felder." |
| Die Antwort ist zu lang für ein Work Item. | Bitte um Begrenzung: „Maximal 8 Zeilen Beschreibung, maximal 5 Akzeptanzkriterien." |
| Darf ich echte Daten in den Agenten kopieren? | Richte dich nach den Vorgaben eurer Organisation. Im Zweifel: Namen, Kunden- und Kontonummern vorher ersetzen. |
| Meine Umlaute sehen im CSV falsch aus. | Kodierung. Siehe [02-excel-und-csv.md](02-excel-und-csv.md). |
