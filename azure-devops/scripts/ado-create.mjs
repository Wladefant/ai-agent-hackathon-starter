#!/usr/bin/env node
// ado-create.mjs — Work Item anlegen (User Story, Bug, Task, Test Case ...).
//
//   node ado-create.mjs --type "User Story" --title "..." --description-file story.md
//   node ado-create.mjs --file story.json
//   node ado-create.mjs --dry-run ...     zeigt den Request, sendet nichts
//
// Endpunkt: POST _apis/wit/workitems/${Typ}?api-version=7.1
// Body-Format: JSON Patch (Content-Type: application/json-patch+json).

import { readFileSync, existsSync } from 'node:fs';
import { getToken, adoFetch, parseArgs, requireEnv, projectBase, toHtml, API_VERSION, fail } from './ado-auth.mjs';

const HELP = `
ado-create.mjs — Work Item in Azure DevOps anlegen

Aufruf:
  node ado-create.mjs --type "User Story" --title "Titel" [Optionen]
  node ado-create.mjs --file story.json

Optionen:
  --type "<Typ>"              User Story | Bug | Task | Test Case | Epic ... (Pflicht)
  --title "<Titel>"           Titel des Work Items (Pflicht)
  --description "<Text>"      Beschreibung als Text
  --description-file <Datei>  Beschreibung aus einer Datei (z. B. Agenten-Output)
  --acceptance "<Text>"       Akzeptanzkriterien als Text
  --acceptance-file <Datei>   Akzeptanzkriterien aus einer Datei
  --area "<Pfad>"             Area Path (Standard: Projektname)
  --iteration "<Pfad>"        Iteration Path
  --tags "a; b"               Tags, mit Semikolon getrennt
  --parent <ID>               verknuepft das neue Item als Kind von <ID>
  --field Ref.Name=Wert       beliebiges Feld setzen, mehrfach verwendbar
  --file <Datei.json>         alle Angaben aus einer JSON-Datei (siehe unten)
  --html                      Texte sind bereits HTML und werden nicht umgewandelt
  --dry-run                   Request ausgeben statt senden (kein Login noetig)
  --json                      Antwort als JSON ausgeben
  --help                      diese Hilfe

Umgebungsvariablen:
  ADO_ORG                     Organisation aus https://dev.azure.com/<ORG>/<PROJEKT>
  ADO_PROJECT                 Projekt

JSON-Datei (--file):
  {
    "type": "User Story",
    "title": "Titel",
    "description": "Mehrzeiliger Text",
    "acceptance": "- Kriterium 1\\n- Kriterium 2",
    "tags": "hackathon; agent",
    "fields": { "Microsoft.VSTS.Common.Priority": 2 }
  }
  CLI-Flags haben Vorrang vor Werten aus der Datei.

Hinweis zu HTML:
  Description und Acceptance Criteria sind in Azure DevOps HTML-Felder. Dieses Skript
  wandelt normalen Text automatisch in einfaches HTML um (Absaetze, Zeilenumbrueche).
  Wenn dein Agent schon HTML liefert, --html setzen.

Beispiele:
  node ado-create.mjs --type "User Story" --title "Kontoauszug als PDF" \\
    --description-file story.md --acceptance-file kriterien.md --tags "hackathon"
  node ado-create.mjs --dry-run --type Bug --title "Falsche Summe im Report"
`;

const FIELD_MAP = {
  title: 'System.Title',
  description: 'System.Description',
  acceptance: 'Microsoft.VSTS.Common.AcceptanceCriteria',
  area: 'System.AreaPath',
  iteration: 'System.IterationPath',
  tags: 'System.Tags',
};
const HTML_FIELDS = new Set(['System.Description', 'Microsoft.VSTS.Common.AcceptanceCriteria', 'Microsoft.VSTS.TCM.ReproSteps']);

function readTextFile(p, label) {
  if (!existsSync(p)) fail('Datei fuer ' + label + ' nicht gefunden: ' + p);
  try {
    return readFileSync(p, 'utf8');
  } catch (e) {
    fail('Datei fuer ' + label + ' nicht lesbar: ' + p + '\n  ' + e.message);
  }
}

