# Doku-Änderungsvorschlag zu CHG-2087

Erzeugt aus `beispiel-eingabe/change.md`. Nicht angewendet. Bitte prüfen und übernehmen.

## Betroffene Seiten

| Datei | Abschnitt | Art |
|---|---|---|
| `docs/api-zahlungen.md` | Zahlungsobjekt | ergänzen |
| `docs/api-zahlungen.md` | Statuswerte | ersetzen |
| `docs/api-zahlungen.md` | Endpunkte | ergänzen |
| `docs/api-zahlungen.md` | Webhooks | ergänzen |
| `docs/betrieb-ueberwachung.md` | Alarme | ersetzen |
| `docs/betrieb-ueberwachung.md` | Kennzahlen im Dashboard | ergänzen |
| `docs/betrieb-ueberwachung.md` | Runbook `zahlung_haengt` | ersetzen |
| beide Seiten | Kopfzeile `Stand:` | ersetzen |

---

### docs/api-zahlungen.md → Zahlungsobjekt

**Vorher** (letzte Zeile der Tabelle)

```markdown
| `grund` | string | nur bei `abgelehnt` gesetzt |
```

**Nachher**

```markdown
| `grund` | string | nur bei `abgelehnt` gesetzt |
| `freigabe_bis` | string | ISO-8601 UTC, nur bei Status `in_pruefung` gesetzt |
```

**Warum** CHG-2087 führt das Feld `freigabe_bis` ein.

---

### docs/api-zahlungen.md → Statuswerte

**Vorher**

```markdown
| Status | Final | Bedeutung |
|---|---|---|
| `angenommen` | nein | Zahlung ist entgegengenommen, Ausführung steht aus |
| `ausgefuehrt` | ja | Zahlung wurde ausgeführt |
| `abgelehnt` | ja | Zahlung wurde nicht ausgeführt, `grund` ist gesetzt |

Eine Zahlung erreicht in der Regel innerhalb weniger Sekunden einen finalen Status.
```

**Nachher**

```markdown
| Status | Final | Bedeutung |
|---|---|---|
| `angenommen` | nein | Zahlung ist entgegengenommen, Ausführung steht aus |
| `in_pruefung` | nein | Zahlung ab 10.000 EUR wartet auf Freigabe durch eine zweite Person |
| `ausgefuehrt` | ja | Zahlung wurde ausgeführt |
| `abgelehnt` | ja | Zahlung wurde nicht ausgeführt, `grund` ist gesetzt |

Zahlungen unter 10.000 EUR erreichen in der Regel innerhalb weniger Sekunden einen finalen
Status. Zahlungen im Status `in_pruefung` bleiben bis zu 24 Stunden offen. Wird die Frist aus
`freigabe_bis` überschritten, wechselt der Status automatisch auf `abgelehnt` mit
`grund: "freigabe_frist_abgelaufen"`.
```

**Warum** Neuer nicht finaler Status aus CHG-2087. Der bisherige Schlusssatz gilt nur noch
für Zahlungen unter der Freigabegrenze.

---

### docs/api-zahlungen.md → Endpunkte

**Vorher** (letzte Zeile der Tabelle)

```markdown
| `GET` | `/zahlungen` | Zahlungen auflisten |
```

**Nachher**

```markdown
| `GET` | `/zahlungen` | Zahlungen auflisten |
| `POST` | `/zahlungen/{id}/freigabe` | Zahlung im Status `in_pruefung` freigeben oder ablehnen |
```

Direkt unter der Tabelle ergänzen:

```markdown
### `POST /zahlungen/{id}/freigabe`

Body: `{ "entscheidung": "freigeben" | "ablehnen", "kommentar": "..." }`

| Antwort | Bedeutung |
|---|---|
| `200` | aktualisiertes Zahlungsobjekt |
| `403` | die freigebende Person hat die Zahlung selbst angelegt |
| `409` | Zahlung ist nicht im Status `in_pruefung` |
```

**Warum** Neuer Endpunkt aus CHG-2087.

