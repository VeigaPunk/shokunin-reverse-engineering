# ConnectFrontier — S037/S038 identity vs outcome, S###, coverage ground

Seat: KaidokuR19.ConnectFrontier-3. Read-only except this report. No production edit, no delegation, no REA/MCP device, no carrier execution, no install.

Axes named: **calibration, freshness, depth**. Learning-trend words asked for: **expansion, quality, discernment**. This seat does not self-attest those trends. `corpus/lessons/round-19.md:50-52` leaves outside sampling to the hyaku closure session.

- Observed main tip: `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` (`git rev-parse refs/heads/main`, exit 0).
- Contract baseline B: `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` (resolves, exit 0).
- Worktree: `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md` is modified (7 lines inserted after committed line 45). Lines 1–45 match the commit (`prefix_equal True`). Command A below reads Git objects, so that hunk does not change the coverage count. Citations of that file are the commit unless noted.

No tool was installed or updated.

## Finding

S037 and S038 are identity/provenance rows. The coverage instrument does not read the Knowledge-table row that cites them, and the r12 “S###” close cites S037 for claims the same entry still lists as ungrounded. A clean sources census does not see either split.

### 1. Scope cells and the outcome path (identity)

**OBSERVATION.** At `d0690fd`, `corpus/SOURCES.md` Registry holds 38 ids, S001–S038. At B the same parser holds 36 ids, S001–S036.

**OBSERVATION.** `corpus/SOURCES.md:43` (S037) scope: “Publish identity and integrity of rea-agents@6.7.0 as served by the npm registry, with its SLSA provenance source commit; not the package's runtime behaviour.” Teaches: pin the tarball by sha512 and release-workflow commit before package code runs. used-by: `corpus/lessons/round-19.md`, `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`.

**OBSERVATION.** `corpus/SOURCES.md:44` (S038) scope: “The official go1.25.0 linux-amd64 archive digest and size, against which the installed 1.25.0 carrier binaries are matched; not the Go 1.26 or 1.27 release train.”

**OBSERVATION.** `corpus/SOURCES.md` `## Paths` is lines 46–57. That section contains neither `S037` nor `S038`. Line 51 still assigns observed Swiss-map outcome to replay receipts: “The lane's replay receipts, not these sources, carry the observed outcome.” The chain named there is S034 → S035 → S023 → S003 → S033.

**OBSERVATION.** The r19 knowledge entry at the commit keeps that split on its own source line and input line:

- `corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md:1` — S038 “carrier provenance only”; “runs/ (observed outcome authority)”.
- `:15` — “Source metadata authenticates identity, not analyzer behavior.”
- `:11` — toolchain ELFs, artifact-held-out; a retained Ghidra log is an analyzer observation.

**OBSERVATION.** The lesson gate matches the scope cells. `corpus/lessons/round-19.md:28`: S037 and S038 “scoped to identity/provenance only” and cites w1 `CriticSourced.md` (“metadata grounds identity sub-claims, not outcomes”). The amendment matches: `.ufo/waves/round-19/claims.json:41`.

**OBSERVATION.** Claim headers put those same ids in the outcome slot:

- `corpus/lessons/round-19.md:14` — “C2 freshness (sourced: S037)”.
- `corpus/lessons/round-19.md:16` — “C3 depth (sourced: S038, with S035/S023/S003)”.
- `SCORECARD.md:2494-2495` — the same “sourced S037” / “sourced S038/S035/S023/S003” headers. The C3 verdict cell then describes the bound-log index rule (vet `13902080`, compares 7/8), which is the log outcome.

**OBSERVATION.** Unamended `claims.json:28` still says the new C3 row is “go.dev/dl JSON … (carrier provenance), with S034/S035/S023”. `claims.json:26` still says “application ELFs”. The amendment at `:37` and `:41` renames the cohort to toolchain ELFs and moves mechanism to S035/S023/S003. Both strings are in the file.

**INFERENCE.** A reader who stops at `:14`, `:16`, or SCORECARD `:2494-2495` can treat publication metadata as the authority for pin-drift equality and for the Swiss-map log. The scope cells, Paths line 51, the r19 entry, and `claims.json:41` say the opposite. w2 `ReopenS038.md` re-checked S038’s digest and did not falsify the identity scope; that reopen is not a mechanism result.

### 2. Knowledge entry S### (the r12 C1 entry)

The debt name is the literal placeholder. It is still open in the claim object and contradicted inside the entry.

