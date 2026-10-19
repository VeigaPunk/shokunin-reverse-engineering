// Round-12 integration: retained, re-runnable form of VZ-1's 27/27 reconciliation
// (VZ-1.md:26-30 recorded the result but kept no script). Recomputes every stored
// inspect_go_binary Evidence ID under claims/c1/ with the pinned rea-agents@6.7.0
// package's own digestCanonicalValue over the semanticProjection field list copied
// verbatim from dist/domain/evidence.js:159-181 (that function is not exported).
// Run from the lane root: node .ufo/waves/arc3-loop1-round12/integration/c1/reconcile-all-go-ids.mjs
import { readFileSync, readdirSync, statSync } from "node:fs";
import { join } from "node:path";
import { digestCanonicalValue } from "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js";

const ROOT = ".ufo/waves/arc3-loop1-round12/claims/c1";
const projection = (e) => ({
  subject: e.subject === null ? null : { digest: e.subject.digest, format: e.subject.format, architecture: e.subject.architecture },
  provider: e.provider, analysis_profile: e.analysis_profile, predicate_type: e.predicate_type,
  operation: e.operation, parameters: e.parameters, raw_result: e.raw_result,
  normalized_result: e.normalized_result, confidence: e.confidence, authority: e.authority,
  environment: e.environment, limitations: e.limitations, relationship_coverage: e.relationship_coverage,
  locations: e.locations, evidence_links: e.evidence_links,
});
const walk = (d) => readdirSync(d).flatMap((n) => {
  const p = join(d, n);
  return statSync(p).isDirectory() ? walk(p) : p.endsWith(".json") ? [p] : [];
});
const found = [];
const visit = (v, file) => {
  if (v && typeof v === "object") {
    if (v.operation === "inspect_go_binary" && typeof v.evidence_id === "string") found.push({ file, e: v });
    for (const k of Object.keys(v)) visit(v[k], file);
  }
};
for (const f of walk(ROOT)) {
  try { visit(JSON.parse(readFileSync(f, "utf8")), f); } catch { /* non-JSON-envelope file */ }
}
let ok = 0;
const bundles = new Set();
for (const { file, e } of found) {
  const id = `ev_${digestCanonicalValue(projection(e), "Evidence")}`;
  const match = id === e.evidence_id;
  ok += match;
  bundles.add(file.split("/")[5]);
  console.log(`${match ? "match" : "MISMATCH"} ${e.evidence_id} ${e.parameters?.path} ${file}`);
}
console.log(`records=${found.length} matched=${ok} bundles=${[...bundles].sort().join(",")}`);
process.exit(found.length > 0 && ok === found.length ? 0 : 1);
