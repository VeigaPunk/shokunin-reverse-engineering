# R30 w1 — ScoutSkillPlacement: where the round-30 SKILL.md section and PROVINCE.md Core addition go, and what each counter needs of them

Scope: placement of the round-30 SKILL.md section (R30-C2 surface) and the PROVINCE.md Core
addition (R30-C1 surface); the exact file lines `province_ok()` / `skill_ok()` require; and the
SHONEN.md box-4 pointer check against PROVINCE.md at main. Read-only lane work; no REA run, no
carrier/mutant executed, no installs, no processes left running.

Lane state at read time (observation): `git rev-parse main HEAD` →
`4ee65c6771058284aa947a266475839d196ed4d4` for both (exit 0); `git log -1 main` →
`4ee65c6771058284aa947a266475839d196ed4d4 2026-10-22T23:35:13-03:00 round-30: freeze R30-C1
(coverage, inspect_rust_binary positive class) and R30-C2 (depth, refusal signatures) — claims.json`;
`git diff main -- PROVINCE.md SKILL.md SHONEN.md | wc -c` → `0`; `git status --porcelain=v1` shows only
untracked `.ufo/waves/round-30/**` scaffolding. So "PROVINCE.md at main" = the working tree = commit
4ee65c6. Producing commands and outputs: `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScoutSkillPlacement/evidence.txt`
(sha256 3126caf038f5970faf14b77a1dae129e3471d1a99ac6c3fc9519027d8a553770), UTC stamp of that run
2026-10-23T02:47:02Z; spot-check at 2026-10-23T02:47:33Z.

## 1. Proposed insertion points (proposal, grounded in the files' own conventions)

**SKILL.md — insert AFTER line 964 (append at EOF).** File is 964 lines; the last heading is
`### Round-29 measurement registry` at 957 (grep -n, exit 0), and line 964 is the last line, the
`round29-prefile` registry row. Rounds 26/27 opened top-level `## <topic> — round N` sections
(`:883`, `:912`), and rounds 27-29 appended `### Round-N measurement registry` subsections at EOF.
Proposed heading text: `## inspect-rust-binary refusal signatures at rea-agents@6.5.0 — round 30`
(the C2 surface: "SKILL.md gains a decision table of inspect_rust_binary refusal signatures" —
`claims.json` R30-C2). If a round-30 measurement registry is added, place it after that section at
EOF as `### Round-30 measurement registry`.

**PROVINCE.md — insert AFTER line 328 (append at EOF).** File is 328 lines; the last section is
`## Round-27 renamed-copy identity and cross-pin attribution — 2026-10-22` at 307, and line 328 is
the last line, the "Round-27 outcome note (appended after the falsify wave): …". Sections below the
Core table are chronological; the round-28/29 additions went *inside* the Frontier EVM bullet, not as
new sections, so EOF is the next free slot. Proposed heading text: `## Round-30 inspect-rust-binary
positive coverage — 2026-10-23` (round-24/27 EOF pattern `## Round-N <topic> — <date>`; the
`### Round-N additions to Core — <date>` family of :121/:166/:222 is equally acceptable — no counter
depends on the heading or level).

## 2. What each counter needs of these files (observation; exact source lines)

C1 `province_ok(root, rev)` — `tools/round-30/c1-rust-positive.py:158-166`:

```
158 def province_ok(root, rev):
159     text = show(root, rev, "PROVINCE.md") or ""
160     base = show(root, BASE, "PROVINCE.md") or ""
161     lines = [l for l in text.splitlines() if "inspect-rust-binary" in l and ENTRY in l]
162     if not lines:
163         return False, "no PROVINCE line names inspect-rust-binary with the entry"
164     if any(l in base.splitlines() for l in lines):
165         return False, "PROVINCE line already at base"
166     return True, "ok"
```

- Needs ≥1 physical line of PROVINCE.md at the measured rev containing **both** `inspect-rust-binary`
  (hyphenated CLI form) **and** the exact ENTRY string `corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`
  (`ENTRY`, :43). The matching line must not occur verbatim in PROVINCE.md at
  `BASE = "d210fb8fa62d2af04d009cfa0c65a4e8137dc742"` (:45).
- `--rev` defaults to `main` (:337), so the line must be committed at the measured rev, not merely in
  the working tree. Failure prints `province_ok=0 (<reason>)` in the counter's final line (:265) and
  exit 0 requires it (:266).
- Current state: `grep -c 'inspect-rust-binary' PROVINCE.md` → `PROVINCE.md:0` (exit 1).

C2 `skill_ok(root, rev)` — `tools/round-30/c2-rust-refusals.py:273-277`:

```
273 def skill_ok(root, rev):
274     text = show(root, rev, "SKILL.md") or ""
275     base = (show(root, BASE, "SKILL.md") or "").splitlines()
276     lines = [l for l in text.splitlines() if "inspect-rust-binary" in l and ENTRY in l and l not in base]
277     return (True, "ok") if lines else (False, "no new SKILL.md line names inspect-rust-binary with the entry")
```

