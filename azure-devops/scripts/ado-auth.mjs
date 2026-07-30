#!/usr/bin/env node
// ado-auth.mjs — Azure DevOps auth without a Personal Access Token.
//
// Auth model: `az login` once, then mint a short-lived Entra bearer token for the
// Azure DevOps resource (499b84ac-1321-427f-aa17-267ca6975798) and send it as
// `Authorization: Bearer <token>`. The token is cached on disk for ~50 minutes so
// repeated script runs do not shell out to `az` every time.
//
// NO PATs. Not in env vars, not in files, not in this repo.
//
// Used as a module by the other scripts:
//   import { getToken, adoFetch, requireEnv } from './ado-auth.mjs';
//
// Run directly for a self-test:
//   node ado-auth.mjs

import { spawnSync } from 'node:child_process';
import { readFileSync, writeFileSync, mkdirSync, existsSync } from 'node:fs';
import { join } from 'node:path';
import { homedir } from 'node:os';

/** The Azure DevOps resource (audience) GUID. Same value in every tenant worldwide. */
export const ADO_RESOURCE_ID = '499b84ac-1321-427f-aa17-267ca6975798';
export const API_VERSION = '7.1';

const CACHE_DIR = join(process.env.LOCALAPPDATA || join(homedir(), '.cache'), 'ado-hackathon');
const TOKEN_CACHE = join(CACHE_DIR, 'token.json');
const TOKEN_TTL_SEC = 50 * 60;

const USE_COLOR = process.stdout.isTTY && !process.env.NO_COLOR;
const green = (s) => (USE_COLOR ? `\x1b[32m${s}\x1b[0m` : s);
const red = (s) => (USE_COLOR ? `\x1b[31m${s}\x1b[0m` : s);
const dim = (s) => (USE_COLOR ? `\x1b[2m${s}\x1b[0m` : s);

/* --------------------------------- helpers --------------------------------- */

/** Print a message to stderr and exit 1. Use for anything the user must fix. */
export function fail(msg) {
  console.error(red('FEHLER: ') + msg);
  process.exit(1);
}

/** Read a required env var or exit with a message that names the variable. */
export function requireEnv(name, hint) {
  const v = (process.env[name] || '').trim();
  if (!v) {
    fail(
      `Umgebungsvariable ${name} ist nicht gesetzt.\n` +
        (hint ? `  ${hint}\n` : '') +
        `  PowerShell:  $env:${name} = "..."\n` +
        `  bash:        export ${name}="..."`,
    );
  }
  return v;
}

/** Minimal argv parser: --flag, --key value, repeated --key collected into arrays. */
export function parseArgs(argv, { repeatable = [], booleans = [] } = {}) {
  const out = { _: [] };
  for (let i = 0; i < argv.length; i++) {
    const a = argv[i];
    if (!a.startsWith('--')) {
      out._.push(a);
      continue;
    }
    let key = a.slice(2);
    let val;
    const eq = key.indexOf('=');
    if (eq !== -1) {
      val = key.slice(eq + 1);
      key = key.slice(0, eq);
    }
    if (booleans.includes(key)) {
      out[key] = val === undefined ? true : val !== 'false';
      continue;
    }
    if (val === undefined) {
      val = argv[i + 1];
      if (val === undefined || val.startsWith('--')) {
        // A value-taking flag with no value: treat as boolean true rather than
        // silently swallowing the next flag.
        out[key] = true;
        continue;
      }
      i++;
    }
    if (repeatable.includes(key)) (out[key] = out[key] || []).push(val);
    else out[key] = val;
  }
  return out;
}

/**
 * Escape plain text and turn it into simple ADO-safe HTML.
 * Blank line = new paragraph. A block whose lines all start with "-", "*" or "1." becomes
 * a list, because that is what agents produce for acceptance criteria.
 */
