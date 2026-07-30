# Demo 1 — Einen Agenten live bauen

**Folie 6 · Tab 1 · 4 Minuten, harte Grenze**

---

## Schritt 1 — Überblick: was ihr gleich seht

**Zuerst sagen, bevor du klickst.**

> Ich baue jetzt vor euren Augen einen Agenten. Von null.
> Das dauert keine fünf Minuten, und danach könnt ihr es nachmachen.

### Was der Agent Builder kann

- **Wissensquellen** anbinden — SharePoint, hochgeladene Dateien, öffentliche Websites
- **Dateien und Diagramme erzeugen** — über den Code-Interpreter
- **Instructions** bis 8.000 Zeichen — das ist das eigentliche Gehirn
- **Sofort testen** im „Try it"-Tab, während ihr baut

### Was er heute nicht kann

- **Keine Actions** — er schreibt in kein System und ruft keine API
- **Keine Trigger** — er startet nicht von selbst

Deshalb die Bauregel von Folie 5: **Der Agent legt vor, ein Mensch schickt ab.**

---

## Schritt 2 — Die sieben Schritte

| # | Was | Wo genau |
|---|---|---|
| 1 | **Neuer Agent** | M365 Copilot, rechte Seitenleiste unter „Agents" |
| 2 | **Beschreiben statt konfigurieren** | In normalem Deutsch sagen, was er tun soll. Name, Beschreibung und Instructions füllen sich selbst |
| 3 | **Auf „Configure" wechseln** | Dort steht, was er generiert hat |
| 4 | **Instructions ersetzen** | Durch den fertigen Prompt aus dem Repo |
| 5 | **Wissensquelle hinzufügen** | Über das `+` — SharePoint-Ordner oder Datei, bis zu 20 Stück |
| 6 | **Capabilities einschalten** | Schalter „Create documents, charts, and code", falls ihr Dateien braucht |
| 7 | **„Try it" testen** | Mit der Beispiel-Eingabe aus derselben Repo-Datei |

---

## Schritt 3 — Was du dabei sagst

**Bei Schritt 2, dem wichtigsten:**

> „Und jetzt der Trick, den die meisten nicht kennen: **Ihr müsst nichts konfigurieren.**
> Ihr beschreibt in normalem Deutsch, was der Agent tun soll — und Name, Beschreibung
> und Instructions füllen sich von selbst. Er schlägt sogar Wissensquellen und
> Fähigkeiten vor."

**Diesen Text als Beschreibung eintippen:**

```
Du hilfst mir, aus einer Anforderung Testfälle abzuleiten. Ich gebe dir eine
User Story mit Akzeptanzkriterien, du erzeugst eine Tabelle mit Testfällen für
Happy Path, Fehlerfälle, Grenzwerte und Berechtigungen.
```

**Bei Schritt 4:**

> „Was er generiert, ist ein brauchbarer Start — aber kein guter Prompt.
> Ich ersetze das jetzt durch unseren fertigen aus dem Repo. Der hat feste Kategorien,
> ein Ausgabeformat und Prüfregeln. **Das ist der Unterschied zwischen einem Versuch
> und einem Werkzeug.**"

**Bei Schritt 7:**

> „Und jetzt sofort testen. **Nicht am Ende — sofort.**
> Rechnet mit drei bis vier Durchläufen, bis der Agent sitzt. Das ist normal,
> und das ist die eigentliche Arbeit heute Nachmittag. Nicht das Anlegen."

---

## Schritt 4 — Die Grenzen zum Merken

Diese Zahlen nennen, während du im Configure-Tab bist:

| Feld | Grenze |
|---|---|
| Name | 30 Zeichen |
| Beschreibung | 1.000 Zeichen |
| **Instructions** | **8.000 Zeichen** |
| Wissensquellen | 20 |

> „Achttausend Zeichen sind viel. Unsere fertigen Prompts brauchen sechs- bis
> siebentausend — ihr habt also noch Platz für eure eigenen Regeln."

---

## ⚠️ Harte Grenze: 4 Minuten

Wenn etwas hakt: **abbrechen.**

> „Das zeig ich euch beim Coaching."

Zurück zum Deck. Nicht reparieren, nicht erklären warum. Der Live-Bau ist wertvoll,
aber nicht wertvoll genug für sechs Minuten Fummelei vor dreißig Leuten.
