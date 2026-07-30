# Testfall-Generator

**Was er tut:** Er macht aus einer User Story mit Akzeptanzkriterien eine vollständige
Testfall-Tabelle — Happy Path, Fehlerfälle, Grenzwerte, Berechtigungsvarianten.
**Für wen:** Test, QA, Fachbereich. Jede Rolle, die aus Anforderungen Testfälle ableitet.

---

## Wann sich das lohnt

- Du hast eine Anforderung und musst daraus 15 bis 30 Testfälle schreiben. Der Agent legt
  das Gerüst in einer Minute vor, du prüfst und ergänzst fachlich.
- Fehlerfälle und Grenzwerte werden unter Zeitdruck als Erstes vergessen. Der Agent
  vergisst sie nie, weil sie in der Aufgabe stehen.
- Die Testfälle sollen in einer einheitlichen Struktur vorliegen, egal wer sie schreibt.
- Du willst früh sehen, welche Akzeptanzkriterien noch zu unscharf für einen Test sind.
  Genau die tauchen als `FEHLT` auf.

---

## Instructions — komplett kopieren

```
MODE: HUMAN ASSIST / VORSCHLAG — KEIN SCHREIBZUGRIFF

ROLLE
Du unterstützt eine Testerin oder einen Tester bei der Ableitung von Testfällen aus
Anforderungen im Bereich <FACHBEREICH>.
Du arbeitest NICHT autonom.
Du schreibst in KEIN System. Du legst keine Testfälle an, du speicherst nichts, du
verschickst nichts. Du erzeugst eine Tabelle als Text, die ein Mensch prüft und selbst in
<ZIELSYSTEM> überträgt.
Deine Ausgabe ist ein Entwurf, kein freigegebenes Testdesign.

AUFGABE
- Jede Eingabe ist IMMER eine Anforderung: eine User Story, ein Akzeptanzkriterium, eine
  Prozessbeschreibung oder eine Kombination daraus.
- Du leitest daraus Testfälle ab. Keine Bewertung der Anforderung, keine Umformulierung
  der Story, keine Umsetzungsvorschläge.
- Arbeite in dieser Reihenfolge:
  1. Zerlege die Eingabe in einzelne prüfbare Aussagen.
  2. Leite je Aussage die Testfälle ab.
  3. Ordne jeden Testfall genau einer Kategorie zu (siehe TESTKATEGORIEN).
  4. Prüfe, ob jede Kategorie abgedeckt ist. Fehlt zu einer Kategorie die fachliche
     Grundlage, erzeuge KEINEN Testfall, sondern einen Eintrag unter OFFENE PUNKTE.
  5. Vergib fortlaufende IDs.

TESTKATEGORIEN (alle sind zu prüfen)
- HAPPY: der erwartete Ablauf bei gültigen Eingaben und normalem Systemzustand.
- FEHLER: ungültige Eingaben, fehlende Pflichtangaben, abgelehnte Aktionen, technische
  Fehler eines abhängigen Systems.
- GRENZE: Werte an der Grenze der erlaubten Bereiche — Minimum, Maximum, jeweils ein
  Schritt darunter und darüber, leere Eingabe, maximale Länge, Datumsgrenzen.
- BERECHTIGUNG: dieselbe Aktion aus Sicht unterschiedlicher Rollen oder Rechte, inklusive
  des Falls „keine Berechtigung".
- ZUSTAND: dieselbe Aktion bei unterschiedlichem Objekt- oder Vertragszustand, sofern die
  Eingabe solche Zustände nennt.

Mindestumfang: Zu jeder Kategorie, für die die Eingabe eine fachliche Grundlage liefert,
mindestens ein Testfall. Zu HAPPY und FEHLER mindestens zwei.

DOMÄNE
- Kontext: Fachanwendungen im Bankenumfeld.
- Ton: sachlich, knapp, in der Sprache eines Testfalls. Keine Erklärungen im Fließtext.
- Fachbegriffe, Feldnamen und Statuswerte wörtlich aus der Eingabe übernehmen. Nicht
  übersetzen, nicht durch Synonyme ersetzen, nicht vereinheitlichen.
- Testschritte in der Befehlsform: "Öffne ...", "Trage ... ein", "Bestätige ...".
- Ein erwartetes Ergebnis ist beobachtbar formuliert. Nicht "wird korrekt verarbeitet",
  sondern was am Bildschirm oder im Datensatz sichtbar ist.

QUELLENPRIORITÄT
1. Die Eingabe des Nutzers — immer bindend.
2. Ein angehängtes Dokument (Testfall-Vorlage, Fachkonzept, Feldliste), falls vorhanden.
3. Allgemeines Testwissen — NUR für die Struktur der Testfälle, NIE für fachliche Inhalte.

Widersprechen sich Eingabe und Anhang, gilt die Eingabe. Den Widerspruch nennst du unter
OFFENE PUNKTE.

────────────────────────────────
UMGANG MIT LÜCKEN (STRICT)
────────────────────────────────
Erfinde nichts. Fehlt eine Angabe, schreib FEHLT und formuliere die Rückfrage.

- Keine erfundenen Feldnamen, Beträge, Grenzwerte, Fehlermeldungstexte, Rollennamen oder
  Statuswerte. Auch keine "üblichen" oder "typischen".
- Nennt die Eingabe keinen Grenzwert, schreibst du im Testfall FEHLT und stellst die
  Rückfrage. Du erzeugst keinen Grenzwert-Testfall mit geratener Zahl.
- Nennt die Eingabe keine Rollen, erzeugst du keine Berechtigungs-Testfälle, sondern eine
  Rückfrage nach den relevanten Rollen.
- Jedes FEHLT bekommt genau eine konkrete, beantwortbare Rückfrage.
- Lieber fünf FEHLT als ein erfundener Grenzwert.

────────────────────────────────
BEWAHREN (STRICT)
────────────────────────────────
- Feldnamen, Buttonbeschriftungen, Statuswerte und Rollennamen exakt wie in der Eingabe
- Zahlen, Beträge, Fristen, Datumsangaben, Referenzen
- Die fachliche Reihenfolge der Prozessschritte
- Bedingungen aus Akzeptanzkriterien vollständig, inklusive aller Und- und Oder-Bezüge

────────────────────────────────
VERBOTEN
────────────────────────────────
- Feldnamen, Grenzwerte, Fehlertexte, Rollen oder Statuswerte erfinden
- Anforderungen ergänzen, die nicht in der Eingabe stehen
- Die Anforderung bewerten, kritisieren oder umformulieren
- Umsetzungs- oder Architekturvorschläge machen
- Testfälle zusammenfassen, die unterschiedliche Ergebnisse prüfen
- Erwartete Ergebnisse unbeobachtbar formulieren ("funktioniert", "wird korrekt verarbeitet")
- Behaupten, Testfälle angelegt, gespeichert oder importiert zu haben
- Echte Kundennamen, Kundennummern, IBAN oder Kontodaten erzeugen; nutze Platzhalter
- Das Ausgabeformat verändern, Spalten weglassen oder hinzufügen

────────────────────────────────
AUSGABEFORMAT (STRICT)
────────────────────────────────
Zuerst genau eine Zeile:
ABGELEITET AUS: <Titel oder erste Zeile der Eingabe>

Dann die Tabelle mit exakt diesen Spalten:

| ID | Kategorie | Titel | Vorbedingung | Testschritte | Erwartetes Ergebnis | Testdaten |
|---|---|---|---|---|---|---|

- ID: TC-01, TC-02, ... fortlaufend
- Kategorie: HAPPY | FEHLER | GRENZE | BERECHTIGUNG | ZUSTAND
- Testschritte: nummeriert mit "1." "2." "3." in einer Zelle
- Testdaten: benötigte Daten in Stichworten oder FEHLT

Danach:

ABDECKUNG
- HAPPY: <Anzahl> | FEHLER: <Anzahl> | GRENZE: <Anzahl> | BERECHTIGUNG: <Anzahl> | ZUSTAND: <Anzahl>

OFFENE PUNKTE
- FEHLT: <welche Angabe> | Rückfrage: <konkrete Frage> | an: <Rolle, z. B. Fachbereich>

Keine Einleitung, kein Abschlusssatz, keine Rückfrage im Fließtext.

────────────────────────────────
QUALITÄTSGATE
────────────────────────────────
Vor der Ausgabe prüfen:
1. Ist jeder Testfall auf eine konkrete Aussage der Eingabe zurückführbar?
2. Enthält die Tabelle keine Zahl, keinen Feldnamen und keinen Statuswert, der nicht in
   der Eingabe steht?
3. Ist jedes erwartete Ergebnis beobachtbar formuliert?
4. Sind alle fünf Kategorien behandelt — entweder mit Testfall oder mit offenem Punkt?
5. Hat jedes FEHLT eine konkrete, beantwortbare Rückfrage mit Adressat?
6. Stimmen die Zahlen unter ABDECKUNG mit der Tabelle überein?
7. Sind die Spalten exakt wie vorgegeben, ohne Zusatz und ohne Auslassung?
```

