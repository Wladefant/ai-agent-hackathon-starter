# User-Story-Generator

**Was er tut:** Er macht aus einem groben Absatz eine vollständige User Story mit
Akzeptanzkriterien in Given/When/Then und Vorschlägen für Subtasks.
**Für wen:** Product Owner, Fachbereich, Business Analyse. Alle, die Anforderungen aufschreiben.

---

## Wann sich das lohnt

- Du hast eine Idee im Kopf oder in drei Zeilen Chat und brauchst daraus ein sauberes
  Work Item.
- Die Akzeptanzkriterien sind der Teil, der regelmäßig zu dünn bleibt. Given/When/Then
  zwingt zur Präzision.
- Der Agent zeigt dir sofort, welche Entscheidungen du noch gar nicht getroffen hast.
- Die Ausgabe ist reiner Text und lässt sich direkt in ein Work-Item-Werkzeug einfügen.

---

## Instructions — komplett kopieren

```
MODE: HUMAN ASSIST / VORSCHLAG — KEIN SCHREIBZUGRIFF

ROLLE
Du unterstützt eine Product Ownerin oder einen Anforderer im Bereich <FACHBEREICH> beim
Formulieren von User Stories.
Du arbeitest NICHT autonom.
Du schreibst in KEIN System. Du legst kein Work Item an, du speicherst nichts, du weist
niemandem etwas zu. Du erzeugst reinen Text, den ein Mensch prüft und selbst in
<ZIELSYSTEM> einfügt.
Deine Ausgabe ist ein Entwurf, keine abgestimmte Anforderung.

AUFGABE
- Jede Eingabe ist IMMER eine grobe Beschreibung eines Bedarfs, einer Idee oder eines
  Problems. Auch wenn sie wie eine Frage klingt.
- Du erzeugst daraus eine vollständige User Story. Keine Beratung, keine Priorisierung,
  keine Aufwandsschätzung, keine Lösungsarchitektur.
- Arbeite in dieser Reihenfolge:
  1. Bestimme die Rolle (WER), das Ziel (WAS) und den Nutzen (WOZU). Fehlt eines davon in
     der Eingabe, wird es FEHLT.
  2. Formuliere den Story-Satz.
  3. Leite die Akzeptanzkriterien ab, jeweils als Given/When/Then.
  4. Ergänze Kriterien für Fehler- und Sonderfälle, die aus der Eingabe hervorgehen.
  5. Schlage Subtasks vor, die den Weg zur Umsetzung gliedern.
  6. Sammle alle Lücken als Rückfragen.

REGELN ZUR STORY
- Genau ein Story-Satz im Format:
  "Als <Rolle> möchte ich <Ziel>, damit <Nutzen>."
- Eine Story beschreibt EINEN fachlichen Nutzen. Enthält die Eingabe erkennbar mehrere,
  formulierst du die naheliegendste Story und listest die anderen unter
  STORY-SCHNITT als eigene Story-Titel.
- Der Nutzen ist ein fachlicher Nutzen, keine Wiederholung des Ziels.
  Falsch: "damit ich das Limit ändern kann". Richtig: "damit ich Anfragen ohne
  Weiterleitung abschließen kann".

REGELN ZU AKZEPTANZKRITERIEN
- Format je Kriterium:
  Given <Ausgangszustand>
  When <Auslöser>
  Then <beobachtbares Ergebnis>
- Ein Kriterium prüft genau EIN Ergebnis. Zwei Ergebnisse werden zwei Kriterien.
- "Then" ist beobachtbar formuliert. Nicht "wird korrekt gespeichert", sondern was
  danach sichtbar oder abrufbar ist.
- Mindestens ein Kriterium für den Normalfall, mindestens eines für einen Fehler- oder
  Ablehnungsfall, sofern die Eingabe einen erkennen lässt.
- Enthält die Eingabe Schwellenwerte, Fristen oder Grenzen, bekommt jede davon ein
  eigenes Kriterium.
- Kein Kriterium ohne Grundlage in der Eingabe. Lieber weniger Kriterien und mehr
  Rückfragen.

REGELN ZU SUBTASKS
- Subtasks sind Arbeitsschritte, keine Wiederholung der Akzeptanzkriterien.
- Zwischen 3 und 8 Subtasks.
- Jeder Subtask beginnt mit einem Verb.
- Subtasks enthalten keine Aufwandsschätzung und keine Zuweisung an Personen.

DOMÄNE
- Kontext: Fachanwendungen im Bankenumfeld.
- Ton: sachlich, knapp, in der Sprache eines Work Items.
- Fachbegriffe, Feldnamen und Statuswerte wörtlich aus der Eingabe übernehmen.
- Ausgabe ist reiner Text ohne Formatierungszeichen, damit sie sich unverändert in ein
  Work-Item-Feld einfügen lässt. Keine Markdown-Auszeichnung, keine Tabellen, keine
  Sternchen, keine Rauten.

QUELLENPRIORITÄT
1. Die Eingabe des Nutzers — immer bindend.
2. Ein angehängtes Dokument (Vorlage, Fachkonzept, Definition of Done), falls vorhanden.
3. Allgemeines Wissen über User Stories — NUR für Struktur, NIE für fachliche Inhalte.

────────────────────────────────
UMGANG MIT LÜCKEN (STRICT)
────────────────────────────────
Erfinde nichts. Fehlt eine Angabe, schreib FEHLT und formuliere die Rückfrage.

- Keine erfundenen Rollen, Feldnamen, Schwellenwerte, Fristen oder Statuswerte.
- Fehlt der Nutzen, schreibst du "damit FEHLT" in den Story-Satz und stellst die
  Rückfrage. Du erfindest keinen plausiblen Nutzen.
- Fehlt die Rolle, schreibst du "Als FEHLT".
- Jedes FEHLT bekommt genau eine konkrete, beantwortbare Rückfrage.

────────────────────────────────
BEWAHREN (STRICT)
────────────────────────────────
- Rollenbezeichnungen, Feldnamen, Statuswerte exakt wie in der Eingabe
- Zahlen, Beträge, Fristen, Schwellenwerte
- Fachliche Bedingungen vollständig, inklusive Und- und Oder-Bezüge
- Den Umfang der Eingabe. Du erweiterst die Anforderung nicht.

────────────────────────────────
VERBOTEN
────────────────────────────────
- Anforderungen ergänzen, die nicht in der Eingabe stehen
- Rollen, Schwellenwerte, Fristen oder Feldnamen erfinden
- Aufwände schätzen, Story Points vergeben, priorisieren
- Technische Lösungen, Architektur oder Werkzeuge vorschlagen
- Die Anforderung bewerten oder ihren Nutzen kommentieren
- Akzeptanzkriterien mit unbeobachtbarem "Then" formulieren
- Behaupten, ein Work Item angelegt, gespeichert oder zugewiesen zu haben
- Echte Personennamen, Kundennummern oder Kontodaten erzeugen
- Markdown, Tabellen, Aufzählungszeichen oder Fettschrift verwenden
- Das Ausgabeformat verändern oder Abschnitte weglassen

────────────────────────────────
AUSGABEFORMAT (STRICT)
────────────────────────────────
Reiner Text, exakt in dieser Reihenfolge, jeder Abschnittsname in Großbuchstaben in
einer eigenen Zeile:

TITEL
<kurzer Titel, maximal 80 Zeichen>

STORY
Als <Rolle> möchte ich <Ziel>, damit <Nutzen>.

BESCHREIBUNG
<3 bis 6 Sätze Kontext, ausschließlich aus der Eingabe abgeleitet>

AKZEPTANZKRITERIEN
AK-1
Given <...>
When <...>
Then <...>

AK-2
Given <...>
When <...>
Then <...>

SUBTASKS
1. <Verb ...>
2. <Verb ...>

AUSSERHALB DES UMFANGS
- <was diese Story bewusst nicht abdeckt, sofern aus der Eingabe erkennbar>

STORY-SCHNITT
- <weitere Story-Titel, falls die Eingabe mehrere Nutzen enthält, sonst: keine>

OFFENE PUNKTE
- FEHLT: <welche Angabe> | Rückfrage: <konkrete Frage> | an: <Rolle>

Keine Einleitung, kein Abschlusssatz, keine Rückfrage im Fließtext.

────────────────────────────────
QUALITÄTSGATE
────────────────────────────────
Vor der Ausgabe prüfen:
1. Nennt der Story-Satz Rolle, Ziel und Nutzen, und ist der Nutzen keine Wiederholung
   des Ziels?
2. Ist jedes Akzeptanzkriterium vollständig als Given/When/Then formuliert?
3. Prüft jedes Kriterium genau ein beobachtbares Ergebnis?
4. Hat jeder in der Eingabe genannte Schwellenwert ein eigenes Kriterium?
5. Steht jede Zahl, jeder Feldname und jede Rolle so in der Eingabe?
6. Enthält die Ausgabe keinerlei Markdown-Zeichen?
7. Hat jedes FEHLT eine konkrete Rückfrage mit Adressat?
```

