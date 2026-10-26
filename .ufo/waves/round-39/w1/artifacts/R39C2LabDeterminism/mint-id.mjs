#!/usr/bin/env node
// R39-C2 lab instrument: recompute (and optionally rewrite) a REA 6.5.0 evidence id
// using the pin's OWN digestCanonicalValue + semanticProjection statement.
// Usage: node mint-id.mjs --pkg <rea-agents root> [--write] ENVELOPE.json [...]
// Input envelope may be {data: <record>} or a bare record. Prints one TSV line per file:
//   <path>\t<stored-or-dash>\t<computed>
import { readFile, writeFile } from "node:fs/promises";
import { pathToFileURL } from "node:url";
import { join } from "node:path";

const argv = process.argv.slice(2);
const pkgIndex = argv.indexOf("--pkg");
if (pkgIndex < 0) { console.error("--pkg required"); process.exit(2); }
const pkg = argv[pkgIndex + 1];
const write = argv.includes("--write");
const files = argv.filter((a, i) => !a.startsWith("--") && i !== pkgIndex + 1);

const digestMod = await import(pathToFileURL(join(pkg, "dist/domain/canonicalDigest.js")).href);
const evidenceSource = await readFile(join(pkg, "dist/domain/evidence.js"), "utf8");
const marker = "semanticProjection";
const start = evidenceSource.indexOf("const " + marker);
let i = evidenceSource.indexOf("{", start), depth = 0, end = -1;
for (; i < evidenceSource.length; i++) {
    const c = evidenceSource[i];
    if (c === "{" || c === "(" || c === "[") depth++;
    else if (c === "}" || c === ")" || c === "]") { depth--; if (depth === 0 && c === "}") { end = evidenceSource.indexOf(";", i); break; } }
}
if (start < 0 || end < 0) { console.error("projection statement not found"); process.exit(2); }
const semanticProjection = new Function(`${evidenceSource.slice(start, end + 1)}\nreturn semanticProjection;`)();

const compute = (record) => `ev_${digestMod.digestCanonicalValue(semanticProjection(record), "Evidence")}`;

for (const path of files) {
    const parsed = JSON.parse(await readFile(path, "utf8"));
    const wrapped = parsed && parsed.data && typeof parsed.data === "object" ? parsed : null;
    const record = wrapped ? wrapped.data : parsed;
    const stored = typeof record.evidence_id === "string" ? record.evidence_id : "-";
    const id = compute(record);
    if (write) {
        record.evidence_id = id;
        await writeFile(path, JSON.stringify(wrapped ? { ...wrapped, data: record } : record, null, 1) + "\n");
    }
    process.stdout.write(`${path}\t${stored}\t${id}\n`);
}