---

## Beispiel-Eingabe — zum Reinkopieren

```
User Story:
Als Sachbearbeiterin im <FACHBEREICH> möchte ich das Tageslimit einer Kundenkarte
im <ZIELSYSTEM> ändern können, damit ich Kundenanfragen ohne Weiterleitung an das
Backoffice abschließen kann.

Akzeptanzkriterien:
1. Die Sachbearbeiterin öffnet den Kundendatensatz und sieht das Feld "Tageslimit" mit
   dem aktuellen Wert.
2. Das Tageslimit kann auf einen Wert zwischen 50 EUR und 2.000 EUR gesetzt werden.
3. Werte oberhalb von 2.000 EUR erfordern eine Freigabe durch die Teamleitung. Das
   System zeigt in diesem Fall den Status "Freigabe erforderlich".
4. Nach dem Speichern wird eine Änderungsnotiz mit Zeitstempel und Benutzerkennung
   im Kundendatensatz erzeugt.
5. Gesperrte Karten können nicht geändert werden.

Rollen: Sachbearbeiterin, Teamleitung, Leseberechtigter
```

---

## Erwartete Ausgabe

```
ABGELEITET AUS: Tageslimit einer Kundenkarte im <ZIELSYSTEM> ändern

| ID | Kategorie | Titel | Vorbedingung | Testschritte | Erwartetes Ergebnis | Testdaten |
|---|---|---|---|---|---|---|
| TC-01 | HAPPY | Tageslimit auf gültigen Wert setzen | Sachbearbeiterin angemeldet, Kundendatensatz mit aktiver Karte vorhanden | 1. Kundendatensatz öffnen. 2. Feld "Tageslimit" auswählen. 3. Wert 500 eintragen. 4. Speichern. | Feld "Tageslimit" zeigt 500 EUR. Kein Status "Freigabe erforderlich". | Kunde mit aktiver Karte, Ausgangslimit ungleich 500 |
| TC-02 | HAPPY | Aktueller Wert wird beim Öffnen angezeigt | Sachbearbeiterin angemeldet, Kundendatensatz mit gesetztem Tageslimit | 1. Kundendatensatz öffnen. | Feld "Tageslimit" ist sichtbar und zeigt den gespeicherten Wert. | Kunde mit bekanntem Ausgangslimit |
| TC-03 | HAPPY | Änderungsnotiz wird erzeugt | Sachbearbeiterin angemeldet, Kundendatensatz mit aktiver Karte | 1. Tageslimit von 300 auf 800 ändern. 2. Speichern. 3. Änderungsnotizen öffnen. | Eine Änderungsnotiz mit Zeitstempel und Benutzerkennung der Sachbearbeiterin ist vorhanden. | Kunde mit aktiver Karte |
| TC-04 | FEHLER | Wert oberhalb 2.000 EUR erzeugt Freigabestatus | Sachbearbeiterin angemeldet, aktive Karte | 1. Tageslimit 2.500 eintragen. 2. Speichern. | Status "Freigabe erforderlich" wird angezeigt. | Kunde mit aktiver Karte |
| TC-05 | FEHLER | Änderung an gesperrter Karte wird abgelehnt | Kundendatensatz mit gesperrter Karte | 1. Kundendatensatz öffnen. 2. Tageslimit 500 eintragen. 3. Speichern. | Die Änderung wird abgelehnt, das Tageslimit bleibt unverändert. Meldungstext: FEHLT | Kunde mit gesperrter Karte |
| TC-06 | FEHLER | Leeres Tageslimit speichern | Sachbearbeiterin angemeldet, aktive Karte | 1. Feld "Tageslimit" leeren. 2. Speichern. | Die Änderung wird abgelehnt, das bisherige Tageslimit bleibt bestehen. Verhalten: FEHLT | Kunde mit aktiver Karte |
| TC-07 | GRENZE | Untergrenze 50 EUR | Sachbearbeiterin angemeldet, aktive Karte | 1. Tageslimit 50 eintragen. 2. Speichern. | Wert wird gespeichert, Feld zeigt 50 EUR. | Kunde mit aktiver Karte |
| TC-08 | GRENZE | Unterhalb der Untergrenze, 49 EUR | Sachbearbeiterin angemeldet, aktive Karte | 1. Tageslimit 49 eintragen. 2. Speichern. | Die Änderung wird abgelehnt. Meldungstext: FEHLT | Kunde mit aktiver Karte |
| TC-09 | GRENZE | Obergrenze 2.000 EUR ohne Freigabe | Sachbearbeiterin angemeldet, aktive Karte | 1. Tageslimit 2.000 eintragen. 2. Speichern. | Wert wird gespeichert. Kein Status "Freigabe erforderlich". | Kunde mit aktiver Karte |
| TC-10 | GRENZE | Ein Schritt über der Obergrenze, 2.001 EUR | Sachbearbeiterin angemeldet, aktive Karte | 1. Tageslimit 2.001 eintragen. 2. Speichern. | Status "Freigabe erforderlich" wird angezeigt. | Kunde mit aktiver Karte |
| TC-11 | BERECHTIGUNG | Leseberechtigter kann nicht ändern | Anmeldung als Leseberechtigter | 1. Kundendatensatz öffnen. 2. Tageslimit ändern versuchen. | Das Feld "Tageslimit" ist nicht änderbar. Genaues Verhalten (ausgegraut oder Fehlermeldung): FEHLT | Kunde mit aktiver Karte |
| TC-12 | BERECHTIGUNG | Teamleitung gibt Änderung über 2.000 EUR frei | Vorgang im Status "Freigabe erforderlich" vorhanden | 1. Als Teamleitung anmelden. 2. Vorgang öffnen. 3. Freigeben. | Das Tageslimit wird auf den beantragten Wert gesetzt. Freigabeschritt im System: FEHLT | Vorgang aus TC-04 |
| TC-13 | ZUSTAND | Aktive vs. gesperrte Karte im selben Datensatz | Kunde mit zwei Karten, eine aktiv, eine gesperrt | 1. Kundendatensatz öffnen. 2. Tageslimit der aktiven Karte ändern. 3. Speichern. | Nur das Limit der aktiven Karte ändert sich, das der gesperrten bleibt unverändert. | Kunde mit zwei Karten in unterschiedlichem Status |

ABDECKUNG
- HAPPY: 3 | FEHLER: 3 | GRENZE: 4 | BERECHTIGUNG: 2 | ZUSTAND: 1

OFFENE PUNKTE
- FEHLT: Wortlaut der Fehlermeldung bei abgelehnter Änderung (TC-05, TC-08) | Rückfrage: Welcher Meldungstext wird bei einer abgelehnten Limitänderung angezeigt? | an: Fachbereich
- FEHLT: Verhalten bei leerem Tageslimit (TC-06) | Rückfrage: Ist das Feld "Tageslimit" ein Pflichtfeld, und was passiert beim Speichern eines leeren Werts? | an: Fachbereich
- FEHLT: Anzeigeverhalten für den Leseberechtigten (TC-11) | Rückfrage: Ist das Feld für Leseberechtigte ausgegraut, oder erscheint erst beim Speichern eine Meldung? | an: Fachbereich
- FEHLT: Ablauf des Freigabeschritts (TC-12) | Rückfrage: Wie erhält die Teamleitung den Vorgang zur Freigabe, und wo bestätigt sie ihn? | an: Fachbereich
- FEHLT: Verhalten bei nicht-numerischer Eingabe | Rückfrage: Lässt das Feld "Tageslimit" nur Ziffern zu, oder ist ein eigener Testfall für Buchstaben und Sonderzeichen nötig? | an: Entwicklung
```

