import { createHash } from 'node:crypto';
import { readFile } from 'node:fs/promises';
import { join } from 'node:path';

const root = '.ufo/waves';
const fields = [
  'provider', 'analysis_profile', 'predicate_type', 'operation', 'parameters',
  'raw_result', 'normalized_result', 'confidence', 'authority', 'environment',
  'limitations', 'relationship_coverage', 'locations', 'evidence_links',
];
const ordered = value => Array.isArray(value)
  ? value.map(ordered)
  : value !== null && typeof value === 'object'
    ? Object.fromEntries(Object.keys(value).sort().map(key => [key, ordered(value[key])]))
    : value;
const projection = evidence => Object.fromEntries([
  ['subject', evidence.subject === null ? null : {
    digest: evidence.subject.digest,
    format: evidence.subject.format,
    architecture: evidence.subject.architecture,
  }],
  ...fields.filter(key => Object.hasOwn(evidence, key)).map(key => [key, evidence[key]]),
]);
const digest = evidence => `ev_${createHash('sha256')
  .update(JSON.stringify(ordered(projection(evidence))), 'utf8').digest('hex')}`;
const read = async (path, unwrap) => {
  const value = JSON.parse(await readFile(path, 'utf8'));
  return unwrap ? value.data : value;
};
const loadSet = async (entries, unwrap) => Object.fromEntries(await Promise.all(
  entries.map(async ([name, path]) => [name, await read(path, unwrap)]),
));
const r7Entries = ['64-base', '64-copyA', '67-base1', '67-base2', '67-copyA', '67-copyB', '67-mutated', '67-raw']
  .map(name => [name, join(root, 'arc3-loop1-round7/claims/c2/EX-3/evidence/probes', `${name}.json`)]);
const r7 = await loadSet(r7Entries, false);
const r10Entries = ['base1', 'base2', 'copyA', 'copyB']
  .map(name => [name, join(root, 'arc3-loop1-round10/claims/c1/EX-4/evidence', `probe-${name}.json`)]);
const r10 = await loadSet(r10Entries, true);
const r11Names = [
  'inspect-artifact-base-1.json', 'inspect-artifact-base-2.json',
  'inspect-artifact-copy.json', 'inspect-artifact-same-name-other-path.json',
];
const r11Entries = r11Names.map(name => [name, join(root, 'arc3-loop1-round11/claims/c1/CR-2/evidence', name)]);
const r11 = await loadSet(r11Entries, true);
const countMatches = records => Object.values(records).filter(evidence => digest(evidence) === evidence.evidence_id).length;
const r7Pairs = [['67-base1', '67-copyA'], ['67-copyA', '67-copyB'], ['64-base', '64-copyA']];
const r7PairHolds = r7Pairs.map(([leftName, rightName]) => {
  const left = r7[leftName];
  const right = r7[rightName];
  return left.evidence_id !== right.evidence_id
    && left.subject.digest.sha256 === right.subject.digest.sha256
    && left.normalized_result.bytecode.sha256 === right.normalized_result.bytecode.sha256
    && JSON.stringify(left.normalized_result.functions) === JSON.stringify(right.normalized_result.functions);
});
const r7DisplayStable = Object.values(r7).every(evidence => {
  const changed = structuredClone(evidence);
  changed.subject.name = 'changed';
  changed.subject.local_path = '/changed';
  return digest(changed) === evidence.evidence_id;
});
const r10Base = r10.base1;
const r10Copy = r10.copyA;
const r10Copies = [r10.copyA, r10.copyB];
const r10AltpathDiffCount = r10Copies.filter(copy => r10Base.subject.digest.sha256 === copy.subject.digest.sha256 && r10Base.evidence_id !== copy.evidence_id).length;
const r10Paths = structuredClone(r10Base);
r10Paths.parameters.path = r10Copy.parameters.path;
r10Paths.normalized_result.artifact.path = r10Copy.parameters.path;
r10Paths.locations[0].path = r10Copy.parameters.path;
const r10Display = structuredClone(r10Base);
r10Display.subject.name = 'changed';
r10Display.subject.local_path = '/changed';
const r11Base = r11[r11Names[0]];
const r11Repeat = r11[r11Names[1]];
const r11SameName = r11[r11Names[3]];
const r11Display = structuredClone(r11Base);
r11Display.subject.name = 'changed';
r11Display.subject.local_path = '/changed';
const r11NestedPath = structuredClone(r11Base);
r11NestedPath.normalized_result.substeps[0].evidence.subject.local_path = '/changed/nested';
const results = [
  `r7: digest_matches=${countMatches(r7)}/${Object.keys(r7).length}; same_path_repeat=${r7['67-base1'].evidence_id === r7['67-base2'].evidence_id}; same_bytes_altpath_pairs=${r7PairHolds.filter(Boolean).length}/${r7PairHolds.length}; display_only_stable=${r7DisplayStable}`,
  `r10: digest_matches=${countMatches(r10)}/${Object.keys(r10).length}; same_path_repeat=${r10Base.evidence_id === r10.base2.evidence_id}; same_bytes_altpath_copies=${r10AltpathDiffCount}/${r10Copies.length}; path_fields_only_reproduce_copy=${digest(r10Paths) === r10Copy.evidence_id}; display_only_stable=${digest(r10Display) === r10Base.evidence_id}`,
  `r11: digest_matches=${countMatches(r11)}/${Object.keys(r11).length}; same_path_repeat=${r11Base.evidence_id === r11Repeat.evidence_id}; same_name_same_bytes_altpath_differs=${r11Base.subject.name === r11SameName.subject.name && r11Base.subject.digest.sha256 === r11SameName.subject.digest.sha256 && r11Base.evidence_id !== r11SameName.evidence_id}; outer_display_only_stable=${digest(r11Display) === r11Base.evidence_id}; nested_inventory_path_changes_outer_id=${digest(r11NestedPath) !== r11Base.evidence_id}`,
];
for (const result of results) console.log(result);
if (countMatches(r7) !== 8 || !r7PairHolds.every(Boolean) || !r7DisplayStable
  || countMatches(r10) !== 4 || r10Base.evidence_id !== r10.base2.evidence_id
  || r10AltpathDiffCount !== 2
  || digest(r10Paths) !== r10Copy.evidence_id || digest(r10Display) !== r10Base.evidence_id
  || countMatches(r11) !== 4 || r11Base.evidence_id !== r11Repeat.evidence_id
  || r11Base.subject.name !== r11SameName.subject.name || r11Base.subject.digest.sha256 !== r11SameName.subject.digest.sha256
  || r11Base.evidence_id === r11SameName.evidence_id || digest(r11Display) !== r11Base.evidence_id
  || digest(r11NestedPath) === r11Base.evidence_id) process.exitCode = 1;
