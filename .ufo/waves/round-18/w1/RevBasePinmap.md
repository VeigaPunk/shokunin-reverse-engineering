# RevBasePinmap — is R17-PINMAP open at `9011581`?

**Verdict: OPEN.** The C1 baseline premise is confirmed, not falsified. At
`9011581d84527ba34c675f9cf912e54d2e72d470` the contract's four R17-PINMAP checks are 0/4, and the
substantive record test fails: 8 second-pass receipts, 29 mid-run pin checks, **0** per-path mid-run
maps. The lesson sentence at `corpus/lessons/round-17-verifier-spotcheck.md:137` is accurate as
written (one harmless off-by-one on the closing brace), so this is **not** "mis-stated"; nothing at
the baseline corrects the overstatement, so it is **not** "already-closed".

Axes: calibration = verdict + exact anchors; operability = a two-read offline test; depth = the
contract's token checks are not a closure test (below).

Baseline checks (all read-only):
`git rev-parse HEAD` = `git rev-parse refs/heads/main` = `9011581…470` (exit 0).
At the time of these reads `git status --porcelain --untracked-files=no` was empty and
`git diff --stat 9011581 -- <cited files>` was empty (exit 0), so working-tree line numbers equalled
baseline line numbers then. Sibling executors have since begun unstaged edits (`carrier-run.py`,
`compare.py`, `verify.py`, see the post-baseline note in §5); every verdict fact below is therefore
read from `git show REV:path`, never the moving working tree.

## 1. What the baseline actually retains (observation)

| Anchor | Observation |
|---|---|
| `.ufo/waves/round-17/tools/carrier-run.py:479-487` | Per mid check: `mid = pins.snapshot(pin_paths)`; `cmp_mid = pins.compare(pins_pre, mid)`; the receipt entry appends exactly `taken_at_utc`, `equal`, `entries` = `len(mid["entries"])` (an **int**), `changed`, `missing`. The snapshot object `mid` is a local and is never written. |
| `.ufo/waves/round-17/tools/carrier-run.py:336-337` | `pins_pre = pins.snapshot(pin_paths)`; `receipt["pins_pre"] = pins_pre` — full map retained. |
| `.ufo/waves/round-17/tools/carrier-run.py:385-388` | `pins_post = pins.snapshot(pin_paths)`; `receipt["pins_post"]` and `receipt["pins_compare"]` — full map + verdict retained. |
| `.ufo/waves/round-17/tools/carrier-run.py:37` | `PIN_CHECK_S = 30.0` (cadence claim). |
| `.ufo/waves/round-17/tools/pins.py:62-72,75-106` | A snapshot is `{taken_at_utc, monotonic_ns, entries:{path:{sha256,size,mtime_ns}}}`; `compare` returns `{equal, changed, missing, errors, pre_taken_at_utc, post_taken_at_utc}`. |
| `.ufo/waves/round-17/runs/*/receipt.json` (8 receipts at baseline) | 29 `steps.analyze.pin_checks` entries total; every entry's key set is exactly `changed, entries, equal, missing, taken_at_utc`; every `entries` is `146` (int); `pins_pre`/`pins_post` each carry 146 full entries. Per label: 4, 2, 3, 2, 4, 4, 2, 8. Example: `pro-aether` `{"changed": [], "entries": 146, "equal": true, "missing": [], "taken_at_utc": "2026-10-20T14:30:47.790881+00:00"}`. No `pins/` directory or `map_path`/`map_sha256` exists anywhere under `runs/`. |
| `da64646:.ufo/waves/round-17/runs/*/receipt.json` (8 first-pass receipts) | `steps.analyze.pin_checks` is **absent**; `pins_pre`/`pins_post` each 146 entries. This confirms knowledge line 33 ("first-pass receipts kept only pre/post maps"). |
| `95e34db:.ufo/waves/round-17/tools/carrier-run.py:456-468` | The producing revision for the second pass has the identical summary append (five fields). `git log -S'"entries": len(mid["entries"])"' -- carrier-run.py` returns only `95e34db`, so the receipt shape and the cited code agree. |

## 2. The cited text sites, at the baseline (observation)

- `corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32`:
  "each pin map is retained with its UTC instant: pre, every 30 s during analyze (2–8 checks per run,
  `steps.analyze.pin_checks`), and post. All maps are equal." The universal "each pin map … every
  30 s" is false: the mid instants keep a verdict and a count, not a map. The temporal qualifier
  "**at those instants** only (QUALITY #19)" on line 32 limits *continuity*, not *map retention*; it
  does not rescue the sentence.
