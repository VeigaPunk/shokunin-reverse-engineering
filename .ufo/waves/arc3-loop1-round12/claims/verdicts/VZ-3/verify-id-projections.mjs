import { createHash } from 'node:crypto';
import { readFileSync } from 'node:fs';

const read = (path) => JSON.parse(readFileSync(path, 'utf8'));
const unwrap = (value) => value.data ?? value;
const semanticProjection = (e) => {
  const projection = {
    subject: e.subject === null ? null : {
      digest: e.subject.digest,
      format: e.subject.format,
      architecture: e.subject.architecture,
    },
    provider: e.provider,
    analysis_profile: e.analysis_profile,
    predicate_type: e.predicate_type,
    operation: e.operation,
    parameters: e.parameters,
    raw_result: e.raw_result,
    normalized_result: e.normalized_result,
    confidence: e.confidence,
    authority: e.authority,
    environment: e.environment,
    limitations: e.limitations,
    locations: e.locations,
    evidence_links: e.evidence_links,
  };
  if (Object.hasOwn(e, 'relationship_coverage')) projection.relationship_coverage = e.relationship_coverage;
  return projection;
};
const canonical = (value) => {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  return `{${Object.keys(value).sort().map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
};
const derived = (e) => `ev_${createHash('sha256').update(canonical(semanticProjection(e))).digest('hex')}`;
const equal = (a, b) => JSON.stringify(a) === JSON.stringify(b);
const assert = (condition, label) => {
  if (!condition) throw new Error(label);
};
const loadSet = (paths) => paths.map((path) => {
  const e = unwrap(read(path));
  assert(derived(e) === e.evidence_id, `id mismatch: ${path}`);
  return e;
});

const r7dir = '.ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/probes';
const r7 = loadSet(['64-base', '64-copyA', '67-base1', '67-base2', '67-copyA', '67-copyB', '67-mutated', '67-raw'].map((name) => `${r7dir}/${name}.json`));
const r7base = r7[2];
const r7repeat = r7[3];
const r7copyA = r7[4];
const r7copyB = r7[5];
const r7fields = ['parameters.path', 'normalized_result.artifact.path', 'locations[0].path'];
const getPath = (e, field) => field === 'parameters.path' ? e.parameters.path : field === 'normalized_result.artifact.path' ? e.normalized_result.artifact.path : e.locations[0].path;
assert(r7base.evidence_id === r7repeat.evidence_id, 'r7 same-path repeat');
assert(r7base.subject.digest.sha256 === r7copyA.subject.digest.sha256 && r7base.normalized_result.bytecode.sha256 === r7copyA.normalized_result.bytecode.sha256 && equal(r7base.normalized_result.functions, r7copyA.normalized_result.functions), 'r7 content comparison');
assert(r7base.evidence_id !== r7copyA.evidence_id && r7copyA.evidence_id !== r7copyB.evidence_id, 'r7 path id changes');
assert(r7fields.every((field) => getPath(r7base, field) !== getPath(r7copyA, field)), 'r7 semantic path fields');
const r7v64base = r7[0];
const r7v64copy = r7[1];
assert(r7v64base.subject.digest.sha256 === r7v64copy.subject.digest.sha256 && r7v64base.evidence_id !== r7v64copy.evidence_id, 'r7 6.4 path control');
console.log(`r7 inspect_evm_interface: envelope_ids=${r7.length}/${r7.length}, same_path_repeat=true, 6.7_path_controls=2, 6.4_path_control=true, bytes/decoded/functions_equal=true, semantic_path_fields_changed=${r7fields.length}`);

const r10dir = '.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence';
const r10 = loadSet(['probe-base1', 'probe-base2', 'probe-copyA', 'probe-copyB'].map((name) => `${r10dir}/${name}.json`));
assert(r10[0].evidence_id === r10[1].evidence_id, 'r10 same-path repeat');
assert(r10.every((e) => e.subject.digest.sha256 === r10[0].subject.digest.sha256 && e.normalized_result.artifact.sha256 === r10[0].normalized_result.artifact.sha256), 'r10 content comparison');
assert(r10[0].evidence_id !== r10[2].evidence_id && r10[2].evidence_id !== r10[3].evidence_id, 'r10 path id changes');
assert(r10.every((e) => e.parameters.path === e.normalized_result.artifact.path && e.parameters.path === e.locations[0].path), 'r10 path field agreement');
assert(r10[0].parameters.path !== r10[2].parameters.path && r10[2].parameters.path !== r10[3].parameters.path, 'r10 alternate paths');
console.log(`r10 inspect_rust_binary: envelope_ids=${r10.length}/${r10.length}, same_path_repeat=true, byte-identical_path_controls=2, artifact_digest_equal=true, semantic_path_fields_changed=3`);

const r11dir = '.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence';
const r11 = loadSet(['inspect-artifact-base-1', 'inspect-artifact-base-2', 'inspect-artifact-copy', 'inspect-artifact-same-name-other-path'].map((name) => `${r11dir}/${name}.json`));
const nested = (e) => e.normalized_result.substeps[0].evidence;
assert(r11[0].evidence_id === r11[1].evidence_id, 'r11 same-path repeat');
assert(r11.every((e) => e.subject.digest.sha256 === r11[0].subject.digest.sha256 && nested(e).subject.digest.sha256 === nested(r11[0]).subject.digest.sha256), 'r11 content comparison');
assert(r11[0].evidence_id !== r11[2].evidence_id && r11[0].evidence_id !== r11[3].evidence_id, 'r11 path id changes');
const display = structuredClone(r11[0]);
display.subject.name = r11[3].subject.name;
display.subject.local_path = r11[3].subject.local_path;
assert(derived(display) === r11[0].evidence_id, 'r11 display-only mutation');
const nestedPath = structuredClone(r11[0]);
nested(nestedPath).subject.local_path = nested(r11[3]).subject.local_path;
const nestedPathId = derived(nestedPath);
assert(nestedPathId !== r11[0].evidence_id, 'r11 nested path sensitivity');
assert(nestedPathId !== r11[3].evidence_id, 'r11 derived inspection field delta');
assert(r11[0].normalized_result.inspection_id !== r11[3].normalized_result.inspection_id, 'r11 inspection id path correlation');
nestedPath.normalized_result.inspection_id = r11[3].normalized_result.inspection_id;
assert(derived(nestedPath) === r11[3].evidence_id, 'r11 nested path plus derived inspection id');
console.log(`r11 inspect_artifact: envelope_ids=${r11.length}/${r11.length}, same_path_repeat=true, byte-identical_path_controls=2, nested_inventory_digest_equal=true, outer_display_only_same_id=true, nested_path_only_changes_outer_id=true, alternate_id_reproduced_after_inspection_id_update=true`);
