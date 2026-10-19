# EX-33 — receipt self-pin audit (chain c2, seat EX-33, arc3-loop1-round3)

Role: executor. Task: **a receipt captured by the revised tool embeds the revised
tool's sha256 (not the old `112d01dc…`); old-tool receipts remain processable.**

Instrument (canonical, read-only use): `.ufo/gates/custody-pair/custody-pair.py`
— written only by the designated implementer (EX-21); this seat never edited it.
Scratch root `/var/tmp/ex33-selfpin/` (no `/tmp`). Evidence: `evidence/`,
tools: `tools/`.

## 0. Revision context (why every number below names its revision)

The EX-21 revision was captured **in flight**: between 13:07Z and 13:13Z the
canonical file moved through at least ten revisions. Evidence pointers:

| revision (sha256 prefix) | where recorded |
|---|---|
| `112d01dc…` (the pre-round revision) | `evidence/poll.log` check 1 baseline; `evidence/canon-pre.receipt` |
| `68e30768…` | `evidence/poll.log` 13:08:28Z REVISION-LANDED |
| `d5e72049…`, `460a01f0…`, `a8f81dcf…` | `evidence/legC.log` first stability gate (5 s apart); `a8f81dcf` STABLE there, capture pinned it |
| `08fb6833…`, `ec2b2d48…`, `57dffff1…`, `03bd6242…` | `evidence/watch.log` (13:10:28–13:12:28Z; `03bd6242` held streak=5 = 75 s) |
| `89bfebec…` | `evidence/legC2.log`: first and last hash of the full canonical leg (mtime 10:12:44 -0300), pre==post |
| `7cd19c3c…` | `evidence/legC3.log`: full canonical leg + selftest CLEAN 22/22 (mtime 10:13:20 -0300), pre==post; the last `sha256sum` in `evidence/watch.log` samples the same value |

(Three manual samples between `a8f81dcf` and `08fb6833` — `b9bd55e9`, `9860149d`,
`d9be407d` — are transcribed from this seat's watch output, not log-backed; they
are consistent with the churn and add no measurement.)

This is D8's class reproduced live: a "stable" sha can last ~90 s mid-landing,
and any receipt's pin names exactly the revision that produced it.

## 1. The self-pin mechanism, as found (unchanged by the revision)

    TOOL_PATH = Path(__file__).resolve()                                        # :145
    tool_sha = sha256_file(TOOL_PATH) if TOOL_PATH.exists() else "(unavailable)"# :295
    "# tool: %s  sha256 %s" % (TOOL_PATH.name, tool_sha)                        # :300

