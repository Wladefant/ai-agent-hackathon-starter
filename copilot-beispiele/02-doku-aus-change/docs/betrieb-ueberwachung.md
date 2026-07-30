# Betrieb: Überwachung payments-api

Stand: 2026-05-30

## Alarme

| Alarm | Bedingung | Schwere | Reaktion |
|---|---|---|---|
| `zahlung_haengt` | Zahlung ist länger als 5 Minuten nicht in einem finalen Status | hoch | Rufbereitschaft anrufen |
| `fehlerquote_hoch` | mehr als 2 Prozent `5xx` über 15 Minuten | hoch | Rufbereitschaft anrufen |
| `latenz_hoch` | p95 über 800 ms über 10 Minuten | mittel | am nächsten Werktag prüfen |

## Kennzahlen im Dashboard

- Zahlungen pro Minute
- Anteil `abgelehnt` an allen Zahlungen
- p95-Latenz `POST /zahlungen`

## Runbook `zahlung_haengt`

1. Zahlung über `GET /zahlungen/{id}` abrufen und Status prüfen.
2. Ist der Status `angenommen`, liegt die Zahlung in der Ausführungsstrecke fest.
3. Warteschlange der Ausführung prüfen.
4. Bleibt der Status länger als 15 Minuten stehen, an Team Payments eskalieren.

> Jede Zahlung, die nicht innerhalb von 5 Minuten final ist, gilt als Störung.
