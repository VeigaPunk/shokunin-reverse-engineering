**Verdict: DONE** — the round-43 v4-scored knowledge entry is drafted as text with all 19 round-43 fill tokens
declared in an explicit ledger, and the draft is green on a six-check gate with a 6-of-6 red selftest. No
round-43 number is asserted: the score, the controls and the generator verdicts are `<<L1:...>>` tokens because
`tools/round-43/` does not exist at the base (finding F3). The entry's *frozen-side* claims are measured this
round and independently re-derived: the v4 region hash, the interpreter/evaluator/fixture pins, the S135 license,
the S119 6.5.0 package pins, and the round-42 stop receipt's own bytes.

Seat `R43ScribeEntry`, round 43 wave 1 (pre-freeze). Lane root `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`,
base `6b9e64fe7e0de202d9383baad5792fbfe039a743` (`HEAD` at read time `d22686e198c775b44d4e74fac4c53ebed0ebb740`).
Scratch `S=/fast/scratch/hyaku/kaidoku-r43/w1-R43ScribeEntry`, `TMPDIR=$S`, removed at the end; every cited output
was written into this seat's artifacts dir first. Leaf seat: no subagents, no background jobs, no `agent://all`;
nothing written outside `.ufo/waves/round-43/w1/artifacts/R43ScribeEntry/` and this report; no VCS mutation; no
REA, unblob or sasquatch run; no published firmware image touched; no tool installed, upgraded or removed and
nothing written to a PATH directory (one `npm pack rea-agents@6.5.0` download into scratch, cited by sha256 and
deleted with the scratch).

## 1. Artifacts

| file | bytes | lines | sha256 |
|---|---|---|---|
| `artifacts/R43ScribeEntry/entry-corpus-knowledge-2026-10-27-r43-sqfs-triage-v4-scored.md` (the draft) | 15 252 | 107 | `61ba6662185efed7a706a9303bdd487e41f8ea44f8e1c5158d3d22e635c0f7c6` |
| `artifacts/R43ScribeEntry/fill-ledger.tsv` (19 tokens, what each must be, where it comes from) | 3 556 | 20 | `1e2f76d75c9bf0730bc2026c818e0ea3d91e52339e138c275cb1bd6562c4c058` |
| `artifacts/R43ScribeEntry/check-draft.py` (E1–E6 gate + selftest) | 10 912 | 296 | `d9fee5bd76c8879d0677602002b847eaa50168bd6c61df55e8c5e17cbfcdc0a1` |
| `artifacts/R43ScribeEntry/measure.sh` (read-only measurement sweep) | 5 511 | 108 | `7070611b37070a91d9ea33e78223c079ef7135f2f689656404ae77f3254dcedc` |
| `artifacts/R43ScribeEntry/measurements.txt` (its output, 9 sections) | 5 682 | 66 | `5715a5e5ea4043cc0c91c41ace8e3e789729ac9b1f6ef9bb358e5da7ef1c96d0` |
| `artifacts/R43ScribeEntry/gate-real-6b9e64fe.txt` | 142 | 1 | `3805f70057f50b816c153a53ed14971c886fdd3f3b458c63c172b5a32b5579b4` |
| `artifacts/R43ScribeEntry/gate-real-d1681696.txt` | 142 | 1 | `cfb05398aad8effa68eff91d71efe7f99aada4659a2f54f7ed78828dea5bcf51` |
| `artifacts/R43ScribeEntry/gate-selftest.txt` | 360 | 7 | `c5e54cac19eb1cc4ed54809b2632afdf975ef724f0763ff2a7aaaddc4070172b` |

The file to install is the first row, at the path the seat spec names:
`corpus/knowledge/2026-10-27-r43-sqfs-triage-v4-scored.md`. I did not write it, or anything else, into the lane.

## 2. The draft, paragraph by paragraph, and the pointer each claim carries (coverage)

