# ScoutS320 — R95-C1 / R95-C2 reproduction and attack (scratch clone at 4bda1d1d)

Seat: `ScoutS320` (scout). Lane read-only; all runs in
`/fast/scratch/hyaku/kaidoku-r95/ScoutS320/clone` (a `--shared` clone checked out at the declaration commit
`4bda1d1dd3788973f10e61212b70df18b3b14ea0`), scratch deleted before yield.

Fixture assertion before the first commit in the clone:

```
git -C "$S/clone" rev-parse --show-toplevel → /fast/scratch/hyaku/kaidoku-r95/ScoutS320/clone   ✔
git -C "$S/clone" rev-parse HEAD            → 4bda1d1dd3788973f10e61212b70df18b3b14ea0
```

Frozen label used everywhere:
`repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2`

---

## 1 — R95-C1: the three frozen counting commands, reproduced

### 1.1 Command 1 — the forgery battery → **exit 0, target met**

```
python3 -I -B tools/round-95/c1-forgery-refusal.py --root . \
  --fixtures .ufo/waves/round-95/forgery --old-prefix forge \
  --old-counter tools/round-94/c1-receipt-agreement.py \
  --honest-dir .ufo/waves/round-95/l1/scores --honest-prefix honest \
  --world-rev b5331db1fb0ce0bf93695ce1730cf831effef6a9 \
  --instrument-rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 \
  --expect '<frozen label>' --json-out $S/out/c1-forgery3.json
```
→ **EXIT=0**, stdout last line `forgeries refused 4 of 4; before admits True; honest accepted True`.

| forgery | refused | reasons | expected | match |
|---|---|---|---|---|
| pos | yes | `['label-not-frozen']` | `label-not-frozen` | ✔ |
| F1 | yes | `['label-not-recomputed']` | `label-not-recomputed` | ✔ |
| F2 | yes | `['revision-not-bound']` | `revision-not-bound` | ✔ |
| F3 | yes | `['pins-not-bound']` | `pins-not-bound` | ✔ |

before leg: `{'admits': True, 'counts': {'agree': 4, 'predicted': 4, 'valid': 4}, 'exit': 0, 'met': True}`.
honest leg: `{'exit': 0, 'met': True, 'rows': [{'agree': True, 'predicted': True, 'reasons': [], 'valid': True}]}`.

**My receipt is byte-identical to the L1's committed receipt** (`diff` of the two JSON files → empty). The L1's
receipt is `.ufo/waves/round-95/l1/scores/c1-forgery-at-4bda1d1d….json` (untracked in the worktree).

**One operational caveat the L1 should know (not a claim defect):** the command's honest leg reads
`.ufo/waves/round-95/l1/scores/honest-pos.{json,stdout,rc}`, and those three files are **untracked** — they are
not in the declaration commit (`git ls-tree -r HEAD -- .ufo/waves/round-95/l1/scores/` lists only the two
`s320-open2-fetch*.html` files). In a clean clone the honest leg therefore finds no honest triple and the battery
exits **1** with `honest accepted False` / `not-valid`. My first run reproduced exactly that (exit 1, honest leg
`{'exit': 1, 'met': false, 'rows': [{'agree': False, 'predicted': False, 'reasons': ['not-valid'], ...}]}`).
After producing the honest triple (command 2 below) into the honest dir, the same command exits **0**.
⇒ **Ordering matters: the honest v5 run (command 2) must precede the battery (command 1)**, or the honest triple
must be committed. Reproduced twice: with my own honest triple and with the L1's honest triple copied in from the
worktree — both exit 0 with identical receipts.

### 1.2 Command 2 — the honest v5 positive control → **exit 0, `selfverify ok=True reasons=0`**