- Needs ≥1 physical line of SKILL.md at the measured rev containing **both** `inspect-rust-binary`
  **and** the exact ENTRY string `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md`
  (`ENTRY`, :50), and that line must not be in SKILL.md at BASE (:52).
- `--rev` defaults to `main` (:438). Failure prints `skill_ok=0 (<reason>)` (:381) and exit 0 requires
  it (:382).
- Current state: `grep -c 'inspect-rust-binary' SKILL.md` → `SKILL.md:0` (exit 1).

Consequences (observation): neither check constrains heading, section or position — both scan the
whole file — so the only hard requirements are (a) one new physical line per file carrying the verb
and the full relative entry path as contiguous substrings, (b) committed at the measured rev. The
underscore operation spelling `inspect_rust_binary` alone does **not** satisfy either check
(the literals at c1:161 / c2:276 are the hyphenated CLI verb). Draft lines that would satisfy them
(proposal, not verbatim requirements): PROVINCE.md —
`- REA 6.5.0 `inspect-rust-binary` positive class now held: 16 frozen cargo-auditable `.dep-v0`
carriers from 7 uv 0.13.0 wheels (ELF, PE, thin Mach-O), each live run agreeing with the committed
envelope and the independent oracle (`corpus/knowledge/2026-10-23-r30-rust-auditable-positive.md`;
carriers `corpus/evidence/round-30/c1/carriers.tsv`).` ; SKILL.md —
`Source: `corpus/knowledge/2026-10-23-r30-rust-auditable-refusals.md` (S090) — 16 refusal signatures
and 3 acceptance classes predicted from the 6.5.0 `inspect-rust-binary` code, frozen in
`corpus/evidence/round-30/c2/predictions.tsv` before any run.`

Note (observation, for the L1's receipt matcher): both counters print the reason parentheticals —
c1:265 `"carriers=%d pass=%d target=%d entry_ok=%d (%s) province_ok=%d (%s)"` → e.g.
`carriers=16 pass=16 target=16 entry_ok=1 (ok) province_ok=1 (ok)`; c2:381 `"mutants=%d matches=%d
target=%d entry_ok=%d (%s) skill_ok=%d (%s)"` → e.g. `mutants=19 matches=19 target=19 entry_ok=1 (ok)
skill_ok=1 (ok)`. The frozen target text in `claims.json` is
`carriers=16 pass=16 target=16 entry_ok=1 province_ok=1` / `mutants=19 matches=19 target=19 entry_ok=1
skill_ok=1`, whose tail (`entry_ok=1 province_ok=1` / `entry_ok=1 skill_ok=1`) is not a contiguous
substring of the printed line. Interpretation is the L1's; recorded here because the kill rule reads
"prints its target line".

## 3. SHONEN.md box-4 pointer check at main (observation) — corrected ranges

SHONEN.md:12 (the no-cross-domain-bleed box) currently says, verbatim:
`asserted boundary only: `PROVINCE.md:95-116` (the `## Adjacent` refusal list; safety refusal at
:114-116; range refreshed round 25 attempt 3, the earlier `88-116` began inside `## Frontier`); …`.

At main (`git show main:PROVINCE.md` greps agree with the worktree, exit 0):

- `## Adjacent` heading = **line 97**; intro 99-100; the five refusal bullets = **102-118**
  (Malware 102-104, Non-REA 105-107, Source-available 108-109, Installing 110-115, Quality/safety
  116-118); 119-120 blank; next section `### Round-4 additions to Core` at 121.
- Lines **95-96 are still inside `## Frontier`** (95 = the round-29 Frontier note ending
  "…belong to other selectors (`corpus…`"; 96 = blank) — so `95-116` repeats exactly the defect the
  round-25 refresh fixed for `88-116`: it begins inside `## Frontier`.
