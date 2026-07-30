# Infoblatt — In welchem System baue ich meinen Agenten?

**Bitte vor dem Bauen lesen. Kostet zwei Minuten und spart vier Stunden.**

---

## Warum es dieses Blatt gibt

Am Ende des Tages sollen **lauffähige** Agenten stehen, die man danach auch wirklich benutzen
darf. Das ist der Haken: Es gibt mehrere Werkzeuge, die alle „KI-Agent" heißen, und **nur
eines davon führt heute in den produktiven Einsatz.**

Wer im falschen Werkzeug baut, hat am Abend eine schöne Demo, die niemand einsetzen kann.

---

## Die Regel in einem Satz

> **Baut mit M365 Copilot.**
> Alles andere ist heute entweder nur lokal oder noch nicht ausgerollt.

---

## Die drei Werkzeuge

| | **M365 Copilot** ✅ | GitHub Copilot | Copilot Studio |
|---|---|---|---|
| **Für wen** | alle mit Lizenz | Entwickler:innen | derzeit nur wenige Zugänge |
| **Läuft produktiv?** | **ja**, als Flow | **nein — nur lokal** | ja |
| **Lesen** | ja | ja | ja |
| **Schreiben** (Ticket anlegen, SharePoint ändern) | **heute meist nicht** | — | ja |
| **Auslöser / Trigger** | nein | nein | ja |
| **Für den Hackathon** | **das hier nehmen** | nur mit Entwickler:in im Team | nicht verfügbar |

**M365 Copilot** ist das Werkzeug der Wahl. Ein Agent, der hier gebaut wird, kann später als
Flow produktiv gestellt werden. Es gilt: Ein Agent, der produktiv arbeiten soll, muss
vollständig produktiv laufen — nicht halb auf einem Arbeitsplatzrechner.

**GitHub Copilot** ist für fachliche Teilnehmende die Sackgasse: Der Agent läuft nur lokal.
Als Entwicklungswerkzeug super. Als Ergebnis, das der Fachbereich danach benutzt, unbrauchbar.

**Copilot Studio** kann alles, was man sich wünscht: Schreibzugriff, echte Flows, Trigger.
Der Rollout läuft aber noch. Für heute nicht planbar.

---

## Die wichtigste Einschränkung

**Die meisten Agenten können heute nur lesen, nicht schreiben.**

```
  WAS HEUTE GEHT                        WAS HEUTE NOCH NICHT GEHT
  ┌──────────────────────────────┐      ┌────────────────────────────┐
  │ lesen, suchen, recherchieren │      │ Ticket automatisch anlegen │
  │ zusammenfassen, strukturieren│      │ SharePoint-Eintrag ändern  │
  │ Entwürfe erzeugen            │      │ sich selbst starten        │
  │ Word / PowerPoint / Excel    │      │   (Trigger)                │
  │ SharePoint, Teams, Outlook,  │      └────────────────────────────┘
  │ OneNote, Besprechungen       │             ↑ kommt mit Copilot Studio
  └──────────────────────────────┘
```

> **Plant euren Agenten so, dass er am Ende etwas *vorlegt*, das ein Mensch abschickt.**
> Nicht so, dass er selbst abschickt.

Dann funktioniert er heute — und wird später, wenn Schreibzugriff kommt, einfach
durchgeschaltet. Der Rest bleibt, wie er ist.

---

## Was als Ergebnis zählt

**Nicht nur der fertige Agent.** Ein durchdachter, geprüfter Prompt, den ab morgen zwanzig
Leute benutzen, schlägt einen halbfertigen Agenten, den niemand anfasst.

Beides ist ein gültiges Ergebnis. Niemand muss um 19 Uhr ein Produkt haben.

---

## Vor dem Start — vier Fragen an den eigenen Use Case

| | Frage | Warum |
|---|---|---|
| 1 | **Wie oft** kommt die Aufgabe vor? | Häufigkeit × Zeit = der Nutzen. |
| 2 | **Woran erkennt man, dass das Ergebnis gut ist?** | Ohne Prüfbarkeit keine Freigabe. |
| 3 | **Wo liegen die Daten**, und darf der Agent ran? | Der häufigste stille Blocker. |
| 4 | Muss der Agent etwas **schreiben oder ändern**? | Wenn ja: als Vorschlag bauen. |

---

## Ein Prompt, der funktioniert — die vier Teile

Der häufigste Fehler ist ein zu kurzer Auftrag.

```
  ROLLE      "Du bist Requirements-Analyst im Fachbereich <FACHBEREICH>."
  AUFGABE    "Prüfe den folgenden Request auf Vollständigkeit."
  REGELN     "Pflichtangaben: Zielsystem, Datenfelder, Frist, Ansprechpartner."
  FORMAT     "Tabelle: Angabe | vorhanden? | Rückfrage an den Anforderer"
```

Fehlt das **Format**, kommt Fließtext zurück und man arbeitet nach.
Fehlen die **Regeln**, bewertet das Modell nach Gefühl.

**Und der eine Satz, der in jeden Prompt gehört:**

> *„Erfinde nichts. Wenn eine Angabe fehlt, schreibe FEHLT und formuliere die Rückfrage."*

Ohne ihn füllt das Modell Lücken plausibel auf, und man sieht dem Ergebnis nicht an, was
echt war und was erfunden.

Fertige Vorlagen: **[prompts/](prompts/)**

---

## Wenn ihr nicht weiterkommt

**Coaches sind vor Ort und im Chat. Fragt früh**, nicht erst in der letzten halben Stunde.

Die häufigste vermeidbare Sackgasse ist ein Use Case, der Schreibzugriff braucht. Das lässt
sich in fünf Minuten umbauen, wenn man es früh merkt, und gar nicht mehr, wenn es 18:30 Uhr ist.
