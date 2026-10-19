import assert from "node:assert/strict";
import { readFileSync } from "node:fs";
import { digestCanonicalValue } from "file:///home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents/dist/domain/canonicalDigest.js";

const evidenceDir = new URL("./", import.meta.url);
const load = (name) => {
  const envelope = JSON.parse(readFileSync(new URL(`${name}.json`, evidenceDir), "utf8"));
  assert.equal(envelope.ok, true, `${name} was not a successful REA call`);
  return envelope.data;
};
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
const derivedId = (evidence) => `ev_${digestCanonicalValue(projection(evidence), "Evidence")}`;
const pathChanges = (left, right, at = "") => {
  if (Array.isArray(left) && Array.isArray(right)) {
    return left.flatMap((value, index) => pathChanges(value, right[index], `${at}[${index}]`));
  }
  if (left && right && typeof left === "object" && typeof right === "object") {
    return [...new Set([...Object.keys(left), ...Object.keys(right)])]
      .flatMap((key) => pathChanges(left[key], right[key], at ? `${at}.${key}` : key));
  }
  const leaf = at.split(/[.[]/).at(-1).replace(/\]$/, "");
  if ((leaf === "path" || leaf === "local_path") && left !== right) {
    return [`${at}: ${JSON.stringify(left)} -> ${JSON.stringify(right)}`];
  }
  return [];
};

const cases = [
  { name: "inspect_evm_interface", base: "evm-base1", repeat: "evm-base2", copy: "evm-copy", field: "parameters.path" },
  { name: "inspect_rust_binary", base: "rust-base1", repeat: "rust-base2", copy: "rust-copy", field: "parameters.path" },
  { name: "inspect_artifact", base: "artifact-base1", repeat: "artifact-base2", copy: "artifact-copy", field: "normalized_result.substeps[0].evidence.subject.local_path" },
];

for (const item of cases) {
  const base = load(item.base);
  const repeat = load(item.repeat);
  const copy = load(item.copy);
  assert.equal(base.operation, item.name);
  assert.equal(repeat.operation, item.name);
  assert.equal(copy.operation, item.name);
  assert.equal(derivedId(base), base.evidence_id, `${item.name} base projection mismatch`);
  assert.equal(derivedId(repeat), repeat.evidence_id, `${item.name} repeat projection mismatch`);
  assert.equal(derivedId(copy), copy.evidence_id, `${item.name} copy projection mismatch`);
  assert.equal(base.subject.digest.sha256, copy.subject.digest.sha256, `${item.name} target bytes changed`);
  assert.equal(base.evidence_id, repeat.evidence_id, `${item.name} same-path repeat changed ID`);
  assert.notEqual(base.evidence_id, copy.evidence_id, `${item.name} same-byte path copy did not change outer ID`);

  const displayOnly = structuredClone(base);
  displayOnly.subject.name = "different-display-name";
  displayOnly.subject.local_path = "/different/display/path";
  assert.equal(derivedId(displayOnly), base.evidence_id, `${item.name} outer display-only mutation changed projected ID`);

  const semanticPathOnly = structuredClone(base);
  if (item.name === "inspect_artifact") {
    semanticPathOnly.normalized_result.substeps[0].evidence.subject.local_path = "/different/nested/path";
  } else {
    semanticPathOnly.parameters.path = "/different/semantic/path";
  }
  assert.notEqual(derivedId(semanticPathOnly), base.evidence_id, `${item.name} semantic path mutation did not affect projected ID`);

  const nested = item.name === "inspect_artifact" ? base.normalized_result.substeps[0].evidence : null;
  let nestedDisplayMutationPreservesId = null;
  if (nested) {
    assert.equal(derivedId(nested), nested.evidence_id, "nested inventory Evidence projection mismatch");
    assert.equal(derivedId(semanticPathOnly.normalized_result.substeps[0].evidence), nested.evidence_id,
      "nested display-path mutation changed inner Evidence ID");
    nestedDisplayMutationPreservesId = true;
  }
  const changed = pathChanges(base, copy);
  console.log(JSON.stringify({
    operation: item.name,
    controlled_semantic_path_field: item.field,
    base_evidence_id: base.evidence_id,
    same_path_repeat_evidence_id: repeat.evidence_id,
    copy_evidence_id: copy.evidence_id,
    byte_identity_equal: base.subject.digest.sha256 === copy.subject.digest.sha256,
    reported_ids_match_recomputed_projection: true,
    same_path_repeat_stable: true,
    copy_path_changes_outer_id: true,
    outer_subject_display_only_mutation_preserves_id: true,
    semantic_path_only_mutation_changes_id: true,
    nested_inventory_id_matches_projection: nested ? true : null,
    nested_display_path_mutation_preserves_inner_id: nestedDisplayMutationPreservesId,
    changed_path_fields: changed,
  }));
}