- `SCORECARD.md:2374`: "… carries pre/mid/post pin maps with instants." False for mid; only pre/post
  maps exist.
- `corpus/QUALITY.md:29` (admission row 19): "the producing tool keeps each pin map (per-path SHA-256
  and size) with its UTC timestamp and the comparison verdict, including mid-run checks, plus a
  retained red run …". The r17 producer meets this for pre/post, not for mid-run. Row 19 is a
  standing criterion, not an overstatement; it is the rule the r17 record fails.
- `corpus/lessons/round-17-verifier-spotcheck.md:108` and `:137`: the "partial disagree" and the
  routed defect. Both quote the sites accurately. `:137` cites `carrier-run.py:481-486`; the append
  literal actually closes at `:487` (`})`), a cosmetic off-by-one, not a mis-statement.

No baseline artifact closes the defect: `grep -n 'R17-PINMAP'` and `grep -n 'comparator verdict'`
return **no match** (exit 1) in the knowledge file and SCORECARD; `grep -n 'map_sha256'` returns no
match (exit 1) in `carrier-run.py`; QUALITY has no admission row with both tokens.

## 3. Verdict on the baseline premise

**Open** — observation plus the contract's own definition:

| Contract `contract.md:29-32` check | Baseline |
|---|---|
| (a) knowledge line with `R17-PINMAP` + `comparator verdict` | `lines=[]` |
| (b) SCORECARD line with both | `lines=[]` |
| (c) admission row why-cell with `round-17-verifier-spotcheck.md` + `R17-PINMAP` | `matching=[]` (the loose scan counted 26 numeric table rows because the rejection table also has numeric first cells; the admission table alone has 20) |
| (d) literal `map_sha256` in `carrier-run.py` | absent |

So **0/4**, `open_count` contribution 1, at the baseline. The C1 claim's `6 at 9011581` holds for this
defect.

Secondary notes (calibration/depth):

1. **The lesson's remedy is prospective on one branch.** "Either retain mid maps (or their digest) or
   append a named correction" (`:137`): the first branch cannot retract the r17 claim, because the
   r17 receipts are immutable by the round's non-goal ("no edit of round-17 retained receipts/logs",
   `claims.json:32`) and the discarded `mid` snapshots cannot be recovered. Only the correction branch
   closes the *r17 text*; a forward fix can only make a *new* sentence about future runs true.
   `[INFERENCE from the two facts]`
2. **The verdict+pre-map is stronger than "no map" sounds, but it is still not the map.**
   `pins.compare` decides `equal` from `sha256`+`size` over all 146 paths (`pins.py:96-98`), and the
   pre map is retained, so `equal:true` deterministically entails same `sha256`+`size` at that instant
   *if the comparator is correct* (the red case guards that). What is absent is the inspectable
   per-path object QUALITY #19 demands, not necessarily byte evidence. This is why the defect is an
   **overstatement of the retained object**, not a claim that the bytes changed. `[INFERENCE]`
3. **A second precision gap.** The mid summary drops `errors` (`carrier-run.py:481-487`), while
   `pins.compare` produces it (`pins.py:103`). A mid check with an unreadable path would record
   `equal:false`, `changed:[]`, `missing:[]` and name no path. `[OBSERVATION of the fields;
   INFERENCE of the consequence]` This gap survives the contract's forward fix unless the new
   `pin_checks` entry also keeps `errors`.
4. **An additional site the routed sentence does not list.** `corpus/lessons/round-17.md:90` says
   "the entry states identical bytes at those instants only"; the entry's mid-instant support is the
   verdict, not a map, so repeating "identical bytes" for mid instants inherits the same gap. It is
   not a map-retention sentence, so it is a scope extension, not a contradiction of `:137`.
   `[OBSERVATION]`

Not "mis-stated": every quoted phrase, key set, count and line anchor checks out. Not
"already-closed": no correction artifact exists at the baseline.

## 4. Minimal objective test (distinguishes open from closed)

Rev-scoped, offline, stdlib. Read Git objects at REV only.

- **T1 `claim_corrected(site)`** for `K = corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md:30-32`
  and `S = SCORECARD.md:2374`: true iff a later line in the same file (append-only; filed bytes
  unchanged) contains `R17-PINMAP`, the site's literal anchor (`…md:30-32` / `SCORECARD.md:2374`), and
  the negation that the mid-run record is the comparator verdict/count against the retained pre map,
  **not the map** (minimally the substring `not the map`), with no later line re-asserting mid-run map
  retention. The original filed line may remain — the lane's append-only rule requires it to — but the
  correction must name the site and override it. The anchor requirement follows the lane's own
  line-exact correction precedent (`corpus/lessons/round-17.md:94-99`).