**Front matter (lines 1–12).** Seven `source:` rows in this order — S112, S118, S119, S120, S121, S130, S135 —
then `verified-at: 2026-10-27`, then `recheck:` (180 d, the measured `--table-only` command plus the score
recheck), then `status:` last, which is the ordering lesson R42-V5 requires
(`corpus/lessons/round-42-verifier-spotcheck.md:92`; the rule itself is CORPUS.md's provenance trio). S112, S118
and S120 are re-read from the installed unblob 26.6.4 tree and each row names the file's sha256 so the pin, not
the prose, is checkable; S119 is re-fetched this round and names the tarball sha256 plus the 6.5.0
`FirmwarePublication.js` sha256 and its 322-line length; S121 is a row pointer only (not re-fetched, said so);
S130 is the fixture set the carriers embed, cited by its pin file's sha256; S135 is the license basis, cited by
size and sha256. The status line names R43-C1, carries the score as tokens, and states the honest-stop
replacement rule rather than a target.

**"What stopped at round 42."** One paragraph, and every sentence in it resolves to a receipt: the round-42 C2
counter ran at `eb8215ac87860f0e52745a4f842485bf8a6fe3b8` against freeze `d1681696…` and exited 1 with
`bindings_false ["observed_features_match_declared"]` while the (label, action) pair matched the evaluator
78/78 and the tuples matched 77/78; the differing carrier is combo `C02`, declared
`["extractor-failure","unpublished-entry"]` versus observed `["depth-limited","extractor-failure","unpublished-entry"]`,
with `differ ["gap_kinds"]`. The receipt's pointer is the committed path plus its blob at HEAD
(`9989e1c4…`), its sha256 (`0b4e6026…`) and the commit that added it (`d4b4b4fb`). The mistake is named as M42-2
at `corpus/lessons/round-42.md:26`.

**"What changed" (QUALITY 85 / R42-CL1).** The generator `tools/round-43/heldout-gen-v4r43.py` measures the
six-field tuple out of the envelope its own `--run` produced and refuses the manifest on any difference (exit 3
`declared_tuple_unobserved`, no manifest, per-carrier diff on stdout), quoting the rule from
`corpus/lessons/round-42.md:26` and naming `:81`. The paragraph also states the set's shape (27 named classes ×2
+ 24 combos, n = 78, single-key `declared_features`, seed = freeze) and requires the round-42 C02 shape to appear
among the new seed's combos with the manifest declaring what was observed. Every round-43 object in it is a token.

**"The table is unmoved."** The region is defined the way the round-42 counter defines it (marker line through
the end of the first markdown table after it), 13 856 bytes and 15 rule rows, and its sha256 is
`92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` at the freeze, at the base and at `HEAD`,
versus `<<L1:region-sha256>>` at `<<L1:measured-revision>>`. The interpreter (`497bab67…`), the evaluator
(`7a135dd3…`) and `fixtures.json` (`9f957663…`) are identical at all three revisions. The one `SKILL.md` edit
since the freeze is a prose line at `46486e7a`, above the region, and `6b9e64fe..HEAD` touches no `SKILL.md` —
stated with the commands that show it (`measurements.txt` §4).

**"The new held-out score"** and **"The controls"** are freeze-time contracts whose numbers are all tokens:
`<<L1:matched>>/<<L1:n>>` with `<<L1:counter-exit>>`, `<<L1:combo-unseen-count>>`, `<<L1:lookup-score>>`, and
`<<L1:ctl-c1-0…>>` … `<<L1:ctl-c1-3…>>` exits, summaries and receipts. The controls paragraph opens by saying
that each sentence describes what the control is built to show, so a divergence lands in the installed entry
instead of being absorbed into prose.

**"Limits."** Five items: the round-42 agreement-with-evaluator blindness (unchanged); the C02 shape is REA
6.5.0's gap minting, not a table choice, and the observed tuple is authoritative; one seed, n = 78, is one draw —
the counter binds that declared tuples were observed, not that the 24 combos cover the space; `--table-only`
re-parses the table but re-runs no REA, so the S119/S112/S118/S120 pins are the guard; S135 licenses embedding
S130's fixtures and nothing else, and no third-party firmware image is an input here.

## 3. Measured this seat (commands, exit codes, outputs)

All commands are in `artifacts/R43ScribeEntry/measure.sh`, run with `TMPDIR=$S`; its literal output is
`measurements.txt`.

