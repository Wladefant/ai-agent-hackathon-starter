# Change: Freigabeschritt für Zahlungen über 10.000 EUR

**Change-ID:** CHG-2087
**Betroffener Service:** payments-api
**Release:** 2026-08-05
**Autor:** Team Payments

## Was sich ändert

Zahlungen ab 10.000 EUR werden nicht mehr sofort ausgeführt. Sie gehen in einen neuen
Zwischenstatus und müssen von einer zweiten Person freigegeben werden.

## Technisch

1. **Neuer Status `in_pruefung`.** Wird gesetzt, wenn `betrag >= 1000000` (Cent).
   Der Status ist nicht final. Bisher waren nur `angenommen`, `ausgefuehrt`,
   `abgelehnt` möglich, davon `ausgefuehrt` und `abgelehnt` final.

2. **Neues Feld `freigabe_bis`** (ISO-8601 UTC) im Zahlungsobjekt. Nur gesetzt, wenn der
   Status `in_pruefung` ist. Läuft die Frist ab, wechselt der Status automatisch auf
   `abgelehnt` mit `grund: "freigabe_frist_abgelaufen"`. Frist: 24 Stunden.

3. **Neuer Endpunkt** `POST /zahlungen/{id}/freigabe`.
   Body: `{ "entscheidung": "freigeben" | "ablehnen", "kommentar": "..." }`.
   Antwort 200 mit dem aktualisierten Zahlungsobjekt.
   Fehler: `409` wenn der Status nicht `in_pruefung` ist, `403` wenn die freigebende
   Person die Zahlung selbst angelegt hat.

4. **Neues Webhook-Event** `zahlung.freigabe_erforderlich`.

## Betrieblich

- Zahlungen können jetzt bis zu 24 Stunden offen stehen, ohne dass etwas kaputt ist.
- Die bestehende Überwachung schlägt Alarm, wenn eine Zahlung länger als 5 Minuten nicht
  final ist. Diese Regel würde ab Release dauerhaft feuern.
- Neue Kennzahl: Anzahl Zahlungen im Status `in_pruefung`, Schwelle 50.

## Nicht Teil des Change

- Vier-Augen-Prinzip für Zahlungen unter 10.000 EUR
- Freigabe über die mobile App
