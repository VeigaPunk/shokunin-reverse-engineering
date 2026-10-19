#!/usr/bin/env node
// EX-08: build the probe matrix artifact from the raw probe JSON files.
const fs = require('fs');
const path = require('path');
const HERE = __dirname;

const files = fs.readdirSync(HERE).filter(f => /^probe-.*\.json$/.test(f)).sort();
const rows = [];
for (const f of files) {
  const label = f.replace(/\.json$/, '');
  const exit = fs.existsSync(path.join(HERE, label + '.exit'))
    ? fs.readFileSync(path.join(HERE, label + '.exit'), 'utf8').trim() : '?';
  const j = JSON.parse(fs.readFileSync(path.join(HERE, f), 'utf8'));
  if (j.normalized_result) {
    const fns = (j.raw_result?.functions ?? []).map(x => `${x.selector}@${x.bytecodeOffset}`);
    rows.push({
      label, exit, shape: fns.length ? 'analysis: selectors recovered' : 'analysis: honest empty',
      code: null, category: null, retryable: null,
      artifact_sha256: j.normalized_result.artifact.sha256,
      bytecode_sha256: j.normalized_result.bytecode.sha256,
      bytecode_kind: j.normalized_result.bytecode.kind,
      functions: fns, dispatch: [...new Set((j.raw_result?.functions ?? []).map(x => x.dispatch))],
      state_mutability: [...new Set((j.raw_result?.functions ?? []).map(x => x.stateMutability))],
      evidence_id: j.evidence_id, provider: j.provider.version,
      evidence_kind: j.normalized_result.evidence_kind,
      runtime_execution: j.normalized_result.runtime_execution,
      completeness: j.normalized_result.discovery_completeness,
      issue: null,
    });
  } else {
    rows.push({
      label, exit, shape: 'typed refusal',
      code: j.code, category: j.category, retryable: j.retryable,
      artifact_sha256: null, bytecode_sha256: null, bytecode_kind: null, functions: [],
      dispatch: [], state_mutability: [], evidence_id: null, provider: j.details?.provider_id ?? null,
      issue: (j.details?.issues ?? []).map(i => i.message)[0] ?? j.details?.diagnostics?.reason ?? null,
      phase: j.details?.diagnostics?.phase ?? null,
    });
  }
}

fs.writeFileSync(path.join(HERE, 'probe-matrix.json'), JSON.stringify(rows, null, 2));
const md = ['# EX-08 probe matrix (arc3-loop1-round1, chain c1)', '',
  '| probe | exit | shape | key fields |', '|---|---|---|---|'];
for (const r of rows) {
  const key = r.shape === 'typed refusal'
    ? `code=${r.code} category=${r.category} retryable=${r.retryable} issue="${r.issue}"`
    : `artifact=${r.artifact_sha256?.slice(0, 12)} bc=${r.bytecode_sha256?.slice(0, 12)} kind=${r.bytecode_kind} fns=[${r.functions.join(', ')}] dispatch=[${r.dispatch.join(',')}] mutability=[${r.state_mutability.join(',')}] ev=${r.evidence_id?.slice(0, 15)}…`;
  md.push(`| ${r.label} | ${r.exit} | ${r.shape} | ${key} |`);
}
fs.writeFileSync(path.join(HERE, 'probe-matrix.md'), md.join('\n') + '\n');
console.log(md.join('\n'));
