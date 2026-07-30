#!/usr/bin/env node
// ado-query.mjs — Work Items lesen: per WIQL-Abfrage oder per ID-Liste.
//
//   node ado-query.mjs --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'User Story'"
//   node ado-query.mjs --ids 1234,1235
//   node ado-query.mjs --ids 1234 --json
//
// Endpunkte: POST _apis/wit/wiql (IDs finden) + GET _apis/wit/workitems (Felder holen).

import { getToken, adoFetch, parseArgs, requireEnv, projectBase, API_VERSION, fail } from './ado-auth.mjs';

const HELP = `
ado-query.mjs — Work Items aus Azure DevOps lesen

Aufruf:
  node ado-query.mjs --wiql "<WIQL>"     Abfrage ausfuehren
  node ado-query.mjs --ids 123,456       bestimmte Work Items laden

Optionen:
  --wiql "<text>"      WIQL-Abfrage (SELECT [System.Id] FROM WorkItems WHERE ...)
  --ids 1,2,3          Komma-Liste von Work-Item-IDs (max. 200 pro Aufruf)
  --fields a,b,c       Felder statt der Standardauswahl
  --top N              maximale Trefferzahl bei --wiql (Standard 50)
  --json               Rohdaten als JSON statt Tabelle
  --help               diese Hilfe

Umgebungsvariablen:
  ADO_ORG              Organisation aus https://dev.azure.com/<ORG>/<PROJEKT>
  ADO_PROJECT          Projekt

Beispiele:
  node ado-query.mjs --wiql "SELECT [System.Id] FROM WorkItems WHERE [System.WorkItemType] = 'Test Case' AND [System.State] <> 'Closed' ORDER BY [System.ChangedDate] DESC" --top 20
  node ado-query.mjs --ids 4711,4712 --fields System.Id,System.Title,System.State
  node ado-query.mjs --ids 4711 --json
`;

const DEFAULT_FIELDS = ['System.Id', 'System.WorkItemType', 'System.Title', 'System.State', 'System.AssignedTo'];
const MAX_IDS_PER_CALL = 200;

function cellValue(v) {
  if (v == null) return '';
  if (typeof v === 'object') return v.displayName || v.name || JSON.stringify(v);
  // NFC: decomposed umlauts (o + combining diaeresis) count as 2 chars and break padEnd.
  return String(v).normalize('NFC').replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim();
}

function printTable(rows, fields) {
  if (!rows.length) {
    console.log('Keine Treffer.');
    return;
  }
  const headers = fields.map((f) => f.replace(/^System\./, '').replace(/^Microsoft\.VSTS\.[^.]+\./, ''));
  const limits = fields.map((f) => (/Title|Description/i.test(f) ? 70 : 24));
  const table = rows.map((r) =>
    fields.map((f, i) => {
      const s = cellValue(r.fields ? r.fields[f] : undefined) || (f === 'System.Id' ? String(r.id ?? '') : '');
      return s.length > limits[i] ? s.slice(0, limits[i] - 1) + '…' : s;
    }),
  );
  const widths = headers.map((h, i) => Math.max(h.length, ...table.map((row) => row[i].length)));
  const line = (cells) => cells.map((c, i) => c.padEnd(widths[i])).join('  ').trimEnd();
  console.log(line(headers));
  console.log(widths.map((w) => '-'.repeat(w)).join('  '));
  for (const row of table) console.log(line(row));
  console.log('\n' + rows.length + ' Work Item(s).');
}

async function fetchByIds(org, project, ids, fields, token) {
  const out = [];
  for (let i = 0; i < ids.length; i += MAX_IDS_PER_CALL) {
    const chunk = ids.slice(i, i + MAX_IDS_PER_CALL);
    const url =
      projectBase(org, project) +
      '/wit/workitems?ids=' +
      chunk.join(',') +
      '&fields=' +
      encodeURIComponent(fields.join(',')) +
      '&api-version=' +
      API_VERSION;
    const r = await adoFetch('GET', url, { token });
    out.push(...(r.value || []));
  }
  return out;
}

async function main() {
  const a = parseArgs(process.argv.slice(2), { booleans: ['help', 'h', 'json'] });
  if (a.help || a.h || process.argv.length <= 2) {
    console.log(HELP.trim());
    process.exit(0);
  }

  if (!a.wiql && !a.ids) fail('Entweder --wiql "<Abfrage>" oder --ids 1,2,3 angeben. `--help` zeigt Beispiele.');
  if (a.wiql === true) fail('--wiql braucht eine Abfrage in Anfuehrungszeichen.');
  if (a.ids === true) fail('--ids braucht eine Komma-Liste, z. B. --ids 4711,4712.');

  const org = requireEnv('ADO_ORG', 'Der Name aus https://dev.azure.com/<ORG>/<PROJEKT>.');
  const project = requireEnv('ADO_PROJECT', 'Der Projektname aus derselben URL.');
  const fields = (a.fields && a.fields !== true ? String(a.fields).split(',') : DEFAULT_FIELDS).map((s) => s.trim()).filter(Boolean);

  let token;
  try {
    token = getToken({ quiet: true });
  } catch (e) {
    fail(e.message);
  }

  let ids = [];
  if (a.ids) {
    ids = String(a.ids)
      .split(',')
      .map((s) => s.trim())
      .filter(Boolean);
    const bad = ids.filter((s) => !/^\d+$/.test(s));
    if (bad.length) fail('Keine gueltigen IDs: ' + bad.join(', '));
  } else {
    const top = Number(a.top && a.top !== true ? a.top : 50);
    const url = projectBase(org, project) + '/wit/wiql?api-version=' + API_VERSION + '&$top=' + top;
    const r = await adoFetch('POST', url, { token, body: { query: String(a.wiql) } });
    // Flat queries -> workItems; tree/one-hop queries -> workItemRelations.
    if (Array.isArray(r.workItems)) ids = r.workItems.map((w) => String(w.id));
    else if (Array.isArray(r.workItemRelations)) {
      ids = [...new Set(r.workItemRelations.filter((w) => w.target).map((w) => String(w.target.id)))];
    }
    if (!ids.length) {
      console.log('Die Abfrage lieferte keine Work Items.');
      process.exit(0);
    }
  }

  const items = await fetchByIds(org, project, ids, fields, token);

  if (a.json) console.log(JSON.stringify(items, null, 2));
  else printTable(items, fields);
}

main().catch((e) => {
  console.error('\nFEHLER: ' + e.message);
  process.exit(1);
});
