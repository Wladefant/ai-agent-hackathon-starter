# Anforderung: Tageslimit für Überweisungen selbst ändern

**Story-ID:** ANF-1042
**Status:** freigegeben

## User Story

Als Kundin im Online-Banking möchte ich mein Tageslimit für Überweisungen selbst
ändern können, damit ich größere Zahlungen nicht telefonisch beauftragen muss.

## Fachlicher Ablauf

1. Kundin öffnet **Einstellungen → Limits**.
2. Das aktuelle Tageslimit wird angezeigt (Standard: 2.000 EUR).
3. Kundin gibt ein neues Limit ein und bestätigt.
4. Die Änderung wird mit einem zweiten Faktor freigegeben.
5. Nach erfolgreicher Freigabe gilt das neue Limit sofort.

## Regeln

| Regel | Wert |
|---|---|
| Minimum | 100 EUR |
| Maximum | 50.000 EUR |
| Schrittweite | volle 100 EUR |
| Erhöhung | nur mit zweitem Faktor |
| Senkung | ohne zweiten Faktor, gilt sofort |
| Änderungen pro Tag | maximal 3 |
| Berechtigung | nur Kontoinhaber:in, nicht Bevollmächtigte |

## Fehlerfälle

- Eingabe außerhalb 100–50.000 EUR → Feldfehler, kein Speichern.
- Eingabe nicht durch 100 teilbar → Feldfehler, kein Speichern.
- Zweiter Faktor abgelaufen oder falsch → Änderung wird verworfen, altes Limit bleibt.
- Viertes Änderungsversuch am selben Tag → Hinweis, Sperre bis zum Folgetag.

## Nicht im Umfang

- Limits für Kartenzahlungen
- Dauerhafte Limitänderung über einen Berater
