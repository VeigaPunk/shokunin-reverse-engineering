# RevPredicateIdentity — predicate identity: claims.json sentence vs counter code vs output label

Scope: does the frozen predicate sentence in `.ufo/waves/round-30/claims.json`
(`predicate`, `predicate_label`) equal the condition each counter's code enforces
and the label its output prints? Files read in full:

- `.ufo/waves/round-30/claims.json` (frozen at 4ee65c67)
- `tools/round-30/c1-rust-positive.py` (sha256 `e07563d6…`, matches the frozen
  `instruments` pin; observed `sha256sum` 2026-10-23T02:42:27Z)
- `tools/round-30/c2-rust-refusals.py` (sha256 `1c357fca…`, matches pin)
- `tools/round-30/rust_dep_oracle.py` (sha256 `f0b144c6…`, matches pin) — needed
  to confirm `normalize()` emits the same tuple shape as both counters'
  `rea_tuples()` (it does, verbatim: `(name, version, source, kind|None,
  bool(root), sorted (dep_name, dep_version))`, list sorted by `repr`).

All line numbers below are of the pinned files on disk.

## Identity of the sentence and label (mechanically verified)

- The P1 docstring block (c1-rust-positive.py:4–14) and the P2 docstring block
  (c2-rust-refusals.py:9–17) are the claims.json `predicate` strings verbatim
  (whitespace-normalized comparison, exit-verified by a python3 -I script on
  2026-10-23T02:4xZ: `P1 claims==docstring: True`, `P2 claims==docstring: True`).
- Output labels: c1 prints `PASS_LABEL = "P1-pass"` (c1:47, printed c1:252);
  claims `predicate_label` = `P1-pass`. c2 prints `MATCH = "P2-match"` (c2:54,
  printed c2:368); claims `predicate_label` = `P2-match`. Identical. (The
  counters' negative labels `P1-fail`/`P2-miss` are internal and not part of the
  frozen claims.)

## P1 clause-by-clause (sentence claims.json line 14)

| # | Clause | Code line(s) | Enforced? |
|---|--------|--------------|-----------|
| 1 | live REA 6.5.0 inspect-rust-binary run | c1:40 `REA=["npx","-y","rea-agents@6.5.0"]`; c1:127 argv `inspect-rust-binary <path> --format json --full-output`; c1:224–228 pins installed `package.json` version == `6.5.0` | yes |
| 2 | exits 0 | c1:96–97 `exit_code != 0` → P1-fail | yes |
| 3 | ok envelope | c1:98–99 `env.get("ok") is not True` → fail (env = parsed stdout, c1:237–240; unparseable stdout ⇒ `env=None` ⇒ fail) | yes |
| 4 | operation is inspect_rust_binary | c1:100–102 | yes |
| 5 | subject sha256 == carrier's frozen sha256 | c1:103–105 compares envelope `subject.digest.sha256` to `r["sha256"]` from the frozen `carriers.tsv` (frozen file equality pinned c1:209–215; per-carrier sha pinned c1:220–223) | yes |
| 6 | auditable_metadata package list equals multiset of (name, version, source, kind, root, dependency (name,version) set) tuples | c1:85–91 `rea_tuples` builds exactly that tuple shape; c1:116–117 `got != oracle_tuples` → fail | yes |
| 7 | equals the list the independent oracle decodes from the carrier's own .dep-v0 section | c1:234–235 `sec, doc = oracle.read_file(r["path"]); tuples = oracle.normalize(doc)`; `read_file`/`locate`/`decode`/`normalize` in rust_dep_oracle.py:99–135 slice the carrier's own section bytes and emit the same tuple shape | yes |
| 8 | oracle list is non-empty | c1:110–111 `not oracle_tuples` → fail (combined with clause 6 ⇒ REA list also non-empty) | yes |
| 9 | REA file_offset == oracle section offset | c1:118–119 | yes |
| 10 | REA compressed_bytes == oracle section size | c1:120–121 | yes |
| 11 | committed envelope first added after the freeze commit | c1:169–179 `freeze_time`/`added_time` (earliest `--diff-filter=A` committer times); c1:186–187 `env_added is None or env_added <= freeze_ct` → fail | yes |
| 12 | committed envelope carries the same evidence_id | c1:188–193: committed `ok is True` required, `cid` truthy required, `cid != lid` → fail | yes (and stricter, see below) |
| 13 | committed envelope carries the same package multiset | c1:194–201: committed `rea_tuples` vs the oracle tuples (equal to the live tuples whenever reached) | yes |
| 14 | round-30 entry names that evidence_id | c1:202–203 `cid not in entry_text` → fail (substring containment in the entry file at `--rev`) | yes |

