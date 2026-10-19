import { createHash } from 'node:crypto';
import fs from 'node:fs';
import path from 'node:path';

const root = process.cwd();
const r7 = path.join(root, '.ufo/waves/arc3-loop1-round7/claims/c2/EX-3/evidence/probes');
const r10 = path.join(root, '.ufo/waves/arc3-loop1-round10/claims/c1/EX-4/evidence');
const r11 = path.join(root, '.ufo/waves/arc3-loop1-round11/claims/c1/CR-2/evidence');
const read = (file) => JSON.parse(fs.readFileSync(file, 'utf8'));
const unwrap = (file) => {
  const value = read(file);
  return value.data && typeof value.data === 'object' ? value.data : value;
};
const clone = (value) => structuredClone(value);
const keys67 = [
  'provider', 'analysis_profile', 'predicate_type', 'operation', 'parameters',
  'raw_result', 'normalized_result', 'confidence', 'authority', 'environment',
  'limitations', 'relationship_coverage', 'locations', 'evidence_links',
];
const keys64 = keys67.filter((key) => key !== 'relationship_coverage');
function projection(evidence, version) {
  return {
    subject: evidence.subject === null ? null : {
      digest: evidence.subject.digest,
      format: evidence.subject.format,
      architecture: evidence.subject.architecture,
    },
    ...Object.fromEntries((version === '6.4.0' ? keys64 : keys67)
      .map((key) => [key, evidence[key]])),
  };
}
function canonical(value) {
  if (value === null || typeof value !== 'object') return JSON.stringify(value);
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  return `{${Object.keys(value).sort()
    .filter((key) => value[key] !== undefined)
    .map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
}
function idFromProjection(value) {
  return `ev_${createHash('sha256').update(canonical(value), 'utf8').digest('hex')}`;
}
function computedId(evidence, version) {
  return idFromProjection(projection(evidence, version));
}
function diffPaths(left, right, prefix = '$', out = []) {
  if (Object.is(left, right)) return out;
  if (Array.isArray(left) && Array.isArray(right) && left.length === right.length) {
    left.forEach((value, index) => diffPaths(value, right[index], `${prefix}[${index}]`, out));
  } else if (left && right && typeof left === 'object' && typeof right === 'object'
      && !Array.isArray(left) && !Array.isArray(right)) {
    const names = [...new Set([...Object.keys(left), ...Object.keys(right)])].sort();
    for (const name of names) diffPaths(left[name], right[name], `${prefix}.${name}`, out);
  } else {
    out.push(prefix);
  }
  return out;
}
function adoptDifferences(left, right) {
  if (Array.isArray(left) && Array.isArray(right) && left.length === right.length) {
    return left.map((value, index) => adoptDifferences(value, right[index]));
  }
  if (left && right && typeof left === 'object' && typeof right === 'object'
      && !Array.isArray(left) && !Array.isArray(right)) {
    return Object.fromEntries(Object.keys(right).map((key) => [
      key,
      Object.hasOwn(left, key) ? adoptDifferences(left[key], right[key]) : clone(right[key]),
    ]));
  }
  return Object.is(left, right) ? clone(left) : clone(right);
}
function mutateDisplay(evidence) {
  const changed = clone(evidence);
  if (changed.subject && typeof changed.subject === 'object') {
    changed.subject.name = 'SC-2-display-only';
    changed.subject.local_path = '/SC-2/display-only';
  }
  return changed;
}
function checkedRows(files, version) {
  return files.map((file) => {
    const evidence = unwrap(file);
    return { file: path.basename(file), evidence, version, reported: evidence.evidence_id,
      recomputed: computedId(evidence, version) };
  });
}
function pathLeaves(paths) {
  return paths.every((value) => /(?:^|\.)(?:path|local_path)$/.test(value));
}

const evmFiles = fs.readdirSync(r7).filter((name) => /^\d{2}-.+\.json$/.test(name))
  .sort().map((name) => path.join(r7, name));
const evmRows = evmFiles.map((file) => {
  const version = path.basename(file).startsWith('64-') ? '6.4.0' : '6.7.0';
  const [row] = checkedRows([file], version);
  return row;
});
const evm64Base = unwrap(path.join(r7, '64-base.json'));
const evm64Copy = unwrap(path.join(r7, '64-copyA.json'));
const evm67Base = unwrap(path.join(r7, '67-base1.json'));
const evm67Repeat = unwrap(path.join(r7, '67-base2.json'));
const evm67Copy = unwrap(path.join(r7, '67-copyA.json'));
const evm67Diff = diffPaths(projection(evm67Base, '6.7.0'), projection(evm67Copy, '6.7.0'));
const evm67Replay = idFromProjection(adoptDifferences(
  projection(evm67Base, '6.7.0'), projection(evm67Copy, '6.7.0')));

const rustFiles = ['probe-base1.json', 'probe-base2.json', 'probe-copyA.json', 'probe-copyB.json']
  .map((name) => path.join(r10, name));
const rustRows = checkedRows(rustFiles, '6.7.0');
const rustBase = unwrap(path.join(r10, 'probe-base1.json'));
const rustRepeat = unwrap(path.join(r10, 'probe-base2.json'));
const rustCopy = unwrap(path.join(r10, 'probe-copyA.json'));
const rustDiff = diffPaths(projection(rustBase, '6.7.0'), projection(rustCopy, '6.7.0'));
const rustReplay = idFromProjection(adoptDifferences(
  projection(rustBase, '6.7.0'), projection(rustCopy, '6.7.0')));

const artifactFiles = [
  'inspect-artifact-base-1.json', 'inspect-artifact-base-2.json',
  'inspect-artifact-copy.json', 'inspect-artifact-same-name-other-path.json',
].map((name) => path.join(r11, name));
const artifactRows = checkedRows(artifactFiles, '6.7.0');
const artifactBase = unwrap(path.join(r11, 'inspect-artifact-base-1.json'));
const artifactRepeat = unwrap(path.join(r11, 'inspect-artifact-base-2.json'));
const artifactCopy = unwrap(path.join(r11, 'inspect-artifact-same-name-other-path.json'));
const artifactDiff = diffPaths(projection(artifactBase, '6.7.0'), projection(artifactCopy, '6.7.0'));
const artifactNestedMutation = clone(artifactBase);
artifactNestedMutation.normalized_result.substeps[0].evidence.subject.local_path =
  artifactCopy.normalized_result.substeps[0].evidence.subject.local_path;
const nestedEvidenceIds = artifactRows.map((row) =>
  row.evidence.normalized_result.substeps[0].evidence.evidence_id);

const summarize = (rows) => ({
  envelope_count: rows.length,
  recomputed_id_matches: rows.filter((row) => row.reported === row.recomputed).length,
  ids: Object.fromEntries(rows.map((row) => [row.file, row.reported])),
});
console.log(JSON.stringify({
  evm: {
    ...summarize(evmRows),
    v6_4_same_bytes_path_ids_differ: evm64Base.evidence_id !== evm64Copy.evidence_id,
    v6_7_same_path_repeat_stable: evm67Base.evidence_id === evm67Repeat.evidence_id,
    v6_7_same_bytes_copy_ids_differ: evm67Base.evidence_id !== evm67Copy.evidence_id,
    v6_7_projection_diff_paths: evm67Diff,
    v6_7_projection_differences_are_paths: pathLeaves(evm67Diff),
    v6_7_copy_rebuilt_from_base_projection: evm67Replay === evm67Copy.evidence_id,
    top_level_display_mutation_stable:
      computedId(mutateDisplay(evm67Base), '6.7.0') === evm67Base.evidence_id,
  },
  rust: {
    ...summarize(rustRows),
    same_path_repeat_stable: rustBase.evidence_id === rustRepeat.evidence_id,
    same_byte_copy_ids_differ: rustBase.evidence_id !== rustCopy.evidence_id,
    projection_diff_paths: rustDiff,
    projection_differences_are_paths: pathLeaves(rustDiff),
    copy_rebuilt_from_base_projection: rustReplay === rustCopy.evidence_id,
    top_level_display_mutation_stable:
      computedId(mutateDisplay(rustBase), '6.7.0') === rustBase.evidence_id,
  },
  inspect_artifact: {
    ...summarize(artifactRows),
    same_path_repeat_stable: artifactBase.evidence_id === artifactRepeat.evidence_id,
    same_name_same_bytes_other_path_changes_outer_id:
      artifactBase.evidence_id !== artifactCopy.evidence_id,
    projection_diff_paths: artifactDiff,
    nested_inventory_id_count: new Set(nestedEvidenceIds).size,
    nested_local_path_change_changes_outer_id:
      computedId(artifactNestedMutation, '6.7.0') !== artifactBase.evidence_id,
    top_level_display_mutation_stable:
      computedId(mutateDisplay(artifactBase), '6.7.0') === artifactBase.evidence_id,
  },
}, null, 2));
