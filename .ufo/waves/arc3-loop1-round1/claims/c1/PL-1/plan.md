# C1 execution plan — real solc bytecode → selector recovery (PL-1)

Seat: PL-1, chain c1, planner. Wave `arc3-loop1-round1`. Frozen claim source:
`.ufo/waves/arc3-loop1-round1/claims-frozen.md:14-38`.

**Status: de-risked end-to-end by PL-1 on `/var/tmp` copies, 2026-10-19.** Every
command in §3 marked `[VERIFIED]` was actually run by the planner; §8 carries the
raw evidence. The executor's job is to re-run them at the wave's own paths, seal
the receipts, and produce the patch-text records. Nothing in this plan requires a
repo write outside the two authorized exceptions (`claims/…` artifacts and the
wave-dir install prefix).

---

## 1. Claim restated, and the before-state it must move

Claim (frozen): after the round's commits, `rea inspect-evm-interface <file>
<raw|hex>` recovers selectors from a **real solc-compiled contract on this
host**; the result lands as a corpus knowledge entry with sealed receipts; the
map gains one line-neutral token; command A re-measures knowledge 81 → 82 with
prior 81 byte-identical and rules 13/13.

Before-state, measured by PL-1 at HEAD `e845c2b524ad2e59871e004c51a1386e192a74ab`
(command A verbatim, §8.1):

```json
{"citation_resolved_rules": 13, "coverage_score": 10.0, "dangling": [],
 "depth_score": 10.0, "knowledge_files": 81, "mapped": 81, "missing": [],
 "revision": "e845c2b524ad2e59871e004c51a1386e192a74ab", "rule_blocks": 13}
```

EVM held today only on the r3-07 synthetic 81-byte dispatcher
(`corpus/knowledge/2026-10-13-r3-evm-interface.md`; PROVINCE.md:91-93 Frontier
"real solc/vyper-compiled bytecode untested"). No `solc` exists on this host
(`which solc` → not found).

---

## 2. Environment facts the de-risk discovered (all plan-critical)

| # | Fact | Evidence |
|---|---|---|
| F1 | npm `solc@0.8.37` is reachable; tarball `https://registry.npmjs.org/solc/-/solc-0.8.37.tgz`, integrity `sha512-ieUYdPDRGNKMsZpCfi9tY64Q+ASoL8tyhLuvf9cFiqDs+6ijlx8Wn2CRi0N71AlCvRx0V092rlUYu3b3PuxWlA==` | §8.2 |
| F2 | The npm package's binary is **`solcjs`**, not `solc` (`node_modules/.bin/solcjs` → `../solc/solc.js`); `solcjs --version` → `0.8.37+commit.f401782d.Emscripten.clang` | §8.2 |
| F3 | `solcjs --standard-json` exits 0 but writes a `>>> Cannot retry compilation with SMT because there are no SMT solvers available.` line to **stdout** before the JSON — a naive `JSON.parse` throws. Filter `^>>>` lines before parsing | §8.3 |
| F4 | **`/tmp` is quota-exhausted** (tmpfs 16G at 80%, mount opts carry `usrquota`; even a 5-byte write fails `Disk quota exceeded`). REA's EVM worker inherits the tmpfs session root and fails closed: `execution_failure`, `reason: "Unknown system error -122: …, write"` (errno 122 = EDQUOT) | §8.4, §8.5 |
| F5 | Setting `TMPDIR` to a **disk-backed** path (`/var/tmp/<seat>/reatmp`) makes the probe succeed (exit 0). This is exactly the lane's own standing rule (`corpus/lessons/2026-10-18-caller-independent-services.md:23-24` — "disk-backed `TMPDIR` (`/var/tmp/<run>` — never the quota-full tmpfs, and no dot-prefixed name") | §8.5, §8.6 |
| F6 | Encoding is the **positional** second arg (`<path> <raw|hex>`); `--format json` returns the envelope; exit 0 on success, 1 on refusal | §8.5-§8.10 |
| F7 | Evidence id domain for this verb family is **path-sensitive**: identical carrier bytes at two paths → two ids (`ev_911108c0…` vs `ev_62e889cf…`); identical (content, path, params) re-run → identical id (`ev_911108c0…` twice). `subject.digest.sha256` = sha256 of the **carrier file** (hex leg = sha256 of the `.hex` file; raw leg = sha256 of the `.bin` file) | §8.6, §8.9 |
| F8 | `raw_result.metadata` decodes the solc CBOR trailer (`solc: 000825` = 0.8.37, plus an `ipfs` hash) — independent on-bytecode proof the artifact is real solc output | §8.11 |
| F9 | Creation code recovers **0** selectors with `metadata.kind` null (consistent with the r3-07 "kind stays unknown" floor) — do not claim kind classification | §8.10 |

