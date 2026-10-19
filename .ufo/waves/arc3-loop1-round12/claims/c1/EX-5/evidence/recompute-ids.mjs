import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const names = ["base-1.json", "base-2.json", "copy-same-name.json", "copy-other-name.json"];
const records = new Map(names.map((name) => [name, JSON.parse(readFileSync(new URL(name, import.meta.url)))]));
const data = new Map([...records].map(([name, envelope]) => {
  if (envelope.ok !== true || envelope.data?.operation !== "inspect_go_binary") throw new Error(`Unexpected envelope: ${name}`);
  return [name, envelope.data];
}));

function canonical(value) {
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  if (value !== null && typeof value === "object") {
    return `{${Object.keys(value).sort().filter((key) => value[key] !== undefined && typeof value[key] !== "symbol").map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
  }
  return JSON.stringify(value);
}

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

function computeId(evidence) {
  return `ev_${createHash("sha256").update(canonical(projection(evidence)), "utf8").digest("hex")}`;
}

function changePathFields(source, target) {
  const changed = structuredClone(source);
  changed.parameters.path = target.parameters.path;
  changed.normalized_result.artifact.path = target.normalized_result.artifact.path;
  const from = changed.locations.findIndex((location) => location.kind === "artifact-path");
  const to = target.locations.find((location) => location.kind === "artifact-path");
  changed.locations[from].path = to.path;
  return changed;
}

const base = data.get("base-1.json");
const displayOnly = structuredClone(base);
displayOnly.subject.name = "display-only-name-change";
displayOnly.subject.local_path = "/display-only-path-change";
const summaries = names.map((name) => {
  const evidence = data.get(name);
  const recomputed = computeId(evidence);
  return {
    file: name,
    reported: evidence.evidence_id,
    recomputed,
    matches: evidence.evidence_id === recomputed,
    input_sha256: evidence.subject.digest.sha256,
    subject_path: evidence.subject.local_path,
    path_parameters: evidence.parameters.path,
    artifact_path: evidence.normalized_result.artifact.path,
    artifact_location: evidence.locations.find((location) => location.kind === "artifact-path")?.path,
  };
});

console.log(JSON.stringify({
  records: summaries,
  same_path_repeat_same_id: data.get("base-1.json").evidence_id === data.get("base-2.json").evidence_id,
  display_only_subject_change_preserves_id: computeId(displayOnly) === base.evidence_id,
  path_field_substitution_reproduces_same_name_copy: computeId(changePathFields(base, data.get("copy-same-name.json"))) === data.get("copy-same-name.json").evidence_id,
  path_field_substitution_reproduces_other_name_copy: computeId(changePathFields(base, data.get("copy-other-name.json"))) === data.get("copy-other-name.json").evidence_id,
}, null, 2));
