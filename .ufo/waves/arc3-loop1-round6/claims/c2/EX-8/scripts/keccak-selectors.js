#!/usr/bin/env node
// EX-8: independent selector derivation for VariantVault.vy — js-sha3 keccak256
// of each signature from vyper's method_identifiers keys, compared byte-wise.
const path='/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3';
const {keccak256}=require(path); const fs=require('fs');
const mi=JSON.parse(fs.readFileSync(process.argv[2]||'out/default/method-identifiers.json','utf8'));
const rows=Object.entries(mi).map(([sig,v])=>{const full=keccak256(sig);const sel=full.slice(0,8);const vy=v.replace(/^0x/,'').padStart(8,'0');return {sig,vyper:vy,js_sha3:sel,agree:sel===vy,full_keccak:full};});
console.log(JSON.stringify({derivation:'js-sha3@0.8.0 keccak256(sig)[0:8] vs vyper method_identifiers',n:rows.length,all_agree:rows.every(r=>r.agree),rows},null,1));