---

## 3. Pipeline (S1–S12)

Path conventions used below (executor substitutes `<SEAT>`):

- Wave dir: `.ufo/waves/arc3-loop1-round1/` (`WD`)
- Install prefix (the only authorized in-repo install target): `$WD/tools/solc-prefix/`
  — **LANDED by EX-02** (§9); the planner's proposed name `tools/npm-solc/` is
  superseded. All later `$WD/tools/…` paths in this plan read `solc-prefix`.
- Scratch (**never** `/tmp` — F4): `/var/tmp/<SEAT>-c1/` or `/dev/shm/<seat>/`
  (both landed in-chain, §9); REA `TMPDIR` must be set to that scratch:
  `/var/tmp/<SEAT>-c1/reatmp`
- Seat artifacts: `$WD/claims/c1/<SEAT>/`
- REA invocation: `npx -y rea-agents@6.7.0 …` (cached; `--version` → `6.7.0`, §8.2)

### S1 — custody pre-pair (owner: EX-01; landed by EX-01/EX-02, §9)
`[VERIFIED form]` 5-path sha256 capture before any install or probe, same format
as the arc2 receipts (`ts` line + `sha256  path` lines):

```bash
TS=$(date -u +%Y-%m-%dT%H:%M:%SZ)
{ echo "$TS"; sha256sum \
  ~/.config/devin/mcp_config.json ~/.omp/agent/mcp.json \
  ~/.kimi-code/config.toml ~/.bashrc ~/.profile; } > "$WD/claims/c1/EX-01/config-pre-pair.txt"
```
Acceptance: 5 hashes + timestamp. These paths are **read-only, capture-only** —
no repair, ever (custody SOP).

### S2 — install solc into the wave-dir prefix (owner: EX-02; **LANDED**, §9)
```bash
npm install --prefix "$WD/tools/solc-prefix" solc@0.8.37 --no-audit --no-fund
"$WD/tools/solc-prefix/node_modules/.bin/solcjs" --version
sha256sum "$WD/tools/solc-prefix/node_modules/solc/package.json"
```
`[VERIFIED]` install is ~164 ms, 8 packages; the dep tree is
`command-exists commander follow-redirects js-sha3 memorystream semver solc tmp`.
Receipt `claims/c1/EX-01/install-receipt.txt` must carry: package name, exact
version, npm integrity string, resolved tarball URL, installed `solcjs` version
string, sha256 of `node_modules/solc/package.json`, dep-tree listing, timestamp.
Optional stronger identity: re-fetch the tarball and record its sha256 +
sha512-vs-integrity comparison.

**Honest-stop branch S2-H1 (install failure).** Registry unreachable, integrity
mismatch, or non-`solc` package pulled → record the failure verbatim, **do not**
substitute another compiler or source; claim NOT verified; the round reports the
honest stop. (The authorization covers npm `solc` + its dep tree only.)

### S3 — author the contract + control (owner: EX-02)
Write the two sources **verbatim** below (byte-exact; PL-1's copies hashed
`5910441f…` / `a74fe10e…`, §8.3). Recording them inline makes the compile
deterministic across executors.

