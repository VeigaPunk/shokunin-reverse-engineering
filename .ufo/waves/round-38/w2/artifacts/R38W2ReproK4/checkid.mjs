import { readFileSync } from 'node:fs';
const { parseEvidence } = await import(process.env.P + '/dist/domain/evidence.js');
const files = process.argv.slice(2);
for (const f of files) {
  const d = JSON.parse(readFileSync(f, 'utf8'));
  try { const p = parseEvidence(d); console.log(`${f.split('/').slice(-2).join('/')}: PASS id=${p.evidence_id}`); }
  catch (e) { const msgs = (e.issues||[]).map(i=>`${i.path.join('.')}: ${i.message}`); console.log(`${f.split('/').slice(-2).join('/')}: FAIL ${msgs.join(' | ') || e.message}`); }
}
