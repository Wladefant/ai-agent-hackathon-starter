#!/usr/bin/env node
// build-workitem.mjs - turns a filled workitem JSON into the Azure DevOps JSON-Patch
// document that would create the work item. Node 18+, zero dependencies.
//
//   node build-workitem.mjs                          # defaults to beispiel-ausgabe/workitem.json
//   node build-workitem.mjs pfad/zu/workitem.json
//   node build-workitem.mjs > patch.json             # stdout is pure JSON, notes go to stderr
//
// PRINTS ONLY. This script never opens a network connection and holds no token.

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const dataPath = resolve(
  process.cwd(),
  process.argv[2] ?? resolve(here, "beispiel-ausgabe/workitem.json"),
);

const TYPEN = ["User Story", "Bug", "Task", "Feature"];
const BEKANNT = [
  "typ", "titel", "beschreibung", "akzeptanzkriterien",
  "area", "iteration", "tags", "prioritaet", "story_points", "parent_id",
];

let wi;
try {
  wi = JSON.parse(readFileSync(dataPath, "utf8"));
} catch (err) {
  console.error(`FEHLER: ${dataPath} nicht lesbar oder kein gueltiges JSON.`);
  console.error(`        ${err.message}`);
  process.exit(1);
}

// --- Pruefung ---------------------------------------------------------------
const fehler = [];
const warnungen = [];

if (!TYPEN.includes(wi.typ)) fehler.push(`typ: "${wi.typ}" ist kein erlaubter Typ (${TYPEN.join(", ")})`);
if (!wi.titel?.trim()) fehler.push("titel: fehlt oder leer");
else if (wi.titel.length > 255) fehler.push(`titel: ${wi.titel.length} Zeichen, Azure DevOps erlaubt 255`);
else if (wi.titel.length > 120) warnungen.push(`titel: ${wi.titel.length} Zeichen, kuerzer als 120 liest sich besser`);
if (!wi.beschreibung?.trim()) fehler.push("beschreibung: fehlt oder leer");
if (!Array.isArray(wi.akzeptanzkriterien) || wi.akzeptanzkriterien.length === 0) {
  fehler.push("akzeptanzkriterien: mindestens ein pruefbares Kriterium erforderlich");
}
if (!wi.area?.trim()) fehler.push("area: fehlt");
if (!wi.iteration?.trim()) fehler.push("iteration: fehlt");
if (![1, 2, 3, 4].includes(wi.prioritaet)) fehler.push(`prioritaet: "${wi.prioritaet}" ist keine Zahl von 1 bis 4`);
if (wi.story_points != null && typeof wi.story_points !== "number") {
  fehler.push("story_points: Zahl oder null erwartet");
}
for (const key of Object.keys(wi)) {
  if (!BEKANNT.includes(key) && !key.startsWith("_")) warnungen.push(`unbekanntes Feld "${key}" wird ignoriert`);
}
for (const platzhalter of [wi.area, wi.iteration]) {
  if (typeof platzhalter === "string" && platzhalter.includes("<DEIN")) {
    warnungen.push(`Platzhalter noch drin: "${platzhalter}" - vor dem echten Anlegen ersetzen`);
  }
}

if (fehler.length) {
  console.error(`FEHLER: ${fehler.length} Problem(e) in ${dataPath}\n`);
  for (const f of fehler) console.error(`  - ${f}`);
  console.error(`\nGib diese Liste in den Copilot-Chat zurueck und lass den Agenten nachbessern.`);
  process.exit(1);
}

// --- JSON-Patch bauen -------------------------------------------------------
const esc = (s) => String(s).replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
const html = (text) => text.split(/\n{2,}/).map((p) => `<div>${esc(p.trim()).replace(/\n/g, "<br>")}</div>`).join("");
const liste = (items) => `<ul>${items.map((i) => `<li>${esc(i)}</li>`).join("")}</ul>`;
const add = (feld, value) => ({ op: "add", path: `/fields/${feld}`, value });

const patch = [
  add("System.Title", wi.titel.trim()),
  add("System.Description", html(wi.beschreibung.trim())),
  add("Microsoft.VSTS.Common.AcceptanceCriteria", liste(wi.akzeptanzkriterien)),
  add("System.AreaPath", wi.area),
  add("System.IterationPath", wi.iteration),
  add("Microsoft.VSTS.Common.Priority", wi.prioritaet),
];

if (wi.tags?.length) patch.push(add("System.Tags", wi.tags.join("; ")));
if (wi.story_points != null) patch.push(add("Microsoft.VSTS.Scheduling.StoryPoints", wi.story_points));
if (wi.parent_id != null) {
  patch.push({
    op: "add",
    path: "/relations/-",
    value: {
      rel: "System.LinkTypes.Hierarchy-Reverse",
      url: `https://dev.azure.com/<DEINE-ORG>/_apis/wit/workItems/${wi.parent_id}`,
    },
  });
}

// --- Ausgabe ----------------------------------------------------------------
const url = `https://dev.azure.com/<DEINE-ORG>/<DEIN-PROJEKT>/_apis/wit/workitems/$${encodeURIComponent(wi.typ)}?api-version=7.1`;

console.error(`# Quelle:        ${dataPath}`);
console.error(`# Work-Item-Typ: ${wi.typ}`);
console.error(`# Wuerde gehen an:`);
console.error(`#   POST ${url}`);
console.error(`#   Content-Type: application/json-patch+json`);
for (const w of warnungen) console.error(`# WARNUNG: ${w}`);
console.error(`# NICHTS GESENDET. Dieses Skript druckt nur.`);
console.error(`# Die lauffaehigen API-Skripte liegen unter ../../azure-devops/.`);
console.error("");

console.log(JSON.stringify(patch, null, 2));
