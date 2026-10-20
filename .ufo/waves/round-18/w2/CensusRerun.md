HOLDS

# CensusRerun: SOURCES census rerun at REV `b2aad08` and what W04 means

Seat: `KaidokuR18.CensusRerun`. This is author-side advisory work, read-only on the lane. Run at 2026-10-20T16:47Z, so the UTC date was 2026-10-20.
No tools were installed or upgraded. I wrote nothing in the lane except this report. All scratch work happened in `mktemp -d` → `/tmp/censusrerun.irLvof`, a `--no-hardlinks` clone with `origin` removed before any checkout. I ran no `jj`, REA or Ghidra.

**Verdict.** Every census claim checked reproduces at REV.
- The required CLI validate exits 0 and prints `ok`.
- The frozen manual census is clean: 36 rows, A31/B4/C1, mined34/rejected2.
- The baseline "before (exit 0, 32 rows)" reproduces at `9011581`.
- The one `W04` line is a warning by the tool's contract, and the tool's selftests confirm that behavior. It does not change the exit code or the `ok` line.
- It comes from S033, the correction row for S032. S033 has the same PR URL as S032 but a reworded `scope`. Three low-severity calibration and operability notes follow; none of them breaks a claim.

## 0. Binding (observation)

| Fact | Command | Exit | Result |
|---|---|---|---|
| lane HEAD = branch tip = REV | `git rev-parse HEAD refs/heads/main` / `git rev-parse --symbolic-full-name HEAD` | 0 / 0 | `b2aad08c…` both; `HEAD`, which means detached (jj) |
| live registry file is the REV blob | `git hash-object corpus/SOURCES.md` vs `git rev-parse b2aad08…:corpus/SOURCES.md` | 0 | `35d74466…` = `35d74466…` (baseline blob is `c6b416de…`) |
| fleet sources are unmodified (fleet HEAD `d21e61f5…`) | `git -C /home/vgpnk/Projects/shokunin hash-object CORPUS.md scripts/sources-census.sh` vs `HEAD:` | 0 | `882d6ca8…` and `3f314620…`, both equal to HEAD |

The runs against the live lane file in §1 and §2 therefore measured REV bytes. Fleet-file anchors below refer to fleet HEAD `d21e61f5`.

## 1. Required CLI census (from the lane, fleet root)

```
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
EXIT=0
$ /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kaidoku
kaidoku rows 36 | tier.A 31 | tier.B 4 | tier.C 1 | status.mined 34 | status.rejected 2
FLEET  rows 36 | tier.A 31 B 4 C 1 invalid 0 | status.queued 0 mined 34 rejected 2 invalid 0 | missing 0
EXIT=0
```

The census output is reformatted onto two lines here; the tool prints one TSV line per metric.

## 2. Frozen manual census, `CORPUS.md:133-148`, cwd `kaidoku-shokunin`

Each command was run verbatim with `; echo "EXIT=$? PIPESTATUS=${PIPESTATUS[*]}"` appended.

| # | CORPUS line | Check | Output at REV | Exit (PIPESTATUS) |
|---|---|---|---|---|
| 1 | :135 | rows (`grep -cE`) | `36` | 0 |
| 2 | :137 | malformed rows, NF!=13 (must be 0) | `0` | 0 |
| 3 | :139 | tier histogram | `A=31 B=4 C=1` | 0 |
| 4 | :141 | status histogram | `mined=34 rejected=2` | 0 |
| 5 | :143 | duplicate ids (must print nothing) | *(empty)* | 0 (0 0 0) |
| 6 | :145 | enum violations and tier inflation (must print nothing) | *(empty)* | 0 |
| 7 | :147 | mined rows whose used-by path is missing (must print nothing) | *(empty)* | 0 (0 0) |

The manual census and the CLI census agree on rows, tiers and statuses.

## 3. Before and after (observation; baseline is a worktree of the scratch clone at `9011581`)