- `:114-116` is also stale: 114-115 are the tail of the previous bullet
  (`**operator-owned**. The lane documents the gap…` / `never runs the installer.`) and a blank; the
  safety refusal bullet is **116-118** (`- **Quality/safety verdicts on findings** …` through
  ``licensed for reuse" `(unowned)`.``).

**Corrected ranges:** `PROVINCE.md:95-116` → **`PROVINCE.md:97-118`** (the `## Adjacent` refusal
list: heading through last refusal bullet; bullets-only alternative **102-118**); safety refusal
`:114-116` → **`:116-118`**.

Cause (observation): the pointer was correct when written — at `0e333eb2` (round-25 commit, the one
that introduced the `95-116` string per `git log -S`), `## Adjacent` = 95 and the safety bullet =
114-116. It then drifted by +2 lines, both from additions to the Frontier EVM bullet:
`2832c5b3` (round-28 hygiene) added a round-28 line at 94 (heading 95→96, seen at 2832c5b3:
`94|  Round 28: the round-25 primary naming rule held out of sample…`, `96|## Adjacent`);
`2f18996d` (round-29) added the round-29 note at 95 (heading 96→97). `071270b5` only rewrote the
round-28 line in place (no shift). Because Frontier keeps growing, the pointer will keep drifting;
pointing at the heading line (97 at main) and re-checking per round is the stable fix.

Bonus spot-check (observation): the same box's version pointers still locate their content at main —
`Surface summary:` at line 8, `Round carrier runs pin the CLI explicitly to the superseded client pin
`rea-agents@6.5.0`` at line 12 (so `:8-14` covers the stated pins), `Installed shared REA skill is
v42/207 tools` at line 24. No correction needed for those two.

## Evidence (command, excerpt, exit, UTC)

All commands below are read-only; full transcript in the artifacts listed under §4.

| Command | Exact excerpt | Exit | UTC |
|---|---|---|---|
| `git rev-parse main HEAD` | `4ee65c6771058284aa947a266475839d196ed4d4` (twice) | 0 | 02:47:02Z |
| `git diff main -- PROVINCE.md SKILL.md SHONEN.md \| wc -c` | `0` | 0 | 02:47:02Z |
| `wc -l SKILL.md PROVINCE.md SHONEN.md` | `964 / 328 / 12` | 0 | 02:47:02Z |
| `grep -c 'inspect-rust-binary' SKILL.md PROVINCE.md` | `SKILL.md:0`, `PROVINCE.md:0` | 1 | 02:47:02Z |
| `grep -n '^## Adjacent…' PROVINCE.md` | `97:## Adjacent`, `116:- **Quality/safety verdicts…`, `118:  licensed for reuse…`, `121:### Round-4…` | 0 | 02:47:02Z |
| `awk 'NR>=93 && NR<=101' PROVINCE.md` | `95|  Round 29 (R29-C1 …`; `96|`; `97|## Adjacent` | 0 | 02:47:02Z |
| `awk 'NR>=113 && NR<=121' PROVINCE.md` | `115|  never runs the installer.`; `116|- **Quality/safety…` | 0 | 02:47:02Z |
| `git show 0e333eb2:PROVINCE.md \| grep -n …` | `95:## Adjacent`, `114:- **Quality/safety…`, `116:  licensed for reuse…`, `119:### Round-4…` | 0 | 02:47:02Z |
| `git log -S 'PROVINCE.md:95-116' -- SHONEN.md` | `0e333eb2 2026-10-22 round-25: R25-C1 calibration repair …` | 0 | 02:47:02Z |
| `git show 2832c5b3:PROVINCE.md \| awk 'NR>=88 && NR<=98'` | `94|  Round 28: the round-25 primary naming rule held out of sample…`; `96|## Adjacent` | 0 | 02:47:02Z |
| `git show 2f18996d:PROVINCE.md \| grep -n '^## Adjacent'` | `97:## Adjacent` | 0 | 02:47:02Z |
| `grep -n 'Surface summary\|Round carrier runs pin\|Installed shared REA skill' PROVINCE.md` | `8:`, `12:`, `24:` | 0 | 02:47:33Z |
| `awk 'NR>=156 && NR<=172' tools/round-30/c1-rust-positive.py` | province_ok body as quoted in §2 | 0 | 02:47:02Z |
| `awk 'NR>=271 && NR<=280' tools/round-30/c2-rust-refusals.py` | skill_ok body as quoted in §2 | 0 | 02:47:02Z |
| `grep -n 'ENTRY = …' tools/round-30/*.py` | c1:43 positive entry, c2:50 refusals entry; both `BASE = d210fb8f…` | 0 | 02:47:02Z |

## 4. Artifacts (scratch, sha256)

- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScoutSkillPlacement/collect.sh` — sha256
  `36cc3bcbf1655eb67df0dd7b891ba91e00ffdb57e4909470cf15b03cc740d19e` (the read-only collector).
- `/fast/scratch/hyaku/kaidoku-r30/seats/w1/ScoutSkillPlacement/evidence.txt` — sha256
  `3126caf038f5970faf14b77a1dae129e3471d1a99ac6c3fc9519027d8a553770` (full command transcript,
  collector exit 0, UTC 2026-10-23T02:47:02Z).

No tool installs or updates; no REA invocation (none was authorized); no processes left running.

## 5. Unresolved / not checked

- Whether the L1 also wants a `### Round-30 measurement registry` row set in SKILL.md — not required
  by either counter (observation); placement suggestion in §1 is convention-only.
- The claims.json target text vs the counters' printed `(ok)` parentheticals (§2 note) — how the
  kill-rule matcher reads "target line" is the L1's call; not evaluated here.
- The round-30 entry files `corpus/knowledge/2026-10-23-r30-rust-auditable-{positive,refusals}.md` do
  not exist yet (glob of `corpus/knowledge/2026-10-23-r30-*` → no matches; `corpus/evidence/round-30/`
  holds only c1/{carriers.tsv,pypi-uv-0.13.0.json} and c2/predictions.tsv) — that is wave-2 content,
  noted because the counters' required line must name those exact paths.
