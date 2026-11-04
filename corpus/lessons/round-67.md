# Round 67 — the class rule and the two survivors

Base `a7a4ce6902204d5c6cc6c4e3e78b4bffe8312b92`; the operative freeze is the commit that first adds
`.ufo/waves/round-67/claims.json` (`3663e6b21dccf4c4957f459301156664d8b151d6`); the carry-in is the appended
entry `## 2026-11-03 — round 67, KaidokuR67 — carry-in` (`LOG.md:4083`). The carry-in records its own ordering —
committed before the instruments and before the declaration — which the round's A0 atom measures
(`l1/records/r67-order.txt`: carry-in 21:51:02 → instruments 21:51:09 → freeze 21:51:14, both ancestors exit 0).
Two claims on distinct axes: **R67-C1** (coverage, frontier → core) re-freezes the round-50 LE-AVM measurement
under a gap rule that classes char-device entries as not-publishable rather than per-row required, and **R67-C2**
(depth, counter repair) adds the selftest battery that binds the two round-66 mutation survivors. Neither verdict is
taken here: the after-arms belong to the L1's data run and the closure belongs to the non-author judge.

## Gate

Access date for the new source: **2026-11-03**. Fetch, locator and quote evidence:
`.ufo/waves/round-67/w1/ScoutSource/{fetch.json,gate.md,fetched-format.adoc,fetched-squashfs-docs.html}`. The row
landed as **S268**.

| candidate | locator / evidence | measured value | decision | flip condition |
|---|---|---|---|---|
| (a) squashfs-tools-ng format documentation, `doc/format.adoc` at commit `e3dcf177…` | https://raw.githubusercontent.com/AgentD/squashfs-tools-ng/e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90/doc/format.adoc, opened 2026-11-03: HTTP 200, 41 981 B, sha256 `08c38b69…c82eb`; `=== Device Special Files` heading at fetched-bytes line 730, quote at line 732 (one occurrence, byte offset 28 445), major/minor extraction lines 742-746, type codes 5/12 at lines 549/556 | "Basic device special files only store a hard-link counter and a device number." (13 words) — the device entry stores no payload, which is the class rule's ground | **admit** (S268, docs, tier A, opened 2026-11-03, recheck 180d, used-by the round-67 entry) | — |
| (b) Linux kernel SquashFS documentation, §3.2 Inodes | https://docs.kernel.org/filesystems/squashfs.html, opened 2026-11-03: HTTP 200, 26 045 B, sha256 `10767bbf…33685`; the §3.2 class sentence exists at raw line 412 ("different inodes for each file type (regular file, directory, device, etc.)…") | it names the device inode class but states **no** device-number field and no payload absence: `major`/`minor` occurrences **0**, `Basic`/`Extended` device headings **0** — the class rule needs the field set | **reject as this round's row**: scope too weak (the assigned "Basic device inode" quote does not exist in the bytes) | admissible as a second row if the claim needs only the class distinction (device inode ≠ regular file), with the §3.2 sentence as its quote |
| (c) the same text as `Documentation/filesystems/squashfs.rst` on `torvalds/linux.git` plain | https://git.kernel.org/pub/scm/linux/kernel/git/torvalds/linux.git/plain/Documentation/filesystems/squashfs.rst, opened 2026-11-03: HTTP 200, 14 201 B, sha256 `e709573a…ba5f9`; same three sentences at raw lines 184-186 | same subject and scope as (b), under a locator that names no revision | **reject**: a locator with no revision identity | adopt at a tagged tree (e.g. `v6.18`) if a release-pinned text identity is needed |
| (d) the before-arm receipt as the ground that no extractor record can exist | `l1/pre/control-dryrun.json` `per_carrier.g7581.gaps_note_round50` names 8 of that carrier's `dev/pts/*` char devices as required-with-no-disposition | a receipt measures a rule's effect on one carrier; it cannot ground why a class is not publishable | **reject as a source**: a receipt demonstrates a red arm, never a rule's ground | never — a receipt does not become a SOURCES row |