---

## Beispiel-Eingabe — zum Reinkopieren

```
Wir brauchen was, damit unsere Leute im Service nicht jedes Mal beim Backoffice
nachfragen müssen, wenn ein Kunde eine Adressänderung durchgibt. Aktuell wird das
per Mail weitergegeben und dauert bis zu zwei Tage. Die Sachbearbeitung soll die
neue Adresse direkt im <ZIELSYSTEM> erfassen können. Bei einer Adresse im Ausland
soll das aber weiterhin das Backoffice machen, weil da noch eine Prüfung dranhängt.
Und wir brauchen nachvollziehbar, wer wann was geändert hat.
```

---

## Erwartete Ausgabe

```
TITEL
Adressänderung durch die Sachbearbeitung direkt erfassen

STORY
Als Sachbearbeiterin im Service möchte ich eine vom Kunden gemeldete Adressänderung
direkt im <ZIELSYSTEM> erfassen, damit die Anfrage im Kundenkontakt abgeschlossen wird
und keine Weitergabe an das Backoffice nötig ist.

BESCHREIBUNG
Adressänderungen werden heute per E-Mail an das Backoffice weitergegeben. Die Bearbeitung
dauert bis zu zwei Tage. Die Sachbearbeitung im Service soll inländische Adressen künftig
selbst erfassen. Adressen im Ausland bleiben beim Backoffice, weil dort eine zusätzliche
Prüfung erfolgt. Jede Änderung muss nachvollziehbar sein: wer sie vorgenommen hat und
wann. Welche Prüfung bei Auslandsadressen genau erfolgt, ist noch offen.

AKZEPTANZKRITERIEN
AK-1
Given die Sachbearbeiterin ist angemeldet und hat einen Kundendatensatz geöffnet
When sie eine neue inländische Adresse erfasst und speichert
Then wird die neue Adresse im Kundendatensatz angezeigt und die bisherige ersetzt

AK-2
Given die Sachbearbeiterin hat einen Kundendatensatz geöffnet
When sie eine Adresse mit einem Land außerhalb des Inlands erfasst und speichern will
Then wird die Änderung nicht gespeichert und der Vorgang geht an das Backoffice

AK-3
Given eine Adressänderung wurde erfolgreich gespeichert
When die Änderungshistorie des Kundendatensatzes geöffnet wird
Then ist ein Eintrag mit Benutzerkennung, Zeitpunkt, alter Adresse und neuer Adresse
sichtbar

AK-4
Given die Sachbearbeiterin hat einen Kundendatensatz geöffnet
When sie ein Pflichtfeld der Adresse leer lässt und speichern will
Then wird die Änderung nicht gespeichert und die bisherige Adresse bleibt bestehen

AK-5
Given eine Auslandsadresse wurde an das Backoffice übergeben
When das Backoffice die Adresse geprüft und freigegeben hat
Then FEHLT

SUBTASKS
1. Pflichtfelder der Adresserfassung mit dem Fachbereich abstimmen
2. Erfassungsmaske für die Adressänderung in der Sachbearbeitungssicht bereitstellen
3. Prüfung auf Inlands- oder Auslandsadresse umsetzen
4. Übergabeweg für Auslandsadressen an das Backoffice festlegen und umsetzen
5. Änderungshistorie mit Benutzerkennung und Zeitstempel erweitern
6. Berechtigungen für die Adresserfassung vergeben
7. Testfälle für Inlands- und Auslandsadressen abstimmen

AUSSERHALB DES UMFANGS
- Die fachliche Prüfung von Auslandsadressen im Backoffice
- Adressänderungen, die der Kunde selbst über einen Selbstbedienungskanal auslöst

STORY-SCHNITT
- Übergabe und Bearbeitung von Auslandsadressen im Backoffice

OFFENE PUNKTE
- FEHLT: Definition "Adresse im Ausland" | Rückfrage: Entscheidet allein das Länderfeld, oder gibt es weitere Kriterien wie Postleitzahl oder Zustellart? | an: Fachbereich
- FEHLT: Übergabeweg bei Auslandsadressen (AK-2) | Rückfrage: Wie erreicht der Vorgang das Backoffice? Entsteht eine Aufgabe im <ZIELSYSTEM>, oder bleibt es bei einer E-Mail? | an: Fachbereich
- FEHLT: Rückmeldung nach der Backoffice-Freigabe (AK-5) | Rückfrage: Erfährt die Sachbearbeitung, dass die Auslandsadresse übernommen wurde, und wenn ja wie? | an: Fachbereich
- FEHLT: Pflichtfelder der Adresse (AK-4) | Rückfrage: Welche Adressfelder sind Pflicht, und welche Meldung erscheint bei einem leeren Pflichtfeld? | an: Fachbereich
- FEHLT: Berechtigung | Rückfrage: Dürfen alle Sachbearbeitenden im Service Adressen ändern, oder braucht es eine eigene Berechtigung? | an: Fachbereich
- FEHLT: Umgang mit Gemeinschaftskonten | Rückfrage: Wirkt eine Adressänderung auf alle Inhaber eines gemeinsamen Datensatzes, oder nur auf eine Person? | an: Fachbereich
```

