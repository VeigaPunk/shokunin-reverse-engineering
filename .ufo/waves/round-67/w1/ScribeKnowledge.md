# ScribeKnowledge — round 67, w1 (kaidoku-shokunin)

Seat: scribe (leaf; no subagent dispatch). Scope: the R67-C1 knowledge entry prose only — no data
run, no counter run, no registry/PROVINCE/README edits, no commits.

## Behavior (what this seat did)

1. Read the frozen inputs: `plans/round-67-claims.md` (R67-C1), `.ufo/waves/round-67/claims.json`
   (pins, predicate, frozen atoms A0-A9), `tools/round-67/gap-rule-v2.json`,
   `tools/round-50/gap-rule.json`, `tools/round-50/c1-counter.py` (binding code, `gap_rule_model`,
   `disposition_check`), `tools/round-67/avm-le-counter.py` (patches, bindings, modes),
   `corpus/knowledge/2026-10-28-r50-avm-le-squashfs-core.md`,
   `corpus/knowledge/2026-10-30-r51-avm-le-squashfs-core.md`, `corpus/QUALITY.md`,
   `PROVINCE.md`/`corpus/README.md` frontier notes, the four round-50 `after.json` receipts and the
   four nonregular tables, and the five pre-freeze before-arm receipts under
   `.ufo/waves/round-67/l1/pre/`.
2. Fetched, into `S=/fast/scratch/hyaku/kaidoku-r67/ScribeKnowledge`, and verified in the bytes:
   - `https://docs.kernel.org/filesystems/squashfs.html` — HTTP 200, 26 045 B, sha256
     `10767bbf8b5c49e81d7aafadd84b6e06602c19641d7f7ae9b0a0258d81733685`. The assigned locator's
     expected device-inode text is absent (`Basic device inode`, `Extended device inode`, `major`,
     `minor`: 0 occurrences); the nearest sentence (raw lines 412-414, 25 words) states only that
     inode types differ in contents/length and is rendered HTML (QUALITY #17). Rejected as the row
     locator.
   - `https://raw.githubusercontent.com/AgentD/squashfs-tools-ng/e3dcf1770fd77a0babcca422dcbe7b2cc7b8ab90/doc/format.adoc`
     — HTTP 200, 41 981 B, sha256 `08c38b69a9fda3d1a7ce9784132a75cb8c8d65f290e2747af74ab58ae50c82eb`.
     Verified: heading `=== Device Special Files` line 730; quote line 732, 13 words, one
     occurrence, byte offset 28 445, single line, no markup inside the span; layout stated identical
     for char and block devices; extended form adds an xattr index; Linux major/minor lines 742-746;
     character type codes 5 (basic) / 12 (extended) at lines 549 / 556.
   - `https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c`
     — HTTP 200, 116 844 B, sha256 `6222d940c45537d597e2b36d1d46abbc90f0863e7106bab8fa7bdd97fd939341`.
     Verified `:1287` `if(root_process)`, `:1296-1297` char/block `mknod`, `:1313-1318` non-root
     `failed` branch, `:1328` FIFO and `:1349` socket outside the gate.
   - `https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py`
     — HTTP 200, 19 842 B, sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`
     (equal to the installed copy). Verified `:455`, `:463`, `:53-54`, `:48`.
3. Re-counted the four carriers from committed bytes only: `normalized_result.files`,
   `normalized_result.extraction_gaps`, `normalized_result.diagnostics` in
   `corpus/evidence/round-50/c1/<id>/after.json`, and `kind` columns of
   `tools/round-50/oracle/<id>.nonregular.tsv`. Result: 4 556 / 4 564 / 4 709 / 3 955 published
   regular files; nonregular rows symlink/dir/char = 639/349/13, 639/349/13, 613/300/1, 568/255/1;
   gaps 636+1, 636+1, 612+1, 567+1; `MaliciousSymlinkRemoved` diagnostics 3, 3, 1, 1. No char-device
   path is gapped or removed on any carrier (path comparison against each carrier's char set).
4. Re-hashed the frozen instruments and compared with `claims.json`: all seven match
   (`avm-le-counter.py` `f78ed365…`, `gap-rule-v2.json` `e66ba022…`, `mutation-battery.py`
   `cabc0a0b…`, `c1-run.sh` `00be5a87…`, `c1-counter.py` `9820811b…`, `closure-boundary.py`
   `3c5cfb03…`, `coverage-selfcheck.py` `1be9d046…`); round-50 rule `43f7c8d7…`.
5. Confirmed read-only that `3663e6b21dccf4c4957f459301156664d8b151d6` is the commit that first adds
   `.ufo/waves/round-67/claims.json` (`git log --diff-filter=A`, committer time
   `2026-11-03T21:51:14-03:00`).
6. Wrote `.ufo/waves/round-67/w1/ScribeKnowledge/entry.md` (237 lines, 5 `source:` lines, provenance
   trio first, observation/inference/unknown labels throughout).

Not run, by design or out of scope: the R67-C1 `--score`/`--control` counters (the before-arms are
committed; the after-arm is the L1's), any REA call, any data run, any git/jj write, any pacman/uv
install (none needed). No file outside `$S` and the two seat paths was written.

## Gates / checks actually exercised

| check | result |
|---|---|
| source quote contiguity + count (format.adoc) | 1 occurrence, byte offset 28 445, line 732, 13 words |
| source quote locator (nearest heading) | `=== Device Special Files` line 730 (QUALITY #91(i)) |
| assigned-locator probe (kernel docs) | HTTP 200, 26 045 B, quote absent — rejected, not paraphrased |
| instrument pins vs `claims.json` | 7/7 equal at read time |
| freeze identity | `3663e6b2…` = first-add commit of `claims.json` |
| staged `--score` at cutoff | exit 2 `unevaluable` (REA package-lock `815c18f1…` != frozen `d42d56f0…`), no `carriers_matched` |
| per-carrier counts vs round-50 entry | equal for files/gaps/kinds/removals |
| char-device path gapped or removed | 0 on all four carriers |
| entry `source:` count | 5 (`S<scout-row>`, S250, S245, S244, S249) |
| labels | every prose conclusion carries observation / inference / unknown |

No verdict is claimed for R67-C1: the four data receipts are observed, but the staged `--score` is
exit 2 (REA package-lock refusal) and no `carriers_matched` key exists at this cutoff. The entry's
status line is conditional in the lane's r41 form.

## Touched surfaces

- `kaidoku-shokunin/.ufo/waves/round-67/w1/ScribeKnowledge/entry.md` (new; the L1 lands it at
  `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md`).
- `kaidoku-shokunin/.ufo/waves/round-67/w1/ScribeKnowledge.md` (this report).
- Scratch `S=/fast/scratch/hyaku/kaidoku-r67/ScribeKnowledge` (removed before yield).

## Findings for the L1 / canonical judge

1. **`gap-rule-v2.json` is not byte-identical to the round-50 rule in `removed`.** The target text
   says the rule keeps "`allowed`/`removed`/`structural` unchanged from
   `tools/round-50/gap-rule.json`". Measured diff: `allowed` and `structural` are equal; `removed`
   loses `"silent": {"char-device": ["247:0"]}`; `required.char-device` true→false; `claim` dropped;
   `round` and `supersedes` added; `class_disposition` added. The `silent` removal is subsumed —
   `disposition_check` consults `silent` only for required kinds — so the rule is not stricter for
   any char-device row, but the "removed unchanged" phrasing is not byte-exact. Verbatim from the
   rule: `"supersedes": "tools/round-50/gap-rule.json (frozen; a per-row required disposition for
   char-device entries, generalised from the Cable-carrier class where one char device exists)"`.
   The entry states this in "The class rule and its exact scope".