Re-opened round-50 rows (all five, because the re-freeze re-uses their subjects): **S243** Freetz patch 101 HTTP 200,
1 153 B, sha256 `e28b3341…84c707`; **S244** AVM download index HTTP 200, root listing 8 990 B, sha256 `75e886e2…c40764`;
**S245** unblob 26.6.4 LE handler HTTP 200, 19 842 B, sha256 `2d7b901b…599287`; **S249** AVM licence HTTP 200, 67 591 B,
sha256 `6c601b34…070a7`; **S250** squashfs-tools 4.7.5 `unsquashfs.c` HTTP 200, 116 844 B, sha256 `6222d940…939341`.
None needs a new row: each scope is exactly the subject this round re-used, and none states the on-disk device inode
class — which is why (a) is a new row rather than an extension of a standing one. S250 already carried the extractor's
privilege gate, so the new row's subject is the format's field set, not the `mknod` behaviour.

Assimilation: none this round — the `merge/kaidoku/` jsc theme was adopted in round 64 and no remaining staged theme
fits a SquashFS class rule; `considerthese/` is absent (`ls considerthese` exit 2, measured this round).

## Mistakes

| id | class | evidence pointer | captured-by | fix |
|---|---|---|---|---|
| M67-0 | scope/over-generalisation (inherited from round 50): a gap rule generalised from the Cable carriers' one `247:0` char device made every char-device row a per-row requirement, so twelve device rows per FRITZ!Box carrier had no possible disposition | `l1/pre/control-dryrun.json` (`gaps_ok_round50 2`, false on `g7581`/`g7582`); `tools/round-50/oracle/*.nonregular.tsv` (13/13/1/1) | none until this round — QUALITY #107 is added from it | the class rule `tools/round-67/gap-rule-v2.json` with its `class_disposition` block; shown by the 2/4 vs 4/4 control |
| M67-1 | boundary/environment: the first freeze passed the patched gap-rule name as an **absolute** path, while the engine reads its rule through `git show <rev>:<path>`; the counter was dead on arrival (exit 2, "gap-rule.json absent at freeze") | `.ufo/waves/round-67/l1/scores/c1-data-stage.json` (first run, exit 2); CriticClaims F0 | none — the pre-freeze control never exercised the `--score` path | lane-relative name + supersession `1e7fe7b7`; the next score reached the carrier clauses |
| M67-2 | process/commit: the "data run" commit named the receipt directory, and a named-directory commit silently skips files over 1 MiB, so the four 2 MB `after.json` envelopes stayed uncommitted and the first score read `receipt_present false` on all four | `git show --stat a4c1d0fc` (4 `run.json` only) vs `git ls-tree`; the score probe at `6dcc447e` | none | the four envelopes committed by name at `454071dd` |
| M67-3 | environment/pin: the L1's own `npx -y rea-agents@6.5.0 --version` probe rewrote the npx cache's `package-lock.json`, so the round-42 pin `d42d56f0` became unreproducible (a fresh cache reproduces `815c18f1`) and the engine refused the run as unevaluable | the cache lock mtime 21:40; the fresh-cache reproduction `815c18f1`; the package's own `package.json` sha `a5003023` unchanged | none — the pin bound a mutable bookkeeping file; QUALITY #110 is added | `REA_PKG_R67` (version + `package.json` sha + the lock this host resolves), disclosed in every receipt; supersession `ecc4de0e` |
| M67-4 | vacuous/patch: dropping `carrier_fresh_ok` was a no-op — the engine's prior-pin sources do not list the four carrier pins, so the clause is true 4/4 — and the docstring stated a false reason ("freshness cannot hold by construction") | `w1/MutCounter/mutants.md` M1 (0 behavioural leaves); the score receipt's `carriers[].carrier_fresh_ok` true 4/4 | none | the clause set is used unchanged; supersession `7cfe83e4` |
| M67-5 | provenance/statement: the rule dropped the round-50 `removed.silent.char-device` row while the docstring and atom A5 said `removed` was unchanged | `w1/SentinelScope/audit.md` F1; `diff -u tools/round-50/gap-rule.json tools/round-67/gap-rule-v2.json` | none | the rule is back at its freeze bytes and the docstring states the dropped row is inert; supersession `3e7b59db` |
| M67-6 | gate strength: the battery's kill test accepted **containment** (any failing case), so a wrong-defect pair certified `killed_after 2` | `w1/MutBattery/mutants.md` N1/N2 and its Probe A | none until this round — QUALITY #108 is added | exact failed-case-set equality per mutant; shown by the re-taken score receipt |
| M67-7 | gate strength: the battery's selftest asserted no case inventory, so a dropped case still printed `SELFTEST CLEAN cases=8` | `w1/MutBattery/mutants.md` N4 | none — QUALITY #109 is added | the `case-inventory` case (names, not a count floor) |
| M67-8 | provenance/statement: the container's A4 still described the first freeze's clause drop after the repair, and A0 cited an order receipt that did not exist yet | `w1/ExecPins.md` F2/F4 | the seat's own pin audit | A4 corrected, `l1/records/r67-order.txt` written; container correction at `4c2c85d3` |