**OBSERVATION.** `corpus/lessons/round-12-verifier-spotcheck.md:17` debt: give the C1 entry an `S###` source row and disclose the unpaired custody legs. `corpus/lessons/round-18.md:88` carries “no `S###` row and no custody-leg disclosure” for `corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md`. `.ufo/waves/round-19/claims.json:32` `carried_open` still lists “r12 C1 entry S### row + custody-leg disclosure”. The amendments do not remove it.

**OBSERVATION.** The addendum header (`…r12-go-evidence-id-domain.md:34`) says it answers that lesson line. Custody legs are disclosed at `:50-57` (no pre-pair; post-only captures; current configs outside the last receipt). That half of the debt has text in the entry.

**OBSERVATION.** Source rows the addendum actually uses for a proposition are S024, S026, S031 (`:40-42`), and they ground the Go version token `go1.26.5-X:nodwarf5`, with S026 marked INFERENCE for the 1.26.5 linker.

**OBSERVATION.** `:44-47` then says the entry’s own subject is ungrounded: “The REA package-source claims (entry lines 11, 13, 15, 19–25) and the identity of rea-agents@6.7.0. No row names rea-agents or npm (`grep -n -i -E 'rea-agents|npm' corpus/SOURCES.md` → no match).”

**OBSERVATION.** That grep is false at `d0690fd`. `git grep -n -i -E 'rea-agents|npm' d0690fd -- corpus/SOURCES.md` exits 0 and hits `corpus/SOURCES.md:43` (S037) and `:71` (search log).

**OBSERVATION.** `:71` and `corpus/lessons/round-19.md:94` nevertheless bundle S037 into the close: the lesson lists “S024/S026/S031/S037” as the source/custody addendum and records that S037 used-by was extended to this knowledge file. `:71` itself only says package identity “is now also registered as S037”.

**OBSERVATION.** `scripts/sources-census.sh` validate checks used-by path existence (E11, script lines 563–568) and table shape. It does not compare a row’s scope cell to the claims in the used-by file. On this lane, `validate --today 2026-10-20` exits 0 with one warning, `W04 S033` (pre-existing duplicate URL). `census` exits 0, `rows 38`, `status.mined 36`, `status.rejected 2`. A green census is compatible with `:47` being false and with S037’s used-by pointing at an evidence-id entry.

**INFERENCE.** S024/S026/S031 are real rows for the version-token subclaim. They do not ground `inspect_go_binary`’s evidence-id projection (entry lines 11, 13, 15, 19–25). S037 grounds publish identity only (`SOURCES.md:43`). Listing S037 beside them in `round-19.md:94` records a discharge the addendum’s own “Not grounded” list does not support. Custody disclosure and the S### outcome-row are separate; only the first is present.

### 3. Coverage ground

**OBSERVATION.** SCORECARD command A (`SCORECARD.md:88-124`) intersects `corpus/knowledge/*.md` stems with regex `2026-10-\d{2}-[a-z0-9-]+` inside the `## Coverage map` section only. The Knowledge table is outside that section (`corpus/README.md:70` starts `## Knowledge`).

| REV | knowledge files | mapped ∩ files | missing | dangling | `round(10 * mapped / files, 2)` |
|---|---|---|---|---|---|
| `8a8da7e19375aadc66c6bcbff0bbcbb596048fb0` | 96 | 96 | `[]` | `[]` | 10.00 |
| `d0690fd44f46d8a7fe9da5f01c6be723d12abd41` | 97 | 96 | `["2026-10-20-r19-go125-toolchain-replay"]` | `[]` | 9.90 |

Raw ratio at the tip: `960/97 = 9.8969072165`, rounded 9.90 by the scorecard rule. The r19 stem is absent from the map section. It is present in the Knowledge table at `corpus/README.md:154`. The Go chain token list at `corpus/README.md:35` stops at `2026-10-20-r18-swiss-map-replay`. `corpus/README.md:9` says a row is written when its file exists; that sentence governs the index, and command A does not read it.

**OBSERVATION.** `SCORECARD.md:2497-2498`: “Coverage unchanged; no new coverage-map ground is claimed.” Round 18’s measured map was 95/95 → 96/96 (`SCORECARD.md:2454`), which is B’s 96/96. The tip’s command A is 96/97.

**OBSERVATION.** `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:102-105` still says both held-out confirmations are Go 1.24.x and that the 1.25 half “rests on calibration plus source, not on a held-out run.” The r19 entry `:42` (commit; same line in the dirty prefix) says it upgrades the artifact-held-out half of that limit. r18 has no append pointing at the r19 file. w1 `CoverageMapGo125.md:35-36` asked for the README chain update and an append on that r18 limit. The Knowledge-table row landed; the map token and the r18 pointer did not.