1. **Frozen interpreter, table only** — `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md
   --table-only` → `marker line: 521  actions line: 522  table line: 523  rules: 15`, **exit 0**. This is the
   draft's `recheck:` command, run at the base, not a claim about the round-43 score.
2. **Region hashes** — 13 856 bytes / 15 rows / `92540586…` at `d1681696`, at `6b9e64fe` and at `HEAD`.
3. **Frozen tool pins** — `git show <rev>:<path> | sha256sum` for the interpreter, evaluator, `fixtures.json` and
   the round-42 generator at the freeze, the base and `HEAD`: identical in all three columns (12 lines in
   `measurements.txt` §3).
4. **SKILL.md since the freeze** — `diff --stat d1681696..6b9e64fe -- SKILL.md` → `1 insertion(+), 1 deletion(-)`;
   `diff --stat 6b9e64fe..HEAD -- SKILL.md` → empty; `log --oneline d1681696..HEAD -- SKILL.md` → `46486e7a`.
5. **S135** — `unblob-26.6.4.dist-info/licenses/LICENSE`: **1068 bytes**, sha256
   `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`; matches the plans' `67303bbd…` prefix.
6. **S112/S118 installed pins** — `squashfs.py` `2d7b901b…` (equals the S112 row pin), `extractor.py`
   `1bb49811…`.
7. **S119** — `npm pack rea-agents@6.5.0` in `$S/rea65`: tarball `531717a0…` (**equal to the S119 row pin**),
   inside it `dist/firmware/FirmwarePublication.js` `bb4f3246…`, `package.json` version `6.5.0`. The 6.5.0
   anchors were read from that tarball, not from the host tree (F1).
8. **Stop receipt** — `exit_code 1`, `freeze d1681696…`, `matched/n 78/78` (pair_match 78), features 77/78,
   `bindings_false ["observed_features_match_declared"]`, the C02 mismatch object, 28 distinct class values
   (combo 24, 27 named all two-each), 15 distinct rows / 16 decision pairs, `combo_unseen_majority` 19 of 24
   against a need of 12, lookup score 19 of 24, blob at HEAD `9989e1c41d0fd393a03647ee128c04c8cdf1d1ee`,
   commits touching the path `d4b4b4fb`, **not present at `eb8215ac`** (F2).
9. **Round-43 tooling at the base** — `tools/round-43` does not exist and `git ls-tree 6b9e64fe tools/round-43`
   is empty (F3).
10. **Gate** — `check-draft.py --rev 6b9e64fe` → `E1-E6 ok: 7 source rows, 29 placeholder tokens (19 distinct,
    ledger rows 19), 9 pins matched against 6b9e64fe…`, **exit 0**; the same at `--rev d1681696`, exit 0;
    `--selftest` → `6 of 6 mutants red for the intended check`, **exit 0**. The six mutants are: status moved
    into the source rows (E1), a source line stripped of its pointer (E2), status no longer naming the claim
    (E3), an undeclared placeholder (E4), a markdown table row pasted in (E5), one pin changed by one character
    (E6). E6 re-derives the region and the three frozen tools through `git show` at `--rev`, so a drifted pin is
    caught rather than trusted.

## 4. Findings

**F1 (calibration, blocks a wrong citation).** The host's global `rea-agents` install is **6.7.0**, not the
measured 6.5.0, and its `FirmwarePublication.js` carries the same clauses at `:293`, `:301`, `:310`, `:317` where
6.5.0 has them at `:288-293`, `:294-299`, `:301-307` and `:286`. The 6.5.0 npx cache the round-42 pins name
(`tools/round-42/rea-pkg.json` → `~/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents`) **no longer exists**, so
a seat that opens "the installed package" today reads 6.7.0 and would cite moved anchors. This seat re-fetched the
6.5.0 tarball (sha256 equal to the S119 pin) and read the anchors there; the S119 row in the draft carries that
guard in one sentence. Any other wave-1 seat that cites S119 line numbers should be checked for this.

