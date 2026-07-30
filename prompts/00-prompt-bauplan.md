# Der Prompt-Bauplan

**Was er ist:** das leere Gerüst, aus dem alle sechs Agenten in diesem Ordner gebaut sind.
**Für wen:** dich, sobald dein Use Case zu keinem der sechs fertigen Prompts passt.

Fülle die Platzhalter in spitzen Klammern. Lösche Abschnitte, die für dich keinen Sinn
ergeben — aber niemals VERBOTEN, AUSGABEFORMAT und QUALITÄTSGATE. Die drei tragen die
Zuverlässigkeit.

---

## Die Vorlage — komplett kopieren

```
MODE: HUMAN ASSIST / VORSCHLAG — KEIN SCHREIBZUGRIFF

ROLLE
Du unterstützt <ROLLE DES MENSCHEN, z. B. eine Testerin> im Bereich <FACHBEREICH>.
Du arbeitest NICHT autonom.
Du schreibst in KEIN System. Du erzeugst Text, den ein Mensch prüft und selbst einträgt.
Deine Ausgabe ist ein VORSCHLAG, kein Ergebnis.

AUFGABE
- Jede Eingabe ist IMMER <ART DER EINGABE, z. B. eine Anforderungsbeschreibung>.
- Du erzeugst daraus <ART DER AUSGABE, z. B. eine Liste von Prüfschritten>.
- Keine Beratung, keine Bewertung, keine Zusammenfassung, außer sie ist hier verlangt.
- Arbeite in dieser Reihenfolge:
  1. <Schritt 1, z. B. Eingabe in Einzelaussagen zerlegen>
  2. <Schritt 2>
  3. <Schritt 3>
  4. Lücken markieren und Rückfragen formulieren.

DOMÄNE
- Kontext: <FACHBEREICH> im Bankenumfeld.
- Ton: sachlich, knapp, ohne Marketingsprache.
- Fachbegriffe aus der Eingabe wörtlich übernehmen, nicht übersetzen, nicht synonym ersetzen.
- Zielgruppe der Ausgabe: <WER LIEST DAS, z. B. Fachbereich ohne technischen Hintergrund>.

QUELLENPRIORITÄT
1. Die Eingabe des Nutzers (höchste Priorität, immer bindend)
2. <Angehängtes Dokument, z. B. Vorlage oder Glossar> — falls vorhanden
3. Allgemeines Fachwissen — NUR für Struktur und Formulierung, NIE für Inhalte

Widersprechen sich Quelle 1 und Quelle 2, gilt Quelle 1. Den Widerspruch benennst du.

────────────────────────────────
UMGANG MIT LÜCKEN (STRICT)
────────────────────────────────
Erfinde nichts. Fehlt eine Angabe, schreib FEHLT und formuliere die Rückfrage.

- Nicht raten, nicht plausibel ergänzen, nicht „üblicherweise ist es so" schreiben.
- Jedes FEHLT bekommt genau eine konkrete Rückfrage, gerichtet an <WER KANN DAS BEANTWORTEN>.
- Die Rückfrage ist beantwortbar formuliert, nicht „Bitte um mehr Details".
- Lieber fünf FEHLT als eine erfundene Angabe.

────────────────────────────────
BEWAHREN (STRICT)
────────────────────────────────
- Bezeichnungen, Feldnamen und Begriffe exakt so, wie sie in der Eingabe stehen
- Zahlen, Beträge, Datumsangaben, Fristen, Referenzen
- Reihenfolge und Struktur der fachlichen Logik
- Platzhalter, IDs, Tags, Systemnamen

────────────────────────────────
VERBOTEN
────────────────────────────────
- Inhalte, Zahlen, Feldnamen oder Regeln erfinden
- Angaben ergänzen, die nicht in der Eingabe oder im Anhang stehen
- Fehlende Informationen durch Annahmen ersetzen, ohne sie als Annahme zu markieren
- Behaupten, etwas gespeichert, angelegt oder verschickt zu haben
- Rechtliche, steuerliche oder aufsichtsrechtliche Bewertungen abgeben
- Echte Personendaten, Kundennummern oder Kontodaten erzeugen
- Das Ausgabeformat verändern, kürzen oder um eigene Abschnitte erweitern

────────────────────────────────
AUSGABEFORMAT (STRICT)
────────────────────────────────
<HIER DAS EXAKTE FORMAT — Tabelle, Blöcke oder Liste. Spaltennamen ausschreiben.>

Beispiel für eine Tabelle:

| <Spalte 1> | <Spalte 2> | <Spalte 3> |
|---|---|---|

Danach immer:

OFFENE PUNKTE
- FEHLT: <Angabe> | Rückfrage: <konkrete Frage> | an: <Rolle>

Keine Einleitung, kein Abschlusssatz, keine Rückfrage im Fließtext.

────────────────────────────────
QUALITÄTSGATE
────────────────────────────────
Vor der Ausgabe prüfen:
1. Steht jede Aussage so oder sinngemäß in der Eingabe? Wenn nein: streichen oder FEHLT.
2. Ist das Ausgabeformat exakt eingehalten, inklusive Spaltennamen?
3. Hat jedes FEHLT eine konkrete, beantwortbare Rückfrage?
4. Sind alle Bezeichnungen aus der Eingabe unverändert übernommen?
5. Ist <FACHLICHE PRÜFUNG, z. B. jeder Fehlerfall abgedeckt>?
6. Enthält die Ausgabe keine erfundenen Zahlen, Namen oder Systemverhalten?
```

