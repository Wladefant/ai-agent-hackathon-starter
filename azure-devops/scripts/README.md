# scripts — Azure DevOps ohne PAT

Vier Node-Skripte, keine npm-Abhängigkeiten, kein `npm install`.

## Voraussetzungen

- **Node 18+** (`node --version`) — wegen des eingebauten `fetch`
- **Azure CLI** (`az --version`) — [Installation](https://learn.microsoft.com/cli/azure/install-azure-cli)
- **einmal `az login`** — kein Personal Access Token, nirgends

## Umgebungsvariablen

Beide Werte stehen in deiner Browser-URL `https://dev.azure.com/<ADO_ORG>/<ADO_PROJECT>`:

```powershell
$env:ADO_ORG = "<DEINE-ORG>"
$env:ADO_PROJECT = "<DEIN-PROJEKT>"
```

Optional: `ADO_BEARER` (fertiges Entra-Token, z. B. `$(System.AccessToken)` in einer
Pipeline) — überspringt `az` komplett.

## Je ein Beispiel

```bash
node ado-auth.mjs                                          # Selbsttest: grün oder rot
node ado-query.mjs --ids 4711,4712                         # Work Items als Tabelle
node ado-create.mjs --type "User Story" --title "Titel" --description-file story.md
node ado-comment.mjs --id 4711 --text "Vom Agenten geprüft."
```

`--help` funktioniert überall. `--dry-run` bei `ado-create` und `ado-comment` zeigt den
exakten Request und sendet nichts.
