#!/usr/bin/env node
// ado-comment.mjs — Kommentar an ein bestehendes Work Item haengen.
//
//   node ado-comment.mjs --id 4711 --text "Vom Agenten geprueft, 3 Testfaelle ergaenzt."
//   node ado-comment.mjs --id 4711 --text-file antwort.md --dry-run
//
// Endpunkt: POST _apis/wit/workItems/{id}/comments?api-version=7.1-preview.4
// Der Kommentar-Endpunkt ist bis heute ein Preview-Endpunkt. Ohne "-preview.4"
// antwortet Azure DevOps mit HTTP 400.

import { readFileSync, existsSync } from 'node:fs';
import { getToken, adoFetch, parseArgs, requireEnv, projectBase, toHtml, fail } from './ado-auth.mjs';

const COMMENTS_API_VERSION = '7.1-preview.4';

const HELP = `
ado-comment.mjs — Kommentar an ein Work Item schreiben

Aufruf:
  node ado-comment.mjs --id <WorkItemId> --text "<Text>"
  node ado-comment.mjs --id <WorkItemId> --text-file <Datei>

Optionen:
  --id <ID>            ID des Work Items (Pflicht)
  --text "<Text>"      Kommentartext
  --text-file <Datei>  Kommentartext aus Datei (z. B. Agenten-Output)
  --html               Text ist bereits HTML und wird nicht umgewandelt
  --dry-run            Request ausgeben statt senden (kein Login noetig)
  --json               Antwort als JSON ausgeben
  --help               diese Hilfe

Umgebungsvariablen:
  ADO_ORG              Organisation aus https://dev.azure.com/<ORG>/<PROJEKT>
  ADO_PROJECT          Projekt

Hinweis:
  Kommentare sind HTML. Normaler Text wird automatisch umgewandelt
  (Absaetze, Zeilenumbrueche). Links: --html benutzen und <a href="...">…</a> liefern.

Beispiele:
  node ado-comment.mjs --id 4711 --text "Agent hat 4 Akzeptanzkriterien ergaenzt."
  node ado-comment.mjs --id 4711 --text-file review.md --dry-run
`;

function main() {
  const a = parseArgs(process.argv.slice(2), { booleans: ['help', 'h', 'json', 'dry-run', 'html'] });
  if (a.help || a.h || process.argv.length <= 2) {
    console.log(HELP.trim());
    process.exit(0);
  }

  const id = a.id;
  if (!id || id === true) fail('--id fehlt. Beispiel: --id 4711.');
  if (!/^\d+$/.test(String(id))) fail('--id muss eine Zahl sein, bekommen: ' + id);

  let raw;
  if (a['text-file'] && a['text-file'] !== true) {
    if (!existsSync(a['text-file'])) fail('Datei nicht gefunden: ' + a['text-file']);
    raw = readFileSync(a['text-file'], 'utf8');
  } else if (a.text && a.text !== true) {
    raw = String(a.text);
  } else {
    fail('Entweder --text "<Text>" oder --text-file <Datei> angeben.');
  }
  if (!raw.trim()) fail('Der Kommentartext ist leer.');

  const org = requireEnv('ADO_ORG', 'Der Name aus https://dev.azure.com/<ORG>/<PROJEKT>.');
  const project = requireEnv('ADO_PROJECT', 'Der Projektname aus derselben URL.');

  const body = { text: a.html ? raw : toHtml(raw) };
  const url = projectBase(org, project) + '/wit/workItems/' + id + '/comments?api-version=' + COMMENTS_API_VERSION;

  if (a['dry-run']) {
    console.log('DRY RUN — es wird nichts gesendet.\n');
    console.log('POST ' + url);
    console.log('Content-Type: application/json');
    console.log('Authorization: Bearer <Token wird beim echten Aufruf via az geholt>\n');
    console.log(JSON.stringify(body, null, 2));
    console.log('\nOhne --dry-run wird dieser Request abgeschickt.');
    process.exit(0);
  }

  let token;
  try {
    token = getToken({ quiet: true });
  } catch (e) {
    fail(e.message);
  }

  return adoFetch('POST', url, { token, body }).then((res) => {
    if (a.json) {
      console.log(JSON.stringify(res, null, 2));
      return;
    }
    const webUrl =
      'https://dev.azure.com/' + encodeURIComponent(org) + '/' + encodeURIComponent(project) + '/_workitems/edit/' + id;
    console.log('Kommentar geschrieben an Work Item #' + id + (res.id ? ' (Kommentar-ID ' + res.id + ')' : ''));
    console.log('Link: ' + webUrl);
  });
}

Promise.resolve()
  .then(main)
  .catch((e) => {
    console.error('\nFEHLER: ' + e.message);
    process.exit(1);
  });
