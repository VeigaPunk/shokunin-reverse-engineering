import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const labels = ["base1", "base2", "copyA", "copyB"];
const records = {};
const sorted = (value) => Array.isArray(value)
  ? value.map(sorted)
  : value !== null && typeof value === "object"
    ? Object.fromEntries(Object.keys(value).sort().map((key) => [key, sorted(value[key])]))
    : value;
const projection = (evidence) => ({
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
const id = (evidence) => `ev_${createHash("sha256").update(JSON.stringify(sorted(projection(evidence))), "utf8").digest("hex")}`;
for (const label of labels) {
  const envelope = JSON.parse(await readFile(join(root, `probe-${label}.json`), "utf8"));
  const evidence = envelope.data;
  const recomputed = id(evidence);
  records[label] = {
    path: evidence.parameters.path,
    artifact_sha256: evidence.normalized_result.artifact.sha256,
    reported: evidence.evidence_id,
    recomputed,
    match: evidence.evidence_id === recomputed,
  };
}
const base = JSON.parse(await readFile(join(root, "probe-base1.json"), "utf8")).data;
const copyA = JSON.parse(await readFile(join(root, "probe-copyA.json"), "utf8")).data;
const displayMutation = structuredClone(base);
displayMutation.subject.name = "mutated-display-name";
displayMutation.subject.local_path = "/mutated/display/path";
const pathMutation = structuredClone(base);
pathMutation.parameters.path = copyA.parameters.path;
pathMutation.normalized_result.artifact.path = copyA.parameters.path;
pathMutation.locations[0].path = copyA.parameters.path;
console.log(JSON.stringify({
  records,
  display_fields_mutation: {
    reported: base.evidence_id,
    recomputed: id(displayMutation),
    unchanged: id(displayMutation) === base.evidence_id,
  },
  path_fields_only_mutation: {
    reported_copyA: copyA.evidence_id,
    recomputed_from_base: id(pathMutation),
    matches_copyA: id(pathMutation) === copyA.evidence_id,
  },
}, null, 2));
