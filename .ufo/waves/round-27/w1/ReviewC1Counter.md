# ReviewC1Counter — attack of tools/round-27/c1-rename-identity.py against R27-C1 (round 27, wave 1)

Date 2026-10-22. Seat KaidokuR27.ReviewC1Counter. Lane rev reviewed: main HEAD = a4f674b343d8564e21f7eb8984630a95089c82d6
(freeze commit); base cd32264f7ee356a9c0f48bd8e3fcdac222db22a0. LSP device: no server answers in this lane (plain text
review; no semantic index available) — noted per reviewer protocol.

## Verdict

holds — every rule clause in claims.json R27-C1 maps to enforcing code; both required commands reproduce their frozen
receipts; no false accept lets a false statement pass. Three coded widenings/deviations from the claims rule text are
recorded below (F1-F3); none breaks the statement because a completing row still requires recomputing evidence ids,
distinct envelope bytes, carrier digests, and both-path string checks.

## Pin and freeze facts (all observation)

- `sha256sum tools/round-27/c1-rename-identity.py` at main = e0a079955c16a759dc3ba4facb6d954431ce605ea2a6da680f43b20cea743bb7,
  equal to claims.json instruments pin; `git show a4f674b:tools/round-27/c1-rename-identity.py | sha256sum` identical. Exit 0, 2026-10-22T14:52Z.
- Freeze commit a4f674b = 1792680683 = 2026-10-22T14:51:23Z (%ct), message "round-27: freeze claims; commit both
  counters, red selftests and before receipts before any data"; `git ls-tree -r` at that commit contains claims.json,
  both counters and before/c1-at-cd32264f.txt + c1-selftest.txt, and no corpus/evidence/round-27/c1. Exit 0, 14:54Z.
- tools/round-26/recompute-ids.py sha256 89afa3756a9b101c8ef6c5274f7ed68dc3533a306812906780949941fd60208b, byte-identical
  at base, at a4f674b, and in the working tree; `git diff --stat cd32264f a4f674b -- tools/round-26/recompute-ids.py`
  empty. The counter loads it from REV bytes (load_recompute, lines 136-149), never the working tree. Exit 0, 14:55Z.
- Carrier constants match reality: sha256 of /usr/bin/jq and its renamed copy both e81566…7806 (size 30800); /usr/bin/tinyxxd
  and its renamed copy both 7b1e5d…ae65 (size 38928). Exit 0, 15:02Z.
- recompute-ids.py compute_evidence_id (line 187) is pure: "ev_" + sha256 of canonical_json(semantic_projection(data));
  projection (lines 161-182) covers subject{digest,format,architecture}, provider, analysis_profile, predicate_type,
  operation, parameters, raw_result, normalized_result, confidence, authority, environment, limitations,
  relationship_coverage, locations, evidence_links — no filesystem name or path.

## Clause map (claims "rules" -> counter code; all observation)

| Clause | Enforced at | Notes |
|---|---|---|
| runs.tsv/table.tsv headers frozen | read_tsv 125-131 | header mismatch raises InputError -> exit 2 (main 589-606), still refuses |
| exactly one table row and one runs row per (carrier,verb,run) | 226-227, 231-232 | |
| run path = frozen base/renamed path | 238-239 | |
| argv = frozen template with path and carrier addr | 240-241 | |
| exit 0 | 242-243 | |
| utc_start parses and is not before counter commit | 244-246, 98-101, 103-109 | first_commit_time = oldest add, %ct |
| pkg_version 6.5.0 and pkg_json_sha256 a50030…0a6c | 247-248 | |
| envelope sha256 distinct across all rows and equal to file bytes | 219-221, 249-250, 259-261 | sha_count global |
| envelope exists at REV and first committed not before counter | 252-258 | |
| ok envelope (ok is True, data dict) | 262-270 | |
| meta.command = verb | 271-272 | |
| evidence_id is ev_…, equals runs.tsv cell | 274-279 | |
| evidence_id recomputes under 6.5.0 rule | 280-284 | any recompute exception fails the row |
| subject sha256 = carrier | 286-292 | also runs.tsv cell (290-292) and table cell (313-314); fallback F2 |
| own path present in envelope bytes, other path absent | 293-296 | substring on raw bytes |
| subject.name = run file name | 297-298 | conditional "when present" — F1 |
| verdict unstable/content-keyed/rename-sensitive re-derived | 300-305 | priority as in rules text |
| table id cells, verdict, subject_sha256 match envelopes | 307-314 | |
| entry cites table + new/mined/opened/Gate S row | check_entry 166-201 | source: line 171-176; new since base 191-192; row[7]=status (col 8) and row[8]=opened (col 9) of SOURCES at 193; Gate membership 182-193 |
| exit 0 iff 16/16 complete and entry_ok = 1 | run_count 320-331 | matches target; 1 otherwise; 2 input error |

SOURCES.md header confirmed: col 8 = status, col 9 = opened — the counter indexes row[7]/row[8] correctly.

## Findings (severity order; each demonstrated in a sandbox git repo under the seat dir)

- F1, medium, false accept vs claims rule text — `subject.name` is checked only when the key exists (297-298).
  Concrete input: build the green state, delete `data.subject.name` from all 48 envelopes, resync envelope_sha256,
  commit. Output: `rows_complete=16/16 entry_ok=1`, exit 0 (probe.py case A, 15:01:40Z). Aggravating: the evidence id
  does not project name or local_path, so nothing else committed binds the file name. The counter docstring says
  "(when present)", so intentional as coded; claims.json "rules" summary omits the conditional. A real REA envelope
  always carries subject.name, so the live claim is not endangered; recommend enforcing presence or fixing the rules
  wording at the next freeze.
