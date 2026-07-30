# Demo 3 — Testfall-Generator

**Folie 11 · Tab 3 · 3 Minuten**

---

## Schritt 1 — Überblick: was der Agent kann und soll

**Zuerst vorlesen.**

> Dieser Agent macht aus einer Anforderung eine **vollständige Testfall-Tabelle**.
> Er ist von mir, aus der Testautomatisierung.

### Was er tun soll

- Eine User Story mit Akzeptanzkriterien in **einzelne prüfbare Aussagen** zerlegen
- Je Aussage Testfälle ableiten, in **vier Kategorien**:
  - **Happy Path** — der erwartete Ablauf
  - **Fehlerfälle** — ungültige Eingaben, fehlende Pflichtangaben
  - **Grenzwerte** — Minimum, Maximum, ein Schritt darüber und darunter, leer
  - **Berechtigungen** — dieselbe Aktion aus Sicht verschiedener Rollen
- Prüfen, ob **jede Kategorie abgedeckt** ist
- Wo die Anforderung nichts hergibt: **kein Testfall, sondern ein offener Punkt**

### Was er ausdrücklich NICHT tun soll

- Keine Feldnamen erfinden — Bezeichnungen werden wörtlich übernommen
- Die Anforderung nicht bewerten und nicht umformulieren
- **Nichts in ein System schreiben** — er erzeugt eine Tabelle, die ein Mensch überträgt

### Warum das ein guter Agent ist

Grenzwerte und Berechtigungsfälle werden unter Zeitdruck als Erstes vergessen.
**Der Agent vergisst sie nie, weil sie in der Aufgabe stehen.**

---

## Schritt 2 — Der Prompt

**Der entscheidende Teil ist die Kategorienliste.** Sie ist der Grund, warum die Ausgabe
vollständig wird — nicht das Modell, sondern der Auftrag.

```
ROLLE
Du unterstützt eine Testerin oder einen Tester bei der Ableitung von Testfällen.
Du arbeitest NICHT autonom.
Du schreibst in KEIN System. Du erzeugst eine Tabelle als Text, die ein Mensch
prüft und selbst überträgt.

AUFGABE
Arbeite in dieser Reihenfolge:
  1. Zerlege die Eingabe in einzelne prüfbare Aussagen.
  2. Leite je Aussage die Testfälle ab.
  3. Ordne jeden Testfall genau einer Kategorie zu.
  4. Prüfe, ob jede Kategorie abgedeckt ist. Fehlt die fachliche Grundlage,
     erzeuge KEINEN Testfall, sondern einen Eintrag unter OFFENE PUNKTE.
  5. Vergib fortlaufende IDs.

TESTKATEGORIEN (alle sind zu prüfen)
- HAPPY:        erwarteter Ablauf bei gültigen Eingaben
- FEHLER:       ungültige Eingaben, fehlende Pflichtangaben, abgelehnte Aktionen
- GRENZE:       Minimum, Maximum, je ein Schritt darüber und darunter, leer
- BERECHTIGUNG: dieselbe Aktion je Rolle, inklusive "keine Berechtigung"
- ZUSTAND:      dieselbe Aktion bei unterschiedlichem Objektzustand

VERBOTEN
- Feldnamen oder Bezeichnungen erfinden
- die Anforderung bewerten oder umformulieren
- Testfälle zu Kategorien erfinden, für die es keine fachliche Grundlage gibt

AUSGABEFORMAT (STRICT)
Tabelle: ID | Kategorie | Titel | Vorbedingung | Schritte | Erwartetes Ergebnis
Danach: ABDECKUNG (Anzahl je Kategorie)
Danach: OFFENE PUNKTE

Erfinde nichts. Fehlt eine Angabe, schreib FEHLT und formuliere die Rückfrage.
```

### Die drei Stellen, die du erklärst

| Stelle | Was du dazu sagst |
|---|---|
| **Schritt 4 der Aufgabe** | „Fehlt die Grundlage, erzeuge KEINEN Testfall." Ohne diesen Satz erfindet das Modell einen Grenzwerttest für ein Feld, das es gar nicht gibt. |
| **TESTKATEGORIEN** | Die Liste ist der ganze Trick. Vollständigkeit kommt nicht vom Modell, sie kommt vom Auftrag. |
| **Der letzte Satz** | Der FEHLT-Satz von Folie 9. Er sorgt dafür, dass ihr die Lücken seht statt einer glatten Erfindung. |

---

## Schritt 3 — Der Input zum Kopieren

```
Als Kundenbetreuer möchte ich beim Anlegen eines Gemeinschaftskontos sehen,
welche Vollmachten für die zweite kontoführende Person gelten, damit ich sie
im Gespräch korrekt beauskunften kann.

Akzeptanzkriterien:
- Die Vollmachten werden erst nach Auswahl beider Kontoinhaber angezeigt.
- Bei minderjährigen Kontoinhabern wird ein Hinweis auf die gesetzliche
  Vertretung eingeblendet.
- Ohne Berechtigung "Kontodaten erweitert" ist der Bereich nicht sichtbar.
```

**Dann laufen lassen. Stille aushalten.**

---

## Schritt 4 — Worauf ihr schaut

### Was zuverlässig gut ist

Struktur und Vollständigkeit über alle vier Kategorien. Das dritte Akzeptanzkriterium
erzeugt automatisch Berechtigungsfälle — die hätte man von Hand leicht übersehen.

### Was ihr prüfen müsst — und das zeigst du

> „Und jetzt der ehrliche Teil: **hier stimmt es nicht.**
> Der Agent kennt unsere Produktlogik nicht. Wo die Anforderung unscharf war,
> erzeugt er trotzdem etwas Plausibles.
>
> Deshalb steht hinter jedem meiner Agenten ein Prüfschritt — ein Mensch schaut
> drauf und sagt ja oder nein.
>
> Ich zeig euch das bewusst, weil ihr um halb sieben genau diesen Moment habt.
> Euer Agent wird nicht perfekt sein. Meiner ist es auch nicht.
> **Ein Agent mit einer bekannten Schwäche und einem Prüfschritt ist besser
> als einer, dem man blind glaubt.**"

> ⚠️ **Die Schwäche nicht wegmoderieren.** Sie ist das stärkste Coaching-Argument
> des Tages. Wer nur Glanzstücke zeigt, bekommt Teams, die um halb sieben frustriert
> sind, weil ihr Agent „nicht so gut wie deiner" ist.

---

## Der fertige Prompt zum Weitergeben

Der vollständige Prompt steht in
**[prompts/01-testfall-generator.md](../prompts/01-testfall-generator.md)** —
mit Beispiel-Eingabe, erwarteter Ausgabe und Prüfschritt. Darauf verweisen, wenn jemand fragt.
