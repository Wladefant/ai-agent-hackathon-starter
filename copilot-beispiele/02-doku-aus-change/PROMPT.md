# PROMPT

Copilot Chat öffnen, **Agent-Modus** wählen, die drei Dateien anhängen
(`beispiel-eingabe/change.md`, `docs/api-zahlungen.md`, `docs/betrieb-ueberwachung.md`)
und den Block unten hineinkopieren.

---

```text
Lies die angehängte Change-Beschreibung und die beiden Doku-Seiten unter docs/.

Erstelle einen Doku-Änderungsvorschlag nach den Repo-Instructions und schreibe ihn
nach beispiel-ausgabe/doku-vorschlag.md. Ändere nichts unter docs/.

Achte besonders auf:
- Statuslisten, die jetzt unvollständig sind
- Feldtabellen, denen ein Feld fehlt
- Endpunkt- und Event-Tabellen
- Aussagen und Schwellwerte, die durch den Change fachlich falsch werden, auch wenn
  der Change sie nicht ausdrücklich nennt
- Runbook-Schritte, die eine Person jetzt in die Irre führen

Gib pro Änderung Vorher, Nachher und einen Satz Begründung mit Change-ID an.
Alles, was du nicht sicher aus Change oder Doku ableiten kannst, kommt unter
"Offene Fragen" mit Adressat. Nichts erfinden.
```

---

## Nachfassen, wenn der erste Wurf zu dünn ist

```text
Du hast die Überwachungsseite nur oberflächlich geprüft. Gehe sie Zeile für Zeile durch und
zeige mir jede Stelle, die nach dem Release eine Person zu einer falschen Handlung führt.
```