```
python3 -I -B tools/round-95/stop-boundary-repair-battery-v5.py --root . \
  --repair-cmd tools/round-92/upx-stop-boundary-search-repair.py --work "$S/work" \
  --rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --expect '<frozen label>' \
  --json-out "$S/out/honest-pos.json" > "$S/out/honest-pos.stdout" 2> "$S/out/honest-pos.stderr"
```
→ **EXIT=0**, stdout:
```
selfverify ok=True reasons=0
repaired 12 of 12; wrong 0; unsafe 0; intact 6 of 6; far-refused 12 of 12; fresh-roundtrip 2 of 2 met True exit 0
```
stderr empty (0 bytes). Receipt keys include `met_target True`, `label` == `expect` == frozen label,
`revision` = `4bda1d1d…`, `counter_sha256` = `6fc81208…` (the pinned v5 digest),
`verdict_sha256` = `60026511…` (the pinned v3 digest). No temp file is left in the receipt's directory
(`ls` of the out dir shows only `honest.json`, `honest.stdout`, `honest.stderr`).

### 1.3 Command 3 — the symlink probe → **exit 0, `victim_intact true`, `receipt_valid true`**

```
python3 -I -B tools/round-95/symlink-probe.py --root . \
  --writer tools/round-95/stop-boundary-repair-battery-v5.py \
  --repair-cmd .ufo/waves/round-93/controls/identity_noop.py --work "$S/work" \
  --rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --expect '<frozen label>' \
  --json-out "$S/out/c1-symlink.json"
```
→ **EXIT=0**; `met true`, `verdict "hardened"`, `victim_intact true`, `receipt_valid true`,
`tmp_is_symlink true`, `tmp_left true`, `writer_rc 1`, `writer_sha256 6fc81208…`.

**Before-state reproduced too:** the same probe against the pinned v4 writer
(`--writer tools/round-94/stop-boundary-repair-battery-v4.py`) exits **1** with
`verdict "followed-symlink"`, `victim_intact false`, `receipt_valid true`, `writer_sha256 c41d54d7…` — i.e. the
SentinelWrite F1 mechanism reproduces on this host, and the committed pre-receipt
`.ufo/waves/round-95/pre/c1-symlink-v4-at-base.json` matches (same fields, `revision` = base).

### 1.4 Frozen pin check at 4bda1d1d — **all pins OK**

```
sha256sum -c /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-95/pins.sha256
```
→ every listed file `OK` (v5 `6fc81208…`, v2 `ca7d213a…`, battery `8e43d7cf…`, probe `e07ff669…`, frozen r94 counter
`c41d54d7…`, frozen r94 agreement `dc384a44…`, frozen v3 verdict `60026511…`, frozen r92 repair `ce1b1769…`,
frozen r93 `identity_noop.py` `518422b5…`, the two manifests, and all twelve forgery fixture files).
Kill-rule diff clause is evaluable and currently clean:
`git diff --stat 4bda1d1d HEAD -- tools/round-95 tools/round-94 tools/round-93` → **empty** (exit 0).

---

## 2 — Attacks on the R95-C1 instrument (all in scratch, all observed)

### 2.1 The strengthened instrument refuses more than the four declared forgeries

Fixtures authored in scratch from the honest receipt, each scored with
`tools/round-95/c1-agreement-v2.py --case <name>` (the case name must be one of the four
`PREDICTED` keys `pos|F1|F2|F3`; an unknown name raises `KeyError` and exits 1 — an input-validation nit, not a
claim defect):

| attack fixture | change vs the honest receipt | v2 verdict | reasons |
|---|---|---|---|
| `atk-pos` | `revision` set to the base rev (a full, valid, wrong revision) | **exit 1** | `revision-not-bound` |
| `atk-F1` | `counter_sha256` = 64 zeros | **exit 1** | `predicted-mismatch`, `pins-not-bound` |
| `atk-F2` | `verdict_sha256` = 64 f's | **exit 1** | `predicted-mismatch`, `pins-not-bound` |
| `atk-F3` | wholly re-authored but self-consistent (labels/stdout/rc/pins all agree) | **exit 1** | `predicted-mismatch` |

The `atk-pos` result is the load-bearing one: a **full-length** revision that is nonetheless not the measured
tree is refused with the typed reason `revision-not-bound` — M94-f's short-`--rev` shape is a special case of a
stronger rule.

