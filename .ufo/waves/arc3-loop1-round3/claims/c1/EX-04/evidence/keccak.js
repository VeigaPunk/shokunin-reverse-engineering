const RC = [0x0000000000000001n,0x0000000000008082n,0x800000000000808an,0x8000000080008000n,0x000000000000808bn,0x0000000080000001n,0x8000000080008081n,0x8000000000008009n,0x000000000000008an,0x0000000000000088n,0x0000000080008009n,0x000000008000000an,0x000000008000808bn,0x800000000000008bn,0x8000000000008089n,0x8000000000008003n,0x8000000000008002n,0x8000000000000080n,0x000000000000800an,0x800000008000000an,0x8000000080008081n,0x8000000000008080n,0x0000000080000001n,0x8000000080008008n];
const ROT = [
 [0,36,3,41,18],
 [1,44,10,45,2],
 [62,6,43,15,61],
 [28,55,25,21,56],
 [27,20,39,8,14]
];
const M = (1n << 64n) - 1n;
function rotl(x, n) { n = BigInt(n) % 64n; return ((x << n) | (x >> (64n - n))) & M; }
function keccakF(A) {
  for (let round = 0; round < 24; round++) {
    const C = [], D = [];
    for (let x = 0; x < 5; x++) C[x] = A[x] ^ A[x+5] ^ A[x+10] ^ A[x+15] ^ A[x+20];
    for (let x = 0; x < 5; x++) D[x] = C[(x+4)%5] ^ rotl(C[(x+1)%5], 1);
    for (let x = 0; x < 5; x++) for (let y = 0; y < 5; y++) A[x+5*y] ^= D[x];
    const B = new Array(25).fill(0n);
    for (let x = 0; x < 5; x++) for (let y = 0; y < 5; y++) B[y + 5*((2*x+3*y)%5)] = rotl(A[x+5*y], ROT[x][y]);
    for (let x = 0; x < 5; x++) for (let y = 0; y < 5; y++) A[x+5*y] = B[x+5*y] ^ ((~B[(x+1)%5+5*y] & M) & B[(x+2)%5+5*y]);
    A[0] ^= RC[round];
  }
  return A;
}
function keccak256(bytes) {
  const rate = 136;
  const A = new Array(25).fill(0n);
  const pad = new Uint8Array(Math.ceil((bytes.length + 1) / rate) * rate);
  pad.set(bytes); pad[bytes.length] = 0x01; pad[pad.length - 1] |= 0x80;
  for (let off = 0; off < pad.length; off += rate) {
    for (let i = 0; i < rate / 8; i++) {
      let lane = 0n;
      for (let b = 7; b >= 0; b--) lane = (lane << 8n) | BigInt(pad[off + i*8 + b]);
      A[i] ^= lane;
    }
    keccakF(A);
  }
  const out = Buffer.alloc(32);
  for (let i = 0; i < 4; i++) { let lane = A[i]; for (let b = 0; b < 8; b++) { out[i*8+b] = Number(lane & 0xffn); lane >>= 8n; } }
  return out;
}
function selector(sig) { return keccak256(Buffer.from(sig, 'utf8')).subarray(0, 4).toString('hex'); }
module.exports = { keccak256, selector };
if (require.main === module) {
  const anchors = [
    ['keccak256("")', keccak256(Buffer.alloc(0)).toString('hex'), 'c5d2460186f7233c927e7db2dcc703c0e500b653ca82273b7bfad8045d85a470'],
    ['transfer(address,uint256)', selector('transfer(address,uint256)'), 'a9059cbb'],
    ['balanceOf(address)', selector('balanceOf(address)'), '70a08231'],
    ['approve(address,uint256)', selector('approve(address,uint256)'), '095ea7b3'],
  ];
  let ok = true;
  for (const [name, got, want] of anchors) { const pass = got === want; ok = ok && pass; console.log(`${pass ? 'PASS' : 'FAIL'}  ${name} -> ${got}${pass ? '' : ' (want ' + want + ')'}`); }
  console.log(ok ? 'ANCHORS: all match' : 'ANCHORS: MISMATCH');
  process.exit(ok ? 0 : 1);
}