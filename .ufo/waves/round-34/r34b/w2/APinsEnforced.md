# APinsEnforced — the enforced pin container under the lane's own freeze gate (R34-C2, r34b w2)

| Field | Value |
|---|---|
| Seat | `L1Kaidoku34-2.APinsEnforced` (leaf, no subagent dispatch) |
| Lane | `/home/vgpnk/Projects/shokunin/kaidoku-shokunin` (read-only; only `git log/show/ls-tree/grep/diff` and `python3 -I -B` reads) |
| Scratch | `/fast/scratch/hyaku/kaidoku-r34b/w2/APinsEnforced/` (three `--shared` clones + captured outputs) |
| Lane tip at start | `cd75b92e583735729546b0ea3b250f2df6d0652a` (`jj-lane.sh state`, 07:28Z: `local=remote=cd75b92e`, head detached) |
| Lane tip at 07:33:45Z | `66b840274390d0868c913a544947f9eb40a4ffe6` (parent `cd75b92e`; landed the w1 reports + record while this seat ran) |
| Stop record | `.ufo/waves/round-34/r34b/claim-stop.json` (landed `cd75b92e`) |
| Tooling installed | **none** (no `uv`/`npx`/binary; nothing needed) |
| Lane files written | this report only |

Scope executed exactly as assigned: run the lane's freeze gate over the new container, run it over the
frozen `claims.json`, report exit / pin count / findings — plus bounded attack probes in scratch on what
that CLEAN does and does not bind. No claim reopened, no frozen instrument, corpus, scorecard or score touched.

---

## 1. Primary runs

### A1 — the new container, tip at task start

```
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 \
  --claims .ufo/waves/round-34/r34b/instruments.json \
  --rev cd75b92e583735729546b0ea3b250f2df6d0652a
```
**exit 0** at `2026-10-25T07:28:31Z`. 26 `ok` rows, every one `commits_after_freeze=0`; final line:

```
freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=cd75b92e583735729546b0ea3b250f2df6d0652a
```

### A2 — the same container, tip after the record landed (07:32:25Z)

```
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 \
  --claims .ufo/waves/round-34/r34b/instruments.json \
  --rev 66b840274390d0868c913a544947f9eb40a4ffe6
```
**exit 0** at `2026-10-25T07:33:45Z` →

```
freeze-integrity: CLEAN pins=26 freeze=b917ea64ebbe rev=66b840274390d0868c913a544947f9eb40a4ffe6
```

### B — the frozen `claims.json` (schema defect)

```
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 \
  --claims .ufo/waves/round-34/r34b/claims.json --rev cd75b92e583735729546b0ea3b250f2df6d0652a
```
**exit 3** at `2026-10-25T07:29:00Z` →

```
freeze-integrity: ERROR schema code=instruments_missing claims=.ufo/waves/round-34/r34b/claims.json where=instruments
```

Cause: `tools/round-34/freeze-integrity.py:92-93` requires a top-level `instruments` object; the frozen
document keeps its 26 pins at `.ufo/waves/round-34/r34b/claims.json:23` (`claims[0].pins`). This is
exactly the defect the stop discloses as record defect **F1**, reproduced on the frozen bytes.

### C — the container pointed at the *claim's* freeze revision

```
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 \
  --claims .ufo/waves/round-34/r34b/instruments.json \
  --rev c79bbe7b0959132b9873ff3431cf5eb313b58b33
```
**exit 2** at `2026-10-25T07:29:32Z` →

```
freeze-integrity: ERROR no commit adds .ufo/waves/round-34/r34b/instruments.json at c79bbe7b0959132b9873ff3431cf5eb313b58b33
```

(The tool finds the freeze commit as the first commit that *adds* the `--claims` path, `freeze-integrity.py:439-445`;
the container was added after the claim freeze, so it is invisible at `c79bbe7b`.)

### D — control: the sibling round-34 pin map that does pin the verifier