| Metric | `9011581` (baseline) | `b2aad08` (REV) | Claim at REV |
|---|---|---|---|
| CLI `validate` | `kaidoku-shokunin ok`, **no W-line**, exit 0 | W04 + `ok`, exit 0 | `claims.json:31` "before (exit 0, 32 rows)" holds |
| rows / A / B / C | 32 / 28 / 3 / 1 | 36 / 31 / 4 / 1 | `corpus/lessons/round-18.md:43` "3 tier A, 1 tier B community. Rows 32 → 36" holds |
| mined / rejected | 30 / 2 | 34 / 2 | — |
| frozen manual census, 7 commands | 32, 0, `A=28 B=3 C=1`, `mined=30 rejected=2`, empty, empty, empty; all exit 0 | §2 | — |
| Registry diff | — | `git diff -U0 9011581 b2aad08 -- corpus/SOURCES.md`: Registry hunk is `@@ -38,0 +39,4 @@`, a pure insertion; the only `-` line is the baseline Paths bullet at :44 | `round-18.md:42` "No in-place S001–S032 cell changed" holds |

At REV, the only lane record of the "before" run is a seat's command log, `.ufo/waves/round-18/w1/CriticSourcedClaim.md:118` ("exit 0 → kaidoku ok"). I found no `sources-before` receipt in round 18 (`git ls-tree -r --name-only b2aad08 -- .ufo/waves/round-18`). The rerun above stands in for one.

## 4. What W04 is and why S033 triggers it

**The two cells** (observation, `git show b2aad08:corpus/SOURCES.md`, split on `|`):
- `corpus/SOURCES.md:38` S032
  - source: `… — https://github.com/NationalSecurityAgency/ghidra/pull/9348`
  - scope: "Candidate mechanism for the aether symbol-markup EOF: …"
  - status: mined
- `corpus/SOURCES.md:39` S033
  - source: `…, head a214355 — https://github.com/NationalSecurityAgency/ghidra/pull/9348 (patch …9348.patch)`
  - scope: "Same subject as S032: … a lead, not a mechanism proof"
  - teaches: opens `supersedes S032 —`
  - status: mined

**The code path** (observation, `scripts/sources-census.sh` at fleet `d21e61f5`):
- `url_of` (:600-605, called at :629) keys each row on the **first** `http(s)://` match in the `source` cell. It strips `#fragment`, a trailing `/` and the scheme, and lowercases the host. Both rows normalize to `github.com/NationalSecurityAgency/ghidra/pull/9348`.
- `scope_key = url SUBSEP scope` (:643).
- **W04** (:644-645) fires when a row's URL was already seen and the (url, scope) pair was not. There is no status or `supersedes` exemption.
- The row named in the warning is the later one in file order: S032 at :38 registers the URL first (:650-652).
- **E04** (:646-649) applies only when the scope is the same. It is exempt if this row is `rejected`, if the earlier same-scope row was rejected, or if `teaches` matches `supersedes S[0-9]{3}`.
- How validate reports: W-lines are printed but only E-codes set `lane_errors`/`findings` (:739-745), so `ok` is still emitted and the exit code stays 0 (:805-806). The header documents this at :25 and :31-33: E04 is "(no supersedes)"; W-codes "do not affect clean lanes".

**Counterfactuals** (observation). Each one mutated `corpus/SOURCES.md` in the scratch REV clone, ran `sources-census.sh validate <clone>`, and restored the file with `git checkout`. The blob hash after each restore was `35d74466…`.