**INFERENCE.** “No new coverage-map ground” is right as a domain claim: the file deepens the held Go chain (round 18’s expansion rule at `SCORECARD.md:2464-2465`). “Coverage unchanged” is false for the owned proxy. The Knowledge-table citation is not coverage ground, the same way S037 used-by is not outcome ground.

## Contradictions (kept separate)

1. Identity scope vs outcome header. `SOURCES.md:43-44`, `round-19.md:28`, `claims.json:41`, r19 entry `:1` and `:15` limit S037/S038 to identity/provenance. `round-19.md:14-16` and `SCORECARD.md:2494-2495` label the freshness and depth claims “sourced” by those ids.
2. S### discharge vs the entry. `round-19.md:94` and r12 `:71` register S037 as the missing source. r12 `:44-47` still says the evidence-id claims and rea-agents identity are ungrounded, and the grep sentence in `:47` is false at this tip. `claims.json:32` still carries the S### item.
3. Coverage prose vs command A. `SCORECARD.md:2497-2498` says coverage unchanged. Command A at the tip is 9.90 with one missing stem. `README.md:154` does not enter the instrument. `README.md:35` does not contain the stem.
4. Prior limit vs new entry. r18 `:102-105` still states the 1.25 calibration-plus-source limit. r19 `:42` says that half was upgraded. No append on r18.

Census exit 0 does not resolve 1–2. A Knowledge-table row does not resolve 3.

## Trend verdicts (recommendation only)

Not an outside admit/reject. `round-19.md:50-52` still pending. Do not write these as self-attested closures.

- **Expansion: unchanged.** The r19 file deepens held Go ground. S037/S038 are repertoire rows for identity, in the sense round 17 already used for new source kinds (`SCORECARD.md:2407-2410`). Do not score a new surface from a Knowledge-table row or from two dataset rows.
- **Quality: do not record improved.** The r19 entry does keep identity and the log outcome apart, and it records compares 7/8 rather than an 8/8 success (`:1`, `:15`, and the decision table). That local care is cancelled, for a round-level trend line, by the false grep at r12 `:47`, the S037 discharge bundle at `round-19.md:94`, and the coverage sentence at `SCORECARD.md:2497-2498` against a measured 9.90. Those are new overclaims. State them; do not average them into “quality improved”.
- **Discernment: unchanged, and not self-attested.** The author gate at `round-19.md:28-34` already rejects census PASS, the emulator `diagnostic` field as D, and “application” / “first 1.25 holdout” wording. Outside sampling has not happened. This seat adds no admit.

## One move

Treat the instrument’s ground as the authority, and repair the two places that currently cite an index instead.

1. Insert the stem `2026-10-20-r19-go125-toolchain-replay` into the existing Go chain at `corpus/README.md:35` (same row, no new map section). Command A then has missing `[]`, 97/97, score 10.00. Expansion stays unchanged. Domain ground stays the held Go chain. `SCORECARD.md:2497-2498` can keep “no new coverage-map ground” only together with the measured 97/97; “coverage unchanged” is available again only after that token exists.
2. Replace the false grep sentence at r12 `:47` with a sentence that names S037 and keeps the limit: S037 is the publish-identity row; entry lines 11, 13, 15, and 19–25 stay without a source row. In `corpus/lessons/round-19.md:94`, take S037 out of the S### parenthetical. Custody text can stay. Add one `## Paths` bullet: S037 and S038 stop at publish identity and archive-member identity; pin-drift equality, the census verdict, and analyzer logs stay with their receipts. Leave `claims.json:32`’s S### item in `carried_open` until that sentence is the one the lesson points at.

Do not delete the “Not grounded” bullet because the grep now matches. Do not rewrite r18 `:102-105` in place; the r19 entry already points at that limit.

**Axes.** Calibration gains a coverage proxy that matches the file set, and an S### record that matches S037’s scope cell. Freshness gains a true grep sentence. Depth is untouched: mechanism stays S035 → S023 → S003 plus the bound logs; S038 stays carrier provenance. Expansion is not scored up.

## Risks