**P1 unstated checks the code adds** (weaker-to-stronger; none contradict the
sentence, but a conforming envelope could be refused by them):

- `auditable_metadata` must occur **exactly once** as a distinct JSON value in
  the envelope data (c1:106–109 `len(metas) != 1`); the sentence says "whose
  auditable_metadata package list" — the singular phrasing supports this but does
  not literally say "exactly one".
- Committed envelope must be `ok is True` (c1:188) and must carry a *truthy*
  `evidence_id` (c1:192 `not cid` fails). The sentence's "carries the same
  evidence_id" implies existence; the explicit `ok` field check is a reasonable
  but unstated requirement.
- Exit-0 gates the sentence does not mention at all: the 16-row pin
  (c1:216–219), package-version pin (c1:224–228), `entry_ok` — entry exists,
  first `source:` line names S089, S089 row present in `corpus/SOURCES.md` at rev
  and absent at base (c1:142–155), and `province_ok` — a new PROVINCE.md line
  naming `inspect-rust-binary` and the entry path (c1:158–166). These are the
  `entry_ok=1 province_ok=1` fields of the frozen **target line**, i.e.
  claim-level conditions alongside the per-carrier predicate, so they belong to
  the target line rather than the P1 sentence. Consistent with claims.json line
  16 (`target`) — noted, not a defect.
- Timing quirk, honest direction: "first added after the freeze commit" is
  approximated by **committer timestamps** (c1:171,177), so an envelope commit
  authored with a skewed/backdated committer date fails even if it is a DAG
  descendant of the freeze commit. Fails closed — safe for the claim, worth
  knowing for diagnosis.

## P2 clause-by-clause (sentence claims.json line 29)

| # | Clause | Code line(s) | Enforced? |
|---|--------|--------------|-----------|
| 1 | live REA 6.5.0 inspect-rust-binary run | c2:42 `REA`; c2:348–349 argv identical shape to C1; c2:329–333 package version pin | yes |
| 2 | agrees with its frozen prediction | c2:200–228 `judge` dispatches on `pred["kind"]` read from frozen `predictions.tsv` (c2:324; file-vs-`--rev` equality pinned c2:325–328; mutant sha256s re-verified against the frozen file in `do_build` c2:305–309) | yes |
| 3 | refusal ⇒ envelope is not ok | c2:203–204 `env.get("ok") is True` → MISS; a missing/unparseable envelope also satisfies "not ok" (sentence read as "the run does not produce an ok envelope"; a stricter reading "an envelope exists and says not-ok" is NOT enforced — see notes) | yes (under the weaker reading) |
| 4 | refusal ⇒ frozen message appears verbatim in stdout or stderr | c2:205–206 `message not in out_text and message not in err_text` → MISS; `not message` fails empty predictions (frozen file has all 16 refusal messages non-empty) | yes |
| 5 | acceptance ⇒ exits 0 | c2:208 `code != 0` → MISS | yes |
| 6 | acceptance ⇒ ok envelope | c2:208 `env.get("ok") is not True` → MISS | yes |
| 7 | acceptance ⇒ operation inspect_rust_binary | c2:210–212 | yes |
| 8 | acceptance ⇒ subject sha256 == mutant's sha256 | c2:213–214 vs `sha(data)` of the rebuilt mutant bytes (c2:341,357) | yes |
| 9 | acceptance ⇒ package multiset == oracle's reading of the mutant | c2:215–224: exactly-one `auditable_metadata`, `oracle_reading is None` → MISS, `rea_tuples` vs `oracle.normalize` | yes |
| 10 | acceptance ⇒ file_offset == oracle offset | c2:226–227 | yes |
| 11 | acceptance ⇒ compressed_bytes == oracle size | c2:226–227 | yes |
| 12 | committed envelope first added after the freeze commit | c2:240–243 `first_add`; c2:334–336 `freeze_ct`; c2:247–248 `added <= freeze_ct` → disagree | yes |
| 13 | committed envelope agrees with live run on **ok** | c2:249–252 `c_ok != l_ok` → disagree | yes |
| 14 | committed envelope agrees with live run on **evidence_id** | c2:253–254 — guarded by `if l_ok` | **partial** |

