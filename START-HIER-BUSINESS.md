# Start hier — fachlicher Einstieg

**Für alle, die fachlich arbeiten: Test, Prozess, Anforderungen, Doku, Betrieb.**
Du brauchst kein Git, keine Installation und keinen Entwickler. Nur einen Browser und M365 Copilot.

---

## In 5 Minuten zum ersten Agenten

### 1. Öffne M365 Copilot

Im Browser oder in Teams. Du brauchst eine Copilot-Lizenz — die hast du, wenn du Copilot in
Word oder Teams schon gesehen hast.

### 2. Leg einen Agenten an

Im Copilot-Chat gibt es die Möglichkeit, einen eigenen Agenten zu erstellen. Du gibst ihm
einen Namen, eine Beschreibung und — das ist der wichtige Teil — **Instructions**.

Die Instructions sind der Text, der dem Agenten sagt, wer er ist und was er tun soll. Genau
diesen Text nimmst du fertig aus diesem Kit.

### 3. Hol dir einen fertigen Prompt

Geh in den Ordner **[prompts/](prompts/)** und such dir den passenden aus. Jede Datei enthält:

- **Instructions zum kompletten Kopieren** — der Text für deinen Agenten
- **eine Beispiel-Eingabe** — damit du sofort testen kannst
- **die erwartete Ausgabe** — damit du weißt, ob es geklappt hat
- **einen Prüfschritt** — worauf ein Mensch schauen muss

### 4. Text kopieren und einfügen

Klick die Datei an. Kopier den Block unter „Instructions — komplett kopieren". Füg ihn in
das Instructions-Feld deines Agenten ein. Speichern.

### 5. Testen

Nimm die Beispiel-Eingabe aus derselben Datei, schick sie an deinen Agenten und vergleich das
Ergebnis mit der erwarteten Ausgabe.

**Das war's. Ab hier passt du den Text an deinen echten Fall an.**

---

## Wie du eine Datei ohne Git herunterlädst

Du musst gar nichts herunterladen — **Copy-Paste aus dem Browser reicht.** Aber falls du die
Datei doch als Datei willst:

| Was du willst | Wie |
|---|---|
| **Nur den Text** | Datei anklicken, Text markieren, kopieren. Fertig. |
| **Die Datei sauber ohne Formatierung** | Datei anklicken → Button **„Raw"** oben rechts → dann Rechtsklick → „Speichern unter" |
| **Alles auf einmal** | Auf der Startseite des Repos: grüner Button **„Code"** → **„Download ZIP"** → entpacken |

**Tipp:** `.md`-Dateien sind reine Textdateien. Du kannst sie mit dem Editor, Word oder
direkt im Browser lesen. Im Browser sehen sie am besten aus.

---

## Bevor du baust — vier Fragen an deinen Use Case

Wenn du eine davon nicht beantworten kannst, schärf den Use Case nach. Das kostet zehn
Minuten und rettet den Nachmittag.

| | Frage | Warum |
|---|---|---|
| 1 | **Wie oft** kommt die Aufgabe vor? | Häufigkeit × Zeit = der Nutzen. Selten und clever bringt nichts. |
| 2 | **Woran erkennst du, dass das Ergebnis gut ist?** | Ohne Prüfbarkeit keine Freigabe und kein Vertrauen. |
| 3 | **Wo liegen die Daten**, und darf der Agent ran? | Der häufigste stille Blocker. |
| 4 | Muss der Agent etwas **schreiben oder ändern**? | Wenn ja: heute als Vorschlag bauen, nicht als Automatik. |

---

## Die eine Regel, die du dir merken musst

> **Dein Agent legt etwas vor. Ein Mensch schickt es ab.**

Die meisten Agenten können heute lesen, recherchieren, zusammenfassen und Entwürfe erzeugen.
Was sie heute **nicht** können: automatisch ein Ticket anlegen, einen SharePoint-Eintrag
ändern oder sich selbst starten.

Das ist keine Einschränkung, das ist der Bauplan. Plan den letzten Schritt als Vorschlag —
dann funktioniert dein Agent heute, und wenn Schreibzugriff kommt, schaltet ihr genau diesen
einen Schritt durch.

Details dazu: **[infoblatt.md](infoblatt.md)**

---

## Wenn dein Use Case an Azure DevOps hängt

Viele Ideen heute enden bei „…und dann legt er das Ticket an". Dafür gibt es einen eigenen
Ordner, gestaffelt nach dem, was du kannst:

👉 **[azure-devops/01-ohne-technik.md](azure-devops/01-ohne-technik.md)** — der Weg ohne
jede Technik: Work Items exportieren, in den Agenten geben, Ergebnis zurück ins Ticket.

---

## Wenn es klemmt

**Frag einen Coach. Früh.** Nicht erst um halb sieben.

Die häufigsten Fälle, und sie sind alle in fünf Minuten lösbar:

| Problem | Was meistens dahintersteckt |
|---|---|
| „Der Agent antwortet, aber unbrauchbar" | Kein Ausgabeformat im Prompt. Sag ihm, ob du eine Tabelle, eine Liste oder Fließtext willst. |
| „Er erfindet Sachen" | Der Satz fehlt: *„Erfinde nichts. Fehlt eine Angabe, schreib FEHLT und formuliere die Rückfrage."* |
| „Er kommt an unsere Daten nicht ran" | Prüf, ob die Quelle für dich freigegeben ist. Wenn nicht: häng die Datei direkt an den Agenten. |
| „Mein Use Case braucht Schreibzugriff" | Bau ihn als Vorschlag um. Dauert fünf Minuten, wenn du früh fragst. |