export function toHtml(text) {
  const esc = (s) => String(s).replace(/&/g, '&amp;').replace(/</g, '&lt;').replace(/>/g, '&gt;');
  const blocks = String(text).replace(/\r\n/g, '\n').trim().split(/\n\s*\n/);
  const out = [];
  for (const block of blocks) {
    const lines = block.split('\n').map((l) => l.trim()).filter(Boolean);
    if (!lines.length) continue;
    const bullets = lines.every((l) => /^[-*•]\s+/.test(l));
    const numbered = lines.every((l) => /^\d+[.)]\s+/.test(l));
    if (bullets || numbered) {
      const tag = numbered ? 'ol' : 'ul';
      out.push('<' + tag + '>' + lines.map((l) => '<li>' + esc(l.replace(/^([-*•]|\d+[.)])\s+/, '')) + '</li>').join('') + '</' + tag + '>');
    } else {
      out.push('<p>' + lines.map(esc).join('<br>') + '</p>');
    }
  }
  return out.join('');
}

/* ----------------------------------- az ----------------------------------- */

function azCandidates() {
  return [
    join(homedir(), 'azure-cli', 'bin', 'az.cmd'),
    'C:\\Program Files (x86)\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',
    'C:\\Program Files\\Microsoft SDKs\\Azure\\CLI2\\wbin\\az.cmd',
  ];
}

/**
 * "az is not installed" looks different depending on how it is launched. With shell:true
 * (needed on Windows, where az is az.cmd) there is no ENOENT — cmd.exe just prints
 * "'az' is not recognized". Both signals count, otherwise the self-test reports a green
 * "Azure CLI gefunden" on a machine that has no Azure CLI at all.
 */
function looksMissing(r) {
  if (r.error && r.error.code === 'ENOENT') return true;
  const s = String(r.stderr || '');
  return /is not recognized as|command not found|No such file or directory/i.test(s);
}

function runAz(args, timeoutMs = 20000, interactive = false) {
  const win = process.platform === 'win32';
  const opts = { timeout: timeoutMs, windowsHide: true, shell: win, encoding: 'utf8' };
  if (interactive) opts.stdio = 'inherit';
  let r = spawnSync('az', args, opts);
  if (looksMissing(r)) {
    for (const c of azCandidates()) {
      if (existsSync(c)) {
        // Still through the shell: since Node 20 a .cmd file cannot be spawned directly
        // (EINVAL). Quote the path, it usually contains spaces.
        r = spawnSync(win ? '"' + c + '"' : c, args, opts);
        break;
      }
    }
  }
  return {
    code: typeof r.status === 'number' ? r.status : r.error ? -1 : 1,
    stdout: r.stdout || '',
    stderr: r.stderr || (r.error ? String(r.error.message) : ''),
    missing: looksMissing(r),
  };
}

function readCache() {
  try {
    if (!existsSync(TOKEN_CACHE)) return null;
    const c = JSON.parse(readFileSync(TOKEN_CACHE, 'utf8'));
    if (c && c.access_token && Number(c.expires_at) > Math.floor(Date.now() / 1000) + 60) {
      return c.access_token;
    }
  } catch {
    /* corrupt cache is not an error, just mint again */
  }
  return null;
}

function writeCache(token) {
  try {
    mkdirSync(CACHE_DIR, { recursive: true });
    writeFileSync(
      TOKEN_CACHE,
      JSON.stringify({ access_token: token, expires_at: Math.floor(Date.now() / 1000) + TOKEN_TTL_SEC }),
      'utf8',
    );
  } catch {
    /* cache is an optimisation, never fatal */
  }
}

/**
 * Return a bearer token for the Azure DevOps REST API.
 *
 * Order: ADO_BEARER env (for pipelines: $(System.AccessToken)) -> disk cache ->
 * `az account get-access-token`. Throws with a readable instruction when none works.
 */
