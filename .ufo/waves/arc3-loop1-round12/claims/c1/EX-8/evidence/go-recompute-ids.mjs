import { createHash } from "node:crypto";
import { readFile } from "node:fs/promises";
import { dirname, join, basename } from "node:path";
import { fileURLToPath } from "node:url";

const root = dirname(fileURLToPath(import.meta.url));
const inputs = ["probe-go-base.json", "probe-go-repeat.json", "probe-go-copyA.json"];
const fields = [
  "provider",
  "analysis_profile",
  "predicate_type",
  "operation",
  "parameters",
  "raw_result",
  "normalized_result",
  "confidence",
  "authority",
  "environment",
  "limitations",
  "relationship_coverage",
  "locations",
  "evidence_links",
];

function projection(evidence) {
  return {
    subject: evidence.subject === null ? null : {
      digest: evidence.subject.digest,
      format: evidence.subject.format,
      architecture: evidence.subject.architecture,
    },
    ...Object.fromEntries(fields.map((field) => [field, evidence[field]])),
  };
}

function canonical(value) {
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
}

function evidenceId(evidence) {
  return `ev_${createHash("sha256").update(canonical(projection(evidence)), "utf8").digest("hex")}`;
}

function differences(left, right, at = "$") {
  if (left === right) return [];
  if (left === null || right === null || typeof left !== "object" || typeof right !== "object") {
    return [{ path: at, left, right }];
  }
  if (Array.isArray(left) || Array.isArray(right)) {
    if (!Array.isArray(left) || !Array.isArray(right) || left.length !== right.length) {
      return [{ path: at, left, right }];
    }
    return left.flatMap((value, index) => differences(value, right[index], `${at}[${index}]`));
  }
  const keys = [...new Set([...Object.keys(left), ...Object.keys(right)])].sort();
  return keys.flatMap((key) => differences(left[key], right[key], `${at}.${key}`));
}

const records = [];
for (const file of inputs) {
  const wrapper = JSON.parse(await readFile(join(root, file), "utf8"));
  if (wrapper.ok !== true || typeof wrapper.data?.evidence_id !== "string") {
    throw new Error(`${file}: not a successful Evidence envelope`);
  }
  const evidence = wrapper.data;
  const recomputed = evidenceId(evidence);
  records.push({ file, evidence, projection: projection(evidence), recomputed });
  console.log(`${basename(file)} observed=${evidence.evidence_id} recomputed=${recomputed} match=${evidence.evidence_id === recomputed} subject_path=${evidence.subject.local_path}`);
  console.log(`${basename(file)} target_sha256=${evidence.subject.digest.sha256} artifact_bytes=${evidence.normalized_result.artifact.bytes} go_version=${evidence.normalized_result.build_info?.go_version ?? null}`);
}

const base = records[0];
const repeat = records[1];
const copy = records[2];
const path = copy.evidence.subject.local_path;
const delta = differences(base.projection, copy.projection);
console.log(`same_path_repeat_id=${base.evidence.evidence_id === repeat.evidence.evidence_id}`);
console.log(`copy_projection_differences=${JSON.stringify(delta)}`);
const pathOnly = structuredClone(base.projection);
pathOnly.parameters.path = path;
pathOnly.normalized_result.artifact.path = path;
pathOnly.locations[0].path = path;
console.log(`three_path_fields_alone_reproduce_copy=${canonical(pathOnly) === canonical(copy.projection)}`);
const displayMutation = structuredClone(base.evidence);
displayMutation.subject.name = "alternate-display-name";
displayMutation.subject.local_path = path;
console.log(`display_subject_path_or_name_alone_changes_id=${evidenceId(displayMutation) !== base.evidence.evidence_id}`);