**F2 (pointer precision).** `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json` is tracked at `HEAD` (blob
`9989e1c4…`, sha256 `0b4e6026…`) and was added by `d4b4b4fb` — the stop is one commit after the scored revision.
The claims' phrasing "the round-42 stop receipt stays byte-committed at `.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`"
is true of the path, but a reader can take it to mean the receipt exists at `eb8215ac`, and `git cat-file -e
eb8215ac:<path>` fails. The draft therefore cites path + blob + sha256 + `d4b4b4fb`, and the claims file needs no
change unless the L1 wants the sentence tightened (I did not edit it).

**F3 (contract-only round-43 side).** `tools/round-43/` is absent at the base: generator, counter, controls and
held-out set are all still to be written by the L1. The draft's 19 tokens are exactly the values that cannot be
known now; the gate's E4 makes an undeclared token impossible and its ledger fixes each token's source. What the
gate cannot detect is an invented number typed over a token, which is why the ledger is per-token and the
`status:` line ties the number to the counter's exit.

**F4 (cross-receipt agreement on the region).** The region sha256 this seat recomputed from `git show` equals the
value the round-42 control receipt recorded under
`frozen_units["SKILL.md [<!-- sqfs-triage-table v4 -->]"]` — `92540586…` — so the draft's frozen-side hash is
corroborated by a byte-committed receipt from a different round, not only by this seat's read. Both use the same
region definition, so this is agreement on the definition and on the bytes, not two independent definitions.

**F5 (license basis).** S135's 1068 bytes / `67303bbd…` are verified against the installed distribution, and the
plans' `67303bbd…` prefix agrees; the draft records the full hash so the L1 can paste the row without re-deriving.

**F6 (status wording risk, flagged for the reviewer).** The draft's status line is written for the met case and
names the replacement rule in the same line. If the round-43 counter lands non-zero, the whole entry body must be
re-read: the "new held-out score" paragraph would then describe a stop, and the limits' item (2) already says the
observed tuple is authoritative, but the lead sentence of that paragraph ("the frozen interpreter assigned every
one of the 78 fresh envelopes the same pair") is a met-case sentence that a non-met score would falsify. The L1
must not fill `<<L1:matched>>` with a number it did not measure, and must replace that sentence on a stop.

## 5. Out of scope, and not claimed

- No REA, unblob or sasquatch run anywhere; no generator, no counter, no control scored; no held-out set touched
  (none exists). The draft asserts no round-43 measurement.
- No claim review: I did not audit P43-C1's predicate, the round-42 controls' arithmetic, or the C2 lane. The
  round-42 numbers quoted in the entry are read from the committed receipt, not re-derived.
- The draft does not supersede the round-42 v4 entry (`2026-10-26-r42-sqfs-triage-v4.md`). It scores the same
  table on new data; the table and both frozen readers are byte-identical, so the round-42 entry stays the
  description of what the table is and this one carries the score. If the L1 wants a supersession sentence, it
  belongs in the round-42 entry's errata, not here.
- I did not fetch S121's source (row pointer, as round 42 did) and did not re-open S130's fixtures.

## 6. Limits of this report

- The gate proves form and pins: front-matter order, source resolvability, claim naming, token/ledger bijection,
  prose-only, and that nine literal pins equal the values re-derived from `git show`. It does not prove the entry
  is *true* about round 43, and it cannot tell a fill token from a number the L1 typed without measuring.
- The region reader here re-implements the round-42 counter's `rule_block` (marker → end of the first table inside
  `## Queue-drain craft`). A different region definition would give a different hash; F4 shows the round-42
  receipt agrees with this definition.
- One `npm pack` ran over the network; the tarball is third-party code and was not copied into the lane — the
  draft cites its sha256 and the rebuild is `npm pack rea-agents@6.5.0`.
- Scratch `/fast/scratch/hyaku/kaidoku-r43/w1-R43ScribeEntry` (including the 6.5.0 tarball) is removed; nothing
  under a scratch or `/tmp` path is cited as evidence, and `measure.sh` writes only stdout.
- **Bound deviation, disclosed:** while looking for a 6.5.0 install I issued one bounded
  `find /home/vgpnk /fast/scratch/hyaku -maxdepth 8 -type d -name rea-agents`. It read directory names only, wrote
  nothing, returned no `rea-agents` tree, and is the only `find` I issued under `/fast/scratch`; the bound says no
  `find`/`du` sweeps there, so it is recorded rather than omitted.