export function getToken({ quiet = true } = {}) {
  const injected = (process.env.ADO_BEARER || '').trim();
  if (injected) {
    if (!quiet) console.error(dim('[auth] ADO_BEARER wird verwendet (az wird nicht aufgerufen).'));
    return injected;
  }

  const cached = readCache();
  if (cached) {
    if (!quiet) console.error(dim('[auth] Token aus Cache (' + TOKEN_CACHE + ').'));
    return cached;
  }

  const m = runAz(['account', 'get-access-token', '--resource', ADO_RESOURCE_ID, '--query', 'accessToken', '-o', 'tsv']);
  if (m.missing) {
    throw new Error(
      'Azure CLI (`az`) wurde nicht gefunden.\n' +
        '  Installieren: https://learn.microsoft.com/cli/azure/install-azure-cli\n' +
        '  Alternative ohne az: ADO_BEARER mit einem gueltigen Entra-Token fuer die Ressource ' +
        ADO_RESOURCE_ID +
        ' setzen.',
    );
  }
  if (m.code === 0 && m.stdout.trim()) {
    const t = m.stdout.trim();
    writeCache(t);
    if (!quiet) console.error(dim('[auth] Token via az geholt, ~50 Min. gecached.'));
    return t;
  }

  const err = (m.stderr || '').trim();
  if (/az login|please run|no subscription|aadsts/i.test(err)) {
    throw new Error(
      'Keine aktive Azure-CLI-Sitzung.\n' +
        '  Bitte einmal ausfuehren:  az login\n' +
        '  (bei mehreren Tenants:    az login --tenant <DEINE-TENANT-ID>)\n' +
        '  Danach dieses Skript erneut starten.\n' +
        dim('  az meldete: ' + err.split('\n')[0]),
    );
  }
  throw new Error('`az account get-access-token` ist fehlgeschlagen:\n  ' + (err || 'unbekannter Fehler'));
}

/* --------------------------------- REST ----------------------------------- */

/**
 * Call the Azure DevOps REST API. Throws Errors that say what to do, not just what broke.
 * @param {string} method  GET | POST | PATCH
 * @param {string} url     absolute https URL
 */
export async function adoFetch(method, url, { token, body, contentType = 'application/json' } = {}) {
  const headers = { Authorization: 'Bearer ' + token, Accept: 'application/json' };
  const init = { method, headers };
  if (body != null) {
    headers['Content-Type'] = contentType;
    init.body = typeof body === 'string' ? body : JSON.stringify(body);
  }

  let res;
  try {
    res = await fetch(url, init);
  } catch (e) {
    throw new Error(
      'Netzwerkfehler beim Aufruf von ' + url + '\n  ' + e.message + '\n' +
        '  Hinter einem Unternehmens-Proxy: HTTPS_PROXY setzen (z. B. $env:HTTPS_PROXY="http://proxy:8080").',
    );
  }

  const text = await res.text();

  if (res.status === 203) {
    throw new Error(
      'HTTP 203 Non-Authoritative Information — Azure DevOps hat eine Anmeldeseite statt JSON geliefert.\n' +
        '  Ursache in fast allen Faellen: falsche Resource-ID beim Token.\n' +
        '  Richtig ist --resource ' + ADO_RESOURCE_ID + '\n' +
        '  Token-Cache leeren und neu holen: Datei ' + TOKEN_CACHE + ' loeschen.',
    );
  }
  if (res.status === 401) {
    throw new Error(
      'HTTP 401 Unauthorized — Token abgelehnt.\n' +
        '  1) `az login` erneut ausfuehren (Token abgelaufen oder falscher Tenant).\n' +
        '  2) Cache loeschen: ' + TOKEN_CACHE,
    );
  }
  if (res.status === 403) {
    throw new Error(
      'HTTP 403 Forbidden — angemeldet, aber keine Berechtigung fuer diese Aktion.\n' +
        '  Pruefe, ob dein Konto im Projekt schreiben darf (Contributor).',
    );
  }
  if (res.status === 404) {
    throw new Error(
      'HTTP 404 Not Found — Organisation, Projekt oder Work Item existiert nicht (oder du siehst es nicht).\n' +
        '  URL war: ' + url + '\n' +
        '  Pruefe ADO_ORG und ADO_PROJECT. Beide sind die Namen aus der Browser-URL:\n' +
        '  https://dev.azure.com/<ADO_ORG>/<ADO_PROJECT>',
    );
  }
  if (!res.ok) {
    let detail = text;
    try {
      const j = JSON.parse(text);
      if (j.message) detail = j.message;
    } catch {
      /* keep raw text */
    }
    throw new Error('HTTP ' + res.status + ' bei ' + method + ' ' + url + '\n  ' + detail.slice(0, 800));
  }

  return text.trim() ? JSON.parse(text) : {};
}

/** Base URL for project-scoped API calls. */
export function projectBase(org, project) {
  return 'https://dev.azure.com/' + encodeURIComponent(org) + '/' + encodeURIComponent(project) + '/_apis';
}