## Outcome

- **R67-C1 — verified.** `--score` at `832399175bf3af1f8a5f684f198fb45da34e313f` reports `carriers_matched 4` of
  `target 4`, `met_target true`, exit 0, every one of the engine's 23 clauses true on all four carriers,
  `failing []`, `bindings_false []`, `carriers_unchanged true`, `gap_rule_unchanged true`
  (`l1/scores/c1-at-landing.json`); re-measured at the record `7a3c21d4cd72549f60b536038f28fa7aa4e1ebc6`
  (`l1/scores/c1-at-record.json`). Before-arm: the same four committed envelopes under the round-50 rule score
  `gaps_ok` on 2 of 4, the round-67 rule on 4 of 4, one removed symlink gap still fails, a char-device path published
  as a regular file is caught, and a junk rule that waives symlinks passes the first red fixture
  (`l1/pre/control-dryrun.json`, exit 0). The counter's receipt binds the predicate's second conjunct by reading the
  committed control receipt and requiring `control_ok true` / `gaps_ok_round50 2`.
- **R67-C2 — verified.** `--score` at `2dd5f2cd4b854ccecc0a55d75f960bc851cdab13` reports `survived_before 2`,
  `killed_before 0`, `killed_after 2`, both pristine counters green (30 and 26 cases), exit 0
  (`l1/scores/c2-at-landing.json`); the do-nothing control scores 0 of 2 killed
  (`l1/pre/control-dryrun-c2.json`). The mutants are the r66 M5 and M2; each dies on its own named case, and the
  exact failed-case-set test means a wrong-defect pair cannot certify.
- **Freeze integrity, disclosed.** Four instrument supersessions before the record (`1e7fe7b7`, `ecc4de0e`,
  `7cfe83e4`, `3e7b59db`), each with a commit, a reason and a re-taken before record; the predicate sentences never
  changed (reviewer sha256 `9cbbc4e3…` / `babeca7b…`); the R29 gate reports round-67 `CLEAN`; the after-arm receipt
  names the instrument sha it ran. The kill rule's "post-freeze instrument edit" is read as an *undisclosed* edit
  (QUALITY #33) — the closure rules on that reading.
- **Wave.** `r67-w1`, 12 seats (3 executor, 1 reviewer, 1 critic, 2 mutation-testers, 1 sentinel, 1 scout,
  1 connector, 2 scribes), 12/12 settled, 0 dead, every seat with a report
  (`l1/records/r67-wave-status.json`). No residual call.
- **Outside closure — pending.** This lesson does not self-certify either verdict, and the two spot-check samples
  (S268 admit; the kernel-page and receipt rejects) are the closure's to re-open.

## Census

Round start (base `a7a4ce69`, recorded 2026-11-04T00:47Z): `sources-census.sh validate --root
/home/vgpnk/Projects/shokunin kaidoku` exit 0, 174 rows, tier `A=160 B=9 C=5`, status `mined=165 rejected=9`,
19 standing W04 (`l1/census-start.txt`). Round end: 175 rows after S268, tier `A=161 B=9 C=5`, status
`mined=166 rejected=9`, malformed rows 0, the same 19 W04 (`l1/census-end.txt`). The 19 W04 stay named debt at both
ends.
