# SOURCES registry census

## Pinned-baseline census

**Observation.** The input was pinned to `14f0260ad319ecc26994381b2415d5a999003375`. I extracted that revision under `/tmp/kr20-sources-census-3sygug3_`, then wrote the `git show` blob over `corpus/SOURCES.md`; the archive supplies the revision's referenced `used-by` paths. Both setup commands exited 0; the temp tree was removed after the runs.

```sh
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive --format=tar 14f0260ad319ecc26994381b2415d5a999003375 | tar -xf - -C /tmp/kr20-sources-census-3sygug3_
# exit 0; stdout/stderr empty

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 14f0260ad319ecc26994381b2415d5a999003375:corpus/SOURCES.md > /tmp/kr20-sources-census-3sygug3_/corpus/SOURCES.md
# exit 0; stdout/stderr empty
```

The following are the manual commands in `/home/vgpnk/Projects/shokunin/CORPUS.md:133-147`, run with the temporary tree as cwd. Outputs are verbatim (empty means no stdout); every command exited 0.

```sh
grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md
# stdout: 39
# exit: 0

awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF!=13 {n++} END{print n+0}' corpus/SOURCES.md
# stdout: 0
# exit: 0

awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {t=$5; gsub(/[[:space:]]/,"",t); n[t]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
# stdout: A=34 B=4 C=1
# exit: 0

awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {s=$9; gsub(/[[:space:]]/,"",s); n[s]++} END{for(k in n) printf "%s=%d ", k, n[k]; print ""}' corpus/SOURCES.md
# stdout: mined=37 rejected=2
# exit: 0

awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ {i=$2; gsub(/[[:space:]]/,"",i); print i}' corpus/SOURCES.md | sort | uniq -d
# stdout: (empty)
# exit: 0

awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {i=$2;k=$4;t=$5;s=$9; gsub(/[[:space:]]/,"",i); gsub(/[[:space:]]/,"",k); gsub(/[[:space:]]/,"",t); gsub(/[[:space:]]/,"",s); if (t !~ /^[ABC]$/) print "tier", i, t; if (s !~ /^(queued|mined|rejected)$/) print "status", i, s; if (k !~ /^(spec|docs|paper|code|tool|dataset|talk|book|community|own-work)$/) print "kind", i, k; if (t=="A" && k=="community") print "tier-inflation", i}' corpus/SOURCES.md
# stdout: (empty)
# exit: 0

awk -F'|' '/^\|[[:space:]]*S[0-9][0-9][0-9]+[[:space:]]*\|/ && NF==13 {s=$9; gsub(/[[:space:]]/,"",s); if (s=="mined") {n=split($12, a, /[,;]/); for (j=1;j<=n;j++) {p=a[j]; gsub(/^[[:space:]]+|[[:space:]]+$/,"",p); if (p!="" && p!="—") print p}}}' corpus/SOURCES.md | while read -r p; do [ -e "$p" ] || echo "missing: $p"; done
# stdout: (empty)
# exit: 0
```

**Observation.** The 39 baseline IDs are contiguous `S001`–`S039`; the last row is `S039` at `corpus/SOURCES.md:45` (first row `S001` at `:7`; pinned baseline). The next unused ID is **S040**, following the “next unused; never reused” rule (`CORPUS.md:89`).

## Maintained validator

**Observation.** Ran the requested command from `/home/vgpnk/Projects/shokunin`. Since `--root` points to the live fleet root and `kaidoku` resolves through its lane roster, this validates the live lane registry, not the pinned temp baseline (`scripts/sources-census.sh:450-469, 510-520`).

```sh
/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
```

Exit: **0**. Stdout:

```text
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

Stderr was empty. **Observation:** validation reports W04 for S033 and still reports `ok`; W04 is documented as a warning that does not fail validation (`scripts/sources-census.sh:31-33, 643-649, 741-765`). This result is scoped to the live path named above.

## Rules for a new registry row

**Observation (contract).** Add it under `## Registry` using the 11 named cells in the table (13 fields when split on `|`); do not put `|` inside a cell (`CORPUS.md:76-90`; manual malformed-row check at `:136-137`). The row must satisfy:

- Use the next unused `S` + at least three digits; never reuse an ID (`CORPUS.md:89`).
- Record a source title and canonical URL/DOI; `own-work` may instead use a repo path or command (`:90`).
- `kind` must be one of `spec`, `docs`, `paper`, `code`, `tool`, `dataset`, `talk`, `book`, `community`, `own-work` (`:91-92`).
- Choose scoped tier A/B/C honestly; community is never A. Anchor the claim to an exact section/heading/page/line and version, commit, or publication date—not a bare homepage (`:93-100`).
- `teaches` must state a grounded learner benefit. For a rejection, use `REJECTED: <reason>; flip: <what would change the verdict>` (`:101-102`).
- Status is `queued`, `mined`, or `rejected`; `opened` is the author's valid ISO open date; `recheck` is a valid ISO date or cadence such as `90d`, `180d`, `on-release` (`:103-106`). A mined row must name at least one existing repo-relative citing knowledge/lesson path in comma-separated `used-by`; otherwise use `—` (`:103-108`; validator path check at `scripts/sources-census.sh:538-568`).
- Open the source in the round that writes the row. The round lesson's `## Gate` must record its URL, access date, and a ≤25-word quote with location grounding `teaches` (`CORPUS.md:112-115`). Keep edits append-only: only `status`, `recheck`, and `used-by` may change in place; a correction is a new row whose `teaches` starts `supersedes S0NN —` (`:116-118`).
- Avoid credential/private URLs or `op://` material (`CORPUS.md:129`). For a new bounded search, update `## Search log` with query/question, where searched, date, identified/screened/included/excluded counts, exclusion reasons, and stop rationale (`:126-128`).

**Validator-specific observations.** New rows must pass the E checks for exact row shape, ID uniqueness, duplicate URL+scope, enum values, valid nonfuture `opened`, `recheck`, community/tier-A, and existing mined `used-by` paths (`scripts/sources-census.sh:634-674, 538-568`). A duplicate URL+scope against a non-rejected row needs `supersedes SNNN` in `teaches` or triggers E04; a same URL across scopes is W04. W01/W02/W03/W04 are warnings, not clean-lane failures (`:31-33, 643-674`).

**Inference.** Given this baseline registry and the contract's no-reuse rule, integration should allocate S040 unless an intervening addition has already claimed it.
