import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { join } from "node:path";
import { fileURLToPath } from "node:url";

const evidenceDirectory = process.argv[2] ?? fileURLToPath(new URL(".", import.meta.url));
const load = (name) => JSON.parse(readFileSync(join(evidenceDirectory, `go-${name}.json`), "utf8")).data;
const records = Object.fromEntries(["base1", "base2", "copyA", "copyB"].map((name) => [name, load(name)]));

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
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
}

function id(evidence) {
  const digest = createHash("sha256").update(canonical(projection(evidence)), "utf8").digest("hex");
  return `ev_${digest}`;
}

function substitutePath(evidence, path) {
  const copy = structuredClone(evidence);
  copy.parameters.path = path;
  copy.normalized_result.artifact.path = path;
  const location = copy.locations.find((item) => item.kind === "artifact-path");
  if (!location) throw new Error("artifact-path location missing");
  location.path = path;
  return copy;
}

const base = records.base1;
const displayOnly = structuredClone(base);
displayOnly.subject.name = "display-only-change";
displayOnly.subject.local_path = "/display-only/path/docker";
const projectedPathFields = [
  ["parameters.path", base.parameters.path],
  ["normalized_result.artifact.path", base.normalized_result.artifact.path],
  ["locations[0].path", base.locations[0].path],
];
const output = {
  formula: "ev_ + SHA-256 of compact canonical JSON for evidence.js semanticProjection(data)",
  records: Object.fromEntries(Object.entries(records).map(([name, evidence]) => [name, {
    evidence_id: evidence.evidence_id,
    recomputed_id: id(evidence),
    matches: id(evidence) === evidence.evidence_id,
  }])),
  same_path_repeat: {
    path: records.base1.parameters.path,
    ids_equal: records.base1.evidence_id === records.base2.evidence_id,
    semantic_projection_equal: canonical(projection(records.base1)) === canonical(projection(records.base2)),
  },
  byte_identity: {
    sha256: base.subject.digest.sha256,
    bytes: base.normalized_result.artifact.bytes,
    all_three_inputs_match: [records.base1, records.copyA, records.copyB].every((record) =>
      record.subject.digest.sha256 === base.subject.digest.sha256 &&
      record.normalized_result.artifact.sha256 === base.normalized_result.artifact.sha256 &&
      record.normalized_result.artifact.bytes === base.normalized_result.artifact.bytes),
  },
  display_only_subject_mutation: {
    recomputed_id: id(displayOnly),
    equals_base_id: id(displayOnly) === base.evidence_id,
  },
  substituted_semantic_path_fields: Object.fromEntries(["copyA", "copyB"].map((name) => {
    const recomputed_id = id(substitutePath(base, records[name].parameters.path));
    return [name, { path: records[name].parameters.path, recomputed_id, reported_id: records[name].evidence_id, matches: recomputed_id === records[name].evidence_id }];
  })),
  path_fields_in_projection: projectedPathFields,
};

const passed =
  Object.values(output.records).every(({ matches }) => matches) &&
  output.same_path_repeat.ids_equal &&
  output.same_path_repeat.semantic_projection_equal &&
  output.byte_identity.all_three_inputs_match &&
  output.display_only_subject_mutation.equals_base_id &&
  Object.values(output.substituted_semantic_path_fields).every(({ matches }) => matches);
output.verification = passed ? "PASS" : "FAIL";
console.log(JSON.stringify(output, null, 2));
if (!passed) process.exitCode = 1;