/* --------------------------------- CLI ------------------------------------ */

const HELP = `
ado-auth.mjs — Token holen und Verbindung pruefen (ohne PAT)

  node ado-auth.mjs            Selbsttest: az vorhanden? Token? Projekt erreichbar?
  node ado-auth.mjs --help     diese Hilfe
  node ado-auth.mjs --clear    gecachten Token loeschen

Umgebungsvariablen:
  ADO_ORG       Name der Organisation aus https://dev.azure.com/<ORG>/<PROJEKT>
  ADO_PROJECT   Name des Projekts (nur fuer den Verbindungstest noetig)
  ADO_BEARER    optional: fertiges Entra-Token; ueberspringt az komplett

Als Modul:
  import { getToken, adoFetch, projectBase } from './ado-auth.mjs';
`;

async function selftest() {
  let ok = true;
  const line = (good, label, extra) =>
    console.log((good ? green('  OK   ') : red('  FEHL ')) + label + (extra ? '\n         ' + dim(extra) : ''));

  console.log('\nAzure-DevOps-Selbsttest\n');

  const nodeMajor = Number(process.versions.node.split('.')[0]);
  line(nodeMajor >= 18, 'Node ' + process.versions.node + (nodeMajor >= 18 ? '' : ' — Node 18+ noetig (fetch fehlt)'));
  if (nodeMajor < 18) ok = false;

  const ver = runAz(['version'], 60000);
  if (ver.missing || ver.code !== 0) {
    line(false, 'Azure CLI gefunden', 'az ist nicht im PATH. https://learn.microsoft.com/cli/azure/install-azure-cli');
    ok = false;
  } else {
    line(true, 'Azure CLI gefunden');
  }

  let token = null;
  try {
    token = getToken({ quiet: true });
    line(true, 'Bearer-Token erhalten', 'Laenge ' + token.length + ' Zeichen, Resource ' + ADO_RESOURCE_ID);
  } catch (e) {
    line(false, 'Bearer-Token erhalten', e.message.replace(/\n/g, '\n         '));
    ok = false;
  }

  const org = (process.env.ADO_ORG || '').trim();
  const project = (process.env.ADO_PROJECT || '').trim();
  if (!token) {
    line(false, 'Verbindung zum Projekt', 'uebersprungen — kein Token');
  } else if (!org || !project) {
    console.log(dim('  --   Verbindung zum Projekt uebersprungen (ADO_ORG / ADO_PROJECT nicht gesetzt)'));
  } else {
    try {
      const r = await adoFetch(
        'GET',
        'https://dev.azure.com/' + encodeURIComponent(org) + '/_apis/projects/' + encodeURIComponent(project) + '?api-version=' + API_VERSION,
        { token },
      );
      line(true, 'Verbindung zum Projekt', 'Projekt "' + (r.name || project) + '" erreichbar, id ' + (r.id || '?'));
    } catch (e) {
      line(false, 'Verbindung zum Projekt', e.message.replace(/\n/g, '\n         '));
      ok = false;
    }
  }

  console.log('');
  if (ok) console.log(green('Alles gruen. Du kannst ado-query.mjs / ado-create.mjs benutzen.\n'));
  else console.log(red('Nicht bereit. Behebe die FEHL-Zeilen oben und starte erneut.\n'));
  process.exit(ok ? 0 : 1);
}

const isMain = process.argv[1] && process.argv[1].replace(/\\/g, '/').endsWith('ado-auth.mjs');
if (isMain) {
  const a = parseArgs(process.argv.slice(2), { booleans: ['help', 'h', 'clear'] });
  if (a.help || a.h) {
    console.log(HELP.trim());
    process.exit(0);
  }
  if (a.clear) {
    try {
      if (existsSync(TOKEN_CACHE)) {
        writeFileSync(TOKEN_CACHE, '{}', 'utf8');
        console.log('Token-Cache geleert: ' + TOKEN_CACHE);
      } else {
        console.log('Kein Token-Cache vorhanden.');
      }
    } catch (e) {
      fail('Cache konnte nicht geleert werden: ' + e.message);
    }
    process.exit(0);
  }
  selftest().catch((e) => {
    console.error(red('Selbsttest abgebrochen: ') + e.message);
    process.exit(1);
  });
}