---

### docs/api-zahlungen.md → Webhooks

**Vorher** (erste Zeile der Tabelle)

```markdown
| `zahlung.ausgefuehrt` | Status wechselt auf `ausgefuehrt` |
```

**Nachher**

```markdown
| `zahlung.freigabe_erforderlich` | Status wechselt auf `in_pruefung` |
| `zahlung.ausgefuehrt` | Status wechselt auf `ausgefuehrt` |
```

**Warum** Neues Event aus CHG-2087.

---

### docs/betrieb-ueberwachung.md → Alarme

**Vorher**

```markdown
| `zahlung_haengt` | Zahlung ist länger als 5 Minuten nicht in einem finalen Status | hoch | Rufbereitschaft anrufen |
```

**Nachher**

```markdown
| `zahlung_haengt` | Zahlung ist länger als 5 Minuten weder final noch im Status `in_pruefung` | hoch | Rufbereitschaft anrufen |
| `freigabestau` | mehr als 50 Zahlungen gleichzeitig im Status `in_pruefung` | mittel | Team Payments informieren |
```

**Warum** Ohne den Zusatz feuert `zahlung_haengt` ab Release für jede Zahlung ab 10.000 EUR
dauerhaft. CHG-2087 nennt die neue Schwelle 50 für den Freigabestau.

---

### docs/betrieb-ueberwachung.md → Kennzahlen im Dashboard

**Vorher**

```markdown
- p95-Latenz `POST /zahlungen`
```

**Nachher**

```markdown
- p95-Latenz `POST /zahlungen`
- Anzahl Zahlungen im Status `in_pruefung`
```

**Warum** Neue Kennzahl aus CHG-2087.

---

### docs/betrieb-ueberwachung.md → Runbook `zahlung_haengt`

**Vorher**

```markdown
2. Ist der Status `angenommen`, liegt die Zahlung in der Ausführungsstrecke fest.
...
> Jede Zahlung, die nicht innerhalb von 5 Minuten final ist, gilt als Störung.
```

**Nachher**

```markdown
2. Ist der Status `in_pruefung`, liegt keine Störung vor. Die Zahlung wartet auf die Freigabe
   durch eine zweite Person, siehe `freigabe_bis`. Alarm schließen.
3. Ist der Status `angenommen`, liegt die Zahlung in der Ausführungsstrecke fest.
...
> Eine Zahlung im Status `in_pruefung` ist keine Störung. Jede andere Zahlung, die nicht
> innerhalb von 5 Minuten final ist, gilt als Störung.
```

Die Nummerierung der Folgeschritte verschiebt sich um eins.

**Warum** Ohne diesen Schritt eskaliert die Rufbereitschaft einen fachlich korrekten Zustand.

---

### beide Seiten → Kopfzeile

`Stand: 2026-06-12` bzw. `Stand: 2026-05-30` wird zu `Stand: 2026-08-05` (Release-Datum aus CHG-2087).

---

## Nicht geändert

| Stelle | Warum |
|---|---|
| `docs/api-zahlungen.md`, Feld `waehrung` | vom Change nicht berührt |
| Alarme `fehlerquote_hoch` und `latenz_hoch` | unabhängig vom Freigabeschritt |
| mobile App | im Change ausdrücklich ausgeschlossen |

## Offene Fragen

1. Gibt es einen Endpunkt oder Filter, um alle Zahlungen im Status `in_pruefung` zu listen? Die Runbook-Ergänzung wäre sonst nur einzeln durchführbar. **An: Team Payments**
2. Wird `zahlung.abgelehnt` auch beim automatischen Fristablauf gesendet? Falls ja, gehört das an die Webhook-Tabelle. **An: Team Payments**
3. Ist die Grenze von 10.000 EUR konfigurierbar? Wenn ja, sollte die Doku den Konfigurationsschlüssel nennen statt den Betrag. **An: Team Payments**
4. Wer ist für den Alarm `freigabestau` zuständig, Rufbereitschaft oder Fachbereich? **An: Betrieb**
