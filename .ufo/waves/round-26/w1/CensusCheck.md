# CensusCheck — SOURCES registry readiness for S079 / S080 (kaidoku round 26, wave 1)

Seat: KaidokuR26.CensusCheck, leaf. Scope: census validate, row count at base
a0639d8e, id-freeness of S079/S080, and the CORPUS.md per-row contract for two new
code/dataset rows. Read-only on the lane except this report. No tools installed or
upgraded (none needed; pacman transactions paused per host directive).

## Findings

F1 — Census validate, working tree. Observation. 2026-10-22T12:12:45Z, exit 0.
Command: /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku
Excerpt (full finding set):
  kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
  kaidoku	W04	S047 duplicate url go.dev/dl/?mode=json&include=all`, across scopes
  kaidoku	W04	S054 duplicate url developer.android.com/ndk/guides/abis across scopes
  kaidoku	W04	S062 duplicate url raw.githubusercontent.com/sigrokproject/sigrok-cli/sigrok-cli-0.7.2/doc/sigrok-cli.1 across scopes
  kaidoku	W04	S069 duplicate url www.wireshark.org/docs/man-pages/tshark.html across scopes
  kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
Verdict: holds — registry validates clean (exit 0); five W04 warnings, which per the
script header "warnings do not affect clean lanes". The S047 excerpt shows a stray
backtick-comma captured from that row's source cell; pre-existing, cosmetic here.

F2 — The five W04 warnings pre-exist at base. Observation. 2026-10-22T12:16:03Z, exit 0.
Command: sandbox clone (git clone -q <lane> seats/CensusCheck/clone; git checkout -q
a0639d8e…), then sources-census.sh validate <clone> (explicit dir arg; the roster
excludes conf rows with repo "."). Output: identical five W04 lines, then
  clone	ok	…/seats/CensusCheck/clone/corpus/SOURCES.md
Verdict: holds — wave 1 adds no new registry warning so far. Confounder disclosed: the
sandbox clone root is the lane repo itself, so a minimal shokunin.conf was added inside
the clone (scratch only, never in the lane).

F3 — Row count at base. Observation. 2026-10-22T12:12:45Z, grep exit 0.
Command: git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show a0639d8e:corpus/SOURCES.md | grep -cE '^\| S[0-9]{3} \|'
Output: 78. Last ids: `| S076`, `| S077`, `| S078`.
Working copy is byte-identical to the base blob: cmp exit 0 at 2026-10-22T12:17:41Z;
sha256 of both 002b8e17ec0876076c9aa632c511ac2812ce72aef46f152c016b27c51b1c62dd.

F4 — S079 and S080 are unused. Observation. 2026-10-22T12:12:45Z.
- No row: grep -nE 'S079|S080' corpus/SOURCES.md exits 1 (no match), base and worktree.
- Committed corpus: git grep -nE 'S079|S080' a0639d8e -- hits only two base64-noise
  strings inside .ufo/waves/round-20/w1/patches/WasmCompareLeg-2.patch (lines 113799,
  138092); not id citations.
- Worktree hits beyond that patch's copies: .ufo/waves/round-26/w1-spec.json,
  w1-dispatch.json, w1-task-result.json — planning text assigning "New SOURCES row S079
  … installed rea-agents 6.5.0 evidence-id minting code" and "New SOURCES row S080: the
  npm registry record for rea-agents@6.5.0" to sibling seats. Inference: dispatch
  references are not registry usage; both ids are free and are the next unused after S078
  (id rule: S + 3+ digits, next unused, never reused).

F5 — The Gate the rows must land in does not exist yet. Observation. 2026-10-22T12:14:37Z.
ls corpus/lessons/round-26.md exits 2 (No such file or directory). R26-C1 entry_ok
requires a SOURCES row opened 2026-10-22 whose id appears in corpus/lessons/round-26.md
under ## Gate; that lesson is written later this wave.

## Checklist — what a new code or dataset row (S079, S080) must meet

Contract: CORPUS.md "SOURCES.md — where a shokunin learns", contract v1 (frozen
2026-10-19, carried in full; changes are new contract versions, never edits).

Per-cell:
- [ ] 11 columns exactly, under ## Registry (E01 fields=13 means NF!=13; E12 row outside
      Registry). No | inside any cell. 0-3 leading spaces ok; 4+ = code block, ignored.
- [ ] id: S079 / S080 — next unused after S078, never reused (E02/E03).
- [ ] source: title — canonical URL or DOI (repo path or command only for own-work).
      Census takes the first https?:// token, strips #fragment and trailing /, lowercases
      the host; that normalized value is what W04/E04 compare.
- [ ] kind: enum — code and dataset are both valid kinds (E05 otherwise).
- [ ] tier: A/B/C scoped to scope, never global. A = primary/authoritative for that scope
      (spec, official docs, source code, original paper, maintainer statement, the lane's
      own re-runnable gate output); B = strong secondary with reproducible detail; C =
      lead only, never sole support. community never A (E10). No NATO/GRADE labels.
- [ ] scope: the claim or topic the tier applies to (half of the duplicate-URL key).
- [ ] anchor: exact section/heading/page/line plus revision (version, commit, or
      publication date). Never a bare homepage. For S079 that means the installed
      6.5.0 package path/commit; for S080 the registry record's version/integrity.
- [ ] teaches: one grounded learner benefit; rejected rows read
      REJECTED: <reason>; flip: <what would flip> (W02 if reason < 8 chars).
- [ ] status: queued | mined (cited by >=1 used-by path; W03 if mined with used-by —) |
      rejected (kept). New rows start queued.
- [ ] opened: ISO date the author opened the source, past/present only (E08).
      This round: 2026-10-22 — required for R26-C1 entry_ok.
- [ ] recheck: ISO date, NNd cadence, or symbolic (on-release) (E09).
- [ ] used-by: repo-relative paths, comma-separated, or — (E11 if a mined row's paths
      do not exist; W01 tier-C mined). queued rows use —.

Duplicate-URL machinery (sources-census.sh, observed semantics):
- W04: same normalized URL already seen in a different scope -> warning, exit stays 0.
  The lane already carries five (S033, S047, S054, S062, S069); a new row sharing e.g.
  an npmjs.com/rea-agents URL with its sibling row would add a sixth. Non-fatal but
  avoidable: give S079 and S080 distinct sources (S079 can be a local repo-path/command
  source, which skips both checks since u=""; S080 the registry-record URL).
- E04 (fails, exit 1): same URL within the same scope where a prior non-rejected row
  holds it, unless teaches contains "supersedes S0NN". Rejected prior rows are exempt.
- Related corpus rules: append-only (new rows appended; only status/recheck/used-by
  change in place, logged old->new in the round lesson); no credential material,
  session/private URLs, or op:// refs (rule 6); any bounded search behind the rows gets
  a ## Search log entry (rule 5); no row quota (rule 4).

Gate (contract rule 1 + R26-C1 entry_ok):
- [ ] Write the row only after opening the source in the round that writes the row.
- [ ] corpus/lessons/round-26.md ## Gate records, for every new row: the URL, the access
      date (2026-10-22), and a <=25-word quote with its location grounding teaches
      (a quote names its location). Non-author verification re-opens a sample.
- [ ] The S079 / S080 ids must literally appear in the ## Gate section for the C1
      knowledge entry to pass entry_ok.

## Artifacts (all under /fast/scratch/hyaku/kaidoku-r26/seats/CensusCheck/)
- census-worktree.out sha256 75ae4b1633b3d7ba5d3ee4add8a4e57ba12b0a48011d3bdce9fd8269b0ec3bde
- census-base.out     sha256 f01f614277395350f6073758c4bf718f3c45dd0c46b2b56a3105bee8825b11c9
- clone/              sandbox clone of the lane at a0639d8e (read-only checks; contains
                      scratch-only shokunin.conf sha256 848ee52ce58e17a66773d71f6d94fb454d1e1f3db1ac1ec4c072727afcd6df01)
- tmp/                empty (no REA calls in this seat's scope)

## Verdict and residual risk
Registry readiness: holds. Census exit 0 with five pre-existing W04 warnings; 78 rows at
base and worktree, ending S078; S079/S080 unused and free; checklist above states every
contract requirement. Gaps: the rows and the round-26 ## Gate do not exist yet — both are
wave-1 landing work outside this seat; until they land, R26-C1 entry_ok is 0 by design.
Unknown: none within scope.
