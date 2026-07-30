#!/usr/bin/env node
// validate.mjs - checks a generated testfaelle.json against testfaelle.schema.json.
// Node 18+, zero dependencies.
//
//   node validate.mjs                                  # defaults to beispiel-ausgabe/testfaelle.json
//   node validate.mjs pfad/zu/testfaelle.json
//
// Exit code 0 = valid, 1 = invalid or unreadable.

import { readFileSync } from "node:fs";
import { dirname, resolve } from "node:path";
import { fileURLToPath } from "node:url";

const here = dirname(fileURLToPath(import.meta.url));
const schemaPath = resolve(here, "testfaelle.schema.json");
const dataPath = resolve(
  process.cwd(),
  process.argv[2] ?? resolve(here, "beispiel-ausgabe/testfaelle.json"),
);

// Supported keyword subset: type, required, properties, items, enum,
// minItems, minLength, pattern. Enough for this contract, small enough to read.
function validate(value, schema, path, errors) {
  const kind = Array.isArray(value) ? "array" : value === null ? "null" : typeof value;

  if (schema.type && kind !== schema.type) {
    errors.push(`${path}: erwartet ${schema.type}, gefunden ${kind}`);
    return;
  }

  if (schema.enum && !schema.enum.includes(value)) {
    errors.push(`${path}: "${value}" ist kein erlaubter Wert (erlaubt: ${schema.enum.join(", ")})`);
  }

  if (schema.type === "string") {
    if (schema.minLength !== undefined && value.length < schema.minLength) {
      errors.push(`${path}: zu kurz (${value.length} Zeichen, mindestens ${schema.minLength})`);
    }
    if (schema.pattern && !new RegExp(schema.pattern).test(value)) {
      errors.push(`${path}: "${value}" passt nicht auf das Muster ${schema.pattern}`);
    }
  }

  if (schema.type === "array") {
    if (schema.minItems !== undefined && value.length < schema.minItems) {
      errors.push(`${path}: ${value.length} Eintraege, mindestens ${schema.minItems} erforderlich`);
    }
    if (schema.items) {
      value.forEach((item, i) => validate(item, schema.items, `${path}[${i}]`, errors));
    }
  }

  if (schema.type === "object") {
    for (const key of schema.required ?? []) {
      if (!(key in value)) errors.push(`${path}: Pflichtfeld "${key}" fehlt`);
    }
    for (const [key, sub] of Object.entries(schema.properties ?? {})) {
      if (key in value) validate(value[key], sub, `${path}.${key}`, errors);
    }
    const known = Object.keys(schema.properties ?? {});
    for (const key of Object.keys(value)) {
      if (known.length && !known.includes(key)) {
        errors.push(`${path}: unbekanntes Feld "${key}" (Schema kennt: ${known.join(", ")})`);
      }
    }
  }
}

function readJson(path, label) {
  let raw;
  try {
    raw = readFileSync(path, "utf8");
  } catch {
    console.error(`FEHLER: ${label} nicht lesbar: ${path}`);
    process.exit(1);
  }
  try {
    return JSON.parse(raw);
  } catch (err) {
    console.error(`FEHLER: ${label} ist kein gueltiges JSON: ${path}`);
    console.error(`        ${err.message}`);
    process.exit(1);
  }
}

const schema = readJson(schemaPath, "Schema");
const data = readJson(dataPath, "Testfaelle");

const errors = [];
validate(data, schema, "testfaelle.json", errors);

// Contract rules the JSON Schema subset cannot express.
if (Array.isArray(data.testfaelle)) {
  const seen = new Map();
  for (const [i, tc] of data.testfaelle.entries()) {
    if (typeof tc?.id !== "string") continue;
    if (seen.has(tc.id)) {
      errors.push(`testfaelle.json.testfaelle[${i}].id: "${tc.id}" doppelt (schon in [${seen.get(tc.id)}])`);
    }
    seen.set(tc.id, i);
  }
  const typen = new Set(data.testfaelle.map((tc) => tc?.typ));
  for (const pflicht of ["happy-path", "fehlerfall"]) {
    if (!typen.has(pflicht)) errors.push(`testfaelle.json.testfaelle: kein Testfall vom Typ "${pflicht}"`);
  }
}

if (errors.length === 0) {
  const n = data.testfaelle.length;
  const typen = data.testfaelle.reduce((acc, tc) => ({ ...acc, [tc.typ]: (acc[tc.typ] ?? 0) + 1 }), {});
  console.log(`OK: ${n} Testfaelle gueltig (${dataPath})`);
  console.log(`    Verteilung: ${Object.entries(typen).map(([k, v]) => `${k} ${v}`).join(" | ")}`);
  console.log(`    Jetzt pruefst du nur noch den Inhalt, nicht das Format.`);
  process.exit(0);
}

console.error(`FEHLER: ${errors.length} Verstoss/Verstoesse gegen testfaelle.schema.json\n`);
for (const e of errors) console.error(`  - ${e}`);
console.error(`\nGib diese Liste zurueck in den Copilot-Chat. Der Agent korrigiert und du pruefst erneut.`);
process.exit(1);
