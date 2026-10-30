# ScoutDraftsInventory — round 52, wave r52-w1

**Seat:** `ScoutDraftsInventory` (scout) · **status:** settled
**Full deliverable:** `.ufo/waves/round-52/w1/ScoutDraftsInventory/inventory.md`
**Receipts:** `.ufo/waves/round-52/w1/ScoutDraftsInventory/receipts/` (`receipts.tsv` = label,
command, exit, stdout sha256, stdout bytes, UTC; plus per-label stdout dumps, `ctl-old.json`,
`ctl-new.json`, `draft-table.md`)

## Verdict

Round 51 landed **only** `tools/round-51/census3.py` + `census3.json` — no counter v2, no triage
v6, no controls, no harness, no fetcher, no gap rule (matches its own claims' Final
disposition). Every r52 instrument is a fresh port. Of the big r51 drafts, **one is a usable
port base and three are not**: the L1-merged counter draft works (measured), while the triage
v6 draft is a **SyntaxError**, the controls driver **cannot drive that same counter**, and the
fetcher draft **regresses a green selftest into a crash**. Port from the r50 sources plus the
r51 *specs*, not from the r51 drafts.

## The three findings that change what the L1 freezes

1. **`l1/drafts/c1-counter.py` is the only usable port base — and it is proven.** In a scratch
   `git clone --shared` of the lane at the claims-draft commit, its `--controls` mode over the
   committed round-50 envelopes gave **CTL-OLD 2/4 exit 1** (r50 rule) and **CTL-NEW 4/4 exit 0**
   (law rule), with per-carrier `gaps_note` naming `dev/pts/0` on `g7581`/`g7582` — it
   independently reproduces the round-50 miss and the law repair. It already carries
   `law_shape_ok`, `census_rederived_ok`, `--controls`, `re_scored_pins`/`prior_pin_sources`,
   the REA retry policy and the rule-label grammar.

2. **Three r51 drafts are broken and must not be copied.** (a) `w1/ExecTriV6/sqfs-triage-v6.py`
   has a literal `CUT 1033.=1033` at line 288 (`py_compile` exit 1), plus a duplicated
   `no-reader-failure` row, an unwired evaluator, no executability audit and no `--table` flag.
   (b) `w1/ExecControls/c1-controls.py` omits `--rev` from the counter argv **and** reads
   `carriers_matched` where the counter emits `dispositions_matched` — measured: all 18 controls
   exit 2 identically, CTL-OLD/NEW/JUNK "misbehaved", driver exit 1. (c)
   `w1/ExecFetchSelftest/fetch-vendor.py` calls `opener.handle_error(...)`, but that attribute
   is urllib's handler **dispatch dict** → `TypeError: 'dict' object is not callable`; the
   landed r50 fetcher's selftest is green 16/16, so the draft is a regression. The correct
   call, measured green: `_AvmOnlyRedirect().redirect_request(req, None, 302, 'Found',
   {'Location': 'http://example.invalid/redirect'}, …)` → `redirect off download.avm.de refused`.

3. **The r52 law rule is not the r51 rule.** `w1/ExecRuleDerive/gap-rule-v2.json` still has
   `allowed['char-device'|'fifo'|'socket'] = ['unpublished-entry']`, so it **fails** r52's
   `law_shape_ok` ("`allowed` for those kinds is the empty list"). Take the r50 rule and apply
   the shape the r51 counter draft's own `law_rule()` helper builds (empty device `allowed`,
   empty `removed.silent`, `required['char-device'] false`).

## Seven deltas the L1 must apply (all measured or source-traced)

* the counter draft lacks `--provenance-base` / `--receipt-fresh-base`, which r52 claims name;
* it emits `depth_gaps_recorded`, r52's predicate spells it `depth_gap_recorded`;
* the r52 **C2 before-arm cannot carry the round-52 freeze** — the v5/v6 freeze gate raises
  `Unevaluable` → exit 2 when the freeze is not an ancestor of `--rev`, and the round-52 freeze
  post-dates the claims-draft base, so the before-arm as written exits 2, not 1 (MutTriV6
  flagged this landmine for r51; it is still unaddressed in the r52 claims);
* `census_outside 0` needs the census **re-derived at the round-52 freeze** — the frozen
  `census3.json` lists 57 paths and the freeze adds 5–6 registry rows, so reusing it yields
  5–6, not 0 (MutTriV6 measured 13 against census2 for the same reason);
* the r51 law-rule draft and the r51 controls driver's "new" variant are whitelists, not the law;
* `misroot-sweep.sh` must lose its `--apply` mode (it copies files out of the fleet tree) and
  its `round-51` classifier string;
* `ExecCounterV2/c1-counter.py` and `l1/drafts/c1-run.sh` are pure constant substitutions over
  the landed r50 files (36 and 39 diff lines) — port from the r50 source.

## Scope honoured

Read-only on the lane tree: the round-51 tree is byte-unchanged (`git status` shows only the
round-52 wave dirs untracked); the only writes are this seat directory and this report. No REA,
no data run, no network, no lane/fleet git mutation, no tools installed. Scratch
`/fast/scratch/hyaku/kaidoku-r52/w1-ScoutDraftsInventory` removed after the receipts were
copied in.