The pin is computed at **render time** and emitted in the receipt header. Nothing
in the tool parses the pin back: `parse_receipt()` reads `receipt-version` only
(`:399`); `verify` never compares pins — so the pin is capture-time provenance
metadata, not an enforced anchor (the D4/D8 surface at the pin's own layer).
All line numbers in this artifact were re-verified at the settled revision
`7cd19c3c…` (`sha256sum` in §5).

## 2. Method

`tools/selfpin-audit.py` — independent verifier: hashes the tool file with its own
hashlib path, extracts the pin with its own regex; never imports the tool, never
trusts the tool's self-report. Checks: C1 pin-present; C2 pin==tool-bytes;
C3 pin!=old `112d01dc…`; C5 basename agrees; C6 sidecar digest == receipt bytes;
C7 tool-file sha stable across the audit. Exit 0 iff all performed checks pass.

Legs: **M** mechanism on scratch copies; **C** canonical captures at named
revisions; **O** old-receipt processability (declared exit map {0,2,3,10,11,12,13}
at the pre-revision tool and {…,14} at the revised tool, whose `:161` declares
`EXIT_UNEVALUABLE = 14`); **attacks** A1/A3/A4/A6.

## 3. Measurements

### 3M — the pin tracks the tool revision (scratch copies; revision-independent)

    M1 unrevised copy  sha 112d01dc…  ->  receipt pin 112d01dc…   (pin == tool bytes)
    M2 revised copy    sha 0ce819c3…  ->  receipt pin 0ce819c3…   (≠ old, == tool bytes)

Pins side by side (raw in `evidence/legM.log`):

    # tool: tool.py  sha256 112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa
    # tool: tool.py  sha256 0ce819c31e52408fd650092cf4de4ff8ab2750cbbcb3ffebcca7f88241b7f401

### 3C — canonical captures at named revisions (independent re-derivation)

| capture | revision at capture (independently hashed) | receipt pin | audit |
|---|---|---|---|
| `evidence/canon-pre.receipt` 13:07:51Z (pre-revision) | `112d01dc…` | `112d01dc…` | 5/5 PASS |
| `evidence/canon-post.receipt` 13:09:22Z | `a8f81dcf…` | `a8f81dcf…` | **6/6 PASS** (`≠112d01dc` checked) |
| `evidence/final-a-89bfebec.receipt`, `final-b-89bfebec.receipt` 13:12:48–49Z | `89bfebec…` | `89bfebec…` both | **6/6 PASS each** (`≠112d01dc` checked) |
| `evidence/final-a-7cd19c3c.receipt`, `final-b-7cd19c3c.receipt` 13:13:52–53Z | `7cd19c3c…` | `7cd19c3c…` both | **6/6 PASS each** (`≠112d01dc` checked) |

Four captures across four revisions — each pin equals the independently-hashed
file at capture time and differs from `112d01dc…`; the two consecutive captures at
each of the last two revisions pin the same revision; the sidecars match their
receipt bytes in all cases. All captures 5/5 exit 0, receipts written to scratch
only; the custody paths were read-only throughout.
Raw: `evidence/legC.log`, `evidence/legC2.log`, `evidence/legC3.log` (C1 sections).

### 3O — old-tool receipts remain processable (revised tool at `a8f81dcf`, `89bfebec`, `7cd19c3c`)

Pre-revision baseline (`evidence/legO-baseline.log`, tool `112d01dc`) and the
battery at each revised capture — `evidence/legC2.log` (tool `89bfebec`) and
`evidence/legO-final.log` (tool `7cd19c3c`) — 7/7 probes processable each,
exit always inside the declared map, verdict line always printed, traceback never:

| probe | exit | class | note |
|---|---|---|---|
| r2 pair (v2 vs v2, both pin `112d01dc`) | 0 | MATCH 5/5 | strongest datapoint |
| r2 v2 vs `--live` | 10 | CONTENT-DRIFT | real `~/.kimi-code/config.toml` drift, not a tool property |
| v1 canonical stanza vs `--live` | 10 | CONTENT-DRIFT | `SHA256-CONTRACT 4/5` printed |
| r2 v2 vs v1 canonical | 12 | METADATA-DRIFT | cross-shape compare on sha256 contract 5/5 |
| **old-tool receipt vs revised-tool receipt** (`canon-pre` `112d01dc` vs that run's final capture `89bfebec`/`7cd19c3c`) | **0** | **MATCH 5/5** | cross-revision comparability, both runs |
| mid-flight revised receipt vs final receipt (`canon-post` `a8f81dcf` vs final capture) | 0 | MATCH 5/5 | superseded-revision receipt still compares clean |
| arc2 sums-v1 pair (real old receipts) | 0 | MATCH-V1-PARTIAL 5/5 | sha256 contract 5/5 |

Additionally: old receipts' sidecars still match their bytes, and
`OLD-RECEIPTS-UNCHANGED-BY-VERIFY: yes` (before/after sha256 of the three input
receipts identical, `evidence/oldreceipts-*.sha256`) — verify is read-only over
receipt stores.

### 3A — attacks (deterministic; receipts in `evidence/`)

- **A1 executed-image ≠ disk-file at render time.** Exec the tool source from
  memory with `__file__` at its path, revise the disk file mid-run, capture:
  executed sha `112d01dc…`, disk sha `a37cf1af…`, **receipt pin `a37cf1af…`**.
  **Verdict: TOCTOU-CONFIRMED** — the pin names the bytes on disk at render time,
  which here are not the bytes that executed. Harm class: misattribution (D8's
  class from the other side). No drift-check bypass is implied.
- **A3 symlink invocation** — pins the resolved canonical file and its basename
  (`custody-pair.py`). **Verdict: transparent.**
- **A4 pin unenforced** — rewrite an old receipt's pin to a wrong sha; verify
  reads MATCH 5/5 exit 0 (`evidence/forged-pin-pre.receipt`). **Verdict:
  confirmed by design** — the pin must be cross-checked by the reader against the
  tool bytes (rule-#14 re-derivation), which is what this audit does.
- **A6 `(unavailable)` pin** — exec with `__file__` at a removed path: pin renders
  `# tool: vanish.py  sha256 (unavailable)` (`:295` fallback) and that receipt
  still verifies cleanly. **Verdict: edge shape confirmed** — reader-side audits
  must fail such a receipt (C1), which this audit's parser does.

### 3S — instrument state at audit time (not this seat's claim, named for the chain)

Two adjacent revisions, 40 s apart in the churn:

- at `89bfebec` (13:12:50Z) the tool's own selftest was **DIRTY:
  cases=21 passed=20 failed=1, exit=3** — failing case
  `require-paths-blocks-partial-reference` with
  `TypeError: _run_verify() got an unexpected keyword argument 'require_paths'`.
  Machine-checkable record: `evidence/legC2.log` (`selftest exit=3`, DIRTY line);
  the full case line is a transcription in
  `evidence/selftest-89bfebec-dirty-transcript.txt` (the scratch log was later
  overwritten by the next run). Mid-flight state: the new case and its harness
  helper landed in different writes.
- at `7cd19c3c` (13:13:54Z, the settled revision at report time) the selftest is
  **CLEAN 22/22 exit 0** (`evidence/selftest-final-7cd19c3c.log`) — the fix landed
  within a minute, and 22 ≥ the claim's ≥17 floor at exit 0.

## 4. Verdict

1. **"A receipt captured by the revised tool embeds the revised tool's sha256
   (not `112d01dc…`)" — SATISFIED at every revision measured** (`a8f81dcf`,
   `89bfebec`, `7cd19c3c`, and the mechanism-level revised copy): independent
   re-derivation shows pin == the file's sha256 at capture, ≠ `112d01dc…`,
   name == basename, sidecar == receipt bytes (audits 6/6 PASS each; four
   captures across four revisions, §3C). The property is structural: the pin is
   derived at render time from `TOOL_PATH` bytes (`:295`).
2. **"Old-tool receipts remain processable" — SATISFIED**: 7/7 probes at the
   revised tool, all classes declared, verdict lines printed, zero tracebacks;
   the strongest case is an old-tool receipt (`pin 112d01dc…`) and a revised-tool
   receipt reading MATCH 5/5 exit 0 in both directions of the battery.
3. **Boundary the wording must carry** (measured, not speculative): the pin is
   provenance, not enforcement — A1 shows it can name bytes that did not execute,
   A4/A6 show receivers accept any pin; and D8 churn means a receipt's pin is
   only meaningful against the revision timeline (table in §0).

## 5. Recheck commands (re-run at the true landing)

    # 1. stability gate + full leg (writes only under /var/tmp)
    bash /var/tmp/ex33-selfpin/watch-tool.sh        # exits STABLE <sha> when settled
    bash /var/tmp/ex33-selfpin/run-legC2.sh         # captures, audits, old-receipt battery
    # 2. the two assertions, independently
    sha256sum .ufo/gates/custody-pair/custody-pair.py
    grep '^# tool: ' /var/tmp/ex33-selfpin/out/final-a.receipt
    # 3. selftest at the settled revision
    python3 .ufo/gates/custody-pair/custody-pair.py selftest --scratch /var/tmp/ex33-selfpin | tail -2

## 6. Blockers

- The EX-21 landing churned through ten+ revisions in six minutes during this
  audit; `7cd19c3c` held stable for ≥75 s (5×15 s samples, `evidence/watch.log`)
  at the time this artifact was written, and every number above names its
  revision. If a further landing supersedes it, re-run §5 — the assertions are
  one command each and the mechanism result is revision-independent.
- A1's harm is attribution-class; consistent with D5's scope sentence — the tool
  is a tripwire for attribution, not an integrity control.