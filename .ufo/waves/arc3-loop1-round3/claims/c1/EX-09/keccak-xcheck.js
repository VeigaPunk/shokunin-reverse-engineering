const sha3 = require('/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/arc3-loop1-round1/tools/solc-prefix/node_modules/js-sha3');
const fs = require('fs');
const file = process.argv[2];
const sigs = fs.readFileSync(file, 'utf8').split('\n').map(s => s.trim()).filter(Boolean);
for (const s of sigs) { const full = sha3.keccak256(s); console.log(full, full.slice(0,8)); }