### 2.2 The declared named limit is real and measurable

The declaration states (R95-C1 "Named limits"): *"a wholly re-authored triple whose stdout/rc/pins/revision/label
all consistently describe the honest world at the honest revision is indistinguishable from an honest capture at
the byte level, and catching it needs independent stdout/rc custody, not another receipt field."*

**Reproduced.** A triple copied byte-for-byte from the honest receipt and re-emitted under a different file stem
(`nl-pos`) is **accepted** by v2: `met true`, `reasons []`, exit **0**
(`repro/named-limit-reauthored-triple.json`). This confirms the limit is a real bound of the instrument, not a
hedge — and it confirms the claim text is honest about it. The instrument's `predicted-mismatch` reason is the
only thing that fires when such a triple is filed under a forgery name; filed under `pos` it is indistinguishable.

### 2.3 The hardened writer's mechanism, verified at the syscall level

Host probes (scratch only):

| probe | observed |
|---|---|
| `os.open(planted_symlink, O_WRONLY)` (the v4 shape) | **follows the link** — the victim file's content was replaced |
| `tempfile.mkstemp(dir=…, prefix=…, suffix=".tmp")` (the v5 shape) | creates a **fresh unique** name; the planted `<out>.tmp` is never touched |
| `os.open(planted_symlink, O_WRONLY\|O_NOFOLLOW)` | **OSError errno 40 ELOOP** — the victim file is untouched |
| `os.open(planted_symlink, O_WRONLY\|O_CREAT\|O_EXCL)` | **OSError errno 17 EEXIST** — victim untouched |
| `os.open(planted_symlink, O_WRONLY\|O_CREAT\|O_EXCL\|O_NOFOLLOW)` | **OSError errno 17 EEXIST** — victim untouched |

This is the `open(2)` `O_NOFOLLOW` ground the S320 knowledge entry cites, measured on this host: the trailing
component being a symbolic link makes `open` fail with `ELOOP` (errno 40) rather than following the link. The v5
writer does not rely on `O_NOFOLLOW` — it relies on `mkstemp`'s unique name plus `O_EXCL` semantics inside
`mkstemp`, and `os.replace` for the final rename — which is why the planted `<json-out>.tmp` is inert.

---

## 3 — R95-C2: the depth claim, before-state and a candidate

### 3.1 Before-state at the declaration commit — reproduced

```
python3 -I -B tools/round-93/craft-citation-semantic.py --root . \
  --manifest .ufo/waves/round-95/manifests/block34-after.json --block 34 \
  --rev 4bda1d1dd3788973f10e61212b70df18b3b14ea0 --json-out $S/out/c2-block34-decl.json
```
→ **EXIT=1**, `failing exit 1 / - block 34 missing (craft has 33 blocks)` — matches the committed pre-receipt
`.ufo/waves/round-95/pre/c2-base-block34-after-manifest.json` exactly.

```
python3 -I -B tools/round-89/depth-blocks-v2.py --root . --rev 4bda1d1d… --expect-blocks 34
```
→ **EXIT=1**, `blocks 33 resolved 33 expect 34 unresolved 0 met=False exit=1`
(matches `pre/c2-base-depth-v2.txt`).

```
python3 -I -B tools/round-91/depth-blocks-v3.py --root . --rev 4bda1d1d… --expect-blocks 34 --shape-from 34
```
→ **EXIT=1**, `blocks 33, resolved 33, required-shaped 0/0 expect 34 shaped_required 0/0 unresolved 0 met=False exit=1`
(matches `pre/c2-base-depth-v3.txt`).

The junk manifest at the declaration commit also exits 1 (block absent), so the rubber-stamp control is
**not** yet discriminating — it only becomes meaningful once block 34 exists. That is the important gap to close.

### 3.2 A candidate block 34 + QUALITY 191/192 (scratch clone only) makes the whole frozen set green

