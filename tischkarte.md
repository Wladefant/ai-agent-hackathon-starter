# Tischkarte — die ersten zehn Minuten

**Eine Seite. Ausdrucken, auf den Tisch legen, gemeinsam laut durchgehen, bevor ihr baut.**

---

## Sagt diese vier Sätze laut im Team

```
  1. Die Aufgabe, die uns nervt, ist:

     ______________________________________________________________


  2. Sie passiert ________ mal pro Woche und dauert ________ Minuten.


  3. Das Ergebnis ist gut, wenn:

     ______________________________________________________________


  4. Unser Agent LEGT VOR:

     ______________________________________________________________

     (nicht: er verschickt, nicht: er legt an)
```

**Wer bei Satz 3 hängt, holt einen Coach.** Das ist kein Scheitern. Das ist genau der Punkt,
an dem ein Use Case entweder scharf wird oder still scheitert.

---

## Dann: welches Werkzeug?

```
        Wer benutzt den Agenten NACH heute?
                      │
        ┌─────────────┴─────────────┐
        │                           │
   Der Fachbereich,           Entwicklung, an Code,
   im Alltag                  Repos, Pull Requests
        │                           │
        ▼                           ▼
   M365 COPILOT              GITHUB COPILOT
   (der Normalfall)          (nur mit Entwickler:in im Team)
```

Im Zweifel: **M365 Copilot.**

---

## Euer Prompt braucht vier Teile

| | |
|---|---|
| **ROLLE** | Wer ist der Agent, und wofür ist er **nicht** zuständig? |
| **AUFGABE** | Was genau soll er tun? |
| **REGELN** | Was ist Pflicht, was verboten, woran misst er sich? |
| **FORMAT** | Wie soll die Antwort aussehen? Tabelle? Liste? Welche Spalten? |

**Und dieser Satz, immer:**

```
Erfinde nichts. Fehlt eine Angabe, schreib FEHLT
und formuliere die Rückfrage.
```

Fertige Vorlagen: **github.com/Wladefant/ai-agent-hackathon-starter** → Ordner `prompts/`

---

## Zeitplan

| | |
|---|---|
| 15:40 | Build Time beginnt |
| **16:30** | **Checkpoint: läuft ein erster Durchlauf?** Wenn nicht, jetzt Coach holen. |
| 17:00 | Essen |
| **17:45** | **Demo vorbereiten.** Ab hier nichts Neues mehr bauen. |
| 18:15 | Demos — 3 Minuten + 2 Minuten Fragen |
| 18:45 | Voting |

> **Um 17:45 hört ihr auf zu bauen.** Der häufigste Fehler auf Hackathons ist ein Team, das
> um 18:14 noch etwas Großes umbaut und dann nichts zeigen kann.

---

## Was ihr am Ende zeigt

**1. Problem** — welchen konkreten Pain Point adressiert der Agent?
**2. Lösung** — was macht er, und wie sieht das Ergebnis aus?
**3. Nutzen** — wem hilft das, welcher Aufwand fällt weg?
**4. Nächster Schritt** — was bräuchte es, um weiterzumachen?

Bewertet nach: **Mehrwert · Machbarkeit · Übertragbarkeit · Wow-Faktor**

---

> **Ein guter Prompt ist ein gültiges Ergebnis.**
> Niemand muss um 19 Uhr ein fertiges Produkt haben. Ein durchdachter Prompt, den ab morgen
> zwanzig Leute benutzen, schlägt einen halbfertigen Agenten, den niemand anfasst.
