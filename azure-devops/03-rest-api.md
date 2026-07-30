# Stufe 3 — REST API

**Wofür:** Work Items aus einem Skript lesen und schreiben — ohne Personal Access Token.
**Für wen:** Entwicklerinnen und Entwickler. Du brauchst Node 18+ und die Azure CLI.

Die fertigen Skripte liegen in [`scripts/`](scripts/). Dieses Dokument erklärt, **was sie
tun**, damit du sie anpassen kannst.

---

## Das Auth-Modell

**Kein PAT. Nirgends.** Personal Access Tokens sind langlebige Geheimnisse, die in Repos und
Chatverläufen landen. Stattdessen:

```
az login                                   einmal pro Tag, interaktiv im Browser
   ↓
az account get-access-token                kurzlebiges Entra-Token (~1 Stunde)
   --resource 499b84ac-1321-427f-aa17-267ca6975798
   ↓
Authorization: Bearer <token>              an jedem REST-Aufruf
```

**Die GUID `499b84ac-1321-427f-aa17-267ca6975798` ist die Azure-DevOps-Ressource.** Sie ist
weltweit in jedem Tenant gleich, sie ist kein Geheimnis und sie ist nicht deine
Organisations-ID. Wenn du sie weglässt oder falsch setzt, bekommst du ein Token für die falsche
Zielgruppe — und Azure DevOps antwortet mit **HTTP 203** und einer HTML-Anmeldeseite statt mit
JSON. Das ist der häufigste Fehler überhaupt.

Token holen, roh:

```bash
az account get-access-token \
  --resource 499b84ac-1321-427f-aa17-267ca6975798 \
  --query accessToken -o tsv
```

`ado-auth.mjs` macht genau das, legt das Ergebnis für ~50 Minuten in einer lokalen Cache-Datei
ab und gibt es an die anderen Skripte weiter. Ein Token ist etwa eine Stunde gültig; der Cache
läuft bewusst früher ab.

**In einer Pipeline** brauchst du kein `az`: setz `ADO_BEARER` auf `$(System.AccessToken)`.
Die Skripte bevorzugen diese Variable und rufen `az` dann gar nicht erst auf.

---

## Konfiguration

Beide Werte stehen in deiner Browser-URL: `https://dev.azure.com/<ADO_ORG>/<ADO_PROJECT>`

```powershell
$env:ADO_ORG = "<DEINE-ORG>"
$env:ADO_PROJECT = "<DEIN-PROJEKT>"
```

```bash
export ADO_ORG="<DEINE-ORG>"
export ADO_PROJECT="<DEIN-PROJEKT>"
```

Alle Skripte brechen mit einer Meldung ab, die die fehlende Variable beim Namen nennt.

---

## Die vier Endpunkte

Basis-URL für alles Folgende:

```
https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_apis
```

### 1. WIQL — Work Items suchen

`POST _apis/wit/wiql?api-version=7.1`

Liefert **nur IDs**, keine Feldwerte. Das ist Absicht: WIQL ist die Suche, nicht der Abruf.

```bash
TOKEN=$(az account get-access-token --resource 499b84ac-1321-427f-aa17-267ca6975798 --query accessToken -o tsv)

curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"query":"SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = '"'"'User Story'"'"' AND [System.State] <> '"'"'Closed'"'"' ORDER BY [System.ChangedDate] DESC"}' \
  "https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_apis/wit/wiql?api-version=7.1&\$top=20"
```

Antwort: `{ "workItems": [ { "id": 4711, "url": "…" }, … ] }`

Bei Tree- oder One-Hop-Queries heißt das Feld stattdessen `workItemRelations`; die IDs stehen
dann in `target.id`. `ado-query.mjs` behandelt beide Fälle.

### 2. Work Items abrufen

`GET _apis/wit/workitems?ids=…&fields=…&api-version=7.1`

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_apis/wit/workitems?ids=4711,4712&fields=System.Id,System.Title,System.State&api-version=7.1"
```

Maximal **200 IDs** pro Aufruf. `ado-query.mjs` teilt längere Listen automatisch auf.
Ohne `fields` bekommst du alle Felder — viel Datenmüll, aber nützlich, um einmal zu sehen, wie
die Referenznamen deines Prozesses heißen.

### 3. Work Item anlegen

`POST _apis/wit/workitems/${Typ}?api-version=7.1`

Zwei Dinge sind hier anders als überall sonst:

- Der Typ steht **in der URL mit einem `$` davor**: `/wit/workitems/$User%20Story`
- Der Body ist **JSON Patch**, Content-Type `application/json-patch+json` — kein normales JSON

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json-patch+json" \
  -d '[
        {"op":"add","path":"/fields/System.Title","value":"Kontoauszug als PDF"},
        {"op":"add","path":"/fields/System.Description","value":"<p>Als Kundin möchte ich …</p>"},
        {"op":"add","path":"/fields/Microsoft.VSTS.Common.AcceptanceCriteria","value":"<ul><li>Download sichtbar</li></ul>"}
      ]' \
  "https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_apis/wit/workitems/\$User%20Story?api-version=7.1"
```

