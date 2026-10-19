import fs from 'node:fs';
import path from 'node:path';
import { createHash } from 'node:crypto';

const [probeDir, databaseA, databaseB] = process.argv.slice(2);
if (!probeDir || !databaseA || !databaseB) {
  throw new Error('usage: node recompute.mjs <probe-dir> <database-a> <database-b>');
}

const fields = [
  'provider',
  'analysis_profile',
  'predicate_type',
  'operation',
  'parameters',
  'raw_result',
  'normalized_result',
  'confidence',
  'authority',
  'environment',
  'limitations',
  'relationship_coverage',
  'locations',
  'evidence_links',
];

function projection(evidence) {
  const subject = evidence.subject === null
    ? null
    : {
        digest: evidence.subject.digest,
        format: evidence.subject.format,
        architecture: evidence.subject.architecture,
      };
  return {
    subject,
    ...Object.fromEntries(fields.map((field) => [field, evidence[field]])),
  };
}

function canonical(value) {
  if (value === null || typeof value !== 'object') {
    const encoded = JSON.stringify(value);
    if (encoded === undefined) throw new TypeError('unsupported JSON value');
    return encoded;
  }
  if (Array.isArray(value)) return `[${value.map(canonical).join(',')}]`;
  const keys = Object.keys(value).sort().filter((key) => value[key] !== undefined);
  return `{${keys.map((key) => `${JSON.stringify(key)}:${canonical(value[key])}`).join(',')}}`;
}

function sha256(value) {
  return createHash('sha256').update(value).digest('hex');
}

function load(name) {
  return JSON.parse(fs.readFileSync(path.join(probeDir, name), 'utf8'));
}

function differences(left, right, prefix = '') {
  if (left !== null && right !== null && typeof left === 'object' && typeof right === 'object') {
    if (Array.isArray(left) && Array.isArray(right)) {
      if (left.length !== right.length) return [`${prefix}:length`];
      return left.flatMap((value, index) => differences(value, right[index], `${prefix}/${index}`));
    }
    const keys = [...new Set([...Object.keys(left), ...Object.keys(right)])].sort();
    return keys.flatMap((key) => {
      if (!Object.hasOwn(left, key) || !Object.hasOwn(right, key)) return [`${prefix}/${key}:presence`];
      return differences(left[key], right[key], `${prefix}/${key}`);
    });
  }
  return Object.is(left, right) ? [] : [prefix];
}

function maskPaths(evidence) {
  const value = structuredClone(projection(evidence));
  value.parameters.path = '<PATH>';
  value.normalized_result.artifact.path = '<PATH>';
  value.locations[0].path = '<PATH>';
  return canonical(value);
}

const a1 = load('a1.json');
const a2 = load('a2.json');
const b1 = load('b1.json');
const records = [['a1', a1], ['a2', a2], ['b1', b1]];
for (const [name, evidence] of records) {
  const encoded = canonical(projection(evidence));
  const digest = sha256(encoded);
  const recomputed = `ev_${digest}`;
  if (recomputed !== evidence.evidence_id) throw new Error(`${name}: semantic ID mismatch`);
  console.log(`${name} observed=${evidence.evidence_id} recomputed=${recomputed} match=yes projection_bytes=${Buffer.byteLength(encoded)} projection_sha256=${digest}`);
}

const samePathBytes = fs.readFileSync(path.join(probeDir, 'a1.json')).equals(fs.readFileSync(path.join(probeDir, 'a2.json')));
const bytesA = fs.readFileSync(databaseA);
const bytesB = fs.readFileSync(databaseB);
const sameDatabaseBytes = bytesA.equals(bytesB);
const projectionDiffs = differences(projection(a1), projection(b1)).sort();
const expectedDiffs = [
  '/locations/0/path',
  '/normalized_result/artifact/path',
  '/parameters/path',
].sort();
const maskedA = maskPaths(a1);
const maskedB = maskPaths(b1);
const masksMatch = maskedA === maskedB;
const samePathStable = a1.evidence_id === a2.evidence_id;
const pathSensitive = a1.evidence_id !== b1.evidence_id;
const excludedSubjectFields = a1.subject.name === b1.subject.name && a1.subject.local_path !== b1.subject.local_path;

if (!samePathBytes || !sameDatabaseBytes || !samePathStable || !pathSensitive ||
    JSON.stringify(projectionDiffs) !== JSON.stringify(expectedDiffs) || !masksMatch || !excludedSubjectFields) {
  throw new Error('path-domain checks failed');
}

console.log(`same_path_envelopes_byte_identical=${samePathBytes ? 'yes' : 'no'}`);
console.log(`fixture_bytes_a=${bytesA.length} fixture_sha256_a=${sha256(bytesA)}`);
console.log(`fixture_bytes_b=${bytesB.length} fixture_sha256_b=${sha256(bytesB)}`);
console.log(`same_database_bytes=${sameDatabaseBytes ? 'yes' : 'no'}`);
console.log(`projection_diff_paths=${projectionDiffs.join(',')}`);
console.log(`masked_projection_sha256_a=${sha256(maskedA)}`);
console.log(`masked_projection_sha256_b=${sha256(maskedB)}`);
console.log(`path_masked_projections_equal=${masksMatch ? 'yes' : 'no'}`);
console.log(`same_path_stable=${samePathStable ? 'yes' : 'no'}`);
console.log(`different_path_ids_distinct=${pathSensitive ? 'yes' : 'no'}`);
console.log(`subject_name_same=${(a1.subject.name === b1.subject.name) ? 'yes' : 'no'}`);
console.log(`subject_local_path_diff=${(a1.subject.local_path !== b1.subject.local_path) ? 'yes' : 'no'}`);
console.log('result=PASS');
