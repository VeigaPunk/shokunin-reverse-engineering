// W2C1Forge TAMPER (scratch npm cache copy only; never the host cache).
// Installed as the first statements of rea-agents/scripts/rea.mjs in the scratch copy.
import { readFileSync as __rf } from 'node:fs';
import { createHash as __ch } from 'node:crypto';
if (process.argv.includes('extract-firmware')) {
  const __in = process.argv[process.argv.length - 2];
  const __sha = __ch('sha256').update(__rf(__in)).digest('hex');
  const __map = JSON.parse(__rf(process.env.TAMPER_MAP, 'utf8'));
  const __env = JSON.parse(__rf(__map[__sha], 'utf8'));
  process.stdout.write(JSON.stringify({ ok: true, data: __env }) + '\n');
  process.exit(0);
}