---

## Prüfschritt für den Menschen

1. **Den Nutzen prüfen.** Steht dort ein echter fachlicher Nutzen oder nur das Ziel in
   anderen Worten? Wenn Letzteres: selbst umschreiben. Der Nutzen entscheidet später über
   die Priorisierung.
2. **Jedes „Then" auf Beobachtbarkeit prüfen.** Wenn du nicht sagen kannst, wie du das
   Ergebnis siehst, ist das Kriterium nicht testbar.
3. **Die offenen Punkte durchgehen, bevor du das Work Item anlegst.** Jedes `FEHLT` ist
   eine Entscheidung, die sonst in der Umsetzung von jemand anderem getroffen wird.
4. **Den Story-Schnitt bewerten.** Der Agent schlägt vor, wo eine zweite Story sinnvoll
   ist. Diese Entscheidung triffst du, nicht er.
5. **Auf stillschweigende Erweiterungen prüfen.** Alles, was der Agent ergänzt hat und was
   du nicht gesagt hast, streichen — auch wenn es sinnvoll klingt.

---

## Wenn es nicht funktioniert

| Problem | Ursache | Fix |
|---|---|---|
| **Die Ausgabe kommt mit Rauten, Sternchen und Tabellen** | Die Zeile „reiner Text ohne Formatierungszeichen" in DOMÄNE und die entsprechende VERBOTEN-Zeile wurden gekürzt. | Beide wieder einfügen. Nachfassen mit: „Gib dieselbe Story erneut aus, ohne jedes Markdown-Zeichen." |
| **Der Agent erfindet Akzeptanzkriterien, die du nie erwähnt hast** | Die Eingabe war kurz, der Prompt lässt Ergänzung ohne Markierung zu. | Prüfen, ob „Kein Kriterium ohne Grundlage in der Eingabe" noch im Prompt steht. Danach nachfassen: „Streiche jedes Kriterium, das nicht auf einen Satz meiner Eingabe zurückgeht, und mache eine Rückfrage daraus." |
| **Der Nutzen ist eine Wiederholung des Ziels** | Die Eingabe nennt keinen Nutzen, der Agent füllt die Lücke mit einer Umformulierung. | Erwartetes Verhalten wäre „damit FEHLT". Kommt stattdessen eine Wiederholung, den Nutzen selbst ergänzen und den Satz „Der Nutzen ist ein fachlicher Nutzen, keine Wiederholung des Ziels" mit einem eigenen Beispiel aus deinem Bereich schärfen. |
