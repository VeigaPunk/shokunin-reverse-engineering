# R44C2Sentinel — adversarial review of the R44-C2 rubric + counter (post-fix pass)

Seat `R44C2Sentinel` (sentinel). Base `c29360e3ba5381a5ab69e372d0d9577970f85018`; lane HEAD at
review close `9a8de923053978342fdba6ce047e1cca4eda9dd2`.
**Artifact reviewed:** `.ufo/waves/round-44/w1/artifacts/R44C2Counter/c2-counter.py`, 1341 lines,
sha256 `c80f25866efb044a7ddf7ffac9b17443bf1f0f8c33d0bbbdf2ade0d1eb811eb4` (read, run, and
probed at that sha), plus `dev-rubric.json`, `dev-rubric-landing-{bound,unbound}.json`, the
seat's seven receipts, its report `.ufo/waves/round-44/w1/R44C2Counter.md`, `plans/round-44-claims.md`
at `fc5eb54a`, and the C2 seat contracts in `.ufo/waves/round-44/w1-spec.json`.
Read-only: this seat wrote only this report and its probe scratch
(`/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Sentinel`, `probe-` prefix honored). No REA, no
network, no lane mutation, no C1 data procedure.

The counter is under active edit; every finding below was re-probed against the sha above after
the seat's "all four blockers addressed" message. Status of the v1 review is in §Status.

## Measured ground truth (command A, frozen recipe, git objects only)

| rev | knowledge_files / mapped | citation_resolved_rules / rule_blocks | SCORECARD assertion for that rev |
|---|---|---|---|
| `c29360e3` (R44 base) | 137 / 137, `missing []`, `dangling []` | 21 / 21 | — (no pin) |
| `4d62ee5a` | 130 / 130 | 19 / 19 | `SCORECARD.md:23` "130/130 … command A at `4d62ee5a`" ✓ |
| `e1c83313` | 133 / 133 | 20 / 20 | `SCORECARD.md:23` "133/133 … at `e1c83313`" ✓; `:24` "20/20 … at `e1c83313`" ✓ |
| `8de80f1d` | 137 / 137 | 21 / 21 | `SCORECARD.md:3508` "`knowledge_files=137`, `mapped=137` … `citation_resolved_rules=21/21`" ✓ |

Every pinned value is **true at its own pin** and differs at REV. 12 sampled `## Capabilities`
evidence pointers all resolve at base (receipt R-05). Pointer existence is thus currently green
and uninformative (H2).

Peer records that bear on these findings (read, not re-derived here):
- `R44C2Readme.md` finds four genuine `corpus/README.md` mismatches (dangling `.ufo/waves/kaidoku-r5/05-riscv-deep.md`,
  a malformed date stem, a 4-cell lessons row, a phantom `lessons/round-13-distillation` entry) and
  reports the headline map count clean at base — so the honest stop does not fire and C2 continues,
  while the *headline* check (category b/f) is the one O1 must not score at REV.
- `R44CritC2.md` A2/F4 independently records the self-reference channel that O2 demonstrates
  end-to-end ("a check argv may read its command out of the file under test").

## Status against the v1 review

| v1 finding | status at `c80f2586` | evidence |
|---|---|---|
| B3 "a correction note repairs a mismatch" | **closed** | `supersession` path deleted; `score` repairs only via `repair_command` re-derivation (`:994-1015`); selftest arms `note_alone` 1, `note+re-derivation` 0 (R-10) |
| B5 "relaxation admits arbitrary in-place edits" | **mostly closed** | `appended_text` requires the FREEZE blob as a prefix (`:461-468`); `append_text` byte-equality, `append` line identity, `preserve` digests (`:471-507`); unit probe: in-place edit → `not_append_only` (R-12); **residual holes O4, O5** |
| B7 "no pre-freeze mode, CTL-C2-0 unevaluable" | **partially closed** | `--pre-freeze` exists, `claim_score: false`, `entries_evaluated`/`mismatches` in the receipt (`:833-940`); **residual hole O6** |
| H1 "empty rubric is met" | **closed** | `entries_evaluated == 0` → exit 2 `no_evaluable_entries` (`:1039-1045`); e2e probe exit 2 (R-19) |
| H4 "pinned-rev checks have no git objects" | **closed by design** | checks get `HYAKU_REPO` (a `git clone --shared`) and `HYAKU_REV`, so a pinned-rev derivation is possible (`:690-700`) |
| B1 rev-mixing, B2 `asserted` provenance, B4 free-form argv, B6 sibling attribution, H2, H3, H5, H6 | **open** | O1, O2, O3, H1–H7 below |