Antwort enthält `id` — das ist deine neue Work-Item-Nummer.

**Ein bestehendes Work Item ändern** ist derselbe Body mit `PATCH` auf
`/wit/workitems/<ID>?api-version=7.1`.

### 4. Kommentar hinzufügen

`POST _apis/wit/workItems/<ID>/comments?api-version=7.1-preview.4`

```bash
curl -s -X POST \
  -H "Authorization: Bearer $TOKEN" \
  -H "Content-Type: application/json" \
  -d '{"text":"<p>Vom Agenten ergänzt: 4 Akzeptanzkriterien.</p>"}' \
  "https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_apis/wit/workItems/4711/comments?api-version=7.1-preview.4"
```

**Das `-preview.4` muss dranbleiben.** Der Kommentar-Endpunkt ist bis heute Preview; mit
`api-version=7.1` allein antwortet er mit HTTP 400.

---

## Feldnamen

Im JSON-Patch benutzt du **Referenznamen**, nicht die Anzeigenamen aus der Oberfläche.

| Anzeigename | Referenzname |
|---|---|
| Title | `System.Title` |
| Description | `System.Description` |
| State | `System.State` |
| Work Item Type | `System.WorkItemType` |
| Area Path | `System.AreaPath` |
| Iteration Path | `System.IterationPath` |
| Tags | `System.Tags` (Trennzeichen `;`) |
| Assigned To | `System.AssignedTo` |
| Acceptance Criteria | `Microsoft.VSTS.Common.AcceptanceCriteria` |
| Repro Steps | `Microsoft.VSTS.TCM.ReproSteps` |
| Steps (Test Case) | `Microsoft.VSTS.TCM.Steps` |
| Priority | `Microsoft.VSTS.Common.Priority` |

Eigene Felder heißen `Custom.<Name>`. Die vollständige Liste deines Projekts:

```bash
curl -s -H "Authorization: Bearer $TOKEN" \
  "https://dev.azure.com/<DEINE-ORG>/_apis/wit/fields?api-version=7.1"
```

---

## Zwei Formate, die überraschen

**HTML-Felder.** `System.Description`, `Microsoft.VSTS.Common.AcceptanceCriteria` und
`Microsoft.VSTS.TCM.ReproSteps` sind HTML. Schickst du reinen Text hinein, verschwinden alle
Zeilenumbrüche und alles steht in einem Block. `ado-create.mjs` wandelt Text deshalb
automatisch in einfaches HTML um (Absätze, `<ul>`-Listen). Mit `--html` schaltest du das ab,
falls dein Agent schon HTML liefert.

**Test-Case-Schritte.** `Microsoft.VSTS.TCM.Steps` ist kein HTML, sondern ein eigenes
XML-Format:

```xml
<steps id="0" last="2">
  <step id="1" type="ActionStep">
    <parameterizedString isformatted="true">&lt;P&gt;Anmelden&lt;/P&gt;</parameterizedString>
    <parameterizedString isformatted="true">&lt;P&gt;Übersicht erscheint&lt;/P&gt;</parameterizedString>
  </step>
</steps>
```

Je Schritt zwei `parameterizedString`: erst *Action*, dann *Expected Result*. Das ist fummelig.
**Für heute:** Test Cases mit Titel und Beschreibung anlegen und die Schritte in der Oberfläche
einfügen. Der Aufwand, das XML korrekt zu erzeugen, lohnt sich in vier Stunden nicht.

---

## Anpassen

Alle vier Skripte importieren `ado-auth.mjs`. Ein eigenes Skript sieht so aus:

```js
import { getToken, adoFetch, projectBase, API_VERSION } from './ado-auth.mjs';

const token = getToken();
const base = projectBase(process.env.ADO_ORG, process.env.ADO_PROJECT);

const res = await adoFetch('GET', `${base}/wit/workitems/4711?api-version=${API_VERSION}`, { token });
console.log(res.fields['System.Title']);
```

`adoFetch` übersetzt die typischen HTTP-Fehler (203, 401, 403, 404, Proxy) in Meldungen, die
sagen, was zu tun ist. Nutze es, statt selbst `fetch` aufzurufen.

---

## Weiterführend

- [Azure DevOps REST API — Work Items](https://learn.microsoft.com/rest/api/azure/devops/wit/work-items)
- [WIQL-Syntax](https://learn.microsoft.com/azure/devops/boards/queries/wiql-syntax)
- [Feld-Referenznamen](https://learn.microsoft.com/azure/devops/boards/work-items/guidance/work-item-field)