`KaidokuToken.sol` (K = 10 selectors: 5 explicit + 5 public getters):

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract KaidokuToken {
    mapping(address => uint256) public balanceOf;
    mapping(address => mapping(address => uint256)) public allowance;
    uint256 public totalSupply;
    string public name = "Kaidoku";
    address public owner;

    event Transfer(address indexed from, address indexed to, uint256 value);

    constructor(uint256 initialSupply) {
        totalSupply = initialSupply;
        balanceOf[msg.sender] = initialSupply;
        owner = msg.sender;
    }

    function transfer(address to, uint256 amount) public returns (bool) {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        balanceOf[msg.sender] -= amount;
        balanceOf[to] += amount;
        emit Transfer(msg.sender, to, amount);
        return true;
    }

    function approve(address spender, uint256 amount) public returns (bool) {
        allowance[msg.sender][spender] = amount;
        return true;
    }

    function transferFrom(address from, address to, uint256 amount) public returns (bool) {
        require(allowance[from][msg.sender] >= amount, "allowance");
        allowance[from][msg.sender] -= amount;
        require(balanceOf[from] >= amount, "insufficient");
        balanceOf[from] -= amount;
        balanceOf[to] += amount;
        emit Transfer(from, to, amount);
        return true;
    }

    function mint(address to, uint256 amount) external {
        require(msg.sender == owner, "not owner");
        totalSupply += amount;
        balanceOf[to] += amount;
    }

    function burn(uint256 amount) external {
        require(balanceOf[msg.sender] >= amount, "insufficient");
        balanceOf[msg.sender] -= amount;
        totalSupply -= amount;
    }
}
```

`KaidokuEmpty.sol` (negative control — zero external functions → zero selectors):

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.20;

contract KaidokuEmpty {
    uint256 private stored;

    constructor(uint256 initial) {
        stored = initial;
    }
}
```

Receipt: `claims/c1/EX-02/source-receipt.txt` — `sha256sum` of both `.sol` files
+ the recorded **planted count K = 10** statement (pre-probe, per the claim's
"planted selector count K recorded pre-probe").

### S4 — compile (owner: EX-03)
Standard-JSON, optimizer OFF, `evmVersion: "cancun"`; outputSelection
`["abi","evm.bytecode.object","evm.deployedBytecode.object","evm.methodIdentifiers"]`
(both sources in one input; a small node builder avoids shell escaping).

```bash
"$WD/tools/solc-prefix/node_modules/.bin/solcjs" --standard-json < input.json > out.json   # exit 0
node -e 'const fs=require("fs");const raw=fs.readFileSync("out.json","utf8");
 fs.writeFileSync("out.cleaned.json", raw.split("\n").filter(l=>!l.startsWith(">>>")).join("\n"));'   # F3
```
Then extract per contract: `evm.methodIdentifiers` (the K table),
`evm.deployedBytecode.object` → `<Name>.runtime.hex` (with trailing newline) and
`<Name>.runtime.bin` (raw bytes), `evm.bytecode.object` → `<Name>.creation.hex`.

Acceptance / expected values `[VERIFIED]` for the pinned sources above:
KaidokuToken runtime 3858 B sha256 `543cdc0dd06ad62b6d38835451bfbe12d95672bed381d424c2439d6c20ad5641`,
creation 5017 B sha256 `e73372c22e0d4e959282ced64ba3944eb60679b1241efaf751963bdf00ff8e88`;
KaidokuEmpty runtime 62 B sha256 `7f0c279205bc243d8275aa01fad9745867d718b77585303ecf34bf7e4c91a146`,
creation 216 B sha256 `d2493b7a5ad355b6aedc987efec821cb456133369182d96ca93c56a4bbc5fec9`.
**A different runtime sha256 means the source or settings drifted — stop and
re-derive, do not "fix" the number.**
Receipt: `claims/c1/EX-03/compile-receipt.txt` (solc version string, source
sha256s, settings JSON, K table, all byte counts + sha256s).

### S5 — independent selector derivation (owner: EX-04)
The K table must not be taken on trust from one source. `js-sha3` ships inside
the solc dep tree; compute `keccak256(signature)[0:4]` for all 10 signatures:

```bash
node -e 'const {keccak256}=require("'$WD'/tools/solc-prefix/node_modules/js-sha3");
const sigs=["transfer(address,uint256)","approve(address,uint256)","transferFrom(address,address,uint256)","mint(address,uint256)","burn(uint256)","balanceOf(address)","allowance(address,address)","totalSupply()","name()","owner()"];
const o={}; for(const s of sigs) o[s]=keccak256(s).slice(0,8); console.log(JSON.stringify(o,null,1));'
```
`[VERIFIED]` 10/10 agreement with solc's `methodIdentifiers` (§8.3). Receipt:
`claims/c1/EX-04/keccak-receipt.txt`.

