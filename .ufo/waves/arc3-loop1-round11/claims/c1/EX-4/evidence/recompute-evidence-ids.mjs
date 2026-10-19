import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";
import { isDeepStrictEqual } from "node:util";

const directory = dirname(fileURLToPath(import.meta.url));
const read = (name) => JSON.parse(readFileSync(join(directory, name), "utf8"));
const records = [
  read("inspect-artifact-signal-base.json"),
  read("inspect-artifact-signal-repeat.json"),
  read("inspect-artifact-signal-pathcopy.json"),
];

const projection = (evidence) => ({
  subject: evidence.subject === null
    ? null
    : {
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

const canonicalJson = (value) => {
  if (value === null || typeof value !== "object") {
    const encoded = JSON.stringify(value);
    if (encoded === undefined) throw new TypeError("Unsupported JSON value");
    return encoded;
  }
  if (Array.isArray(value)) return `[${value.map(canonicalJson).join(",")}]`;
  return `{${Object.keys(value).sort()
    .filter((key) => value[key] !== undefined)
    .map((key) => `${JSON.stringify(key)}:${canonicalJson(value[key])}`)
    .join(",")}}`;
};

const recompute = (evidence) => `ev_${createHash("sha256")
  .update(canonicalJson(projection(evidence)), "utf8")
  .digest("hex")}`;
const inventoryEvidence = (record) => record.data.normalized_result.substeps[0].evidence;
const recordsValid = records.every((record) => record.ok === true);
if (!recordsValid) throw new Error("A retained REA command result is not successful");

const [base, repeat, copy] = records.map((record) => record.data);
const normalizedProjection = (evidence) => {
  const value = structuredClone(projection(evidence));
  value.normalized_result.substeps[0].evidence.subject.local_path = "<path>";
  value.normalized_result.inspection_id = "<derived-from-nested-path>";
  return value;
};

console.log(JSON.stringify({
  records: records.map((record) => ({
    ok: record.ok,
    operation: record.data.operation,
    evidence_id: record.data.evidence_id,
    recomputed_id: recompute(record.data),
    subject_path: record.data.subject.local_path,
    subject_sha256: record.data.subject.digest.sha256,
    inventory_evidence_id: inventoryEvidence(record).evidence_id,
    inventory_recomputed_id: recompute(inventoryEvidence(record)),
    inventory_subject_path: inventoryEvidence(record).subject.local_path,
    observations: record.data.normalized_result.coverage.observations_retained,
    integrity_contradictions: record.data.normalized_result.contradictions.length,
    coverage: record.data.normalized_result.coverage.status,
  })),
  same_path_repeat: {
    outer_id_equal: base.evidence_id === repeat.evidence_id,
    nested_id_equal: inventoryEvidence(records[0]).evidence_id === inventoryEvidence(records[1]).evidence_id,
    normalized_result_equal: JSON.stringify(base.normalized_result) === JSON.stringify(repeat.normalized_result),
  },
  same_bytes_different_path: {
    root_sha256_equal: base.subject.digest.sha256 === copy.subject.digest.sha256,
    nested_id_equal: inventoryEvidence(records[0]).evidence_id === inventoryEvidence(records[2]).evidence_id,
    outer_id_differs: base.evidence_id !== copy.evidence_id,
    projection_equal_after_nested_path_and_derived_inspection_id_normalization:
      isDeepStrictEqual(normalizedProjection(records[0].data), normalizedProjection(records[2].data)),
  },
}, null, 2));