function main() {
  const a = parseArgs(process.argv.slice(2), { booleans: ['help', 'h', 'json', 'dry-run', 'html'], repeatable: ['field'] });
  if (a.help || a.h || process.argv.length <= 2) {
    console.log(HELP.trim());
    process.exit(0);
  }

  // 1. Werte aus --file einlesen, CLI-Flags gewinnen.
  let spec = {};
  if (a.file && a.file !== true) {
    const raw = readTextFile(a.file, '--file');
    try {
      spec = JSON.parse(raw);
    } catch (e) {
      fail('--file ist kein gueltiges JSON: ' + a.file + '\n  ' + e.message);
    }
  }

  const pick = (flag) => (a[flag] !== undefined && a[flag] !== true ? String(a[flag]) : spec[flag]);
  const type = pick('type');
  if (!type) fail('--type fehlt. Beispiel: --type "User Story". `--help` zeigt alle Optionen.');

  const values = {};
  values[FIELD_MAP.title] = pick('title');
  values[FIELD_MAP.description] =
    a['description-file'] && a['description-file'] !== true
      ? readTextFile(a['description-file'], '--description-file')
      : pick('description');
  values[FIELD_MAP.acceptance] =
    a['acceptance-file'] && a['acceptance-file'] !== true
      ? readTextFile(a['acceptance-file'], '--acceptance-file')
      : pick('acceptance');
  values[FIELD_MAP.area] = pick('area');
  values[FIELD_MAP.iteration] = pick('iteration');
  values[FIELD_MAP.tags] = pick('tags');

  for (const [k, v] of Object.entries(spec.fields || {})) values[k] = v;
  for (const f of a.field || []) {
    const eq = String(f).indexOf('=');
    if (eq < 1) fail('--field braucht die Form Referenz.Name=Wert, bekommen: ' + f);
    values[String(f).slice(0, eq)] = String(f).slice(eq + 1);
  }

  if (!values[FIELD_MAP.title]) fail('--title fehlt (oder "title" in der --file JSON).');

  // 2. JSON-Patch-Body bauen.
  const patch = [];
  for (const [field, raw] of Object.entries(values)) {
    if (raw === undefined || raw === null || raw === '') continue;
    const value = HTML_FIELDS.has(field) && !a.html && typeof raw === 'string' ? toHtml(raw) : raw;
    patch.push({ op: 'add', path: '/fields/' + field, value });
  }

  const org = requireEnv('ADO_ORG', 'Der Name aus https://dev.azure.com/<ORG>/<PROJEKT>.');
  const project = requireEnv('ADO_PROJECT', 'Der Projektname aus derselben URL.');

  const parent = pick('parent');
  if (parent) {
    if (!/^\d+$/.test(String(parent))) fail('--parent muss eine Work-Item-ID sein, bekommen: ' + parent);
    patch.push({
      op: 'add',
      path: '/relations/-',
      value: {
        rel: 'System.LinkTypes.Hierarchy-Reverse',
        url: 'https://dev.azure.com/' + encodeURIComponent(org) + '/_apis/wit/workItems/' + parent,
      },
    });
  }

  const url = projectBase(org, project) + '/wit/workitems/$' + encodeURIComponent(type) + '?api-version=' + API_VERSION;

  // 3. Dry-Run: exakten Request zeigen, nichts senden, keinen Token holen.
  if (a['dry-run']) {
    console.log('DRY RUN — es wird nichts gesendet.\n');
    console.log('POST ' + url);
    console.log('Content-Type: application/json-patch+json');
    console.log('Authorization: Bearer <Token wird beim echten Aufruf via az geholt>\n');
    console.log(JSON.stringify(patch, null, 2));
    console.log('\n' + patch.length + ' Patch-Operation(en). Ohne --dry-run wird dieser Request abgeschickt.');
    process.exit(0);
  }

  let token;
  try {
    token = getToken({ quiet: true });
  } catch (e) {
    fail(e.message);
  }

  return adoFetch('POST', url, { token, body: patch, contentType: 'application/json-patch+json' }).then((res) => {
    if (a.json) {
      console.log(JSON.stringify(res, null, 2));
      return;
    }
    const webUrl =
      'https://dev.azure.com/' + encodeURIComponent(org) + '/' + encodeURIComponent(project) + '/_workitems/edit/' + res.id;
    console.log('Angelegt: ' + type + ' #' + res.id);
    console.log('Titel:    ' + (res.fields ? res.fields['System.Title'] : values[FIELD_MAP.title]));
    console.log('Link:     ' + webUrl);
  });
}

Promise.resolve()
  .then(main)
  .catch((e) => {
    console.error('\nFEHLER: ' + e.message);
    process.exit(1);
  });