### S6 — probe legs (owners: EX-05 hex, EX-06 raw)
```bash
export TMPDIR=/var/tmp/<SEAT>-c1/reatmp          # F5 — mandatory
npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/<SEAT>-c1/KaidokuToken.runtime.hex hex --format json > probe-token-hex.json; echo "exit=$?"
npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/<SEAT>-c1/KaidokuToken.runtime.bin raw --format json > probe-token-raw.json; echo "exit=$?"
```
Capture per leg: exit code, full envelope JSON, `evidence_id`, `subject.digest.sha256`,
`normalized_result.functions[]` (`selector`, `bytecode_offset`, `dispatch`,
`inferred_arguments`, `inferred_state_mutability`), `raw_result.metadata`,
`limitations[]`, `authority`/`confidence`. `[VERIFIED]` both legs exit 0 and
recover 10/10 with `dispatch: "abi"` (§8.6, §8.7).

### S7 — 3-way selector reconciliation (owner: EX-07)
Compare four sets and require exact set equality:
1. solc `evm.methodIdentifiers` (compiler table, S4)
2. `js-sha3` keccak of the source signatures (S5)
3. EVMole probe, hex leg (S6)
4. EVMole probe, raw leg (S6)

Weak 5th leg (evidence, not equality): each selector's 4-byte pattern appears in
the runtime hex (`grep -o`/regex **count**, per QUALITY.md #13 — never `grep -c`).
`[VERIFIED]`: all four sets identical (10/10, symmetric differences empty);
byte-presence ≥1 for all ten; `42966c68` (burn) occurs twice — a raw-byte
collision, exactly why byte-presence is the weak leg.
Deliverable: `claims/c1/EX-07/reconciliation.txt` (the script + verbatim output).
Any missing/extra selector → §5 branch H4; do not silently widen the claim.

### S8 — controls (owner: EX-08)
1. **Empty control** `[VERIFIED]`: probe `KaidokuEmpty.runtime.hex hex` → 0
   functions in both `normalized_result` and `raw_result` (exit 0) — no
   false positives on dispatch-less real bytecode.
2. **Mutation control** `[VERIFIED]`: copy the runtime hex, change one selector
   constant (`a9059cbb` → `a9059cbc`), probe the mutant → recovered set contains
   `0xa9059cbc` and not `0xa9059cbb` (10/10). This proves recovery tracks the
   carrier bytes rather than any expected table.
Deliverable: `claims/c1/EX-08/control-receipt.txt` (both envelopes + ids
`ev_39e1526d…`, `ev_7628d241…`).

### S9 — rerun / id-stability (owner: EX-10)
Re-run the exact S6 hex command; require byte-identical `evidence_id`.
`[VERIFIED]`: `ev_911108c0…` both runs. Also record the path-variant result
(same bytes at `…/alt/…` → different id, F7) so the knowledge entry can state
the id domain honestly (QUALITY.md #14/#15). Deliverable:
`claims/c1/EX-10/rerun-receipt.txt`.

### S10 — custody post-pair + MANIFEST (owner: EX-11)
Re-capture the 5 custody paths; diff vs S1. Expected `[VERIFIED precondition]`:
zero drift for a short window, but **record whatever is measured** — in-window
operator churn has happened twice in arc2 (config.toml) and is a recorded
finding, not a failure. Then `sha256sum` every artifact in `claims/c1/*/` into
`claims/c1/EX-11/MANIFEST.txt` (arc2 receipt form:
`.ufo/waves/arc2-loop1-round10/receipts/MANIFEST.txt`).

### S11 — knowledge entry (owner: EX-12, patch text)
Draft `corpus/knowledge/2026-10-19-arc3-r1-evm-solc.md` as **patch text**
(`claims/c1/EX-12/knowledge-entry.patch.md`) — no seat writes `corpus/`. Content
must satisfy QUALITY.md's admission bar: pinned artifact identities (source +
carrier sha256s), evidence ids + the exact reproducing call, observation vs
inference labels (EVMole output = upstream inference), limitations (worker
limits, "SHA-256 ≠ keccak code hash", no RPC lookup, creation-code kind
unknown), version pins (solc 0.8.37 / REA 6.7.0 / EVMole 0.9.3), the synth
recipe retained (sources inline + settings), occurrence counts via `grep -o`.
The entry should contrast real-bytecode behavior with r3-07: on real solc output
`inferred_state_mutability` now carries signal (`view`/`nonpayable` etc.) where
the stubs reported `pure`.

### S12 — map token + after-measurement (owner: EX-13 + EX-15)
Line-neutral token append to the EVM row (`corpus/README.md:38`), as patch text
(`claims/c1/EX-13/map-token.patch.md`). Primary form — same physical line, no
row insert, no line-count change:

```
-| EVM | `2026-10-13-r3-evm-interface` | held — EVMole selectors recovered from synthetic dispatcher; positional encoding quirk |
+| EVM | `2026-10-13-r3-evm-interface`, `2026-10-19-arc3-r1-evm-solc` | held — EVMole selectors recovered from synthetic dispatcher (r3-07) and real solc-compiled runtime (arc3-r1); positional encoding quirk |
```

Then command A at the parent's records commit must read: `knowledge_files 82`,
`mapped 82`, `missing []`, `dangling []`, `citation_resolved_rules 13`,
`rule_blocks 13`, coverage/depth 10.0. "Prior 81 byte-identical" = the existing
81 files untouched (verify with `git diff --stat` limited to `corpus/knowledge`
showing only the one added file).

---

## 4. Per-executor task splits (proposed; parent dispatch assigns finally)

| Seat | Step | Deliverable under `claims/c1/<SEAT>/` |
|---|---|---|
| EX-01 | S1, S2 | `config-pre-pair.txt`, `install-receipt.txt` |
| EX-02 | S3 | `source-receipt.txt` (+ the two `.sol` copies) |
| EX-03 | S4 | `compile-receipt.txt` (+ carriers + `out.cleaned.json`) |
| EX-04 | S5 | `keccak-receipt.txt` |
| EX-05 | S6 hex | `probe-token-hex.json` |
| EX-06 | S6 raw | `probe-token-raw.json` |
| EX-07 | S7 | `reconciliation.txt` |
| EX-08 | S8 | `control-receipt.txt` |
| EX-09 | S8 mutation (independent) | `mutation-receipt.txt` |
| EX-10 | S9 | `rerun-receipt.txt` |
| EX-11 | S10 | `config-post-pair.txt`, `MANIFEST.txt` |
| EX-12 | S11 | `knowledge-entry.patch.md` |
| EX-13 | S12 | `map-token.patch.md` (+ optional PROVINCE patch text) |
| EX-14 | records | `LOG-entry.patch.md`, `SCORECARD-section.patch.md` |
| EX-15 | S12 measurement | `command-a-after.txt` (command A verbatim at the parent's records commit) |
| SC-1..3 | independently re-run S4+S6 and compare hashes/ids; SC-3 audits the honest-stop branches were exercised as written |
| RV-1..4 | re-derive command A before/after; verify carrier↔subject digest identity; verify K table independently of EX-04; review the knowledge entry against QUALITY.md's 16 criteria |
| CR-1, CR-2 | attacks: (a) "selectors recovered from a table, not bytes" → mutation control; (b) "the carriers are hand-edited, not compiler output" → CBOR metadata + creation code; (c) "the entry is a re-run dressed as a move" (r3 CR3 precedent) → require the real-bytecode delta (mutability/argument signal) to be the entry's core |
| VZ-1 | convergence: reconcile all seat artifacts, confirm the 3-way equality and the map-token patch is line-neutral |

**Parallelism:** S3→S4→S6 is the critical path (≈3 commands, seconds each).
S1/S2, S5, S7–S10, S11–S14 branch off it. Because every leg is sub-second, the
whole chain fits one wave; no long-running containment is needed (this is not a
PE-scale job).

---

## 5. Honest-stop branches (pre-written; each seals evidence, no costume retry)

- **H1 install failure** (S2): record verbatim; claim NOT verified; no
  substitute compiler.
- **H2 compile failure** (S4): a work item, not a stop — fix the source, but any
  source change invalidates the recorded sha256s and must be re-receipted.
- **H3 probe host-resource refusal** (S6): if the envelope is
  `execution_failure` with `Unknown system error -122 … write`, that is F4
  (quota), not a bytecode verdict. Declared one-time remedy: set `TMPDIR` to a
  disk-backed path and re-run. If it still fails, seal the refusal envelope and
  stop; do **not** claim a bytecode refusal.
- **H4 selector mismatch** (S7): K/K is the claim's bar. Any missing or extra
  selector → seal the reconciliation verbatim, report the typed difference, and
  the claim reports honest stop (partial recovery is recorded, never rounded).
  One declared second hypothesis is allowed **only** if the difference is typed
  and pre-registered before the re-run (e.g. optimizer on/off), and both
  envelopes are sealed.
- **H5 encoding mismatch** (S6): both legs must recover the identical set. A
  divergence is sealed as a finding (it contradicts r3-07's convergence result).
- **H6 custody drift** (S1/S10): record it; drift on operator-owned config is a
  recorded finding, not a seat failure; never repair.
- **H7 id instability** (S9): record; the knowledge entry then states the id
  domain as run-varying (with both ids) instead of claiming stability.
- **H8 records blocked** (S11–S14): patch text only; if the parent cannot land
  the token, the claim reports the measurement without the map move.

---

## 6. Records plan (parent-owned; seats deliver patch text)

1. `corpus/knowledge/2026-10-19-arc3-r1-evm-solc.md` — new file (EX-12 patch).
2. `corpus/README.md:38` — line-neutral token append (EX-13 patch).
3. `LOG.md` — one entry citing the evidence ids + receipt sha256s (EX-14 patch).
4. `SCORECARD.md` — new `arc3-loop1-round1` section with the before→after
   command A numbers (EX-14 patch).
5. Optional (parent decision): `PROVINCE.md:91-93` Frontier bullet annotation —
   "real solc-compiled bytecode" now held; keep the edit minimal and cite the
   new entry. `SKILL.md` EVM row needs no change (no new verb).
6. Receipts: parent copies `claims/c1/*/` artifacts into
   `$WD/receipts/` (install receipt, compile receipt, probe envelopes, control
   envelopes, custody pairs, MANIFEST) and commits them.

---

## 7. Risks

1. **`/tmp` quota (highest operational risk).** Every seat in this wave will hit
   F4 if it uses `/tmp`. Mitigation: scratch + `TMPDIR` under `/var/tmp/<seat>`;
   record the deviation from the dispatch's "/tmp scratch" wording in the seat
   report and the round report (precedent: arc2-loop1-round4, "seats relocated,
   no evidence lost").
2. **Contract drift between executors.** Mitigation: sources are inline in this
   plan + sha256-pinned; the expected runtime sha256 (`543cdc0d…`) is a hard
   check.
3. **`solcjs` name / `>>>` stdout line (F2/F3)** — silent failure modes if a
   seat copies the obvious command. Both are in the plan's exact commands.
4. **Claim inflation.** The temptation is to report "EVM frontier closed
   entirely" — the claim covers runtime selector recovery; creation-code `kind`
   stays unknown (F9) and no signature DB exists. The knowledge entry must scope
   exactly what was shown.
5. **Receipt-vs-artifact duplication.** Install prefix lives under `$WD/tools/`;
   the prefix must **not** be committed wholesale (node_modules). Only the
   receipt (name/version/sha256) is committed; note this explicitly or the
   integration commit will balloon.
6. **Custody scope**: the 5-path pair excludes npm cache (by the frozen rule);
   the install itself is receipted instead — say so in the receipt.

---

## 8. Planner de-risk evidence (raw, 2026-10-19)

All commands below were run by PL-1 against `/var/tmp/pl1` copies; `/tmp` is
unusable (F4). Scratch is left in place for the wave's duration and is cleaned
by the planner at close (or by the parent if the wave outlives this seat).

**8.1 command A at HEAD** — see §1 JSON (recipe from `SCORECARD.md:86-124`).

**8.2 registry + install**
```
npm view solc version            → 0.8.37
npm view solc dist.tarball       → https://registry.npmjs.org/solc/-/solc-0.8.37.tgz
npm view solc dist.integrity     → sha512-ieUYdPDRGNKMsZpCfi9tY64Q+ASoL8tyhLuvf9cFiqDs+6ijlx8Wn2CRi0N71AlCvRx0V092rlUYu3b3PuxWlA==
npm install --prefix /var/tmp/pl1/tools solc@0.8.37 --no-audit --no-fund
  → "added 8 packages in 164ms"; npm ls → solc@0.8.37
node_modules/.bin/               → solcjs -> ../solc/solc.js ; semver
solcjs --version                 → 0.8.37+commit.f401782d.Emscripten.clang
npx -y rea-agents@6.7.0 --version → 6.7.0
```

**8.3 compile + independent keccak**
```
sha256sum KaidokuToken.sol → 5910441fdeddcf5bb9599cc95d097969724dda78dfca12074cf5981cbf230830
sha256sum KaidokuEmpty.sol → a74fe10e56a979432658edcdc4a443bd957fe1b44d4bb604af933507c9973a92
solcjs --standard-json < input.json > out.json ; exit 0; stdout carries a leading ">>> Cannot retry compilation with SMT…" line
KaidokuToken: runtime 3858 B 543cdc0d…, creation 5017 B e73372c2…, K = 10
KaidokuEmpty: runtime   62 B 7f0c2792…, creation  216 B d2493b7a…, K = 0
keccak (js-sha3) 10/10 == solc methodIdentifiers (symmetric diff empty)
```

**8.4 `/tmp` quota**
```
df -h /tmp            → tmpfs 16G 13G used 3.1G avail 80%
df -i /tmp            → 896064/1048576 inodes
findmnt -no OPTIONS /tmp → rw,nosuid,nodev,nr_inodes=1048576,inode64,huge=advise,usrquota
echo test > /tmp/pl1-quota-probe.txt → "write error: Disk quota exceeded"
```

**8.5 probe without disk-backed TMPDIR (the failure mode)**
```
npx -y rea-agents@6.7.0 inspect-evm-interface /var/tmp/pl1/KaidokuToken.runtime.hex hex --format json
  exit=1
  {"code":"execution_failure", … "diagnostics":{"phase":"worker","path":"…/KaidokuToken.runtime.hex",
   "configured_resource_limits":{"addressSpaceBytes":3221225472,"cpuSeconds":30,"fileSizeBytes":16777216},
   "reason":"Unknown system error -122: Unknown system error -122, write"}}
```

**8.6 probe with TMPDIR=/var/tmp/pl1/reatmp (hex leg)**
```
exit=0; evidence_id ev_911108c0270ce68d1bda9566148283a6eec008d27428d6606e399e72962d0bad
normalized_result.functions: 10; fn[0] = {selector:"0x06fdde03", bytecode_offset:160,
  dispatch:"abi", inferred_arguments:"", inferred_state_mutability:"view"}
subject.digest.sha256 = 021a5f6fc558f2e48fef04a2af0e15d203d5ceb2e8b397672665850f99d14841
  = sha256(KaidokuToken.runtime.hex)
authority "shipped-artifact"; confidence "inferred"; predicate_type "rea.analysis"
```

**8.7 raw leg** — exit 0, 10/10, `ev_80d075d313f87c01a71d9b9fa82b6c538c75970b37c39822210922e2fc266d11`,
subject digest `543cdc0d…` = sha256(`KaidokuToken.runtime.bin`); hex-decoded bytes
sha256 `543cdc0d…` = raw bytes sha256 (carrier encodings carry identical bytecode).

**8.8 controls** — empty contract: exit 0, 0/0 functions, `ev_39e1526d…`;
mutant (`a9059cbb`→`a9059cbc`): exit 0, 10/10 including `0xa9059cbc`,
`ev_7628d241…`.

**8.9 id domain** — same bytes, different path (`/var/tmp/pl1/alt/…`) →
`ev_62e889cf31d2eb6c4265539654ac12b72e7f6d7c46677666454736cfd81f102d` ≠ `ev_911108c0…`;
identical (content, path, params) re-run → `ev_911108c0…` again.

**8.10 creation code** — `ev_4643108825c84bb9e4ae04eacc4150092105dca8cb4521dae89373a003debae3`,
0 functions, `metadata.kind` null.

**8.11 CBOR trailer** — `raw_result.metadata` = `{bytecodeOffset: 3805, cborLength: 51,
entries:[{key:"ipfs", …},{key:"solc", value:{type:"bytes", value:"000825"}}]}` (0x000825 = 0.8.37).

**8.12 3-way reconciliation output** (`reconcile.py`, verbatim):
```
K (solc methodIdentifiers): 10
solc == keccak (signature-derived): True | symmetric diff: set()
probe hex == solc: True | symmetric diff: set()
probe raw == solc: True | symmetric diff: set()
probe hex == probe raw: True
byte-presence counts in runtime hex: {'06fdde03':1,'095ea7b3':1,'18160ddd':1,'23b872dd':1,
 '40c10f19':1,'42966c68':2,'70a08231':1,'8da5cb5b':1,'a9059cbb':1,'dd62ed3e':1}
selectors absent from runtime bytes: []
missing from probe: [] | extra in probe: []
```

---

## 9. Integration note (planner, 2026-10-19T10:07Z) — plan vs landed reality

The chain ran while this plan was being written. State at the planner's close,
so later readers can separate what the plan predicted from what landed:

- **Install (S2) LANDED by EX-02** — prefix `$WD/tools/solc-prefix/`,
  `npm install … solc@0.8.37` → "added 8 packages in 402ms", bin `solcjs`,
  tarball sha256 `0e1a1ab6d12c37f5503271b2c4679cd433459c884851920d148d6fb154575a51`
  (EX-02 re-fetched the tarball and matched the registry integrity — stronger
  than this plan's minimum receipt form). Evidence:
  `claims/c1/EX-02/install-receipt.txt`.
- **Custody pre-pair (S1) LANDED** — `claims/c1/EX-01/config-pre-pair.txt`,
  `claims/c1/EX-02/custody-pre-pair.txt`, chain staging
  `claims/c1/receipts/config-pre-pair.txt`.
- **Before-measurement (baseline of §1) LANDED by EX-11** — command A at
  `e845c2b` → 81/81, 13/13, missing/dangling empty: byte-identical to the
  planner's own run. Evidence: `claims/c1/EX-11/command-A-before.txt`.
- **Probe legs (S6) LANDED by EX-05/EX-06 on a *different, independently
  authored* contract** (`KdxToken.sol`, K = 6, scratch `/dev/shm/ex06`, `TMPDIR`
  set; EX-06's `repro.sh` also reproduces the EDQUOT failure with `TMPDIR`
  unset — an independent corroboration of F4/F5). The chain's multi-contract
  evidence (KdxToken K=6 + RV-2's token) **supersedes this plan's single-source
  recommendation**: reconciling independently authored contracts is strictly
  stronger than the three-way check on one contract.
- **Reconciliation (S7) LANDED by EX-07** — seven sources agree 6/6 (M1 chain,
  M1 eq-sites, ABI, PLANTED, probe hex, probe raw, M2 keccak scan) with
  `VERDICT: ALL SOURCES AGREE`; probe offsets equal the parsed JUMPDEST
  destinations; the probe's code-digest pin matches EX-07's own sha256.
  Evidence: `claims/c1/EX-07/reconciliation-run.txt`.
- **Hardening legs contributed by this plan, vs. what the chain had landed at
  close**: (a) the carrier-**mutation** control (§8.8 — the mutant selector
  `a9059cbc` appears in no other chain artifact; EX-09's mutation tests target
  the *envelope* for id re-derivation, a different attack); (b) a **compiled
  dispatch-less contract** control (62-byte real solc runtime → 0/0 — EX-08's
  negative controls use an empty file / non-bytecode / ELF magic, not a compiled
  contract); (c) the CBOR-trailer reading as solc-origin proof (`solc 000825` =
  0.8.37 — the raw `metadata` is captured by EX-05/EX-06, the version decode
  appears only here). **Corroborated, not unique**: the path-variant id test
  (§8.9/F7) matches EX-05's `kdx.raw.renamed.json` (same bytes, renamed file →
  different id) and the creation-blob leg (F9) matches EX-05's
  `kdx-creation.raw.json` (0 functions). The round record may cite (a)-(c) from
  §8 with the planner's evidence ids, or a seat re-runs them on the chain's
  KdxToken (≈4 probes, seconds each).
- **Divergence to record once**: `/tmp` is unusable for every seat this wave
  (F4). Executors used `/dev/shm/exNN` (RAM-backed) and `/var/tmp/…`
  (disk-backed); both satisfy the lane lesson's requirement (never the
  quota-full tmpfs). The round report should name the substitution once, not
  per seat.
