# 02 · Doku aus Change

**Ein Change kommt rein, ein Änderungsvorschlag für die Doku kommt raus. Der Mensch übernimmt ihn.**

## Was das zeigt

| Teil | Datei | Wozu |
|---|---|---|
| Dauerkontext | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Rolle, Aufbau des Vorschlags, Verbot, `docs/` selbst zu ändern |
| Prompt | [`PROMPT.md`](PROMPT.md) | der Text zum Hineinkopieren, plus Nachfass-Prompt |
| Eingabe | [`beispiel-eingabe/change.md`](beispiel-eingabe/change.md) | die Change-Beschreibung |
| Bestand | [`docs/api-zahlungen.md`](docs/api-zahlungen.md), [`docs/betrieb-ueberwachung.md`](docs/betrieb-ueberwachung.md) | zwei Seiten, die der Change veraltet |
| Zielbild | [`beispiel-ausgabe/doku-vorschlag.md`](beispiel-ausgabe/doku-vorschlag.md) | so sieht ein gutes Ergebnis aus |

Der interessante Teil steckt in der Überwachungsseite: der Change nennt sie nur nebenbei,
aber ohne Anpassung schlägt dort nach dem Release dauerhaft ein Alarm an.

## Demo in 2 Minuten

1. Ordner in VS Code öffnen: `code copilot-beispiele/02-doku-aus-change`
2. `docs/betrieb-ueberwachung.md` zeigen, letzte Zeile vorlesen:
   „Jede Zahlung, die nicht innerhalb von 5 Minuten final ist, gilt als Störung."
3. `beispiel-eingabe/change.md` zeigen: ab jetzt stehen Zahlungen bis zu 24 Stunden offen.
   → Der Satz oben ist ab dem Release falsch. Genau das soll der Agent finden.
4. Copilot Chat im Agent-Modus öffnen, die drei Dateien anhängen und den Block aus
   [`PROMPT.md`](PROMPT.md) hineinkopieren.
5. Während der Agent schreibt: [`beispiel-ausgabe/doku-vorschlag.md`](beispiel-ausgabe/doku-vorschlag.md)
   danebenlegen und den Aufbau zeigen — Vorher, Nachher, Warum, offene Fragen.
6. Schlusspunkt setzen: unter `docs/` hat sich nichts geändert. Der Vorschlag liegt daneben,
   ein Mensch entscheidet, was davon in den Pull Request geht.

## Was du davon mitnimmst

- Der Agent liefert einen Vorschlag mit Vorher/Nachher, keinen fertigen Commit. Das macht die Prüfung schnell und die Verantwortung eindeutig.
- Der Wert liegt in den Stellen, die der Change nicht nennt und die trotzdem falsch werden. Danach musst du in den Instructions ausdrücklich fragen.
- „Nicht erfinden, stattdessen offene Frage mit Adressat" ist die eine Regel, die aus einem plausiblen Text ein brauchbares Arbeitsergebnis macht.

## Voraussetzungen

VS Code mit GitHub-Copilot-Erweiterung. Kein Node nötig.
