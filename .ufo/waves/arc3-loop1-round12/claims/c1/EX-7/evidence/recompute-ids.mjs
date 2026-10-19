import { createHash } from "node:crypto";
import { readFileSync, writeFileSync } from "node:fs";
import { isDeepStrictEqual } from "node:util";
import { digestCanonicalValue } from "/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js";

const paths = process.argv.slice(2);
if (paths.length !== 3) throw new Error("Pass base-1, base-2, and alternate-path Evidence JSON files");
const records = paths.map((path) => JSON.parse(readFileSync(path, "utf8")).data);
const semanticProjection = (evidence) => ({
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
const projections = records.map(semanticProjection);
const ids = projections.map((projection) => `ev_${digestCanonicalValue(projection, "Evidence")}`);
const pathFields = [];
const visit = (value, at) => {
  if (Array.isArray(value)) return value.forEach((child, index) => visit(child, `${at}[${index}]`));
  if (value && typeof value === "object") {
    for (const [key, child] of Object.entries(value)) {
      if (/path|filename/i.test(key)) pathFields.push(`${at}.${key}`);
      visit(child, `${at}.${key}`);
    }
  }
};
projections.forEach((projection, index) => visit(projection, `projection[${index}]`));
const displayOnlyMutation = {
  ...records[2],
  subject: { ...records[2].subject, name: "mutated-display-name", local_path: "/var/tmp/display-only-change" },
};
const displayOnlyId = `ev_${digestCanonicalValue(semanticProjection(displayOnlyMutation), "Evidence")}`;
const projectionBytes = projections.map((projection) => JSON.stringify(projection));
const projectionSha256 = projectionBytes.map((bytes) => createHash("sha256").update(bytes).digest("hex"));
for (let index = 0; index < records.length; index += 1) {
  if (ids[index] !== records[index].evidence_id) throw new Error(`ID mismatch for ${paths[index]}`);
}
if (!isDeepStrictEqual(projections[0], projections[1]) || !isDeepStrictEqual(projections[0], projections[2])) {
  throw new Error("The three semantic projections differ");
}
if (displayOnlyId !== records[2].evidence_id) throw new Error("Display-only subject mutation changed the ID");
console.log(JSON.stringify({
  operation: records.map((record) => record.operation),
  evidence_ids: ids,
  returned_ids_match_recomputed: ids.map((id, index) => id === records[index].evidence_id),
  subject_paths: records.map((record) => record.subject.local_path),
  subject_sha256: records.map((record) => record.subject.digest.sha256),
  exact_semantic_projection_equal: [isDeepStrictEqual(projections[0], projections[1]), isDeepStrictEqual(projections[0], projections[2])],
  projection_sha256_of_json_serialization: projectionSha256,
  projection_path_or_filename_fields: [...new Set(pathFields)],
  display_name_and_path_mutation_id: displayOnlyId,
  original_alternate_path_id: records[2].evidence_id,
}, null, 2));
