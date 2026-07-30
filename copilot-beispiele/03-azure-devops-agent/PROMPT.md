# PROMPT

Copilot Chat öffnen, **Agent-Modus** wählen, `beispiel-eingabe/idee.md` anhängen und den
Block hineinkopieren.

---

```text
Lies die angehängte Notiz und mach daraus ein Work Item nach den Repo-Instructions.

Fülle die Struktur aus workitem.template.json aus und schreibe das Ergebnis nach
beispiel-ausgabe/workitem.json. Danach führe aus:

  node build-workitem.mjs beispiel-ausgabe/workitem.json

Meldet das Skript Fehler, korrigiere die Datei und führe es erneut aus. Antworte erst,
wenn es fehlerfrei durchläuft.

Nenne mir am Ende:
1. den Titel
2. die Akzeptanzkriterien als Liste
3. alles, was du aus der Notiz nicht sicher ableiten konntest, als offene Frage
```

---

## Nachfassen, wenn die Kriterien schwammig sind

```text
Kriterium 2 kann ich nicht testen. Formuliere jedes Akzeptanzkriterium so um, dass eine
Testerin es ohne Rückfrage als bestanden oder nicht bestanden markieren kann.
```

## Wenn die Notiz zwei Themen enthält

```text
Trenne die Notiz in Themen. Nenne mir die Themen, bevor du irgendetwas schreibst.
Ich sage dir dann, welches Ticket wird.
```
