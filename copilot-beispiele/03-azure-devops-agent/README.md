# 03 · Azure-DevOps-Agent

**Aus einer Meeting-Notiz wird ein strukturiertes Work Item. Das Skript druckt den API-Aufruf, es sendet ihn nicht.**

## Was das zeigt

| Teil | Datei | Wozu |
|---|---|---|
| Dauerkontext | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Rolle, Feldregeln, Verbot zu senden |
| Prompt | [`PROMPT.md`](PROMPT.md) | Text zum Hineinkopieren, plus zwei Nachfass-Prompts |
| Vertrag | [`workitem.template.json`](workitem.template.json) | die Felder, die der Agent füllen muss |
| Eingabe | [`beispiel-eingabe/idee.md`](beispiel-eingabe/idee.md) | eine formlose Notiz aus dem Daily |
| Prüfung + Ausgabe | [`build-workitem.mjs`](build-workitem.mjs) | prüft die Pflichtfelder und druckt das JSON-Patch-Dokument |
| Zielbild | [`beispiel-ausgabe/workitem.json`](beispiel-ausgabe/workitem.json) | ein ausgefülltes Work Item |

> Das hier ist die **Vorstufe**. Die lauffähigen Skripte, die tatsächlich mit der
> Azure-DevOps-API sprechen, liegen unter [`../../azure-devops/`](../../azure-devops/).
> `build-workitem.mjs` öffnet keine Verbindung und kennt kein Token.

## Demo in 2 Minuten

1. Ordner in VS Code öffnen: `code copilot-beispiele/03-azure-devops-agent`
2. `beispiel-eingabe/idee.md` zeigen. Formlos, drei Absätze, so kommt es aus dem Daily.
3. Terminal:
   ```bash
   node build-workitem.mjs
   ```
   → oben die Kopfzeilen mit `POST .../_apis/wit/workitems/$User%20Story?api-version=7.1`
   und **NICHTS GESENDET**, darunter das fertige JSON-Patch-Array.
4. Kurz auf die Zeilen `/fields/System.Title`, `/fields/Microsoft.VSTS.Common.AcceptanceCriteria`
   und `/relations/-` zeigen. Genau das nimmt Azure DevOps entgegen.
5. In `beispiel-ausgabe/workitem.json` `"prioritaet"` auf `9` setzen, speichern, erneut laufen lassen:
   ```
   FEHLER: 1 Problem(e) ...
     - prioritaet: "9" ist keine Zahl von 1 bis 4
   ```
   Zurückändern.
6. Copilot Chat im Agent-Modus öffnen, `beispiel-eingabe/idee.md` anhängen, den Block aus
   [`PROMPT.md`](PROMPT.md) einfügen und zeigen, wie der Agent schreibt, prüft und nachbessert.

## Was du davon mitnimmst

- Der Agent bereitet den Schreibvorgang vollständig vor, der letzte Klick bleibt beim Menschen. Genau so kommst du heute ohne Schreibrechte weiter.
- Eine Vorlage plus ein Prüfskript zwingen die formlose Notiz in eine Form, die dein Backlog akzeptiert.
- Trenne strikt: Struktur bauen (hier) und API rufen (unter [`../../azure-devops/`](../../azure-devops/)). Dann kannst du den zweiten Teil einschalten, ohne den ersten anzufassen.

## Voraussetzungen

VS Code mit GitHub-Copilot-Erweiterung, Node 18 oder neuer. Kein Azure-DevOps-Zugang nötig.