- F2, medium (coded widening) — "subject sha256" is accepted from `normalized_result.artifact.sha256` when
  `data.subject.digest` is absent (286-292). Concrete input: envelopes born without subject.digest, carrier sha in
  normalized_result.artifact.sha256. Output: `rows_complete=16/16 entry_ok=1`, exit 0 (probe2.py, 15:02:39Z).
  Legitimate under "as coded in the pinned counter", but the claims summary does not disclose the second slot.
- F3, low, false reject hazard — check_entry parses only the FIRST `source:` line (174). Concrete input: entry with
  `source: S900` then `source: \`corpus/evidence/round-27/c1/table.tsv\`; S900`. Output: `entry: source: line does not
  name …table.tsv`, rows_complete=16/16, entry_ok=0, exit 1 despite a qualifying second line (probe.py case D).
  Seats write one line today; a multi-line entry would be refused.
- F4, low, selftest gap — the envelope first-commit gate (256-258) has no selftest case (22 cases, none targets it).
  Gate verified live: green state with data committed before the counter commit yields all 16 rows
  `envelope first committed before the counter`, exit 1 (probe.py case B). Enforcement exists; only the red test is missing.
- F5, info, boundary — utc_start equal to the counter commit second passes (probe.py case C: `COMPLETE jq analyze`,
  exit 0). Consistent with freeze_kind "runs that started … before its own commit" (>= not >). Gate uses committer
  time (%ct); a future jj rewrite of committer times would move the gate — none in scope.
- F6, info — non-UTF-8 envelope bytes raise an uncaught UnicodeDecodeError (json.loads 262, text decode 283): traceback,
  exit 1, no rows_complete line. Still refuses completion, so no false accept, but the failure mode is a crash, not a
  row reason. Extra runs.tsv rows and foreign-carrier table rows are ignored except for global sha distinctness —
  they can only cause false rejects, never false accepts.

Attacks that failed (counter caught them): envelope byte swap base->renamed and single-run reuse with resync
(selftest cases 1-2, sha equality + distinctness); swapped verb envelopes (meta.command); consistent forged id across
envelope/runs/table (recompute mismatch); verdict and table-cell tampering; entry citing a base-era row, wrong status,
or a row outside ## Gate (selftest cases 3-22). No false accept found in any clause other than F1/F2.

## Commands run (observation)

1. `python3 -I -B tools/round-27/c1-rename-identity.py --selftest` — exit 0, 2026-10-22T14:58:57Z.
   Output ends `selftest cases=22 failures=0`; all 22 PASS lines byte-identical to the frozen receipt
   .ufo/waves/round-27/before/c1-selftest.txt (diff clean after dropping the receipt's trailing captured `exit=0` line).
2. `python3 -I -B tools/round-27/c1-rename-identity.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev cd32264f7ee356a9c0f48bd8e3fcdac222db22a0`
   (the claims.json counting/before command at the base) — exit 1, 2026-10-22T14:58:56Z.
   Excerpt: `entry: entry absent` / `rows_complete=0/16 entry_ok=0 rev=cd32264f7ee356a9c0f48bd8e3fcdac222db22a0`.
   Matches the frozen receipt .ufo/waves/round-27/before/c1-at-cd32264f.txt line for line (receipt additionally carries
   the captured `exit=1` line); before figures 0/16, entry_ok 0, exit 1 confirmed.

## Residual risk and verification gaps

- The counter verifies internal consistency of committed bytes; it cannot prove envelopes came from real npx runs
  (a forger able to compute 6.5.0 ids could fabricate self-consistent envelopes — the green selftest builder does
  exactly that). Package columns are asserted, not measured. Authenticity rests on seat discipline and wave-2 falsifiers.
- Path binding is substring presence of the plain path text; an envelope writer that escaped `/` (e.g. `\/`) would
  false-reject. REA writes plain paths; not exercised here.
- `[INFERENCE]` next merge-commit-in-history edge: first_commit_time relies on default git log simplification; a file
  first added in a merge commit could be missed. Lane history is linear jj; not tested.
- Not in my scope: REA runs against carriers (none run), R27-C2, SOURCES web provenance.

## Artifacts (seat scratch, sha256)

- out/selftest.txt 076519e5420df7a5256c589480be78729d2f22b57c2fa515d36c3c84a4530dab
- out/before-cd32264f.txt 27d7bbbc964302934135eb5f18cc8314601f55c31cf73515db0dcc6797b0ea56
- out/probe.txt b154960a945fab1e4995610bc05f54a1d5f2cab97643d6d2443e6aa39c98a64b
- out/probe2.txt eda01a37dc4b94928a05b7c10f9e0ec1da456e70a2aa0b976c4df3385a255bf1
- attack/probe.py 9cee2c573c6089fa158c63683894195a7fed94ef065481d144ceed1a2b47b876
- attack/probe2.py 8273993636f375fb9fd5307f30b77ef72f3733f27618977bcf23c255a6fb541b

Tooling directive: no installs or upgrades were needed or performed. Lane untouched except this assigned report file;
all git writes happened in sandbox repos under the seat scratch dir.