```
python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --rev cd75b92e583735729546b0ea3b250f2df6d0652a
```
**exit 0** at `2026-10-25T07:32:58Z` → `freeze-integrity: CLEAN pins=21 freeze=54a87a51a865 rev=cd75b92e…`
(merges 4 `instruments` + 17 `frozen_inputs`; `tools/round-34/freeze-integrity.py` is pinned there as
`fe955c5789123a94a575a2a2e29e2fac8702889817417b4d9892e91bc8a40138`).

**Pin count: 26.** Exit 0 on both tips, exit 3 on the frozen claims file, exit 2 at the claim freeze revision.

---

## 2. What the CLEAN actually certifies (pin fidelity measurements)

Read-only `git show <rev>:<path> | sha256` loop over all 26 pins (script inline, exit 0):

| revision | pins compared | mismatches |
|---|---|---|
| `c79bbe7b…` (claim freeze) | 26 | **0** |
| `b917ea64…` (container landing) | 26 | **0** |
| `cd75b92e…` (stop tip) | 26 | **0** |

- `instruments.json` `instruments` map **==** `claims[0].pins` byte-for-byte in content (26 keys, identical digests).
- Container blob `sha256 224cc44124c52c4bf1135a5994c8366590887334317bf5eff22b70ffc5a8a6b6` identical at
  `b917ea64` and `cd75b92e` and in the worktree.
- Declared `frozen_claims_sha256 de3afbfb…facd828` equals the sha256 of `claims.json` at `c79bbe7b` and in the worktree.
- Tree coverage: `tools/round-34` has 29 files at both revisions; the 3 unpinned are the **R34-C1**
  instruments (`elf-version-needs.py`, `freeze-integrity.py`, `version-needs-counter.py`). No pinned path is absent.

So the container is **content-faithful**: it did not rewrite or re-derive any digest. The stop's record
defect F1 is a container/schema relocation, and that part of the stop survives this audit.

---

## 3. Findings

### F1 — CONFIRMED (stop's own F1): frozen `claims.json` is unreadable to the lane gate
Exit 3 `instruments_missing` (run B), cause at `freeze-integrity.py:92-93` vs `claims.json:23`. No new claim.

### F2 — MATERIAL (new): the CLEAN certifies a window that starts at the container's own landing commit, not at the claim freeze
`freeze=b917ea64ebbe` is the commit that added `instruments.json` (04:22:30-03:00 = 07:22:30Z), nine
minutes **after** the claim freeze `c79bbe7b` (07:13:11Z). The gate then asserts two things: pins read
from `b917ea64` equal tip blobs, and no commit in `b917ea64..rev` touched a pinned path
(`freeze-integrity.py:456-462`). Both are true and neither is the freeze property the claim needs.
At the claim revision the same argv exits 2 (run C). The container therefore cannot produce any receipt
whose `freeze` is `c79bbe7b`; the freeze of record is only reachable through the *frozen claims blob*, which
the same tool rejects (run B).

The only receipt line the landed record quotes is
`.ufo/waves/round-34/r34b/w1/ScribeSkillRegistry.md:111` (row E16), and it used
`--rev b917ea64` — i.e. `freeze == rev`, a zero-width history window in which `commits_after_freeze=0`
is arithmetically forced. The first **non-degenerate** receipts (`--rev cd75b92e…`, `--rev 66b84027…`)
are runs A1/A2 in this report; nothing in the lane retained them before this wave.

### F3 — MATERIAL (new): the container is not self-verifying; its own bytes and metadata are forgeable without the gate noticing
Probe P3 (scratch clone at tip, one commit `635325be07b5…`, `2026-10-25T07:32:05Z`): added a 27th pin
`bin/forged-pin.py = 1*64` and set `frozen_claims_sha256` to 64 zeros, committed, then ran A1's argv with
`--rev HEAD` → **exit 0**, `freeze-integrity: CLEAN pins=26`. Two causes:

1. pins are read from the **freeze** blob (`freeze-integrity.py:445`), so a post-landing edit of the
   container is by design not re-read — but then nothing compares the tip container to the freeze container,
   and the printed `pins=26` cannot be tied to the tip document a downstream reader opens;
2. `frozen_claims_sha256` is read by **no** instrument (`grep -rn "frozen_claims_sha256\|instruments.json"
   tools/round-34` → no hits), and nothing pins the container: no `claims.json` in the lane lists
   `.ufo/waves/round-34/r34b/instruments.json` as a pin.

Consequence: the "binding" from container → frozen claims file is a comment, not a check. A reviewer cannot
distinguish the landed container from a forged one using lane instruments alone.

### F4 — MEDIUM (new): worktree drift is invisible; the gate is history-only
Probe P2 (scratch clone, `2026-10-25T07:32:04Z`): appended a line to `tools/round-34/replay-gate.py` in the
worktree only (file sha256 `febbbdf4b23f…` vs pinned `8fa94b2332a6…`), ran A1's argv with `--rev HEAD` →
**exit 0**, `ok … sha=8fa94b2332a6`, `CLEAN pins=26`. The gate reads blobs at `--rev`
(`freeze-integrity.py:456`), never the worktree, so any execution that consumes on-disk instrument bytes
(the gate's own production path) is outside this receipt.

### F5 — LOW (new): the verifier is outside the 26-pin map; no automated caller exists
The 3 files under `tools/round-34` that the container does not pin include `freeze-integrity.py` itself.
Its bytes are covered only by the *separate* `.ufo/waves/round-34/claims.json` map (run D, CLEAN pins=21),
and `grep -rn "freeze-integrity" --include='*.py' --include='*.sh' tools scripts` finds **no** runner that
invokes it. Enforcement is therefore entirely procedural: every receipt in the lane, including E16 and
this wave's, is a seat typing the command.

### F6 — POSITIVE CONTROL (kept): the gate is not vacuous on committed drift
Probe P1 (scratch clone at tip, `2026-10-25T07:32:03Z`): appended a line to `tools/round-34/replay-gate.py`
and committed (`ac50343f7f5a…`), ran A1's argv with `--rev HEAD` → **exit 1**:

```
FAIL	tools/round-34/replay-gate.py	sha=62639f8c7754	commits_after_freeze=ac50343f
freeze-integrity: FAIL pins=26 changed=1 freeze=b917ea64ebbe rev=HEAD
```

So the instrument does catch a committed post-freeze edit of a pinned path. It is a real (narrow) verifier,
not a vacuous one — the attack is on the word **enforced**, not on its correctness.

### F7 — unchanged by the repair: no counted run hashes anything
`grep -c hashlib` → `c2-shortcut-gate-counter.py: 0`, `replay-gate.py: 0` (`mini-counter.py: 3` are
opaque-path naming). The counter never invokes `freeze-integrity.py` and never opens `instruments.json`
(grep in §F3). The container relocates the pins to a shape the lane gate accepts; it does not add the
runtime binding that stop finding F1 and w1 `SentinelContainment.md` C6 name.

---

## 4. Effect on the stop

The stop is **not** falsified by this seat. Its F1 disclosure is reproduced verbatim (run B), its pin
content is honest (26/26 at three revisions), and its kill rule does not depend on the container being
stronger than it is. What the audit does falsify is the *strength of the repair citation*:

- "`instruments.json` (byte-identical 26-pin container) + freeze-integrity receipt over it" — the container
  is byte-identical in content (true), but the receipt was **not in history** at the stop commit: no commit
  before `66b84027` contains `CLEAN pins=26` (`git log --all -S"CLEAN pins=26"` first hits `66b84027` /
  `98bcb34a`, both children of the stop commit, and the hit is a quoted line in `w1/ScribeSkillRegistry.md:111`,
  not an artifact under `after/`). At `cd75b92e` the `after/` tree holds only the counter receipts.
- That quoted receipt is over `--rev b917ea64` — the degenerate zero-width window (§F2).
- The container cannot be evaluated at the claim freeze at all (§F2, exit 2), and it is forgeable and
  worktree-blind without the gate noticing (§F3, §F4).

No score, capability row or claim state is changed by this report; I award none and reopen none.

---

## 5. Command ledger (exact argv, exit, UTC)

| # | argv (cwd = lane unless noted) | exit | UTC |
|---|---|---|---|
| A1 | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --claims .ufo/waves/round-34/r34b/instruments.json --rev cd75b92e583735729546b0ea3b250f2df6d0652a` | 0 | 07:28:31Z |
| B | same, `--claims .ufo/waves/round-34/r34b/claims.json` | 3 | 07:29:00Z |
| C | A1 with `--rev c79bbe7b0959132b9873ff3431cf5eb313b58b33` | 2 | 07:29:32Z |
| D | `python3 -I -B tools/round-34/freeze-integrity.py --root . --round 34 --rev cd75b92e…` | 0 | 07:32:58Z |
| A2 | A1 with `--rev 66b840274390d0868c913a544947f9eb40a4ffe6` | 0 | 07:33:45Z |
| P0 | `git clone -q --shared <lane> $S/p0 && git checkout -q cd75b92e…`; A1 argv with `--rev HEAD`, output captured to `p0.out` | 0 | 07:35:10Z |
| P1 | p1: append line to `tools/round-34/replay-gate.py`; `git -c user.name=probe -c user.email=probe@example.invalid -c commit.gpgsign=false commit -q -am …`; gate `--rev HEAD` | 1 | 07:32:03Z |
| P2 | p2 (fresh clone): worktree-only append to `replay-gate.py`; gate `--rev HEAD` | 0 | 07:32:04Z |
| P3 | p3 (fresh clone): rewrite tip container (forged pin + zeroed `frozen_claims_sha256`), commit; gate `--rev HEAD` | 0 | 07:32:05Z |
| M | pin-fidelity loop (`git show <rev>:<path>` → sha256, 3 revs × 26 paths) | 0 | 07:28:3x–07:29:0xZ |

Scratch contents (only these were created): `APinsEnforced/p0/`, `p1/`, `p2/`, `p3/` (`--shared` clones),
`p0.out`, `p1.out`, `p2.out`, `p3.out`, `container-at-newtip.out`, `round34-claims-gate.out`.

## 6. Evidence pointers

- Container: `.ufo/waves/round-34/r34b/instruments.json` (26 pins, 224cc441…).
- Frozen pins: `.ufo/waves/round-34/r34b/claims.json:23`; sha256 `de3afbfb…facd828`.
- Gate semantics: `tools/round-34/freeze-integrity.py:84-98` (schema), `:439-445` (freeze-commit resolution),
  `:456-462` (blob-at-rev + history window).
- Stop record: `.ufo/waves/round-34/r34b/claim-stop.json` (`record_defects_disclosed` F1/F5, `kill_rule_applied`).
- Only quoted receipt: `.ufo/waves/round-34/r34b/w1/ScribeSkillRegistry.md:111` (E16, `--rev b917ea64`).
- w1 corroboration: `w1/RevClaimsVsInstruments.md` §4 F1 (26/26 match at c79bbe7b), `w1/SentinelContainment.md` C6.

**VERDICT: the enforced pin container passes the lane freeze gate (exit 0, pins=26, freeze=b917ea64ebbe at both tips), the frozen claims.json fails it as disclosed (exit 3 instruments_missing) and the container cannot certify the claim freeze (exit 2 at c79bbe7b); the repair is content-honest and non-vacuous on committed drift but is documentary, self-unverified and worktree-blind, so it does not convert the stop's F1 into enforcement — the stop stands, no score or claim moves.**
