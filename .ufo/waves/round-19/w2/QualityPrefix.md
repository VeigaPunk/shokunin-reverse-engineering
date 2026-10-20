# QualityPrefix — no-harm review

**Scope:** `corpus/QUALITY.md`, B=`8a8da7e19375aadc66c6bcbff0bbcbb596048fb0`, observed `refs/heads/main`=`279e8b19c51658bfd05b9e31a1c0894ab2e70537`. Axes considered: **calibration, freshness, depth**. Read-only review; no production edits, builds, tests, or installs.

## Findings (severity order)

**No actionable finding in scope.** [OBS] The only B→main change to `corpus/QUALITY.md` is one inserted admission row at line 32 (`1 insertion, 0 deletions`). Admission rows 1–21 each occur once in each version and are byte-identical, including line endings. Row 22 is absent from B and occurs exactly once in main and once in the whole file; it does not occur in the weak-signal table. The separate `Signals of weak material` table still has only its six rows numbered 1–6 (`corpus/QUALITY.md:34–43`). [OBS]

**Classification and grounding.** [OBS] Row 22 is an **admission criterion**, under `## Admission criteria` at `corpus/QUALITY.md:7–32`, not a weak-signal row. It applies to round-wave seat-status claims: name the observation cutoff, distinguish terminal failures from seats not yet returned, retain per-seat causes and their source pointers (or explicitly mark unknown and state what was tried), and append later reclassifications at their own cutoff. Its lesson cites the R18 disagreement and missing causes at `corpus/lessons/round-18-verifier-spotcheck.md:146,197`; the round-19 mistake record also identifies the gap and the correction at `corpus/lessons/round-19.md:83`.

The retained red/green evidence is consistent with that correction: red says 98 seats, 94 reports, four missing and four uncaused, with exit 1 (`.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-red.stdout:1–4`; `r18-w2-red.exit:1`); green retains causes for all four, reports zero uncaused and exit 0 (`r18-w2-green.stdout:1–4`; `r18-w2-green.exit:1`). The separate per-seat record gives the cutoff and missing-seat summary and includes cause/source references for the four affected seats (`.ufo/waves/round-19/evidence/r18-dead-seats.json:4–7,11–34,38–70`). These cited evidence files are present in the observed main tree. [OBS]

[INFERENCE] This is a bounded addition for claims about round-seat status, not a rewrite of existing artifact-analysis admission rules. The unchanged rows avoid no-harm regressions; the added cutoff/cause requirements address the evidenced stale-count and missing-record problem without asserting that a seat's cause is known when it is not.

## Residual risk and verification gaps

[OBS] The retained `wave-outcomes` green record defines success as a non-empty cause for each missing report (`.ufo/waves/round-19/evidence/wave-outcomes/r18-w2-outcomes.json:10–19`) and has `cause_sources: {}` (`:29`). Therefore that green exit alone does **not** verify the new row's stronger source-pointer and cutoff requirements; those remain manual admission checks against records such as `r18-dead-seats.json`. This is a limitation of the evidence's scope, not a contradiction in the QUALITY diff.

LSP was unavailable: `read xd://lsp` returned “No such tool” and `read xd://lsp/status` returned “Tool 'lsp' has no doc topics.” No references/definition/diagnostics queries were possible. No text grep was used as semantic proof. No tool was installed or updated.

## Commands and exits

Observed main tip: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main` → **0**, `279e8b19c51658bfd05b9e31a1c0894ab2e70537`.

`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=0 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0 refs/heads/main -- corpus/QUALITY.md` → **0**; output: one insertion at `+32`, no deletions. `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --exit-code 279e8b19c51658bfd05b9e31a1c0894ab2e70537 -- corpus/QUALITY.md` → **0** (worktree file equals the observed main blob).

The byte-level comparison was run with this read-only command → **0**:

```sh
python3 -I -B -c '
import subprocess
repo = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
base = "8a8da7e19375aadc66c6bcbff0bbcbb596048fb0"
tip = "279e8b19c51658bfd05b9e31a1c0894ab2e70537"
path = "corpus/QUALITY.md"
def blob(rev):
    return subprocess.run(["git", "-C", repo, "show", rev + ":" + path], check=True, stdout=subprocess.PIPE).stdout
def section(data, start, end):
    return data.split(start + b"\n", 1)[1].split(end + b"\n", 1)[0].splitlines(keepends=True)
def row(lines, number):
    prefix = b"| " + str(number).encode() + b" |"
    return [line for line in lines if line.startswith(prefix)]
b, m = blob(base), blob(tip)
ba = section(b, b"## Admission criteria", b"## Signals of weak material")
ma = section(m, b"## Admission criteria", b"## Signals of weak material")
mw = section(m, b"## Signals of weak material", b"For tier definitions, scope, and recheck policy, use `corpus/SOURCES.md`; claim admission still follows this QUALITY bar.")
prefix_equal = all(len(row(ba, n)) == len(row(ma, n)) == 1 and row(ba, n) == row(ma, n) for n in range(1, 22))
counts = (len(row(ba, 22)), len(row(ma, 22)), sum(line.startswith(b"| 22 |") for line in m.splitlines(keepends=True)), len(row(mw, 22)))
weak_ids = [n for n in range(1, 7) if len(row(mw, n)) == 1]
print("MAIN_TIP", tip)
print("ADMISSION_1_21_BYTE_EQUAL", prefix_equal)
print("ROW22_COUNTS_B_MAIN_FILE_WEAK", counts)
print("WEAK_SIGNAL_IDS", weak_ids)
assert prefix_equal and counts == (0, 1, 1, 0) and weak_ids == list(range(1, 7))
print("RESULT PASS")
'
```

Output: `MAIN_TIP 279e8b19c51658bfd05b9e31a1c0894ab2e70537`, `ADMISSION_1_21_BYTE_EQUAL True`, `ROW22_COUNTS_B_MAIN_FILE_WEAK (0, 1, 1, 0)`, `WEAK_SIGNAL_IDS [1, 2, 3, 4, 5, 6]`, `RESULT PASS`.

No outside-verifier or axis-score claim is made by this scoped review.