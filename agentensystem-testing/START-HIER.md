# Produktionsreifes Agentensystem — das große Beispiel

**Was das ist:** Eine komplette Sechs-Agenten-Kette, die aus Projektdokumenten validierte
Anforderungen und Testfälle macht. Kein Spielzeug, kein Ausschnitt — das läuft.

**Für wen:** Alle, die sehen wollen, wie ein ernsthaftes Agentensystem von innen aussieht.
Zum Anschauen braucht es nichts außer einem Browser. Zum Ausführen Python und GitHub Copilot.

> **Wichtig: Das ist nicht meine Arbeit.** Das System wurde intern geteilt und liegt hier,
> damit ihr es als Vorlage benutzen könnt. Wenn ihr Teile davon übernehmt, sagt dazu, woher
> es kommt.

---

## Warum ihr da reinschauen solltet

Die meisten Teams bauen heute einen Agenten. Dieses System zeigt, wie es aussieht, wenn
**sechs** zusammenarbeiten — und was man dafür braucht, das im Vortrag nicht vorkam:

| Was ihr hier seht | Warum es zählt |
|---|---|
| **Rollenteilung statt Alleskönner** | Sechs Agenten mit je einer Aufgabe. Extrahieren, validieren, generieren, prüfen sind getrennte Schritte |
| **Skills als eigene Dateien** | Die Prüfregeln liegen in `.github/skills/` und werden von mehreren Agenten benutzt. Regel ändern heißt: Textdatei ändern, nicht Code |
| **Ein Orchestrator** | `orchestrator.agent.md` fährt die Kette und hält an den Prüfpunkten an |
| **Menschliche Prüfgates** | `human-review-preparation.skill.md` — genau das Muster aus dem Vortrag, nur ausgebaut |
| **Bridge-Architektur** | Python macht nur Ein- und Ausgabe. Alle Bewertung und Formulierung macht das Modell. Kein hartkodiertes Urteil |
| **Selbstkorrektur mit Grenze** | `intelligent-remediation.skill.md` plus `max_remediation_iterations: 3` in `config.json`. Der Agent bessert nach, aber nicht endlos |
| **Schwellwerte statt Bauchgefühl** | `config.json` legt fest, ab wann etwas besteht. Nachlesbar, diskutierbar, änderbar |

---

## In 3 Minuten überflogen — die Reihenfolge

Nur lesen, nichts installieren:

1. **[`.github/copilot-instructions.md`](.github/copilot-instructions.md)** — der Gesamtkontext.
   Das ist die Datei, die Copilot immer mitliest.
2. **[`.github/agents/orchestrator.agent.md`](.github/agents/orchestrator.agent.md)** — wie die
   Kette gefahren wird und wo sie anhält.
3. **[`.github/skills/test-case-quality-check.skill.md`](.github/skills/test-case-quality-check.skill.md)** —
   ein Prüf-Skill im Detail. Das ist der Teil, den ihr für euren eigenen Fall am ehesten
   abschreiben könnt.
4. **[`config.json`](config.json)** — alle Schwellwerte an einem Ort.

**Der Aha-Moment liegt in Schritt 3.** Ein Skill ist eine Markdown-Datei mit Prüfregeln.
Mehr nicht. Genau so baut ihr euren eigenen.

---

## Ausführen (optional, braucht 15 Minuten Setup)

Vollständige Anleitung: **[README.md](README.md)** — die Originaldokumentation des Systems.

Kurzfassung:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Beispielprojekt liegt schon bereit:
python scripts/extract.py --input inputs/SAMPLE_IP --output output/extracted/SAMPLE_IP
```

Danach im Copilot-Chat: `@orchestrator Run the full pipeline for SAMPLE_IP`

**Der Windows-Stolperstein:** Die Konsole ist auf cp1252. Vorher
`$env:PYTHONIOENCODING="utf-8"` setzen, sonst brechen die Skripte bei Sonderzeichen ab.

**Beispieldaten sind dabei.** `inputs/SAMPLE_IP/` enthält eine
Instant-Payments-Anforderung, `output/` die dazu erzeugten Zwischenergebnisse. Ihr könnt
also durchlaufen lassen, ohne eigene Dokumente zu haben.

---

## Was ihr davon heute klauen solltet

Ihr baut das an einem Nachmittag nicht nach. Sollt ihr auch nicht. Nehmt drei Dinge mit:

1. **Eine Skill-Datei mit Prüfregeln.** Trennt „was soll rauskommen" von „woran erkenne ich,
   dass es gut ist". Zwei Dateien, nicht ein Prompt.
2. **Ein Prüfgate an der richtigen Stelle.** Nicht am Ende, sondern dort, wo ein Fehler
   sonst in alle Folgeschritte durchschlägt.
3. **Schwellwerte, die irgendwo geschrieben stehen.** „Gut genug" muss eine Zahl sein, die
   man diskutieren kann — sonst diskutiert ihr das Gefühl.

---

## Grenzen, ehrlich

- Läuft lokal mit GitHub Copilot. Damit gilt dieselbe Leitplanke wie im Vortrag: Für
  fachliche Anwender:innen im Alltag ist das **kein** produktiver Weg, dafür braucht es M365.
  Siehe [Infoblatt](../infoblatt.md).
- Excel-Dateien als Zwischenformat. Praktisch, aber kein Systemintegrationsmuster.
- Die Beispiel-IDs und Komponentennamen stammen aus dem Ursprungsprojekt. Wenn ihr das
  System übernehmt, ersetzt sie durch eure eigenen.