| Mutation | validate | Exit | What it shows |
|---|---|---|---|
| none (control: the clone at REV) | W04 S033 + `ok` | 0 | The clone reproduces the lane run |
| M1: S033.scope := S032.scope | `ok` only | 0 | A reworded scope is the only W04 trigger. With the same scope, the `supersedes` marker suppresses E04 |
| M2: M1 plus `supersedes S032 —` removed from S033.teaches | **E04** S033 "within scope Candidate mechanism…" | **1** | The supersedes marker is what keeps a same-scope correction legal |
| M3: S032.status := rejected (scopes as at REV) | W04 S033 + `ok` | 0 | W04 ignores status |
| M3b: M2 plus S032 rejected | `ok` | 0 | The rejected-pair exemption for E04 (:646-647) |
| M4: S033's first URL removed, so `…9348.patch` becomes first | `ok` | 0 | W04 is keyed only on the first URL in the cell |
| M5: S033 URL changed to `http://GitHub.com/…/pull/9348/#top` | W04 S033 + `ok` | 0 | Scheme, host case, trailing slash and fragment are all normalized away |

Selftest (observation): `TMPDIR=$T sources-census.sh selftest` exited 0 with 96 `killed` and 0 `SURVIVED`. Among the killed checks are `W04-scope-sensitive-mutant` and `W04-does-not-fail-validation`. Their fixture (:350-365: S901/S902, same URL, different scope, exit 0) has the same shape as S032/S033. The lane therefore hit the tool's tested, intended W04 path.

**Interpretation (inference).** W04 is the census mechanically noting that S033 registers S032's PR again under a narrower scope. This is the correction form CORPUS prescribes (`CORPUS.md:116-118`: a correction is a new row whose `teaches` opens `supersedes S0NN —`). The tool exempts supersession only from E04, not from W04. Because `tier` is scoped to `scope` (`CORPUS.md:93,98`), rewording the scope is a substantive edit, so the warning is expected and benign. Silencing it by copying S032's scope (M1) would erase S033's narrowing.

## 5. Findings. Each has a reproducing command; none breaks a claim.

- **F1. Calibration, low: the W04 appears in no committed lane record, and the planned check predicted only `ok`.**
  - Observation: `git grep -c W04 b2aad08 -- .` exits 1, meaning no lane file mentions W04.
  - Observation: the post-write check planned in `.ufo/waves/round-18/w1/ConnCorrectionPlacement.md:222` expects `# ok`.
  - Observation: `corpus/lessons/round-18.md:42-43` records rows 32 → 36 but not the warning.
  - Observation: `verify.py:250-252` expects only exit 0 (`run(..., 0)`, `exit_as_expected`, :117-127), so the pass will be green and will keep the W04 line in stdout.
  - Inference, advisory: record "W04 S033 vs S032 — correction row, reworded scope; warning by contract" next to `round-18.md:43`.
- **F2. Calibration, info: rows +4 but distinct sources +3.**
  - Observation: first-URL distinct count at `9011581` → `b2aad08` is 26 → 29; rows 32 → 36; URL-less rows 6 → 6; S033 is the only row that repeats a URL.
  - Command: the gawk below re-implements `url_of` (:600-605) over Registry rows.
  - Inference: "Rows 32 → 36" is accurate as a row count. The actual change is 3 new sources (S034–S036) plus 1 superseding re-registration. Wave 1 raised the same point in substance (`.ufo/waves/round-18/w1/CriticSourcedClaim.md:29-35`).
- **F3. Operability, info: exit 0 depends on the run date.**
  - Observation: `sources-census.sh validate --today 2026-10-19 --root /home/vgpnk/Projects/shokunin kaidoku` gives 14 × `E08 opened=2026-10-20` (S023–S036) plus the W04, exit 1.
  - The default `--today` is `date -u +%F` (:90).
  - Inference: 10 of those 14 rows (S023–S032) predate round 18, so this is not a round-18 regression. Replays are valid on or after 2026-10-20 UTC.
- **F4. Operability, info: the frozen manual census cannot see W04.**
  - Observation: the 7 checks in `CORPUS.md:133-148` contain no URL or scope check, no date or recheck check, and no section scoping.
  - So they cannot see W04, E04, E08, E09 or E12. At REV this hides only the W04, since the CLI reports no E-code.
  - Two other divergences are latent. The manual used-by split is `[,;]` (:147) while the CLI E11 split is `,` (:562); no used-by cell has `;` at either revision. The manual row regex is column-zero and file-wide, while the CLI scopes rows to `## Registry`; both give 36.

