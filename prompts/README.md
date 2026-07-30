# Prompt-Bibliothek

**Sechs fertige Agenten zum Kopieren. Plus der Bauplan, mit dem du deinen eigenen baust.**

Jede Datei enthält die vollständige Anweisung, eine Beispiel-Eingabe zum Reinkopieren und
die Ausgabe, die du erwarten darfst. Du musst nichts umschreiben, um zu starten.

---

## Die Dateien

| Datei | Agent | Für wen | Demo-tauglich? |
|---|---|---|---|
| [00-prompt-bauplan.md](00-prompt-bauplan.md) | Der Bauplan (Vorlage, kein Agent) | alle, die einen eigenen Agenten bauen | – |
| [01-testfall-generator.md](01-testfall-generator.md) | Testfall-Generator | Test, QA, Fachbereich | **ja — Live-Demo** |
| [02-testkonstellationen.md](02-testkonstellationen.md) | Testkonstellationen-Finder | Test, QA, Testdaten-Verantwortliche | ja |
| [03-user-story-generator.md](03-user-story-generator.md) | User-Story-Generator | Product Owner, Fachbereich, Business Analyse | **ja — Live-Demo** |
| [04-request-pruefer.md](04-request-pruefer.md) | Anforderungs-Prüfer | alle, die Anfragen entgegennehmen | ja |
| [05-doku-agent.md](05-doku-agent.md) | Doku-Konsolidierer | alle, die Wissen verstreut liegen haben | nein (braucht Dateianhang) |
| [06-incident-triage.md](06-incident-triage.md) | Incident-Triage | Betrieb, Support, 2nd Level | ja |

Die beiden mit **Live-Demo** markierten Agenten werden vorne vorgeführt. Du kannst sie
parallel mitbauen.

---

## So benutzt du das

1. **Copilot öffnen.** Microsoft 365 Copilot im Browser oder in Teams starten.
2. **Agent anlegen.** Im Agent Builder einen neuen Agenten erstellen. Name und
   Beschreibung frei wählen, beides ist nur Kosmetik.
3. **Instructions einfügen.** Den kompletten Block aus `## Instructions — komplett kopieren`
   markieren und in das Anweisungsfeld einsetzen. Wirklich alles, von `MODE:` bis zum
   letzten Punkt des Qualitätsgates.
4. **Optional Datei anhängen.** Wenn dein Agent eine Vorlage, ein Glossar oder eine
   Beispiel-Sammlung braucht: als Wissensquelle hochladen. Ohne Anhang funktionieren alle
   sechs Agenten trotzdem.
5. **Testen.** Die Beispiel-Eingabe aus der Datei in den Chat kopieren, absenden, Ergebnis
   mit `## Erwartete Ausgabe` vergleichen. Weicht es stark ab, schau in
   `## Wenn es nicht funktioniert`.

Rechne mit drei bis vier Durchläufen, bis der Agent sitzt. Das ist normal und ist der
eigentliche Teil der Arbeit.

---

## Die 4 Teile eines Prompts

Jeder brauchbare Agenten-Prompt besteht aus vier Blöcken. Fehlt einer, rät das Modell.

| Teil | Beantwortet | Beispiel |
|---|---|---|
| **ROLLE** | Wer bist du und wofür bist du **nicht** zuständig? | „Du unterstützt einen menschlichen Tester. Du schreibst in kein System." |
| **AUFGABE** | Was genau ist zu tun, Schritt für Schritt? | „Leite aus der User Story Testfälle ab: Happy Path, Fehlerfälle, Grenzwerte." |
| **REGELN** | Was ist Pflicht, was ist verboten? | „Erfinde keine Feldnamen. Übernimm Bezeichnungen wörtlich aus der Eingabe." |
| **FORMAT** | Wie sieht die Antwort aus? | „Markdown-Tabelle mit exakt diesen Spalten: ID, Titel, Vorbedingung, Schritte …" |

**ROLLE** und **AUFGABE** liefern die meisten Leute mit. **REGELN** und **FORMAT** werden
fast immer vergessen — und genau daran scheitern die Agenten am Ende des Tages.

---

## Der eine Satz, der in jeden Prompt gehört

```
Erfinde nichts. Fehlt eine Angabe, schreib FEHLT und formuliere die Rückfrage.
```

Ohne diesen Satz füllt das Modell Lücken mit plausiblen Erfindungen. Das ist der
gefährlichste Fehlermodus überhaupt, weil das Ergebnis dabei gut aussieht.

Mit diesem Satz bekommst du statt einer erfundenen Antwort eine ehrliche Lücke und eine
Rückfrage, die du weiterleiten kannst. Ein Ergebnis mit drei `FEHLT`-Markern ist ein
**besseres** Ergebnis als eines ohne.

---

## Zwei Grenzen, die heute für alle gelten

- **Der Agent schreibt in kein System.** Er erzeugt Text, den ein Mensch prüft und dann
  einträgt. Alle sechs Prompts sagen das explizit in der ROLLE.
- **Der Mensch bleibt verantwortlich.** Jede Datei hat einen Abschnitt
  `## Prüfschritt für den Menschen`. Der ist nicht optional.

---

## Wenn du deinen eigenen Agenten baust

Nimm [00-prompt-bauplan.md](00-prompt-bauplan.md) als Gerüst. Oder — schneller — nimm den
Prompt, der deinem Fall am nächsten kommt, und tausche ROLLE, AUFGABE und AUSGABEFORMAT
aus. Die Regelblöcke passen meistens fast unverändert.