- **T2 `mid_maps_retained`** (forward-fix check only): for every new run receipt at REV, for every
  `steps.analyze.pin_checks[i]`, a per-path map exists at that check's `taken_at_utc`: either an inline
  `entries` dict of 146 path→{sha256,size}, or `map_path` whose file's sha256 equals `map_sha256`.
  A source-level identifier is not evidence.
- **Verdict:** `closed_r17(REV) = T1(K) AND T1(S)`. `forward_fix_ok(REV) = T2`, required only if a text
  at REV claims the producer now retains mid maps. `open` otherwise.

Baseline result: `T1(K)=false`, `T1(S)=false`, `T2=false` (no new-run receipts either) → **open**.
The actual receipts and the contract checks were evaluated by the ad-hoc run in §6; there is no
`W18/tools/routed-defects.py` yet (`ls` exit 2), so §6 emulates its four checks exactly as written.

Why this is minimal: two `git show` reads (text) plus one JSON parse (receipts). It cannot be
satisfied by token co-occurrence without the site anchor and the negation, and it cannot be satisfied
by a comment in the producer.

## 5. Is `contract.md:29-32` too weak or too strong?

**Too weak as a truth test.** (a), (b), (c), (d) are presence checks over file text. Concrete
false-closure witness: keep the false sentences at knowledge:30-32 and SCORECARD:2374 unchanged, add
a line `R17-PINMAP comparator verdict` to each file, add a QUALITY row whose why-cell contains the two
tokens, and add a comment `# map_sha256` to `carrier-run.py` — all four pass, yet no mid map exists
and the two false claims still stand. The contract never opens a receipt, never checks a digest,
never requires the correction to negate the claim, and never requires the site anchor. Check (d) in
particular accepts a substring in a comment or dead string; it does not require `map_path`,
`map_sha256`, a matching sidecar digest, `receipt-validate.py` recomputation, or the tampered-map red
selftest. `[INFERENCE from the check text; no routed-defects.py exists to run]`

The contract's own selftest does not catch this: its "closed" fixture is defined by the same tokens
(`contract.md:46-47`), so the tool is green on a token-only fixture by construction.

**Too strong relative to the routed remedy.** `:137` allows "either retain mid maps (or their digest)
or append a named correction". The contract requires (a)+(b) corrections **and** (d) the tool-side
fix; a lane that chose the correction-only branch, which the routed defect authorizes, is reported
open. It also imposes exact wording ("comparator verdict"), a specific file for the correction (a),
and a new QUALITY admission row (c) as closure conditions — (c) is a separate C1 deliverable (the new
criterion), not evidence that the false r17 sentence was corrected.

**Wrong owner for (d).** The `carrier-run.py` change lives in the C3 in-place-fix list
(`contract.md:128-131`, "exactly one owner each"), yet C1's `open_count == 0` depends on it. So C1's
discharge is not independently attributable to C1, and (d) can be satisfied by a comment while the
actual defect remains. `[OBSERVATION of the contract's ownership split]`

Recommended amendment: keep (a)-(c) as reporting checks but replace (d) with T2 over an actual
post-fix receipt (or a red selftest fixture), and add T1's anchor+negation condition. Add a
false-close selftest case: baseline false sentences + token line + `# map_sha256` must report `open`
(or `text_only`). Otherwise `open_count 6 → 0` measures token compliance, not defect closure.

### Post-baseline snapshot (observation; work in progress, may move)

At this seat's last read `git status --porcelain` listed `M .ufo/waves/round-17/tools/carrier-run.py`,
`M .ufo/waves/round-17/tools/compare.py`, `M .ufo/waves/round-17/verify.py` (exit 0). The working-tree
`carrier-run.py` now writes each mid snapshot to `out_dir/pins/mid-<n>.json` and records
`map_path`/`map_sha256` (working-tree lines 369-370, 493-515), which would satisfy contract (d) at the
delivered revision. `receipt-validate.py` was still unmodified at that read, so the contract's
recompute/tampered-map-red half (`contract.md:128-131`) was not yet in the tree, and no new receipt
carrying a `map_path` exists yet. This is exactly why (d) alone cannot close the defect: the literal
and the validator half can land at different times, and only a post-fix receipt (T2) proves the
behavior. The baseline verdict above is unaffected — it is read from `9011581`, not the worktree.