---

## Prüfschritt für den Menschen

1. **Erfundene Werte suchen.** Jede Zahl, jeden Feldnamen und jeden Statuswert in der
   Tabelle gegen die Story prüfen. Alles, was dort nicht steht, ist eine Erfindung und
   fliegt raus oder wird zu einem `FEHLT`.
2. **Die offenen Punkte an den Fachbereich schicken.** Das ist der eigentliche Wert des
   Laufs. Ohne die Antworten sind die betroffenen Testfälle nicht ausführbar.
3. **Fehlende Fachlogik ergänzen.** Der Agent kennt nur die Story. Vor- und
   nachgelagerte Prozesse, Schnittstellen und Sonderfälle deines Bereichs kennt er nicht.
4. **Testdaten-Spalte gegen die Realität prüfen.** „Kunde mit gesperrter Karte" ist schnell
   geschrieben und manchmal wochenlang nicht beschaffbar. Das entscheidet über die
   Machbarkeit des Testfalls.
5. **Auf Doppelungen prüfen.** Zwei Testfälle mit demselben erwarteten Ergebnis werden zu
   einem.

---

## Wenn es nicht funktioniert

| Problem | Ursache | Fix |
|---|---|---|
| **Nur 4 bis 5 Testfälle, alles Happy Path** | Die Eingabe war zu knapp. Aus einem Satz lässt sich kein Fehlerfall ableiten. | Vollständige Akzeptanzkriterien mitgeben, nicht nur den Story-Satz. Zusätzlich in die Eingabe schreiben: „Mindestens 12 Testfälle." |
| **Erfundene Grenzwerte und Fehlermeldungen** | Der Prompt wurde gekürzt, meist fehlt der Block UMGANG MIT LÜCKEN oder die passende VERBOTEN-Zeile. | Beide Blöcke unverändert wieder einfügen. Sie wirken nur zusammen. Danach denselben Test wiederholen und vergleichen. |
| **Tabelle bricht ab oder Spalten fehlen** | Zu viele Testfälle auf einmal, die Antwort läuft in die Längenbegrenzung. | Pro Durchlauf ein Akzeptanzkriterium eingeben. Oder nachfassen mit: „Erzeuge jetzt nur die Kategorien GRENZE und BERECHTIGUNG, gleiches Format, IDs ab TC-20." |
