import { createHash } from "node:crypto";
import { readFileSync } from "node:fs";

const directory = new URL("./", import.meta.url);
const load = (name) => JSON.parse(readFileSync(new URL(name, directory), "utf8")).data;
const base1 = load("probe-base1.json");
const base2 = load("probe-base2.json");
const copy = load("probe-copy.json");

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
  if (value === null || typeof value !== "object") return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(",")}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(",")}}`;
};
const compute = (evidence) => `ev_${createHash("sha256").update(canonical(projection(evidence)), "utf8").digest("hex")}`;
const reported = (evidence) => evidence.evidence_id;
const result = (evidence) => ({ reported: reported(evidence), recomputed: compute(evidence), match: reported(evidence) === compute(evidence) });

const displayOnly = structuredClone(base1);
displayOnly.subject.name = copy.subject.name;
displayOnly.subject.local_path = copy.subject.local_path;

const semanticPathsOnly = structuredClone(base1);
semanticPathsOnly.parameters.path = copy.parameters.path;
semanticPathsOnly.normalized_result.artifact.path = copy.normalized_result.artifact.path;
semanticPathsOnly.locations[0].path = copy.locations[0].path;

const output = {
  operation: base1.operation,
  observed: { base1: result(base1), base2: result(base2), copy: result(copy) },
  same_path_semantic_projection_equal: JSON.stringify(projection(base1)) === JSON.stringify(projection(base2)),
  controls: {
    display_subject_fields_only: { recomputed: compute(displayOnly), matches_base1: compute(displayOnly) === reported(base1) },
    semantic_path_fields_substituted: { recomputed: compute(semanticPathsOnly), matches_copy: compute(semanticPathsOnly) === reported(copy) },
  },
};
console.log(JSON.stringify(output, null, 2));
if (Object.values(output.observed).some((entry) => !entry.match) ||
    !output.same_path_semantic_projection_equal ||
    !output.controls.display_subject_fields_only.matches_base1 ||
    !output.controls.semantic_path_fields_substituted.matches_copy) {
  process.exitCode = 1;
}
