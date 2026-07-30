# Beispiel — vom Absatz zur User Story in Azure DevOps

**Wofür:** ein vollständiges Beispiel zum Nachbauen. Grober Absatz → Agenten-Prompt →
Agenten-Ausgabe → angelegtes Work Item.
**Für wen:** Teams mit Entwicklerin oder Entwickler. Die Schritte 1 bis 3 funktionieren auch
ohne Skript — dann legst du das Work Item am Ende per Hand an
(siehe [01-ohne-technik.md](01-ohne-technik.md)).

**Dauer:** 15 Minuten. Das ist euer erster sichtbarer Erfolg.

---

## Schritt 1 — Das, was ihr habt

So kommt eine Anforderung im echten Leben an. Ein Absatz aus einer Mail, unstrukturiert:

> Kunden rufen an, weil sie einen Dauerauftrag für ein paar Monate aussetzen wollen, zum
> Beispiel während einer Elternzeit oder wenn die Miete mal direkt überwiesen wird. Heute
> müssen sie ihn löschen und später neu anlegen, dabei geht die Referenz verloren und die
> Servicemitarbeiter machen Tippfehler. Wir hätten gern eine Pausieren-Funktion mit
> Enddatum, danach läuft er automatisch weiter.

---

## Schritt 2 — Der Prompt

Wichtig ist der Formatteil am Ende. Ohne ihn bekommst du Fließtext, den du nicht direkt
weiterverwenden kannst.

```
Du bist Business Analyst und schreibst User Stories für ein Scrum-Team.

Aufgabe: Formuliere aus der folgenden Anforderung genau eine User Story
mit Akzeptanzkriterien.

Format, exakt so und in dieser Reihenfolge:

TITEL:
<ein Satz, maximal 80 Zeichen, keine Anführungszeichen>

BESCHREIBUNG:
Als <Rolle> möchte ich <Ziel>, damit <Nutzen>.
<2 bis 4 Sätze Kontext. Reiner Text, kein Markdown.>

AKZEPTANZKRITERIEN:
- <prüfbares Kriterium>
- <prüfbares Kriterium>
(5 bis 7 Stück, jedes einzeln testbar, jedes beginnt mit einem Bindestrich)

OFFENE FRAGEN:
- <Frage an den Fachbereich>

Regeln:
- Reiner Text. Kein Markdown, keine Sternchen, keine Überschriften mit #.
- Keine technische Lösung vorschlagen. Nur fachliches Verhalten beschreiben.
- Was in der Anforderung nicht steht, kommt unter OFFENE FRAGEN — nicht erfinden.

Anforderung:
Kunden rufen an, weil sie einen Dauerauftrag für ein paar Monate aussetzen wollen,
zum Beispiel während einer Elternzeit oder wenn die Miete mal direkt überwiesen wird.
Heute müssen sie ihn löschen und später neu anlegen, dabei geht die Referenz verloren
und die Servicemitarbeiter machen Tippfehler. Wir hätten gern eine Pausieren-Funktion
mit Enddatum, danach läuft er automatisch weiter.
```

---

## Schritt 3 — Was der Agent liefert

Ein realistisches Ergebnis. So sieht eine brauchbare Antwort aus:

```
TITEL:
Dauerauftrag befristet pausieren statt löschen

BESCHREIBUNG:
Als Kontoinhaberin möchte ich einen bestehenden Dauerauftrag für einen selbst
gewählten Zeitraum pausieren, damit er danach unverändert weiterläuft und ich ihn
nicht löschen und neu anlegen muss.
Heute ist Löschen und Neuanlegen der einzige Weg. Dabei gehen Verwendungszweck und
Referenz verloren, und beim manuellen Neuanlegen im Service entstehen Tippfehler.
Der pausierte Auftrag bleibt sichtbar und behält alle Daten.

AKZEPTANZKRITERIEN:
- In der Detailansicht eines aktiven Dauerauftrags gibt es die Aktion "Pausieren".
- Beim Pausieren wird ein Enddatum abgefragt; das Datum muss in der Zukunft liegen.
- Ein pausierter Dauerauftrag wird in der Übersicht mit dem Status "Pausiert bis TT.MM.JJJJ" angezeigt.
- Zwischen Pausierungsbeginn und Enddatum wird keine Ausführung ausgelöst.
- Am Tag nach dem Enddatum wird der Auftrag automatisch wieder aktiv und die nächste turnusmäßige Ausführung findet statt.
- Betrag, Empfänger, Verwendungszweck und Referenz bleiben unverändert erhalten.
- Ein pausierter Dauerauftrag kann jederzeit vorzeitig manuell reaktiviert werden.

OFFENE FRAGEN:
- Gibt es eine maximale Pausendauer, oder ist sie unbegrenzt?
- Was passiert, wenn das Enddatum genau auf einen Ausführungstag fällt: erste Ausführung oder erst der nächste Turnus?
- Soll die Kundin über die automatische Reaktivierung benachrichtigt werden?
- Dürfen Servicemitarbeiter das ebenfalls auslösen, oder nur die Kundin selbst?
```

**Kurz prüfen, bevor du weitermachst:** Ist jedes Kriterium einzeln testbar? Steht unter
OFFENE FRAGEN wirklich das, was nicht in der Anforderung stand? Ein Agent, der nichts fragt,
hat wahrscheinlich etwas erfunden.

---

## Schritt 4 — In zwei Dateien speichern

Alles nach `BESCHREIBUNG:` bis vor `AKZEPTANZKRITERIEN:` → `story.md`
Die Zeilen unter `AKZEPTANZKRITERIEN:` → `kriterien.md`