## Reproduce

```sh
L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin; S=/home/vgpnk/Projects/shokunin/scripts/sources-census.sh
$S validate --root /home/vgpnk/Projects/shokunin kaidoku; echo $?        # §1
cd "$L" && sed -n '135p;137p;139p;141p;143p;145p;147p' /home/vgpnk/Projects/shokunin/CORPUS.md   # §2: run each line from the lane root
T=$(mktemp -d) && git clone -q --no-hardlinks --no-checkout "$L" "$T/rev/kaidoku-shokunin" \
 && git -C "$T/rev/kaidoku-shokunin" remote remove origin \
 && git -C "$T/rev/kaidoku-shokunin" checkout -q --detach b2aad08ceeee8dd125ce0d316056d8bd766c7f94 \
 && git -C "$T/rev/kaidoku-shokunin" worktree add -q --detach "$T/base/kaidoku-shokunin" 9011581d84527ba34c675f9cf912e54d2e72d470
$S validate "$T/base/kaidoku-shokunin"; $S census "$T/base/kaidoku-shokunin"   # §3 baseline
cd "$T/rev/kaidoku-shokunin"                                                   # §4 counterfactuals
mut() { gawk -F'|' -v OFS='|' "{id=\$2; gsub(/[[:space:]]/,\"\",id)} $1 {print}" corpus/SOURCES.md > corpus/SOURCES.mut && mv corpus/SOURCES.mut corpus/SOURCES.md; }
run() { $S validate "$PWD"; echo "EXIT=$?"; git checkout -q -- corpus/SOURCES.md; }
mut 'id=="S032"{s=$6} id=="S033"{$6=s}'; run                                            # M1
mut 'id=="S032"{s=$6} id=="S033"{$6=s; sub(/supersedes S032 — /,"",$8)}'; run          # M2
mut 'id=="S032"{$9=" rejected "}'; run                                                   # M3
mut 'id=="S033"{sub(/— https:\/\/github\.com\/NationalSecurityAgency\/ghidra\/pull\/9348 /,"",$3)}'; run   # M4
TMPDIR=$T $S selftest | grep -E 'W04|E04|SURVIVED'
cd "$L" && git grep -c W04 b2aad08ceeee8dd125ce0d316056d8bd766c7f94 -- .; echo $?          # F1 (1 = none)
for R in 9011581 b2aad08; do git show $R:corpus/SOURCES.md | gawk -F'|' '/^ {0,3}##[ \t]/{l=$0;sub(/^ {0,3}/,"",l);reg=(substr(l,4)=="Registry");next} /^ {0,3}#[ \t]/{reg=0;next}
 reg && /^\|[ \t]*S[0-9]{3,}[ \t]*\|/{r++; if(match($3,/https?:\/\/[^[:space:]|]+/)){u=substr($3,RSTART,RLENGTH);sub(/#[^ ]*$/,"",u);sub(/\/$/,"",u);sub(/^[A-Za-z]+:\/\//,"",u);n=index(u,"/");u=tolower(substr(u,1,n-1)) substr(u,n);if(!(u in s))d++;s[u]=1}}
 END{print r" rows, "d" distinct first URLs"}'; done                                       # F2
```

## Limits

- My first M2/M3 attempt chained `grep -c … && run`. `grep -c` returned 0 matches and exit 1, which skipped M2's run and left the M2 mutation in place for "M3". I discarded both results.
- The M2/M3/M3b rows in §4 come from a clean rerun that began from verified blob `35d74466…`.
- I did not mutation-test which row W04 names when the file order is swapped; that statement comes from reading the code (:650-652).
- Out of scope and not examined: `## Gate` quote fidelity for S033–S036, and the Paths-section edit at baseline :44.
