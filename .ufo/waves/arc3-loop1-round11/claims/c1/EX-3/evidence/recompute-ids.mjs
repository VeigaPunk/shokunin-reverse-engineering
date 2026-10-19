import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";

const evidenceDir = new URL("./", import.meta.url);
const names = ["docker-base-1.json", "docker-base-2.json", "docker-copy.json"];
const records = await Promise.all(names.map(async (name) => {
  const envelope = JSON.parse(await readFile(new URL(name, evidenceDir), "utf8"));
  if (!envelope.ok) throw new Error(`${name}: CLI result is not ok`);
  return envelope.data;
}));

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

const canonical = (value) => {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value !== null && typeof value === "object") {
    return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
};
const deriveId = (evidence) => `ev_${createHash("sha256").update(canonical(projection(evidence)), "utf8").digest("hex")}`;

const diffPaths = (left, right, prefix = "") => {
  if (left === right) return [];
  if (left === null || right === null || typeof left !== "object" || typeof right !== "object") return [prefix || "$"];
  if (Array.isArray(left) !== Array.isArray(right)) return [prefix || "$"];
  const keys = [...new Set([...Object.keys(left), ...Object.keys(right)])].sort();
  return keys.flatMap((key) => diffPaths(left[key], right[key], prefix ? `${prefix}.${key}` : key));
};

const [base1, base2, copy] = records;
const baseProjection = projection(base1);
const copyProjection = projection(copy);
const differingProjectionPaths = diffPaths(baseProjection, copyProjection);
const copyWithBasePaths = structuredClone(copy);
copyWithBasePaths.parameters.path = base1.parameters.path;
copyWithBasePaths.normalized_result.artifact.path = base1.normalized_result.artifact.path;
copyWithBasePaths.locations[0].path = base1.locations[0].path;
const displayOnlyMutation = structuredClone(base1);
displayOnlyMutation.subject.name = "different-display-name";
displayOnlyMutation.subject.local_path = "/different/display/path";

const results = {
  reported_ids: records.map((record) => record.evidence_id),
  recomputed_ids: records.map(deriveId),
  same_path_repeat_matches: base1.evidence_id === base2.evidence_id,
  all_recomputed_ids_match: records.every((record) => deriveId(record) === record.evidence_id),
  copied_artifact_digest_matches: base1.subject.digest.sha256 === copy.subject.digest.sha256,
  copied_path_changes_id: base1.evidence_id !== copy.evidence_id,
  differing_semantic_projection_paths: differingProjectionPaths,
  copy_after_replacing_semantic_path_fields_id: deriveId(copyWithBasePaths),
  copy_after_path_replacement_matches_base: deriveId(copyWithBasePaths) === base1.evidence_id,
  display_subject_only_mutation_id: deriveId(displayOnlyMutation),
  display_subject_only_mutation_matches_base: deriveId(displayOnlyMutation) === base1.evidence_id,
};
console.log(JSON.stringify(results, null, 2));
if (!results.same_path_repeat_matches || !results.all_recomputed_ids_match || !results.copied_artifact_digest_matches || !results.copied_path_changes_id || !results.copy_after_path_replacement_matches_base || !results.display_subject_only_mutation_matches_base) process.exitCode = 1;