```
story.md
─────────────────────────────────────────────────────────
Als Kontoinhaberin möchte ich einen bestehenden Dauerauftrag für einen selbst
gewählten Zeitraum pausieren, damit er danach unverändert weiterläuft und ich ihn
nicht löschen und neu anlegen muss.

Heute ist Löschen und Neuanlegen der einzige Weg. Dabei gehen Verwendungszweck und
Referenz verloren, und beim manuellen Neuanlegen im Service entstehen Tippfehler.
Der pausierte Auftrag bleibt sichtbar und behält alle Daten.
```

```
kriterien.md
─────────────────────────────────────────────────────────
- In der Detailansicht eines aktiven Dauerauftrags gibt es die Aktion "Pausieren".
- Beim Pausieren wird ein Enddatum abgefragt; das Datum muss in der Zukunft liegen.
- Ein pausierter Dauerauftrag wird in der Übersicht mit dem Status "Pausiert bis TT.MM.JJJJ" angezeigt.
- Zwischen Pausierungsbeginn und Enddatum wird keine Ausführung ausgelöst.
- Am Tag nach dem Enddatum wird der Auftrag automatisch wieder aktiv und die nächste turnusmäßige Ausführung findet statt.
- Betrag, Empfänger, Verwendungszweck und Referenz bleiben unverändert erhalten.
- Ein pausierter Dauerauftrag kann jederzeit vorzeitig manuell reaktiviert werden.
```

Die leere Zeile in `story.md` wird zu zwei Absätzen. Die Bindestrich-Zeilen in `kriterien.md`
werden zu einer HTML-Liste. Darum kümmert sich das Skript.

---

## Schritt 5 — Erst trocken, dann echt

```powershell
# einmalig
az login
$env:ADO_ORG = "<DEINE-ORG>"
$env:ADO_PROJECT = "<DEIN-PROJEKT>"
cd azure-devops/scripts
```

**Trockenlauf — zeigt den Request, sendet nichts:**

```powershell
node ado-create.mjs --dry-run `
  --type "User Story" `
  --title "Dauerauftrag befristet pausieren statt löschen" `
  --description-file story.md `
  --acceptance-file kriterien.md `
  --tags "hackathon; agent-entwurf"
```

Ausgabe (gekürzt):

```
DRY RUN — es wird nichts gesendet.

POST https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_apis/wit/workitems/$User%20Story?api-version=7.1
Content-Type: application/json-patch+json

[
  { "op": "add", "path": "/fields/System.Title", "value": "Dauerauftrag befristet pausieren statt löschen" },
  { "op": "add", "path": "/fields/System.Description", "value": "<p>Als Kontoinhaberin …</p><p>Heute ist …</p>" },
  { "op": "add", "path": "/fields/Microsoft.VSTS.Common.AcceptanceCriteria", "value": "<ul><li>In der Detailansicht …</li>…</ul>" },
  { "op": "add", "path": "/fields/System.Tags", "value": "hackathon; agent-entwurf" }
]
```

**Sieht gut aus? Dann ohne `--dry-run`:**

```powershell
node ado-create.mjs `
  --type "User Story" `
  --title "Dauerauftrag befristet pausieren statt löschen" `
  --description-file story.md `
  --acceptance-file kriterien.md `
  --tags "hackathon; agent-entwurf"
```

```
Angelegt: User Story #4711
Titel:    Dauerauftrag befristet pausieren statt löschen
Link:     https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_workitems/edit/4711
```

Unter bash statt PowerShell: statt Backtick am Zeilenende einen Backslash `\` benutzen.

---

## Schritt 6 — Die offenen Fragen sichtbar machen

Die vier Rückfragen des Agenten gehören nicht in die Beschreibung, sonst liest sie niemand.
Häng sie als Kommentar an:

```powershell
node ado-comment.mjs --id 4711 --text "Offene Fragen aus der Agenten-Analyse:
- Gibt es eine maximale Pausendauer?
- Was passiert, wenn das Enddatum auf einen Ausführungstag fällt?
- Soll über die automatische Reaktivierung benachrichtigt werden?
- Dürfen Servicemitarbeiter das ebenfalls auslösen?"
```

**Genau das ist der Demo-Moment.** Nicht „der Agent hat Text geschrieben", sondern: der Agent
hat die Lücken in der Anforderung gefunden und sie als Kommentar an das richtige Ticket
gehängt.

---

## Schritt 7 — Kontrolle

```powershell
node ado-query.mjs --ids 4711
```

```
Id    WorkItemType  Title                                          State  AssignedTo
----  ------------  ---------------------------------------------  -----  ----------
4711  User Story    Dauerauftrag befristet pausieren statt löschen  New
```

Alles, was der Agent an diesem Tag angelegt hat:

```powershell
node ado-query.mjs --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.Tags] CONTAINS 'agent-entwurf' ORDER BY [System.CreatedDate] DESC"
```

Der Tag `agent-entwurf` ist eure Demo-Folie. Eine Query, eine Liste, fertig.

---

## Was ihr jetzt variieren könnt

| Statt … | macht ihr … |
|---|---|
| einer Story | eine Schleife über zehn Absätze aus einer Mail |
| `--type "User Story"` | `--type Bug` mit `--field Microsoft.VSTS.TCM.ReproSteps=…` |
| Story schreiben | Story **prüfen**: bestehende Story per `ado-query.mjs --ids … --json` lesen, vom Agenten bewerten lassen, Bewertung per `ado-comment.mjs` zurückschreiben |
| einer neuen Story | `--parent 4700`, damit sie unter dem richtigen Epic hängt |

Die dritte Zeile ist der unterschätzte Fall: **lesen, beurteilen, kommentieren.** Das braucht
keine Schreibrechte auf Feldern, es kann nichts kaputtmachen, und es lässt sich am Montag
sofort auf 200 bestehende Work Items loslassen.