2. **Source-row substitution.** The planned source (Linux kernel SquashFS docs, "device-node inode
   text") does not carry the text; the ScoutSource seat rejected it and proposed squashfs-tools-ng
   `doc/format.adoc` at `e3dcf177…` (proposed S268, "renumber at append"). The entry cites that row
   as `S<scout-row>` for the L1 to substitute. The counter's `sourced` binding needs the admitted row
   to have `opened = 2026-11-03` and `used-by` containing
   `corpus/knowledge/2026-11-03-r67-avm-le-squashfs-core.md` (or its stem).
3. **After-arm state at this seat's cutoff (2026-11-03 ~22:05 lane-local).** The four data receipts
   exist at `corpus/evidence/round-67/c1/<id>/{after.json,run.json}` (first written 21:54-21:56;
   subject digests equal the carrier pins; counts reproduce round 50: 4 556/4 564/4 709/3 955 files,
   637/637/613/568 gaps, 3/3/1/1 removals). The staged `--score` is **exit 2, not a verdict**:
   `l1/scores/c1-data-stage.json` records `unevaluable` "rea package does not match the freeze:
   package-lock.json sha256 815c18f14daefceeee603065a291e008330ae1af763639e31bab52a58373f803 != frozen
   d42d56f0f4f8baf3ecc24f2bd24f9f09e3c99b83592ef85201f74df255e0c6ca", with no `carriers_matched`.
   The entry's status line is a conditional promotion; the L1 must keep it only if `--score` reports
   `carriers_matched 4`, `met_target true`, exit 0, and otherwise replace it and the PROVINCE row with
   the honest stop (R67-C1 kill rule). I did not author the receipts or the stage score (no writes
   under `corpus/` or `l1/`).
4. **Rule scope beyond the carriers.** `required.fifo`/`required.socket` are false with
   `allowed ["unpublished-entry"]`, but no FIFO or socket row exists on the four carriers; S250's
   privilege gate is char/block-specific (FIFO :1328 / socket :1349 are outside it). The entry marks
   this unexercised (QUALITY #96) rather than extending the device law.
5. **Freshness clause dropped.** `carrier_fresh_ok` is dropped by `patches.dropped_clauses`; the
   entry discloses it in "What moved" and in the limits.
6. **Date.** The fetch's HTTP `Date` was `2026-11-04T00:55:58Z` (lane-local 2026-11-03); the entry's
   `verified-at: 2026-11-03` is the lane-local date the L1 must reconcile with the landing commit
   (committer time is `2026-11-03T2x:xx-03:00`, i.e. UTC 2026-11-04).

## Artifact paths

- `.ufo/waves/round-67/w1/ScribeKnowledge/entry.md`
- `.ufo/waves/round-67/w1/ScribeKnowledge.md`
- Source bodies (scratch, removed): `squashfs.html`, `format.adoc`, `unsquashfs.c`, `squashfs.py`.
- Scout receipts (peer-owned, read): `.ufo/waves/round-67/w1/ScoutSource/{row.md,gate.md,fetch.json}`
  and its retained fetched bodies.
