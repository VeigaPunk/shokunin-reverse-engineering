import { readFile } from "node:fs/promises";
import { join } from "node:path";
import { digestCanonicalValue } from "file:///home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js";

const root = process.cwd();
const packageRoot = "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents";
const packageInfo = JSON.parse(await readFile(join(packageRoot, "package.json"), "utf8"));
const projection = evidence => ({
  subject: evidence.subject === null ? null : {
    digest: evidence.subject.digest,
    format: evidence.subject.format,
    architecture: evidence.subject.architecture,
  },
  provider: evidence.provider,
  analysis_profile: evidence.analysis_profile,
  predicate_type: evidence.predicate_type,
  operation: evidence.operation,
  parameters: evidence.parameters,
  raw_result: evidence.raw_result,
  normalized_result: evidence.normalized_result,
  confidence: evidence.confidence,
  authority: evidence.authority,
  environment: evidence.environment,
  limitations: evidence.limitations,
  relationship_coverage: evidence.relationship_coverage,
  locations: evidence.locations,
  evidence_links: evidence.evidence_links,
});
const id = evidence => `ev_${digestCanonicalValue(projection(evidence), "Evidence")}`;
const load = async (path, wrapped = false) => {
  const parsed = JSON.parse(await readFile(join(root, path), "utf8"));
  return wrapped ? parsed.data : parsed;
};
const r7 = {};
for (const name of ["67-base1", "67-base2", "67-copyA", "67-copyB"]) {
  r7[name] = await load(`.ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/probes/${name}.json`);
}
const r10 = {};
for (const name of ["base1", "base2", "copyA", "copyB"]) {
  r10[name] = await load(`.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence/probe-${name}.json`, true);
}
const r11 = {};
for (const [name, file] of [
  ["base-1", "base-1"],
  ["base-2", "base-2"],
  ["copy", "copy"],
  ["same-name", "same-name-other-path"],
]) {
  r11[name] = await load(`.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence/inspect-artifact-${file}.json`, true);
}

console.log(`algorithm=rea-agents@${packageInfo.version}/dist/domain/canonicalDigest.js; scope=stored full envelopes; no new REA invocation`);
for (const [group, records] of [["evm", r7], ["rust", r10], ["artifact", r11]]) {
  for (const [name, evidence] of Object.entries(records)) {
    console.log(`${group}/${name}: ${id(evidence) === evidence.evidence_id ? "MATCH" : "MISMATCH"} ${evidence.evidence_id}`);
  }
}
for (const [label, records, base, repeat, copy] of [
  ["evm", r7, "67-base1", "67-base2", "67-copyA"],
  ["rust", r10, "base1", "base2", "copyA"],
]) {
  const original = records[base];
  const repeated = records[repeat];
  const copied = records[copy];
  const pathOnly = structuredClone(original);
  pathOnly.parameters.path = copied.parameters.path;
  pathOnly.normalized_result.artifact.path = copied.parameters.path;
  pathOnly.locations[0].path = copied.parameters.path;
  const displayOnly = structuredClone(original);
  displayOnly.subject.name = "changed";
  displayOnly.subject.local_path = "/display-only";
  console.log(`${label}/controls: repeat_id_equal=${original.evidence_id === repeated.evidence_id} same_bytes=${original.subject.digest.sha256 === copied.subject.digest.sha256} path_fields_only_matches_copy=${id(pathOnly) === copied.evidence_id} display_only_id_unchanged=${id(displayOnly) === original.evidence_id}`);
}
const artifact = r11["base-1"];
const alternate = r11["same-name"];
const artifactDisplayOnly = structuredClone(artifact);
artifactDisplayOnly.subject.name = "changed";
artifactDisplayOnly.subject.local_path = "/display-only";
const nestedPathOnly = structuredClone(artifact);
nestedPathOnly.normalized_result.substeps[0].evidence.subject.local_path = "/isolated/nested/path/jq";
console.log(`artifact/controls: repeat_id_equal=${artifact.evidence_id === r11["base-2"].evidence_id} same_name_same_bytes=${artifact.subject.name === alternate.subject.name && artifact.subject.digest.sha256 === alternate.subject.digest.sha256} different_path_outer_id=${artifact.evidence_id !== alternate.evidence_id} display_only_id_unchanged=${id(artifactDisplayOnly) === artifact.evidence_id} nested_path_only_id_changes=${id(nestedPathOnly) !== artifact.evidence_id} nested_inventory_ids_equal=${artifact.normalized_result.substeps[0].evidence_id === alternate.normalized_result.substeps[0].evidence_id}`);