The seat's 12-arm selftest is green on an independent run (receipt R-10, stdout sha
`94156c8ac1d77d30`), so the paths exercised below are the delivered ones.

---

# Open findings

## O1 (blocking) — No pin binding: a **true** historical statement is scored as a mismatch, and the sanctioned repair rewrites it

The rubric schema has no `pin` field. A check is arbitrary argv evaluated against the REV export;
nothing requires it to read a pin out of the line it measures, and nothing forbids scoring a
pinned statement at REV.

**Exploit (measured, and already in the round's own reasoning).** `SCORECARD.md:23` says
"133/133 knowledge files mapped after the round-41 landing … command A at `e1c83313`". Measured:
133/133 **at `e1c83313`** (R-03) and 137/137 at REV (R-01). A rubric entry that runs command A at
REV reports a mismatch; the repair is an appended line carrying 137/137, which now contradicts the
`at e1c83313` qualifier inside the same cell — and the counter passes it. The seat's own dev-arm
report takes exactly this reading: "*`dev-scorecard-map-count` — `SCORECARD.md`'s coverage headline
claims 133 … `corpus/knowledge/*.md` holds 137 at the base. A real candidate for the frozen rubric
(category b), and a candidate C2 repair*" (`R44C2Counter.md`, "Lane dev-arm findings"). That
statement is true at its pin; treating it as a defect is the failure mode, not a probe artefact.
Same for depth: `:24` "20/20 … at `e1c83313`" → 20/20 at the pin, 21/21 at REV.

**Does the counter catch it?** No. It compares one observation to one transcribed `asserted` at
one revision.

**Smallest fix.** Entry field `pin` (`null` or a commit). The counter (i) extracts the qualifier
from the entry's cited line (`at\s+\`([0-9a-f]{7,40})\``) and refuses a disagreement (exit 2
`pin_disagrees_with_line`); (ii) for a pinned entry, materialises that rev (the counter already has
`HYAKU_REPO`) and requires the check to derive against it — a check that reads the REV export for a
pinned entry is exit 2; (iii) a REV-state entry is admissible only when the line carries no
qualifier; (iv) the appended block may not carry a value for a pinned entry (pinned history is
immutable; a supersession is a *new* dated statement with its own derivation).

## O2 (blocking) — `asserted` has no provenance, and a self-referential check scores the round met

`asserted` is a free transcription (schema `R44C2Rubric`: `{id, file, line_at_base, asserted, …}`);
the counter never relates it to the base blob. Combined with O3, the predicate is satisfiable
without doing the calibration work.

**Exploit A (measured end-to-end).** One entry, `command` = a Python one-liner that does
`'133/133' in Path('SCORECARD.md').read_text()`, `asserted = true`. Result: `entries_evaluated 1`,
`mismatches []`, `met_target true`, **exit 0** (receipt R-18). The check reads the file it asserts
about, so a corrupt-but-self-consistent file passes; the current count is 137.
**Exploit B (green without work).** Transcribe `asserted = "137/137"` for `SCORECARD.md:23`: the
REV observation matches, no mismatch, the frozen line still says 133/133.
**Exploit C (manufactured work).** Transcribe `asserted = "136/136"`: the base mismatch is
guaranteed, CTL-C2-0 is red by construction, and one bound append repairs it.

**Does the counter catch it?** No — there is no `line_at_base`, `line_sha256` or substring check
anywhere in `parse_rubric`/`score`.

