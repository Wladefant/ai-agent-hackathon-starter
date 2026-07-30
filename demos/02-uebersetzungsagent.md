# Demo 2 — Übersetzungsagent

**Folie 10 · Tab 2 · 3 Minuten**

---

## Schritt 1 — Überblick: was der Agent kann und soll

**Zuerst vorlesen. Bevor irgendetwas auf dem Bildschirm passiert.**

> Dieser Agent ist ein **Übersetzungsassistent für den Kundenservice**.
> Er wurde von einem Kollegen gebaut. In M365. Ohne eine Zeile Code.

### Was er tun soll

- Jede Eingabe ist ein **Quelltext zum Übersetzen** — Deutsch nach Englisch oder umgekehrt
- Er **erkennt die Richtung selbst**
- Er zieht Fachbegriffe aus einem **angehängten Glossar**, statt sie frei zu übersetzen
- Er liefert zusätzlich ein **Audit-Log**: was kam aus dem Glossar, was nicht

### Was er ausdrücklich NICHT tun soll

- Nicht antworten, nicht erklären, nicht zusammenfassen, nicht beraten
- Nichts hinzufügen: keine Zusagen, keine Richtlinien, keine Annahmen
- Nichts weglassen
- **Nicht selbst an Kundinnen und Kunden schreiben** — ein Mensch entscheidet über die Nutzung

### Warum das ein guter Agent ist

Er hat **mehrere Schritte** (Richtung erkennen, Glossar prüfen, übersetzen, protokollieren)
und sein Ergebnis ist **prüfbar** — genau die zwei Bedingungen von Folie 7.

---

## Schritt 2 — Der Prompt

**Jetzt den Auftrag zeigen und erklären.** Das ist der Teil, der die Leute befähigt.
Nicht vollständig vorlesen — die vier markierten Stellen erklären.

```
ROLLE
Sie sind ein Übersetzungsassistent für Kundenservice-Mitarbeitende.
Sie unterstützen einen MENSCHLICHEN Agenten.
Sie handeln NICHT autonom und kommunizieren NICHT direkt mit Kundinnen oder Kunden.

AUFGABE
- Jede Eingabe ist IMMER ein Quelltext für eine Übersetzung.
- Keine Beantwortung, Erklärung, Zusammenfassung, Bewertung oder Beratung.
- Übersetzen Sie ausschließlich in die jeweils andere Sprache (DE <-> EN).
- Liefern Sie zusätzlich ein Audit-Log zur Terminologie-Prüfung.

QUELLENPRIORITÄT
1. Excel-Glossar
2. Professionelles Übersetzungsurteil

BEWAHREN (STRICT)
- Verantwortlichkeiten
- Produkt- und Markennamen
- Platzhalter, Variablen, IDs, Tags
- Zahlen, Beträge, Datumsangaben, Referenzen

VERBOTEN
- Inhalte erfinden
- zusammenfassen oder erklären
- Verantwortlichkeiten ändern
- rechtliche, steuerliche oder finanzielle Beratung ergänzen

AUSGABEFORMAT (STRICT)
[TRANSLATE]
<übersetzter Text>

[AUDIT_LOG]
ExcelLookup: {SUCCESSFUL | NOT_AVAILABLE}
Richtung: {EN->DE | DE->EN}
SourceCoverage:
- SOURCE: <Begriff> | STATUS: {FOUND | NOT_FOUND} | TARGET_USED: <Begriff oder NONE>
```

### Die vier Stellen, die du erklärst

| Stelle | Was du dazu sagst |
|---|---|
| **„Sie handeln NICHT autonom"** | Steht ganz oben, weil es die wichtigste Regel ist. Der Agent weiß, dass ein Mensch das Ergebnis prüft. |
| **QUELLENPRIORITÄT** | Erst das Glossar, dann eigenes Urteil. So bleibt Fachterminologie stabil, statt jedes Mal anders zu klingen. |
| **BEWAHREN (STRICT)** | Beträge, IDs, Zuständigkeiten werden nicht angefasst. Genau da entstehen sonst die teuren Fehler. |
| **AUSGABEFORMAT** | Erzwingt das Audit-Log. **Ohne Format kein Prüfschritt** — das ist der Kern der ganzen Demo. |

---

## Schritt 3 — Der Input zum Kopieren

**Diesen Text einfügen:**

```
Thank you for the information. We need the notification. You can upload it
via the document upload in online banking or send it to us by email. Please
note that we currently cannot see your Extra account because it is a separate
account and you are logged into your joint account.
```

**Falls Zeit bleibt oder der erste Lauf zu glatt war** — dieser läuft in die andere Richtung
und zeigt, dass der Agent sie selbst erkennt:

```
Wir senden Ihnen einen Zwischenkontoauszug per Post-Box zu. Bitte reichen Sie
die Anzeige bis zum 15.08. ein, sonst müssen wir den Vorgang schließen.
```

---

## Schritt 4 — Worauf ihr schaut

**Nicht auf die Übersetzung.** Die kann jedes Modell.

**Auf das Audit-Log darunter.** Der Satz dazu:

> „Das Kunststück ist nicht die Übersetzung. Das Kunststück ist, dass ein Mensch
> **in fünf Sekunden prüfen kann, ob er dem Ergebnis trauen darf.**
> Genau das meinte ich mit prüfbarem Ergebnis — und es kostet drei Zeilen Prompt."

---

## Wenn es nicht läuft

> „Das Netz will heute nicht. Ich zeig's euch nachher am Tisch — kommt vorbei."

Screenshots liegen auf dem Desktop. Denselben Text sprechen, es funktioniert auch so.
