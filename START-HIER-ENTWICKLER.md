# Start hier — technischer Einstieg

**Für alle, die entwickeln: Repos, APIs, Skripte, Pipelines.**
Du klonst, du liest den Code, du baust weiter.

---

## Klonen

```bash
git clone https://github.com/Wladefant/ai-agent-hackathon-starter.git
cd ai-agent-hackathon-starter
```

**Voraussetzungen:**

| | Wofür |
|---|---|
| VS Code + GitHub-Copilot-Extension | die drei Beispiele in `copilot-beispiele/` |
| Node 18+ | die Skripte in `azure-devops/scripts/` und die Validatoren |
| Azure CLI (`az`) + `az login` | die Azure-DevOps-Skripte. **Keine PATs** — Auth läuft über deinen Login |

---

## Was du dir zuerst anschaust

### 1. Die drei Copilot-Beispiele — je 2 Minuten

👉 **[copilot-beispiele/](copilot-beispiele/)**

Jedes Beispiel zeigt dasselbe Muster in einem anderen Anwendungsfall:

```
  .github/copilot-instructions.md   ← der persistente Kontext. Copilot liest das immer mit.
  PROMPT.md                          ← der wiederverwendbare Auftrag
  beispiel-eingabe/                  ← womit du es fütterst
  <ein kleines Skript>               ← womit die Ausgabe geprüft wird
```

**Der Punkt, um den es geht:** Ein „Agent" in GitHub Copilot ist zu 80 % gut geschriebener
Kontext plus ein Prüfmechanismus. Nicht Magie, nicht Framework.

### 2. Das Azure-DevOps-Toolkit

👉 **[azure-devops/](azure-devops/)**

Lauffähige Skripte gegen die ADO REST API, ohne Personal Access Token — Authentifizierung
über `az account get-access-token`. Work Items abfragen, anlegen, kommentieren.

```bash
export ADO_ORG=<deine-org>
export ADO_PROJECT=<dein-projekt>
node azure-devops/scripts/ado-auth.mjs      # Selbsttest: klappt der Login?
```

---

## Die Leitplanke, die auch für dich gilt

> **GitHub Copilot läuft lokal.** Für dich ist das großartig. Für die Fachbereichskollegin
> im selben Team ist es eine Sackgasse — sie kann dein Ergebnis danach nicht benutzen.

**Die praktische Konsequenz für gemischte Teams:** Klärt in den ersten zehn Minuten, wer den
Agenten am Ende benutzen soll.

| Wer benutzt ihn danach? | Womit ihr baut |
|---|---|
| Der Fachbereich, im Alltag | **M365 Copilot.** Auch wenn du es in 20 Minuten in Python könntest. |
| Entwicklung, an Code / Repos / PRs | GitHub Copilot. Genau richtig. |
| Beides | Zweigleisig: der Prompt ist das gemeinsame Artefakt, die Ausführung unterschiedlich. |

**Der häufigste Fehler in gemischten Teams:** Der Entwickler baut in vier Stunden etwas
Beeindruckendes, das nach dem Hackathon niemand aus dem Fachbereich starten kann. Ein guter,
geprüfter Prompt in M365 hat mehr Halbwertszeit.

---

## Wenn du Schreibzugriff automatisieren willst

Geht — mit deinem eigenen Login, über die Skripte in `azure-devops/scripts/`. Aber:

1. **Immer erst `--dry-run`.** Die Write-Skripte drucken den Request, bevor sie ihn senden.
2. **Nichts in Produktivumgebungen.** Für heute reichen Test-/Sandbox-Bereiche.
3. **Keine PATs anlegen.** Auth über `az login`, Token wird gecacht, nichts landet im Repo.
4. **Keine Zugangsdaten committen.** Das Repo hat eine `.gitignore` dafür, verlass dich
   trotzdem nicht darauf.

---

## Was am Abend gezeigt wird

3 Minuten Demo + 2 Minuten Fragen. Bewertet nach **Mehrwert · Machbarkeit · Übertragbarkeit ·
Wow-Faktor**.

**Zeig, was läuft, nicht was geplant ist.** Ein Skript, das eine Sache richtig macht, schlägt
eine Architektur, die noch nichts tut. „Übertragbarkeit" heißt: Kann ein anderes Team das
morgen für seinen Fall nachbauen? Wenn dein Ergebnis ein gut dokumentierter Prompt plus
20 Zeilen Glue-Code ist, ist die Antwort ja.