**P2 unstated checks the code adds:**

- Acceptance requires exactly one distinct `auditable_metadata` (c2:216), the
  oracle reading to exist (c2:216 `oracle_reading is None` → MISS — the sentence
  presupposes an oracle reading, so this is a tightening only for mutants the
  oracle itself cannot parse), and a non-empty oracle list (c2:219–220 — the P2
  sentence does not say "non-empty" where P1 does).
- Prediction `kind` is not validated: any value other than the literal
  `"refuse"` falls into the acceptance branch (c2:202 vs 208). The frozen file
  contains only `ok` (3) and `refuse` (16) — observed `cut -f2 | sort | uniq -c`
  — so this cannot misfire under the frozen input; it is a robustness gap only.
- Exit-0 claim-level gates beyond the sentence: mutant rebuild + frozen-sha pin
  (c2:289–317), prediction-file pin (c2:325–328), package pin (c2:329–333),
  `entry_ok` (c2:258–270, S090/SOURCES/base-absence — same shape as C1), and
  `skill_ok` (c2:273–277: a SKILL.md line naming `inspect-rust-binary` and the
  entry, absent at base). Again these are the `entry_ok=1 skill_ok=1` fields of
  the frozen target line, not the P2 sentence.
- Refusals are checked on stdout/stderr **text** (UTF-8-replace decoded,
  c2:351–352); "verbatim" = substring of decoded text — a faithful reading.
- Per-mutant verdict lines carry `P2-match`/`P2-miss`; summary line
  `mutants=19 matches=… target=19 entry_ok=… skill_ok=…` (c2:381–383). The
  claims.json `target` string is a key-for-key match but not a contiguous
  substring of the printed line (the counter appends `(<reason>)` after
  `entry_ok=%d`/`skill_ok=%d`). Cosmetic; noted for any exact-string grepper.

## Finding (the one unenforced clause)

**P2 clause 14 is enforced only for the 3 predicted-accepted mutants.**
`committed_agrees` (c2:253) checks `evidence_id` equality only `if l_ok`. For a
predicted refusal the live envelope is not-ok, so the code requires the
committed envelope merely to exist after the freeze and to agree on `ok`
(not-ok == not-ok). The sentence says "agrees with the live run on ok **and
evidence_id**" unconditionally. Counterexample the code would pass while the
sentence fails: a committed refusal envelope carrying
`data.evidence_id = "ev_x"` against a live refusal run carrying no `evidence_id`
(or `ev_y`) → c2:253 skips the comparison → `committed_agrees` returns True.
Practical reachability is low — REA refusal envelopes plausibly carry no
`evidence_id`, and then both sides hold None-vacuous agreement — but as a
predicate-identity question the clause is not uniformly enforced. (P1 has no
such gap: c1:190–193 requires a truthy matching `cid` for every carrier.)

Secondary note (weaker): P2 clause 3 "the envelope is not ok" is enforced as
"no ok envelope" — an empty/invalid-JSON stdout satisfies it. This matches the
natural reading of a refusal (there may be no envelope at all) and is the only
sane implementation given refusal envelopes may legitimately be absent.

## Verdict

**fails (narrowly).** The sentences are verbatim-identical between claims.json
and both docstrings, the output labels equal `predicate_label`, and every P1
clause plus P2 clauses 1–13 are enforced. The single gap: P2's unconditional
committed-envelope `evidence_id` agreement is checked only when the live run is
ok, so for the 16 refused mutants the code enforces agreement on `ok` alone.

## Commands and evidence

- `read` of the three files above plus `rust_dep_oracle.py` — all quotes/line
  numbers from those reads (observation).
- `sha256sum tools/round-30/*.py corpus/evidence/round-30/{c1,c2}/*.tsv` → all
  five hashes equal the `instruments`/`frozen_inputs` pins in claims.json
  (observation, 2026-10-23T02:42:27Z).
- `python3 -I -B` heredoc comparing claims predicates to docstring strings →
  `P1 claims==docstring: True`, `P2 claims==docstring: True` (observation).
- `cut -f2 corpus/evidence/round-30/c2/predictions.tsv | sort | uniq -c` →
  `3 ok`, `16 refuse` (observation).
- No REA runs, no carrier/mutant execution, no lane writes other than this
  report. No tools installed; none needed. Conclusions labeled above are
  observations from the named code lines; the "low practical reachability" of
  the P2 gap is inference.
