# 01 · Testfall-Generator

**Aus einer Anforderung werden Testfälle. Ein Skript prüft die Form, du prüfst den Inhalt.**

## Was das zeigt

Ein Agent ist hier drei Dinge:

| Teil | Datei | Wozu |
|---|---|---|
| Dauerkontext | [`.github/copilot-instructions.md`](.github/copilot-instructions.md) | Rolle, Regeln, Abdeckung, Selbstprüfung |
| Vertrag | [`testfaelle.schema.json`](testfaelle.schema.json) | die verbindliche Ausgabestruktur |
| Prüfung | [`validate.mjs`](validate.mjs) | sagt dem Agenten, ob er sich daran gehalten hat |

Die Anforderung liegt in [`beispiel-eingabe/anforderung.md`](beispiel-eingabe/anforderung.md),
eine gültige Ausgabe in [`beispiel-ausgabe/testfaelle.json`](beispiel-ausgabe/testfaelle.json).

## Demo in 2 Minuten

1. Ordner in VS Code öffnen: `code copilot-beispiele/01-testfall-generator`
2. `.github/copilot-instructions.md` aufmachen und kurz zeigen: **das** ist der Agent.
3. Terminal öffnen und den geprüften Stand laufen lassen:
   ```bash
   node validate.mjs
   ```
   → `OK: 8 Testfaelle gueltig` plus Verteilung nach Typ.
4. Im Editor in `beispiel-ausgabe/testfaelle.json` bei `TC-001` das Feld `"typ"` auf
   `"regression"` ändern, speichern, erneut `node validate.mjs`:
   ```
   FEHLER: 1 Verstoss gegen testfaelle.schema.json
     - testfaelle.json.testfaelle[0].typ: "regression" ist kein erlaubter Wert (...)
   ```
   Zurückändern.
5. Copilot Chat öffnen (Agent-Modus), `beispiel-eingabe/anforderung.md` anhängen und schreiben:
   > Erzeuge die Testfälle zu dieser Anforderung nach den Repo-Instructions. Prüfe deine
   > Ausgabe mit `node validate.mjs` und liefere erst ab, wenn das Skript OK meldet.
6. Zeigen, wie der Agent das Skript selbst aufruft, Fehler liest und nachbessert.

Wenn die Zeit knapp wird: Schritt 3, 4 und 5 reichen.

## Was du davon mitnimmst

- Ein Schema plus ein Prüfskript machen die Agenten-Ausgabe maschinell überprüfbar. Der Mensch prüft dann Inhalt, nicht Format.
- Die Instructions gelten für jeden Chat in diesem Repo. Du wiederholst deine Regeln nicht mehr.
- Der Agent korrigiert sich selbst, sobald er ein Kommando hat, das ihm sagt, dass er falsch liegt.

## Voraussetzungen

VS Code mit GitHub-Copilot-Erweiterung, Node 18 oder neuer (`node --version`).