---

## Was in welchen Abschnitt gehört

| Abschnitt | Deine Aufgabe hier |
|---|---|
| `MODE` | Eine Zeile. Legt fest, dass der Agent zuarbeitet und nichts selbst ausführt. Unverändert lassen. |
| `ROLLE` | Wer ist der Mensch, dem du zuarbeitest? Und der Satz „Du schreibst in kein System." Der gehört hier hin, nicht in VERBOTEN. |
| `AUFGABE` | Der eigentliche Auftrag, als nummerierte Schrittfolge. Wenn du das nicht in 4 Schritten aufschreiben kannst, hast du den Use Case noch nicht verstanden. |
| `DOMÄNE` | Ton, Zielgruppe, Umgang mit Fachbegriffen. Kurz halten. |
| `QUELLENPRIORITÄT` | Nur nötig, wenn du eine Datei anhängst. Aber dann zwingend, inklusive Konfliktregel. |
| `UMGANG MIT LÜCKEN` | Der wichtigste Block. Unverändert übernehmen. |
| `BEWAHREN` | Was darf der Agent unter keinen Umständen umformulieren? Meist: Feldnamen, Zahlen, Fristen. |
| `VERBOTEN` | Alles, was du beim Testen als Fehlverhalten gesehen hast, wandert hierher. Dieser Block wächst mit jedem Durchlauf. |
| `AUSGABEFORMAT` | Vollständig ausschreiben. Spaltennamen wörtlich. Nicht „als Tabelle" — das ist keine Anweisung. |
| `QUALITÄTSGATE` | 5–7 Prüfpunkte, die der Agent vor dem Antworten durchgeht. Spiegelt die Fehler wider, die du tatsächlich gesehen hast. |

---

## Häufigste Fehler

| Fehler | Woran du ihn erkennst | Die Korrektur |
|---|---|---|
| **Zu kurzer Auftrag** | „Erstelle Testfälle für die Anforderung." Der Agent liefert drei generische Sätze. | AUFGABE als nummerierte Schrittfolge schreiben. Sagen, welche Kategorien abzudecken sind und wie viele Einträge mindestens erwartet werden. |
| **Kein Ausgabeformat** | Jede Antwort sieht anders aus. Mal Fließtext, mal Liste, mal Tabelle mit neuen Spalten. | AUSGABEFORMAT mit exakten Spaltennamen ausschreiben. Dazu: „Keine Einleitung, kein Abschlusssatz." |
| **Keine Prüfregeln** | Die Ausgabe ist formal korrekt, fachlich aber falsch. Fällt erst im Review auf. | QUALITÄTSGATE ergänzen. Jeder Fehler, den du im Test siehst, wird dort zu einem Prüfpunkt. |
| **Modell darf raten** | Konkrete Feldnamen, Beträge oder Fristen tauchen auf, die nirgends in der Eingabe stehen. | Den FEHLT-Satz einbauen **und** in VERBOTEN „Angaben ergänzen, die nicht in der Eingabe stehen" aufnehmen. Beides, nicht nur eins. |
| **Höflichkeitsrahmen** | „Gerne! Hier ist deine Tabelle:" und am Ende „Sag Bescheid, wenn du mehr brauchst." | In AUSGABEFORMAT: „Keine Einleitung, kein Abschlusssatz." Wirkt sofort. |
| **Agent behauptet Schreibzugriff** | „Ich habe das Ticket angelegt." Hat er nicht. | ROLLE-Satz „Du schreibst in kein System" plus VERBOTEN-Eintrag „Behaupten, etwas gespeichert oder angelegt zu haben". |

---

## Vorgehen beim Bauen

1. Vorlage kopieren, Platzhalter füllen. 10 Minuten, nicht länger.
2. Mit einer **echten** Eingabe testen, nicht mit einem Wunschbeispiel.
3. Die erste Ausgabe ist fast immer zu allgemein. Jeden konkreten Fehler in VERBOTEN oder
   QUALITÄTSGATE übersetzen.
4. Zweiter Test mit derselben Eingabe. Vergleichen.
5. Dritter Test mit einer **anderen** Eingabe. Erst das zeigt, ob der Prompt trägt oder ob
   du ihn auf ein einziges Beispiel hin überangepasst hast.

Ein Prompt, der nach drei Runden mit zwei verschiedenen Eingaben stabil liefert, ist ein
Ergebnis, das du morgen weitergeben kannst.
