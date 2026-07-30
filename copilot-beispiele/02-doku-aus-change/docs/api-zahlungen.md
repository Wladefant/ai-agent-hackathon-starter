# API: Zahlungen

Stand: 2026-06-12

## Zahlungsobjekt

| Feld | Typ | Beschreibung |
|---|---|---|
| `id` | string | Eindeutige ID der Zahlung |
| `betrag` | integer | Betrag in Cent |
| `waehrung` | string | ISO-4217, aktuell nur `EUR` |
| `status` | string | siehe Statuswerte |
| `erstellt_am` | string | ISO-8601 UTC |
| `grund` | string | nur bei `abgelehnt` gesetzt |

## Statuswerte

| Status | Final | Bedeutung |
|---|---|---|
| `angenommen` | nein | Zahlung ist entgegengenommen, Ausführung steht aus |
| `ausgefuehrt` | ja | Zahlung wurde ausgeführt |
| `abgelehnt` | ja | Zahlung wurde nicht ausgeführt, `grund` ist gesetzt |

Eine Zahlung erreicht in der Regel innerhalb weniger Sekunden einen finalen Status.

## Endpunkte

| Methode | Pfad | Zweck |
|---|---|---|
| `POST` | `/zahlungen` | Zahlung anlegen |
| `GET` | `/zahlungen/{id}` | Zahlung lesen |
| `GET` | `/zahlungen` | Zahlungen auflisten |

## Webhooks

| Event | Wann |
|---|---|
| `zahlung.ausgefuehrt` | Status wechselt auf `ausgefuehrt` |
| `zahlung.abgelehnt` | Status wechselt auf `abgelehnt` |
