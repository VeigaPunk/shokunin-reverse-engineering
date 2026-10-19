import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";

const directory = new URL("./", import.meta.url);
const names = ["base-1", "base-2", "copy-a", "copy-b"];
const envelopes = Object.fromEntries(names.map((name) => [
  name,
  JSON.parse(readFileSync(new URL(`${name}.json`, directory), "utf8")).data,
]));

function projection(evidence) {
  return {
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
  };
}

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value !== null && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

function derive(evidence) {
  return `ev_${createHash("sha256").update(canonical(projection(evidence)), "utf8").digest("hex")}`;
}

function differencePaths(left, right, prefix = "$") {
  if (left === right) return [];
  if (left === null || right === null || typeof left !== "object" || typeof right !== "object") return [prefix];
  const keys = [...new Set([...Object.keys(left), ...Object.keys(right)])].sort();
  return keys.flatMap((key) => differencePaths(left[key], right[key], Array.isArray(left) ? `${prefix}[${key}]` : `${prefix}.${key}`));
}

const records = Object.fromEntries(names.map((name) => [name, {
  reported: envelopes[name].evidence_id,
  recomputed: derive(envelopes[name]),
  matches: envelopes[name].evidence_id === derive(envelopes[name]),
  path: envelopes[name].parameters.path,
  subjectDigest: envelopes[name].subject.digest.sha256,
}]));
const displayMutation = structuredClone(envelopes["base-1"]);
displayMutation.subject.name = "changed-display-name";
displayMutation.subject.local_path = "/different/display/path/docker";
const semanticCopyA = structuredClone(envelopes["base-1"]);
const semanticCopyB = structuredClone(envelopes["base-1"]);
for (const [evidence, path] of [
  [semanticCopyA, envelopes["copy-a"].parameters.path],
  [semanticCopyB, envelopes["copy-b"].parameters.path],
]) {
  evidence.parameters.path = path;
  evidence.normalized_result.artifact.path = path;
  evidence.locations[0].path = path;
}

console.log(JSON.stringify({
  records,
  baseCallsDataEqual: canonical(envelopes["base-1"]) === canonical(envelopes["base-2"]),
  baseToCopyAProjectionDiffPaths: differencePaths(projection(envelopes["base-1"]), projection(envelopes["copy-a"])),
  baseToCopyBProjectionDiffPaths: differencePaths(projection(envelopes["base-1"]), projection(envelopes["copy-b"])),
  displayOnlyMutation: {
    recomputed: derive(displayMutation),
    unchangedFromBase: derive(displayMutation) === envelopes["base-1"].evidence_id,
  },
  pathFieldsOnly: {
    copyARecomputed: derive(semanticCopyA),
    matchesCopyA: derive(semanticCopyA) === envelopes["copy-a"].evidence_id,
    copyBRecomputed: derive(semanticCopyB),
    matchesCopyB: derive(semanticCopyB) === envelopes["copy-b"].evidence_id,
  },
}, null, 2));