- Deleting r12 `:47` because S037 exists would make an identity row the outcome source for the evidence-id projection. That harms calibration and depth.
- A new coverage-map section, or an “expansion improved” line for this file, would count held Go ground twice.
- An in-place edit of r18 `:102-105` would erase the limit the r19 comparison is measured against.
- The dirty hunk in the r19 knowledge file (uncommitted, after line 45) is not this move. The map token is the filename stem.
- `sources-census.sh validate` will stay exit 0 either way. It is not the check. Re-run command A.
- w2 `ReopenS038.md` found S038’s digest still matches and noted `claims.json:28` vs `:41`. This move does not reopen that digest and does not pick S034 back up as the mechanism source.

## Verification (for the L1, after the edit; not run here)

- Command A at the edited tip: `missing=[]`, `knowledge_files=97`, `coverage_score=10.00`, dangling empty.
- `git grep -n -i -E 'rea-agents|npm' <REV> -- corpus/SOURCES.md` still exits 0 on S037. The addendum must not say “no match”.
- S037 scope cell still contains “not the package's runtime behaviour”. S038 scope cell still stops at the archive digest. Paths line 51 still gives the Swiss outcome to replay receipts.
- No edit to compare counts, prediction freeze `a1140e7`, or r18’s original cohort paragraph.

## Commands and exits

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
d0690fd44f46d8a7fe9da5f01c6be723d12abd41
exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse --verify 8a8da7e19375aadc66c6bcbff0bbcbb596048fb0^{commit}
8a8da7e19375aadc66c6bcbff0bbcbb596048fb0
exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin status --porcelain -- corpus/README.md corpus/SOURCES.md corpus/knowledge/2026-10-19-arc3-r12-go-evidence-id-domain.md corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md corpus/knowledge/2026-10-20-r18-swiss-map-replay.md corpus/lessons/round-19.md SCORECARD.md .ufo/waves/round-19/claims.json
 M corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md
exit 0
```

Command A (Git objects only; rule is the script’s `rule` field). Exit 0. Tip JSON: `coverage_score` 9.9 (that is 9.90), `missing` the r19 stem. Baseline JSON: `coverage_score` 10.0, `missing` [].

```
python3 -I -B - <<'PY'
import json, pathlib, re, subprocess
lane = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"
revs = ["8a8da7e19375aadc66c6bcbff0bbcbb596048fb0", "refs/heads/main"]

def git(*args):
    p = subprocess.run(["git", "-C", lane, "--no-optional-locks", *args], text=True, capture_output=True)
    return p.returncode, p.stdout, p.stderr

def measure(rev):
    rc, out, err = git("rev-parse", "--verify", f"{rev}^{{commit}}")
    commit = out.strip()
    rc, paths, err = git("ls-tree", "-r", "--name-only", commit, "--", "corpus/knowledge")
    files = {pathlib.PurePosixPath(p).stem for p in paths.splitlines() if p.endswith(".md")}
    rc, readme, err = git("show", f"{commit}:corpus/README.md")
    section = readme.split("## Coverage map\n", 1)[1].split("\n## ", 1)[0]
    mapped = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", section))
    know = readme.split("\n## Knowledge\n", 1)[1].split("\n## ", 1)[0]
    know_tokens = set(re.findall(r"2026-10-\d{2}-[a-z0-9-]+", know))
    inter = files & mapped
    return {
        "commit": commit,
        "knowledge_files": len(files),
        "mapped_tokens_in_files": len(inter),
        "missing": sorted(files - mapped),
        "dangling": sorted(mapped - files),
        "coverage_score": round(10 * len(inter) / len(files), 2),
        "r19_in_map_section": "2026-10-20-r19-go125-toolchain-replay" in mapped,
        "r19_in_knowledge_table": "2026-10-20-r19-go125-toolchain-replay" in know_tokens,
    }

for rev in revs:
    print(json.dumps(measure(rev), sort_keys=True))
PY
```

```
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin --no-optional-locks diff -- corpus/knowledge/2026-10-20-r19-go125-toolchain-replay.md
exit 0
```

The diff is one insertion after the receipt paragraph (Evidence id `ev_3dc824c4…`, subject sha256 `9b9d776e…`). It is not used as coverage or S### evidence.

```
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --today 2026-10-20 --root /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokunin/kaidoku-shokunin
kaidoku-shokunin	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku-shokunin	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
census_validate_exit=0

/home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --today 2026-10-20 --root /home/vgpnk/Projects/shokunin /home/vgpnk/Projects/shokunin/kaidoku-shokunin
kaidoku-shokunin	rows	38
… status.mined 36, status.rejected 2, FLEET.missing 0
census_exit=0
```

Paths check at `d0690fd:corpus/SOURCES.md`: `paths_mentions_S037 False`, `paths_mentions_S038 False`, outcome sentence at line 51. Helper exit 0.