**Smallest fix.** (i) Parse-time: `asserted` must be a byte substring of `blob(BASE, file)` at
`line_at_base`, and `line_sha256` must equal sha256 of that line; otherwise exit 2
(`asserted_not_in_base_line`). (ii) The census's `observed_at_base` is re-derived by the counter at
BASE and must equal the committed census value (drift is exit 2, not a mismatch). (iii) Rubric
contract: every entry declares `derivation` = the independent source of truth (e.g. "count of
`git ls-tree corpus/knowledge`" for a claim about counts) and the counter requires a per-entry
mutation control: in a scratch tree, mutate the *reality* side and require the check to flip
(`derivation_fails_mutation`). A check that cannot be made to fail is exit 2, not a pass. This is
the only defence against the always-true class.

## O3 (blocking) — Free-form `command`/`repair_command`: trivially green, and committed data is executed

`check.command` is arbitrary argv (`parse_rubric :370-401`; `run_entry :683-760`), executed with
`env = dict(os.environ)` (`:966-970`) and `cwd` = exported tree. No script pin, no allow-list, no
env scrub.

**Exploit 1 (always-true).** `{"command": ["sh","-c","echo 137/137"], "asserted": "137/137"}` —
schema-legal, green on every revision, no repo read (the O2 demo is the same class with a file
read).
**Exploit 2 (execution from frozen data).** A pre-freeze-corrupted rubric can run `git checkout`,
write inside the clone, or read absolute paths; `-I -B` on the counter does not constrain the
child. `repair_command` is a second such argv, so the "independent re-derivation" of B3 can itself
be a command that prints the asserted value.
**Exploit 3 (environment leakage).** HOME, proxy/credential variables and `HYAKU_*` are visible;
a check can be satisfied by bytes outside the scored tree. `HYAKU_REPO` also lets any check read
any revision (`git -C $HYAKU_REPO show <rev>:<path>`), so the *export* surface is not a
containment boundary — a trade-off the design should state, since that handle is what makes O1's
pinned checks possible.

**Does the counter catch it?** No.

**Smallest fix.** `command` becomes `{script: "tools/round-44/checks/<name>.py", script_sha256,
args:[…]}` with `script_sha256` frozen; execute `[sys.executable,"-I","-B",script,*args]`,
`shell=False`, a fixed minimal env (`PATH`, `HYAKU_*`, `TMPDIR` under `--work`; no HOME, no
proxy vars), args confined to the tree; require `repair_command` to satisfy the same constraint.
Document `HYAKU_REPO` as read-any-rev (not containment).

## O4 (blocking) — A file **added** under `frozen_dirs` is not `frozen_path_changed`

`freeze_integrity` `:520-523`: when the path has no blob at FREEZE it records
`{'state': 'added_under_frozen_dir'}` and `continue`s — it is not appended to `changed`.

**Exploit (measured, unit probe R-14).** Freeze a repo containing `tools/round-44/a.txt`; add
`tools/round-44/evil.py` and commit. `freeze_integrity(..., frozen_dirs=('tools/round-44',))`
returns `frozen_path_changed: []` with only the note above. The claim freezes `tools/round-44/*`
("all round-44 tools"), so a post-freeze tool/check/data file is an admitted freeze violation that
the receipt reports as clean. The seat's selftest arm tests a *changed* file, not an added one.

**Smallest fix.** In that branch, `changed.append(path)` as well (state `added_under_frozen_dir`);
add a selftest arm for the added case. (Deliberate over-strictness elsewhere — touched-and-restored
is `changed` — is correct and should stay.)

## O5 (blocking) — `expected_edit` marker-only and empty-`append` bind arbitrary appended content

`verify_expected_edit` `:471-507`: `append_text` is byte-exact and `append` is line-exact, but if
only `marker` is given the function returns `bound_edit` after checking that the marker occurs
somewhere in the appended block; `{"append": []}` also returns `bound_edit`.

**Exploit (measured, unit probes R-11, R-13).**
- `{"marker": "Round-44 C2 correction"}` on `SCORECARD.md` + append
  `"Round-44 C2 correction: fabricated"` and `"### R43-C2 met"` → `bound_edit`, arbitrary content
  admitted. Variant B of my v1 demo, now at the appended-block level rather than in place.
- `{"append": []}` → `bound_edit` while binding nothing.
In-place edits and deletions remain blocked (prefix), so this is content-level fraud (a fabricated
verdict appended to a frozen file), not history rewriting.

**Smallest fix.** At parse time, any declared `expected_edit` must carry `append_text` (non-empty
string) or a non-empty `append` list; `marker`/`preserve` are *additional* conditions only. An edit
that binds nothing (`append: []`, marker-only) is exit 2 `expected_edit_binds_nothing`. Also report
the sha256 of the whole appended block in the receipt so the reviewer sees exactly what landed.

## O6 (blocking) — `--pre-freeze` cannot score the frozen rubric: `rubric_freeze_mismatch`

`score :876-883` enforces `rubric['freeze'] == freeze` unconditionally, and in pre-freeze mode
`freeze` is set to the measured rev (`:838-841`).

**Exploit / failure (measured, e2e R-15).** A rubric that names the round-44 freeze (the field the
claim needs) scored at BASE with `--pre-freeze` exits 2:
`rubric_freeze_mismatch: 3b0fcaa9… != c29360e3…`. So CTL-C2-0 ("the frozen rubric scored at the
BASE") is still unevaluable as specified; the only workaround is a rubric copy whose `freeze`
field is rewritten — i.e. the control scores a different rubric than the frozen one, which is
exactly the "loosening" the kill rule is meant to prevent. The seat's `pre-freeze-census` receipt
uses such a copy.

**Smallest fix.** In `--pre-freeze`, do not enforce declared-freeze equality. Record
`declared_freeze` and `declared_freeze_matches: false` in the receipt and continue; `claim_score`
already distinguishes a census from a score. Then CTL-C2-0 can score the frozen bytes.

## O7 (blocking) — `--rubric` mints a `claim_score: true` receipt without the rubric-freeze check

`score :846-856, 890-900`: with `--rubric FILE`, `rubric_source = 'file'` and the
`if rubric_source == 'freeze'` byte comparison is skipped; `claim_score` is `not pre_freeze`, so a
claim score can be issued from an arbitrary (e.g. edited) rubric file.

**Exploit.** Edit the installed rubric's asserted values, score with `--rubric /tmp/edited.json
--rev <REV> --freeze <FREEZE>` → exit 0, `claim_score: true`, `rubric_sha256` of the edited file,
and no `frozen_path_changed`. The receipt records `rubric_source: "file"`, so it is auditable —
but nothing refuses it, and the L1 must know to reject it (my O2 demo receipt shows
`claim_score: true` with `rubric_source: "file"`, R-18).

**Smallest fix.** A claim score (`not pre_freeze`) requires `rubric_source == 'freeze'`, else exit
2 `claim_score_requires_frozen_rubric`; or split the switch: `--dev-arm` implies
`claim_score: false`. `--pre-freeze` may keep `--rubric`.

---

# Hardening

**H1 — inventory binding (rubric seat).** The counter now refuses an empty rubric, but not a
degenerate one. Freeze `inventory_sha256` over the census's sorted entry ids; the rubric must
contain exactly those ids; report `entries_count`, `superseded_count` and a per-category count. A
`superseded` entry needs a resolvable at-BASE reference or it is exit 2.

**H2 — pointer existence is not evidence.** 12/12 sampled capability pointers resolve at base, so
`test -e` is green now and green for a stub. Freeze the pointer's blob hash at BASE and report it;
a pointer created at REV is `fabricated_pointer` (exit 1), not a repair.

**H3 — self-reference discriminator.** The rule is "a second source of truth", not "reads a
file". `SCORECARD` "137/137" must be checked by counting `git ls-tree corpus/knowledge` and command
A's mapped-stem set — never by grepping SCORECARD/README. For SHONEN's "`PROVINCE.md:97-125`
byte-identical at `52b0eb29`" there is no second copy: freeze a reference blob hash and name the
other side, or drop the entry with a reason.

**H4 — category (e) receipt trust.** A cited receipt is committed JSON; editing `exit_code` 1→0
flips "not met" to agreement. Freeze every cited receipt blob and its counter blob; require the
receipt's `counter_sha256` to equal the frozen counter blob's hash.

**H5 — category (d) must be token-bound.** Keyword overlap is a green generator. The planned
(round 43) row promises a R42-C2 refreeze and a wave-2 attack; round 44 worked SquashFS v1/v2
(`SCORECARD.md:3498, :3507`). Score only `R{N+1}-C{k}` or an existing path/stem as a membership
test; prose plans are dropped with a reason.

**H6 — sibling attribution.** `mismatches` is a flat list: a partial C1 landing (file without its
index row → 138 files / 137 mapped) makes C2 unreachable, and the tempting repair is an append on
a surface C2 does not own. Record `mismatch_origin` (first commit introducing the state, or
`sibling:<claim>`) and report `mismatches_self` vs `mismatches_sibling`; the claim target is
`mismatches_self == 0`.

**H7 — receipt completeness.** Add `rubric_sha256_at_freeze`, `appended_block_sha256` per bound
file, `mismatches_self/sibling`, and `pin` per entry to the receipt. `counter_sha256_at_freeze` is
already present but is `null` when the counter is installed after the freeze (the seat discloses
this; installing counter+rubric in the freeze commit is the only admissible order).

---

# Freeze checklist (apply to the landed rubric + installed counter)

1. Every `asserted` is a byte substring of the cited base line; `line_sha256` matches (O2).
2. Every pinned statement carries `pin` extracted from its own line; pinned checks derive at the
   pin, not at REV (O1).
3. `command`/`repair_command` are frozen scripts with `script_sha256`, fixed env, tree-contained
   args; every entry has a mutation control that makes it fail (O3, H1).
4. `frozen_dirs` added-file → `frozen_path_changed` (O4) and a selftest arm for it.
5. `expected_edit` uses `append_text` (or non-empty `append`); marker-only and empty binds are
   exit 2 (O5).
6. `--pre-freeze` skips the declared-freeze equality so CTL-C2-0 scores the frozen rubric (O6).
7. A claim score is refused unless `rubric_source == 'freeze'` (O7).
8. Counter + rubric committed **in** the freeze commit; `counter_sha256_at_freeze` and
   `rubric_sha256_at_freeze` non-null in every claim score.

---

# Receipts

Commands run by seat `R44C2Sentinel`; `sha256_stdout` is the first 16 hex of the stdout sha256;
`exit` is semantic (0 clean, 1 not met, 2 could-not-evaluate). Counter sha
`c80f25866efb044a…` where a probe ran the artifact.

| id | command | exit | sha256_stdout | wall |
|---|---|---|---|---|
| R-01 | command A `--rev c29360e3` | 0 | `ae2fa5a4f6dd103b` | 0.10s |
| R-02 | command A `--rev 4d62ee5a` | 0 | `963a187dbd28e2a4` | 0.10s |
| R-03 | command A `--rev e1c83313` | 0 | `d70a5800cf6407f4` | 0.10s |
| R-04 | command A `--rev 8de80f1d` | 0 | `ae2fa5a4f6dd103b` | 0.10s |
| R-05 | 12 capability pointers, `git cat-file -e c29360e3:<p>` | 0 | `f4d3f1452008dd4f` | 0.02s |
| R-06 | v1 relaxation demo (suffix containment vs exact blob) | 0 | `6e6f326f0b3b97d6` | 0.02s |
| R-07 | `merge-base --is-ancestor 6b9e64fe f3f8db38` (round-43 base→freeze) | 0 | `01ba4719c80b6fe9` | 0.00s |
| R-08 | `merge-base --is-ancestor f3f8db38 6b9e64fe` (freeze→base) | 1 | `01ba4719c80b6fe9` | 0.00s |
| R-09 | lane HEAD at first review | 0 | `d72cc836adbe6e43` | 0.00s |
| R-10 | `c2-counter.py --selftest` (independent) | 0 | `94156c8ac1d77d30` | 0.39s |
| R-11 | unit: marker-only `expected_edit` + fabricated append | 0 | `0d65abce16e32b0f` | 0.03s |
| R-12 | unit: in-place edit under `append` binding | 0 | `e84ef0528cb2e850` (`not_append_only`) | 0.03s |
| R-13 | unit: `{"append": []}` binding | 0 | `38e4d1159a4457fd` | 0.03s |
| R-14 | unit: **added** file under `frozen_dirs` | 0 | `2cc33efe7fdebf09` | 0.04s |
| R-15 | e2e: `--pre-freeze` with rubric declaring the canonical freeze | 2 | `74773bada9747eb6` | 0.04s |
| R-18 | e2e: self-referential entry (grep SCORECARD for `133/133`) | 0 | `3be7eb0377a7564a` | 0.35s |
| R-19 | e2e: empty rubric | 2 | `46a29fd3dabd5ddd` | 0.33s |

Scratch: `/fast/scratch/hyaku/kaidoku-r44/probe-R44C2Sentinel/` (`cmdA.py`, `relax.py`,
`dirprobe2/`, `pre-rubric.json`, `selfref-rubric.json`, `empty-rubric.json`, `r-*.json`,
`receipts.tsv`).

# Residual risk

- The artifact is under active edit. Everything here was re-probed at sha `c80f2586…`; if the seat
  pushes another revision before the freeze, re-run R-11, R-13, R-14, R-15, R-18, R-19 against the
  installed sha.
- Findings are about the **predicate as implemented**, not about the census's real mismatch count.
  Whether the honest stop fires is decided by the frozen rubric, which is another seat's artifact.
- Probes used a fabricated rubric and the lane's committed bytes only. No REA, no network, no
  fixture driver, no write to `tools/round-44/` or any fleet-root tracked file.
