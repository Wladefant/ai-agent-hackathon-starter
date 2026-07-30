# GitHub-Copilot-Beispiele

Drei kleine Repos. Jedes zeigt dieselbe Sache aus einem anderen Winkel: **ein Agent ist keine
Zauberei, sondern eine Instructions-Datei, ein Prompt und ein Stück Code, an dem er sich selbst
messen kann.**

| Beispiel | zeigt | Dauer |
|---|---|---|
| [01 · Testfall-Generator](01-testfall-generator/) | Anforderung rein, Testfälle raus. Ein Schema plus `validate.mjs` prüfen die Form, der Agent korrigiert sich selbst | 2 min |
| [02 · Doku aus Change](02-doku-aus-change/) | Change rein, Doku-Änderungsvorschlag mit Vorher/Nachher raus. Der Mensch übernimmt ihn | 2 min |
| [03 · Azure-DevOps-Agent](03-azure-devops-agent/) | Formlose Notiz rein, fertiges JSON-Patch-Dokument für ein Work Item raus. Gedruckt, nicht gesendet | 2 min |

## Voraussetzungen

VS Code mit der GitHub-Copilot-Erweiterung. Für die beiden Skripte in 01 und 03 zusätzlich
Node 18 oder neuer (`node --version`). Beispiel 02 braucht kein Node.

```bash
git clone https://github.com/Wladefant/ai-agent-hackathon-starter.git
cd ai-agent-hackathon-starter/copilot-beispiele
```

## In welcher Reihenfolge vorführen

1. **01 zuerst.** Hier ist der Aha-Moment am schnellsten sichtbar: das Prüfskript sagt in einer
   Zeile, ob der Agent geliefert hat.
2. **02 danach.** Zeigt dieselbe Idee ohne Code: der Vertrag steckt in der Struktur des
   Vorschlags, geprüft wird von einem Menschen.
3. **03 zum Schluss.** Führt beides zusammen und landet dort, wo die meisten Use Cases heute
   enden: der Agent bereitet vor, ein Mensch schickt ab.

In jedem Ordner liegt die eigentliche Botschaft in `.github/copilot-instructions.md`.
Öffne sie zuerst. Der Rest ist Beiwerk.
