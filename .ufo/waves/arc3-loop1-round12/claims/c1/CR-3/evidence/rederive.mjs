import assert from 'node:assert/strict';
import { readFile } from 'node:fs/promises';
import { isDeepStrictEqual } from 'node:util';

const packageRoot = '/home/vgpnk/.npm/_npx/a1722018f28f9df2/node_modules/rea-agents';
const { digestCanonicalValue } = await import(`${packageRoot}/dist/domain/canonicalDigest.js`);
const root = process.argv[2];
assert.ok(root, 'Pass the directory containing the four REA JSON envelopes.');
const names = ['base-1', 'base-2', 'alt-same-name', 'alt-different-name'];
const project = (evidence) => ({
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
const valuesForKey = (value, key, values = []) => {
  if (Array.isArray(value)) {
    for (const item of value) valuesForKey(item, key, values);
  } else if (value !== null && typeof value === 'object') {
    for (const [name, item] of Object.entries(value)) {
      if (name === key) values.push(item);
      valuesForKey(item, key, values);
    }
  }
  return values;
};
const rows = [];
for (const name of names) {
  const wrapper = JSON.parse(await readFile(`${root}/${name}.json`, 'utf8'));
  assert.equal(wrapper.ok, true, `${name} must be a successful REA result.`);
  const outer = wrapper.data;
  assert.equal(outer.operation, 'inspect_artifact');
  const [step] = outer.normalized_result.substeps;
  assert.equal(step.operation, 'inventory_artifact');
  const child = step.evidence;
  const outerProjection = project(outer);
  const nestedProjection = project(child);
  const outerRecomputed = `ev_${digestCanonicalValue(outerProjection, 'Evidence')}`;
  const nestedRecomputed = `ev_${digestCanonicalValue(nestedProjection, 'Evidence')}`;
  assert.equal(outerRecomputed, outer.evidence_id, `${name} outer ID must rederive.`);
  assert.equal(nestedRecomputed, child.evidence_id, `${name} nested ID must rederive.`);
  const selectedPath = child.subject.local_path;
  const row = {
    run: name,
    selected_path: selectedPath,
    subject_name: child.subject.name,
    outer_id: outer.evidence_id,
    outer_recomputed: outerRecomputed,
    nested_id: child.evidence_id,
    nested_recomputed: nestedRecomputed,
    nested_projection_has_absolute_selected_path: JSON.stringify(nestedProjection).includes(selectedPath),
    nested_projection_path_keys: valuesForKey(nestedProjection, 'path'),
    nested_logical_paths: child.normalized_result.occurrences.map(({ logical_path }) => logical_path),
    subject_projection_keys: Object.keys(nestedProjection.subject),
    projection_fields: Object.keys(nestedProjection),
  };
  rows.push({ outerProjection, nestedProjection, row });
}
assert.equal(rows[0].row.outer_id, rows[1].row.outer_id, 'Same-path parent rerun must be stable.');
assert.notEqual(rows[0].row.outer_id, rows[2].row.outer_id, 'Alternate-path parent ID must differ.');
assert.notEqual(rows[0].row.outer_id, rows[3].row.outer_id, 'Different-basename parent ID must differ.');
assert.ok(rows.every(({ row }) => row.nested_id === rows[0].row.nested_id), 'Nested inventory IDs must agree.');
assert.ok(rows.every(({ nestedProjection }) => isDeepStrictEqual(nestedProjection, rows[0].nestedProjection)), 'Nested semantic projections must be equal.');
assert.ok(rows.every(({ row }) => row.nested_projection_has_absolute_selected_path === false));
assert.ok(rows.every(({ row }) => row.nested_projection_path_keys.length === 0));
for (const { row } of rows) console.log(JSON.stringify(row));
console.log(JSON.stringify({
  package_version: JSON.parse(await readFile(`${packageRoot}/package.json`, 'utf8')).version,
  outer_projection_equal_all_runs: rows.every(({ outerProjection }) => isDeepStrictEqual(outerProjection, rows[0].outerProjection)),
  nested_projection_equal_all_runs: rows.every(({ nestedProjection }) => isDeepStrictEqual(nestedProjection, rows[0].nestedProjection)),
}));