## 6. Commands exercised (read-only; `L=…/kaidoku-shokunin`, `R=9011581…470`)

```text
git -C "$L" rev-parse '9011581d84527ba34c675f9cf912e54d2e72d470^{commit}'   -> 9011581…470, exit 0
git -C "$L" rev-parse HEAD                                               -> 9011581…470, exit 0
git -C "$L" rev-parse refs/heads/main                                    -> 9011581…470, exit 0
git -C "$L" cat-file -t 9011581…470                                      -> commit, exit 0
git -C "$L" log -1 --format='%H %ci %s' 9011581                          -> 2026-10-20 12:06:56 -0300, exit 0
git -C "$L" status --porcelain --untracked-files=no                      -> empty, exit 0
git -C "$L" diff --stat 9011581 -- corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md SCORECARD.md corpus/QUALITY.md .ufo/waves/round-17/tools/carrier-run.py corpus/lessons/round-17-verifier-spotcheck.md -> empty, exit 0
git -C "$L" show "$R:corpus/knowledge/2026-10-20-r17-go-carrier-diagnostics.md" | nl -ba | sed -n '28,33p' -> lines quoted, exit 0
git -C "$L" show "$R:SCORECARD.md" | nl -ba | sed -n '2374p'             -> "pre/mid/post pin maps with instants", exit 0
git -C "$L" show "$R:corpus/QUALITY.md" | nl -ba | sed -n '29p'          -> row 19, "including mid-run checks", exit 0
git -C "$L" show "$R:.ufo/waves/round-17/tools/carrier-run.py" | nl -ba | sed -n '465,505p' -> 479-487 summary, exit 0
git -C "$L" show "$R:.ufo/waves/round-17/tools/carrier-run.py" | grep -n 'map_sha256' -> no match, exit 1
grep -n 'map_sha256' "$L/.ufo/waves/round-17/tools/carrier-run.py"        -> no match at read time, exit 1 (post-baseline note)
python3 aggregate over 8 `runs/*/receipt.json` at R                        -> RECEIPTS 8 mid_checks 29 all_mid_maps_retained False, exit 0
python3 emulation of contract checks (a)-(d) at R                          -> a,b,c,d all ok=False, exit 0
git -C "$L" show '95e34db:.ufo/waves/round-17/tools/carrier-run.py' | nl -ba | grep -A10 -B6 'pin_checks' -> summary at 456-468, exit 0
git -C "$L" log --oneline --all -S'"entries": len(mid["entries"])' -- .ufo/waves/round-17/tools/carrier-run.py -> only 95e34db, exit 0
python3 parse of 8 `da64646:runs/*/receipt.json`                           -> pin_checks absent; pre/post 146, exit 0
git -C "$L" show "$R:corpus/lessons/round-17.md" | nl -ba | sed -n '90p'  -> secondary site, exit 0
git -C "$L" show "$R:corpus/lessons/round-17-verifier-spotcheck.md" | nl -ba | sed -n '100,150p' -> :108, :137, exit 0
git -C "$L" show "$R:.ufo/waves/round-17/tools/receipt-validate.py" | grep -n -E 'pin_checks|map_path|map_sha256|mid' -> :186-191 checks `equal` only; no map digest, exit 0
ls "$L/.ufo/waves/round-18/tools"                                          -> absent, exit 2
```

Aggregate output at the baseline:

```text
CHECK a ok=False lines=[]
CHECK b ok=False lines=[]
CHECK c ok=False admission why-cells matching=[] (rows=26; admission table alone = 20)
CHECK d ok=False literal map_sha256 present=False
RECEIPTS 8 mid_checks 29 all_mid_maps_retained False
calib-esbuild-0.25.12 4 / calib-shfmt 2 / pro-aether 3 / pro-containerd-shim 2 /
pro-esbuild-0.21.5 4 / pro-esbuild-0.27.7 4 / pro-notesmd-cli 2 / pro-op 8
```

## Limits

Read-only: no lane file edited except this report; no jj/git write; no REA analyze/search/decompile,
no Ghidra, no carrier execution. `routed-defects.py` does not exist at the baseline or in the current
W18 tree, so §5's "too weak" witness is an argument from the contract's literal predicates, not a
tool run. No installs or upgrades were needed or performed.

Report: `.ufo/waves/round-18/w1/RevBasePinmap.md`
