# Azure DevOps + Agent

**Wofür:** Work Items (User Stories, Test Cases, Bugs) aus Azure DevOps in deinen Agenten
bekommen — und das Ergebnis wieder zurück.
**Für wen:** alle. Es gibt drei Wege, gestaffelt nach dem, was du heute wirklich tun kannst.

---

## Der eine Satz, der heute zählt

> **Die meisten Agenten können lesen, aber nicht schreiben.**
> Das realistische Muster für heute ist deshalb:
> **Agent erzeugt den fertigen Inhalt → ein Mensch legt ihn in Azure DevOps an.**

Das ist keine Notlösung. Der Agent macht die Arbeit, die weh tut (formulieren, strukturieren,
Akzeptanzkriterien ableiten, Testfälle ausdenken). Das Einfügen dauert 30 Sekunden.

Die Skripte in [`scripts/`](scripts/) automatisieren genau diesen letzten Schritt — für Teams,
die eine Entwicklerin oder einen Entwickler dabei haben. Alle anderen kommen mit Copy-Paste
genauso weit und verlieren dabei keinen Punkt bei der Bewertung.

---

## Welcher Weg ist meiner?

| Stufe | Du kannst … | Dein Weg | Anleitung |
|---|---|---|---|
| **1 — ohne Technik** | Azure DevOps im Browser öffnen | Query bauen, Text kopieren, Agenten-Output per Hand als Work Item anlegen | [01-ohne-technik.md](01-ohne-technik.md) |
| **2 — Excel / CSV** | Dateien herunterladen und hochladen | Query als CSV exportieren, Agent füllt Spalten, CSV zurück importieren | [02-excel-und-csv.md](02-excel-und-csv.md) |
| **3 — Skript** | `node` und PowerShell benutzen | REST API mit Azure-CLI-Login, kein Token-Handling | [03-rest-api.md](03-rest-api.md) + [scripts/](scripts/) |

**Nicht sicher?** Nimm Stufe 1. Wenn ihr um 17:00 Uhr noch Luft habt, geht eine Stufe höher.
Ein Team, das um 18:00 Uhr noch an einem Login scheitert, hat den Tag verloren.

---

## Quickstart für den Skript-Weg

```powershell
# 1. Voraussetzungen: Node 18+ und Azure CLI installiert
node --version
az --version

# 2. Einmal anmelden (kein PAT, kein Token kopieren)
az login

# 3. Organisation und Projekt setzen — beides steht in deiner Browser-URL:
#    https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>
$env:ADO_ORG = "<DEINE-ORG>"
$env:ADO_PROJECT = "<DEIN-PROJEKT>"

# 4. Verbindung prüfen (grün/rot Selbsttest)
cd azure-devops/scripts
node ado-auth.mjs
```

Danach: `node ado-query.mjs --ids 4711` liest, `node ado-create.mjs --help` schreibt.
Ein vollständiges Beispiel von der Idee bis zum angelegten Work Item liegt in
[beispiel-user-story-agent.md](beispiel-user-story-agent.md).

---

## Auth in einem Absatz

Keine Personal Access Tokens. Nirgends. Die Skripte melden sich über die Azure CLI an
(`az login`) und holen sich damit ein kurzlebiges Entra-Token für die Azure-DevOps-Ressource
`499b84ac-1321-427f-aa17-267ca6975798`. Das Token wird ~50 Minuten lokal zwischengespeichert
und als `Authorization: Bearer <token>` mitgeschickt. Details:
[03-rest-api.md](03-rest-api.md).

---

## Wenn etwas nicht geht

| Symptom | Wahrscheinliche Ursache | Was du tust |
|---|---|---|
| `az login` öffnet nichts / bricht ab | mehrere Tenants, oder Browser-Fenster im Hintergrund | `az login --tenant <DEINE-TENANT-ID>` · Alt+Tab prüfen |
| `az` nicht gefunden | Azure CLI fehlt oder ist nicht im PATH | Terminal neu öffnen. Sonst: [Azure CLI installieren](https://learn.microsoft.com/cli/azure/install-azure-cli) |
| **HTTP 401** Unauthorized | Token abgelaufen oder falscher Tenant | `node ado-auth.mjs --clear`, dann `az login` |
| **HTTP 203** Non-Authoritative | falsche Resource-ID beim Token — Azure DevOps liefert eine Anmeldeseite statt JSON | muss `--resource 499b84ac-1321-427f-aa17-267ca6975798` sein. Cache leeren, neu holen |
| **HTTP 403** Forbidden | angemeldet, aber keine Schreibrechte im Projekt | Projekt-Admin fragen (Rolle *Contributor*) |
| **HTTP 404**, "project not found" | `ADO_ORG` / `ADO_PROJECT` falsch geschrieben | beide **exakt** aus der Browser-URL kopieren: `https://dev.azure.com/<ORG>/<PROJEKT>`. Leerzeichen im Namen sind erlaubt, dann in Anführungszeichen setzen |
| Netzwerkfehler / Timeout | Unternehmens-Proxy | `$env:HTTPS_PROXY = "http://<proxy>:<port>"` setzen und erneut versuchen |
| Umlaute kaputt nach CSV-Import | falsche Kodierung | CSV als **UTF-8** speichern, siehe [02-excel-und-csv.md](02-excel-und-csv.md) |
| Beschreibung sieht aus wie `<p>Text</p>` | Description ist ein HTML-Feld | Agent bitten, reinen Text zu liefern — die Skripte wandeln ihn um |

---

## Dateien hier

| Datei | Inhalt |
|---|---|
| [01-ohne-technik.md](01-ohne-technik.md) | Query-UI, Export to CSV, Copy-Paste-Rezept |
| [02-excel-und-csv.md](02-excel-und-csv.md) | Massenexport, Agent füllt CSV, Re-Import mit den echten Import-Regeln |
| [03-rest-api.md](03-rest-api.md) | Auth-Modell, die vier Endpunkte, curl-Beispiele |
| [beispiel-user-story-agent.md](beispiel-user-story-agent.md) | Durchgängiges Beispiel: Absatz → Prompt → Agenten-Output → angelegtes Work Item |
| [scripts/](scripts/) | Vier Node-Skripte, keine npm-Abhängigkeiten |