I drafted, **in the scratch clone only**, a candidate block 34 (4 body rows × 4 cells, marker
`receipt-world-binding v1`, criteria `QUALITY 191` / `QUALITY 192`) and two candidate QUALITY rows carrying the
frozen keyword atoms, plus a stub knowledge file, then ran the four frozen C2 commands at that scratch commit:

| frozen command | at declaration commit (before) | at the scratch candidate |
|---|---|---|
| `craft-citation-semantic.py --manifest block34-after.json --block 34` | exit 1 — block 34 missing | **exit 0 — `ok exit 0`** |
| `depth-blocks-v2.py --expect-blocks 34` | exit 1 — `blocks 33 resolved 33` | **exit 0 — `blocks 34 resolved 34 expect 34 unresolved 0 met=True`** |
| `depth-blocks-v3.py --expect-blocks 34 --shape-from 34` | exit 1 — `required-shaped 0/0` | **exit 0 — `blocks 34, resolved 34, required-shaped 1/1 … met=True`** |
| `craft-citation-semantic.py --manifest block34-junk.json --block 34` (rubber-stamp control) | exit 1 — block 34 missing (not discriminating) | **exit 1 — `QUALITY 191 lacks ['str() fallback']`; `QUALITY 192 lacks ['complete JSON or absent']`; `QUALITY 192 lacks ['helper-only selftest']`** |

⇒ The frozen C2 target is **reachable**: with the block present and the QUALITY rows carrying the frozen atoms,
commands 1–3 go green and command 4 stays red **for the right reason** (named keyword atoms missing, not a
missing block). The junk control is a real discriminator once block 34 exists.

**Two landing requirements the depth counters impose, measured here (they are the L1's to satisfy):**

1. **`depth-blocks-v2` resolves block 34's `corpus/knowledge/` citation, and a missing knowledge file is an
   unresolved block.** My first candidate commit failed with
   `unresolved: [{block: 34, problems: ["absent:2026-11-05-r95-receipt-world-binding.md: absent at HEAD …"]}]`
   → `blocks 34 resolved 33`. The knowledge file `corpus/knowledge/2026-11-05-r95-receipt-world-binding.md`
   must exist **at the landing commit** and be cited by block 34 for the depth counters to resolve 34/34.
2. **Block 34's shape floor (`depth-blocks-v3 --shape-from 34`):** a Markdown decision table with a header row,
   a separator row and **≥3 body rows of ≥4 cells** (plus v2's ≥25 words / ≥2 backtick spans). My 4×4 table
   satisfied it (`required-shaped 1/1`).

**Calibration note on the C2 named limit (already declared):** the keyword atom is a vocabulary check — a
criterion that merely *carries* the phrases passes whether or not it states the rule. My scratch candidate
demonstrates this literally: the QUALITY 191/192 rows I wrote state the rules in prose, but the checker only
verifies the phrases are present. The junk-manifest control is the only thing separating a rule-stating criterion
from a phrase-stuffed one, and it only fires on *other* phrases.

---

## 4 — Files written by this seat (reproduction half)

Under `.ufo/waves/round-95/w1/ScoutS320/repro/`:

`c1-forgery-repro.json`, `c1-forgery-repro.stdout`, `honest-pos.json`, `honest-pos.stdout`,
`c1-symlink-v5-repro.json`, `c1-symlink-v4-repro.json`, `depth-v2-at-decl.txt`, `depth-v3-at-decl.txt`,
`depth-v2-candidate.txt`, `depth-v3-candidate.txt`, `c2-block34-at-decl.txt`, `c2-after-candidate.txt`,
`c2-junk-candidate.txt`, `named-limit-reauthored-triple.json`, `attack-consistent-wrong-rev.json`,
`attack-bad-counter-pin.json`, `attack-reauthored-F3.json`

Full detail in `.ufo/waves/round-95/w1/ScoutS320/repro-c1-c2.md` (this file).
Scratch `/fast/scratch/hyaku/kaidoku-r95/ScoutS320` (including the clone and its two scratch commits) deleted
before yield. No lane file outside the seat directory was created, edited or deleted.
