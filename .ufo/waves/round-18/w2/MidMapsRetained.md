HOLDS

# MidMapsRetained: r18 mid-run pin maps (wave 2, falsify)

Seat: KaidokuR18.MidMapsRetained, an author-side advisory reviewer (a recommendation, not an admission).
REV `b2aad08ceeee8dd125ce0d316056d8bd766c7f94`. Lane `HEAD` = `refs/heads/main` = REV.

The working tree equals REV for every file used: 39/39 blobs equal (A0), and the lane status for the inspected paths is empty.

**Verdict: the target holds.**

- Every r18 receipt was checked: 15 receipts with 22 `pin_checks`, which point to 22 retained `pins/mid-<n>.json`.
- 22 of 22 recomputed sha256 values equal `map_sha256`.
- For all 22, `pins.py compare <pins_pre> <mid map>` exits 0 with `equal: true` and 0 changed, missing or errors (A2, A3).

The side findings F1–F4 do not change any r18 number at REV on this host.

## Totals (observed)

| quantity | value |
|---|---|
| r18 receipts at REV | 15 |
| `pin_checks` entries | 22, all in `steps.analyze`; `inspect-go-binary` has none; there are no search steps |
| `pins/mid-*.json`: tracked at REV / on disk / referenced | 22 / 22 / 22. Orphans 0, dangling 0 |
| sha256 recomputed = recorded `map_sha256` | 22/22, using both the REV blob (A2) and the working-tree file (A3) |
| `pins.py compare pins_pre mid` exit 0, `equal: true` | 22/22, with 0 changed, missing or errors |
| per-entry `(sha256,size,mtime_ns)` = `pins_pre` | 3,344/3,344 (22 maps × 152 entries). This is stricter than `pins.compare`, which ignores `mtime_ns` (`pins.py:96`) |
| recorded `equal/changed/missing` = recomputed; `entries` = len(map) = len(`pins_pre`) = 152; recorded `taken_at_utc` = map's | 22/22 each |
| `pins_pre` < mid < `pins_post` (UTC and monotonic); mid inside `[analyze.started_at, ended_at]` | 22/22. Max \|Δutc−Δmonotonic\| is 0.006 ms |
| map bytes = writer form `json.dumps(sort_keys=True, indent=2)+"\n"` (`carrier-run.py:504-509`) | 22/22 |
| `map_path` = `<lane>/.ufo/waves/round-18/runs/<label>/pins/mid-<n>.json`, n contiguous 1..k | 15/15 |
| `carrier-run.stdout` `pin_checks` = `receipt.json` `pin_checks` | 15/15 |
| `receipt-validate.py --require-mid-maps`, run once per receipt | exit 0 for 15/15 (A6) |

Maps per label:

- 3 maps: calib-aether.
- 2 maps each: calib-notesmd-cli, real-kimi-webbridge, s1246-noswiss-nethttp, s1250-noswiss-nethttp, s1250-swiss-nethttp.
- 1 map each: the other 9 labels.

Anchors at REV:

- `runs/<label>/receipt.json:1938` holds `map_sha256` for mid-1, `:1947` for mid-2, and `:1956` for aether mid-3. `map_path` is on the line before each.
- `pins_pre` is at `:1120` and `mid_run_drift_steps: []` at `:25` (checked in real-kimi-webbridge and s1246-swiss-nethttp).
- The writer is `carrier-run.py:483-517`. The verifier is `receipt-validate.py:453-586`. The comparator is `pins.py:75-106`, with CLI exits at `:144-157`.

Lane statements that these totals confirm:

- `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:66-68` (15/15 exit 0; 22 maps).
- `SCORECARD.md:2438` ("round-18 receipts retain each mid map with `map_sha256`").
- `corpus/lessons/round-18.md:62` ("0 on all 15 r18 receipts").

Producer identity:

- The tool blobs `pins.py`, `carrier-run.py` and `receipt-validate.py` are identical at the producing revision `eb6c266` (`runs/run-log.txt:1`) and at REV.
- All 15 `producer.json` files record the REV `pins.py`/`carrier-run.py` sha256 and `branch_tip` eb6c266 (A1).

The pinned set has 152 paths:

- the carrier;
- 143 Ghidra `typeinfo/golang` files;
- `round-16/selection.py`;
- 5 `round-17/tools` files;
- 1 `round-18/tools` file;
- the label's own `predictions/<label>.prediction.json`.

All 22 distinct lane-internal (path, sha256) pairs equal their blobs at eb6c266 and at REV (A8). Because every mid map equals `pins_pre`, the frozen prediction files had their frozen bytes at every recorded mid instant.

## Findings (by severity)

### F1 — MEDIUM (operability): the retained-map commitment binds a host path, not the committed file
**Observation.**

- `map_path` is absolute (`carrier-run.py:501-502,510`; `runs/real-kimi-webbridge/receipt.json:1937`).
- `receipt-validate.py` hashes whatever is at that path (`:480-481,508-517`). It never resolves the path relative to the receipt or the checkout.
- Neither the knowledge-entry recheck (`corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:3`) nor the validator's stated limitation (`receipt-validate.py:46-49`) mentions this.

Results in a mkdtemp clone with origin removed (A9, A10):

- After tampering the clone's kimi `mid-1.json`, the clone's validator on the clone's receipt exits **0** with no findings (a false green). `pins.py compare` against the recorded path also exits 0.
- Control: with `map_path` rewritten to point into the clone, the validator exits 1 with `mid_map_sha256_mismatch`.
- With the lane path hidden (bwrap tmpfs, simulating another host or path), the clone's 15 receipts all fail: exit 1 with `mid_map_missing` × 22. This happens although the clone holds all 22 committed maps with matching digests.

A2 avoids both failures by resolving every map as `REV:<path relative to lane>`.

[INFERENCE] An outside verifier cannot reproduce "15/15 exit 0" from a checkout of REV without rewriting paths.

### F2 — LOW (calibration/depth): 15/22 "mid-run" maps predate Ghidra's first log line
**Observation.**

- The first check fires on the first poll iteration (`carrier-run.py:470` `last_pin_check = 0.0`; `:483-486`). It lands 45–53 ms after `analyze.started_at_utc` in all 15 receipts (A12). A map's instant is stamped after hashing (`pins.py:68-71`).
- Against each retained `ghidra.log`, the 15 first maps all precede the first logged second, with leads of 0.088–1.017 s. 7 maps fall inside the log window and 0 after it.
- 9 of 15 labels have no mid map inside the window. They are the 9 one-map labels, including held-out D label `s1246-swiss-nethttp`: its map is at 16:28:56.073Z and its log starts at 16:28:57Z (A11).

[INFERENCE] `ghidra.log` uses local -03:00 wall-clock time. This is consistent with `runs/run-log.txt:2` and with all 15 alignments.

No REV text derives during-analysis stability from the mid maps; the `git grep` in A13 finds only retention statements. A future "identical bytes at the named instants" statement (QUALITY #19, `corpus/QUALITY.md:29`) built on them would name pre-analysis instants for 9 runs.

### F3 — LOW (wording; arguable): "maps recomputed"
**Observation.** Three REV texts describe the validator as recomputing maps:

- `corpus/knowledge/2026-10-20-r18-swiss-map-replay.md:3` ("every retained mid-run map recomputed");
- `:68` ("22 mid-run maps recomputed");
- `LOG.md:2145` ("`receipt-validate.py` recomputes it").

The validator actually recomputes the map file's sha256, the `pins.compare(pins_pre, map)` verdict, the `entries` count and `taken_at_utc` (`receipt-validate.py:512-569`). A map is a past observation and cannot be recomputed.

QUALITY #21 (`corpus/QUALITY.md:31`) admits a validator exit 0 "only by the fields it recomputes". Suggested wording: "22 mid-map digests and verdicts recomputed".

Reproduce with `git show REV:corpus/knowledge/2026-10-20-r18-swiss-map-replay.md` (lines 3, 66-68) and `git show REV:.ufo/waves/round-17/tools/receipt-validate.py` (lines 512-569).

### F4 — INFO: the check record drops `pins.compare`'s `errors`
**Observation.**

- `pin_checks` keep only `{changed, entries, equal, map_path, map_sha256, missing, taken_at_utc}` (A7; `carrier-run.py:488-494`).
- The validator compares only `equal/changed/missing` (`receipt-validate.py:558`).
- An errored mid path would therefore surface only as `equal:false` with empty lists.
- No impact at REV: there are 0 errors in 22/22 maps (A2).

## Residual risk / verification gaps
- **Self-attestation.** `map_sha256` is computed by the writer itself (`carrier-run.py:504-512`). The maps and receipts land in a single commit: `git log REV -- .ufo/waves/round-18/runs` lists only `b2aad08` (13:38:07-03:00, about 6 min after the last run ended at 16:32:10Z; A14). A digest match proves file↔receipt consistency at REV, not run-time authenticity.
- **Hashing plausibility [INFERENCE].** The 45–53 ms from analyze start to mid-1 for 98–117 MB pinned implies at least 2.1 GB/s. Today `pins.snapshot` of kimi's 152 paths takes 60–64 ms under heavy concurrent load, and it still equals `pins_pre` (A15). These are the same order of magnitude, which is consistent with real re-hashing but not proof.
- **Continuity.** Continuity between instants is never evidenced (QUALITY #19). Map gaps are 30.076–30.136 s (`carrier-run.py:39` `PIN_CHECK_S = 30.0`). The largest map-free tail is 30.03 s (kimi). [INFERENCE] No check was dropped: each check taken is appended (`carrier-run.py:517`), and there is no `map_error`.
- **Not run (other seats' items):** `receipt-validate.py --selftest`, `carrier-run.py --selftest`, the r17 receipts.

## Housekeeping
Writes:

- this report;
- `/tmp/kr18w2-mmr-rv.json`, which held one superseded validator output and was deleted;
- the mkdtemp clone `/tmp/kr18w2-mmr-5Fz0yh`, with origin removed, which was deleted afterwards (`ls` reports it absent).

Lane status for `.ufo/waves/round-18/runs .ufo/waves/round-17/tools corpus LOG.md SCORECARD.md` was 0 lines after the work. No `jj`, no git writes in the lane, no REA/Ghidra runs, and no carrier executed.

Tools: preinstalled only. git 2.56.0, Python 3.14.8, GNU coreutils sha256sum 9.12, `/usr/bin/jq` 1.8.2, bubblewrap 0.13.1. No installs.

## Appendix — commands verbatim, with observed exit codes
LANE = `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Bash scripts ran as `/usr/bin/bash -c "$SCRIPT"`; Python programs ran as `python3 -I -B -c "$PROG"`.

**A0** prints `files=39 differ=0`, exit 0:
```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && n=0; bad=0; for f in .ufo/waves/round-17/tools/pins.py .ufo/waves/round-17/tools/receipt-validate.py .ufo/waves/round-18/runs/*/receipt.json .ufo/waves/round-18/runs/*/pins/mid-*.json; do n=$((n+1)); [ "$(git hash-object "$f")" = "$(git rev-parse "$REV:$f")" ] || { bad=$((bad+1)); echo "DIFF $f"; }; done; echo "files=$n differ=$bad"; [ $bad -eq 0 ]
```
Also run:

- `git -C LANE rev-parse HEAD refs/heads/main` (REV, REV; exit 0).
- `GIT_OPTIONAL_LOCKS=0 git -C LANE status --porcelain=v1 --untracked-files=all -- .ufo/waves/round-18/runs .ufo/waves/round-17/tools` (empty; exit 0).
- `git -C LANE ls-tree -r --name-only REV -- .ufo/waves/round-18/runs | python3 -I -B -c '…'` printed `248 tracked files; 15 receipts; 22 pins files` (exit 0 0).

**A1** prints `producer.json pins/carrier-run sha256 == REV blobs and branch_tip==eb6c266: 15/15`, exit 0:
```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && T=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-17/tools && P=$(git show $REV:.ufo/waves/round-17/tools/pins.py | /usr/bin/sha256sum | cut -d' ' -f1) && C=$(git show $REV:.ufo/waves/round-17/tools/carrier-run.py | /usr/bin/sha256sum | cut -d' ' -f1) && echo "REV pins.py sha256=$P carrier-run.py sha256=$C" && n=0; ok=0; for d in $(git ls-tree -d --name-only $REV .ufo/waves/round-18/runs/); do n=$((n+1)); r=$(git show $REV:$d/producer.json | /usr/bin/jq -r --arg p "$T/pins.py" --arg c "$T/carrier-run.py" '"\(.tool_sha256[$p]) \(.tool_sha256[$c]) \(.branch_tip)"'); [ "$r" = "$P $C eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0" ] && ok=$((ok+1)) || echo "MISMATCH $d $r"; done; echo "producer.json pins/carrier-run sha256 == REV blobs and branch_tip==eb6c266: $ok/$n"; [ $ok -eq $n ]; echo "exit=$?"
```
Also run: `cd LANE && F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 && REV=… && for f in pins.py carrier-run.py receipt-validate.py; do echo "$f F=$(git rev-parse $F:.ufo/waves/round-17/tools/$f) REV=$(git rev-parse $REV:.ufo/waves/round-17/tools/$f)"; done; git diff --stat $F $REV -- .ufo/waves/round-17/tools/; echo "diff_exit=$?"`. It printed equal blob ids at F and REV: `pins.py` 6568a49…, `carrier-run.py` 37961db…, `receipt-validate.py` bf04388…. The diff output was empty, with `diff_exit=0`.

**A2** reads REV objects only. It prints 22 rows, each `digest=match compare_exit=0 [equal,changed,missing,errors]=[true,0,0,0]`, then `TOTAL receipts=15 maps=22 digest_match=22 digest_mismatch=0 compare_exit0=22 compare_nonzero=0`. Exit 0.
```bash
set -u
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin || exit 2
REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94; LANE=$PWD; P=.ufo/waves/round-17/tools/pins.py
nr=0; nm=0; dok=0; dbad=0; c0=0; cbad=0
for R in $(git ls-tree -r --name-only $REV -- .ufo/waves/round-18/runs | LC_ALL=C sort | python3 -I -B -c 'import sys;[print(l.strip()) for l in sys.stdin if l.strip().endswith("/receipt.json")]'); do
  nr=$((nr+1))
  while read -r STEP M S; do
    nm=$((nm+1)); rel=${M#$LANE/}
    A=$(git show "$REV:$rel" | /usr/bin/sha256sum | cut -d' ' -f1)
    OUT=$(python3 -I -B <(git show $REV:$P) compare <(git show "$REV:$R" | /usr/bin/jq '.pins_pre') <(git show "$REV:$rel") 2>&1); E=$?
    EQ=$(printf '%s' "$OUT" | /usr/bin/jq -c '[.equal, (.changed|length), (.missing|length), (.errors|length)]' 2>/dev/null)
    if [ "$A" = "$S" ]; then dok=$((dok+1)); D=match; else dbad=$((dbad+1)); D=MISMATCH; fi
    if [ $E -eq 0 ]; then c0=$((c0+1)); else cbad=$((cbad+1)); fi
    echo "$(basename $(dirname $R)) $STEP $(basename $M) recorded=${S:0:12} recomputed=${A:0:12} digest=$D compare_exit=$E [equal,changed,missing,errors]=$EQ"
  done < <(git show "$REV:$R" | /usr/bin/jq -r '.steps | to_entries[] | .key as $k | .value.pin_checks[]? | "\($k) \(.map_path) \(.map_sha256)"')
done
echo "TOTAL receipts=$nr maps=$nm digest_match=$dok digest_mismatch=$dbad compare_exit0=$c0 compare_nonzero=$cbad"
[ $dbad -eq 0 ] && [ $cbad -eq 0 ] && [ $nm -gt 0 ]
```

**A3** uses the working tree and the recorded absolute paths. It prints `maps=22 digest_match=22 compare_exit0=22`, exit 0:
```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin || exit 2
P=.ufo/waves/round-17/tools/pins.py; nm=0; dok=0; c0=0
for R in .ufo/waves/round-18/runs/*/receipt.json; do
  while read -r M S; do nm=$((nm+1))
    [ "$(/usr/bin/sha256sum "$M" | cut -d' ' -f1)" = "$S" ] && dok=$((dok+1))
    python3 -I -B $P compare <(/usr/bin/jq '.pins_pre' "$R") "$M" >/dev/null 2>&1 && c0=$((c0+1))
  done < <(/usr/bin/jq -r '.steps[].pin_checks[]? | "\(.map_path) \(.map_sha256)"' "$R")
done
echo "maps=$nm digest_match=$dok compare_exit0=$c0"; [ $nm -eq $dok ] && [ $nm -eq $c0 ]
```

**A4** runs the depth checks. It prints `TOTALS {'receipts': 15, 'maps': 22, 'orphans': 0, 'unreferenced': 0, 'max_tail_s': 30.03} gap_min/max_s 30.076 30.136 n_gaps 7` and `FINDINGS []`. Exit 0.
```python
import json, subprocess, hashlib
from datetime import datetime
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; REV = "b2aad08ceeee8dd125ce0d316056d8bd766c7f94"
RUNS = ".ufo/waves/round-18/runs"
def show(p): return subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"], capture_output=True, check=True).stdout
def ts(s): return datetime.fromisoformat(s.replace("Z", "+00:00")).timestamp()
ns = {"__name__": "pins_at_rev"}; exec(compile(show(".ufo/waves/round-17/tools/pins.py"), "pins.py", "exec"), ns)
tree = subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only", REV, "--", RUNS], capture_output=True, text=True, check=True).stdout.split()
labels = sorted({p.split("/")[4] for p in tree if p.endswith("/receipt.json")})
bad = []; T = {"receipts": 0, "maps": 0, "orphans": 0, "unreferenced": 0, "max_tail_s": 0.0, "gaps": []}
for lab in labels:
    rc = json.loads(show(f"{RUNS}/{lab}/receipt.json")); T["receipts"] += 1
    pre, post = rc["pins_pre"], rc["pins_post"]
    chks = [(k, i, c) for k, s in rc["steps"].items() for i, c in enumerate(s.get("pin_checks") or [])]
    psteps = sorted({k for k, _, _ in chks})
    on_tree = sorted(p for p in tree if p.startswith(f"{RUNS}/{lab}/pins/"))
    ref = [c["map_path"][len(LANE) + 1:] for _, _, c in chks]
    if sorted(ref) != on_tree: bad.append((lab, "ref_vs_tree", ref, on_tree))
    exp_paths = [f"{LANE}/{RUNS}/{lab}/pins/mid-{n}.json" for n in range(1, len(chks) + 1)]
    if [c["map_path"] for _, _, c in chks] != exp_paths: bad.append((lab, "path_sequence"))
    a = rc["steps"]["analyze"]; st, en = ts(a["started_at_utc"]), ts(a["ended_at_utc"])
    if pre["entries"][rc["carrier"]["path"]]["sha256"] != rc["carrier"]["sha256_pre"]: bad.append((lab, "carrier_pre"))
    if not rc["pins_compare"]["equal"] or rc["mid_run_drift_steps"]: bad.append((lab, "prepost_or_drift"))
    so = json.loads(show(f"{RUNS}/{lab}/carrier-run.stdout"))
    if [c for s in so["steps"].values() for c in (s.get("pin_checks") or [])] != [c for _, _, c in chks]: bad.append((lab, "stdout_pin_checks_differ"))
    prev = None
    for k, i, c in chks:
        T["maps"] += 1
        b = show(c["map_path"][len(LANE) + 1:]); m = json.loads(b)
        if hashlib.sha256(b).hexdigest() != c["map_sha256"]: bad.append((lab, i, "digest"))
        if b != json.dumps(m, sort_keys=True, indent=2).encode() + b"\n": bad.append((lab, i, "not_writer_form"))
        if set(m) != {"entries", "monotonic_ns", "taken_at_utc"}: bad.append((lab, i, "keys", sorted(m)))
        if set(m["entries"]) != set(pre["entries"]): bad.append((lab, i, "entry_keys"))
        for p, e in m["entries"].items():
            q = pre["entries"][p]
            if (e.get("sha256"), e.get("size"), e.get("mtime_ns")) != (q.get("sha256"), q.get("size"), q.get("mtime_ns")): bad.append((lab, i, "entry_diff", p))
        cmp = ns["compare"](pre, m)
        for f in ("equal", "changed", "missing"):
            if c.get(f) != cmp[f]: bad.append((lab, i, "verdict", f))
        if c.get("entries") != len(m["entries"]) or c["entries"] != len(pre["entries"]): bad.append((lab, i, "entries"))
        if c.get("taken_at_utc") != m["taken_at_utc"]: bad.append((lab, i, "taken_at"))
        if not (pre["monotonic_ns"] < m["monotonic_ns"] < post["monotonic_ns"]): bad.append((lab, i, "monotonic_order"))
        if not (ts(pre["taken_at_utc"]) < ts(m["taken_at_utc"]) < ts(post["taken_at_utc"])): bad.append((lab, i, "utc_order"))
        if not (st <= ts(m["taken_at_utc"]) <= en): bad.append((lab, i, "outside_analyze"))
        if prev is not None: T["gaps"].append(round((m["monotonic_ns"] - prev) / 1e9, 3))
        prev = m["monotonic_ns"]; last = ts(m["taken_at_utc"])
        if c.get("map_error") or a.get("pins_changed_during_run"): bad.append((lab, i, "error_or_drift"))
    tail = round(en - last, 3); T["max_tail_s"] = max(T["max_tail_s"], tail)
    print(f"{lab}: steps={sorted(rc['steps'])} pin_check_steps={psteps} maps={len(chks)} tree_pins={len(on_tree)} pinned={len(pre['entries'])} analyze_s={en-st:.1f} first_after_start_s={ts(json.loads(show(ref[0]))['taken_at_utc'])-st:.2f} tail_s={tail}")
print("pinned paths (last receipt):", sorted(pre["entries"]))
print("TOTALS", {k: v for k, v in T.items() if k != "gaps"}, "gap_min/max_s", min(T["gaps"]), max(T["gaps"]), "n_gaps", len(T["gaps"]))
print("FINDINGS", bad)
raise SystemExit(1 if bad else 0)
```

**A5** red controls, using in-memory streams only:
- The reformatted map fails to match its digest. It printed `reformatted=0ec4f482… recorded=6b4957f9…`, exit **1**:
  `cd LANE && REV=… && M=.ufo/waves/round-18/runs/real-kimi-webbridge/pins/mid-1.json && A=$(git show $REV:$M | /usr/bin/jq -c . | /usr/bin/sha256sum | cut -d' ' -f1) && S=$(git show $REV:.ufo/waves/round-18/runs/real-kimi-webbridge/receipt.json | /usr/bin/jq -r '.steps.analyze.pin_checks[0].map_sha256') && echo "reformatted=$A recorded=$S" && [ "$A" = "$S" ]`
- A flipped carrier sha in `pins_pre` gives pins.py exit **1**, `{"equal":false,"changed":["/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge"]}`:
  `cd LANE && REV=… && R=.ufo/waves/round-18/runs/real-kimi-webbridge && python3 -I -B .ufo/waves/round-17/tools/pins.py compare <(git show $REV:$R/receipt.json | /usr/bin/jq '.pins_pre | .entries["/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge"].sha256 = ("0"*64)') <(git show $REV:$R/pins/mid-1.json) | /usr/bin/jq -c '{equal,changed}'; exit ${PIPESTATUS[0]}`
- A dropped map entry gives exit **1**, `{"equal":false,"missing":[…kimi-webbridge]}`. This is the same command with `/usr/bin/jq '.pins_pre'` and the map stream piped through `/usr/bin/jq 'del(.entries["/home/vgpnk/.kimi-webbridge/bin/kimi-webbridge"])'`.
- The unmodified control gives exit 0, `{"equal":true,"changed":[],"missing":[],"errors":[]}`.
- The first attempt at the two compare reds lacked `PIPESTATUS`, so it reported jq's exit 0. It was rerun as shown above.

**A6** validator corroboration:

- `cd LANE && python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps .ufo/waves/round-18/runs/*/receipt.json | /usr/bin/jq -c '{exit, counts, require_mid_maps, n: (.receipts|length), r0keys: (.receipts[0]|keys)}'; exit ${PIPESTATUS[0]}` gave exit 0, `counts {invalid:0, receipts:15, unreadable:0, valid:15}`.
- The per-receipt loop gave exit 0 and `exit0=15/15`:
  `n=0; z=0; for R in .ufo/waves/round-18/runs/*/receipt.json; do n=$((n+1)); python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps "$R" >/dev/null 2>&1; e=$?; [ $e -eq 0 ] && z=$((z+1)) || echo "$R exit=$e"; done; echo "receipt-validate --require-mid-maps per-receipt exit0=$z/$n"; [ $z -eq $n ]`

**A7** prints `22 ["changed","entries","equal","map_path","map_sha256","missing","taken_at_utc"]`, exit 0 0 0:
`cd LANE && REV=… && for d in $(git ls-tree -d --name-only $REV .ufo/waves/round-18/runs/); do git show $REV:$d/receipt.json | /usr/bin/jq -c '.steps.analyze.pin_checks[] | keys'; done | LC_ALL=C sort | uniq -c`

**A8** prints `lane-internal pinned (path,sha256) pairs: 22; equal to blob at eb6c266 and at REV: 22`, exit 0:
```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && F=eb6c2668e5cb7054fd1e16d2f615cb65586d0fe0 && REV=b2aad08ceeee8dd125ce0d316056d8bd766c7f94 && L=$PWD && n=0; ok=0; for d in $(git ls-tree -d --name-only $REV .ufo/waves/round-18/runs/); do git show $REV:$d/receipt.json | /usr/bin/jq -r --arg L "$L/" '.pins_pre.entries | to_entries[] | select(.key | startswith($L)) | "\(.key) \(.value.sha256)"'; done | LC_ALL=C sort -u | { while read -r p s; do n=$((n+1)); rel=${p#$L/}; a=$(git show $F:$rel | /usr/bin/sha256sum | cut -d' ' -f1); b=$(git show $REV:$rel | /usr/bin/sha256sum | cut -d' ' -f1); if [ "$a" = "$s" ] && [ "$b" = "$s" ]; then ok=$((ok+1)); else echo "DIFF $rel pinned=${s:0:12} F=${a:0:12} REV=${b:0:12}"; fi; done; echo "lane-internal pinned (path,sha256) pairs: $n; equal to blob at eb6c266 and at REV: $ok"; [ $ok -eq $n ]; }; echo "exit=$?"
```
A companion `jq … | python3 -I -B -c` grouping (exit 0 0) found 150 common non-carrier paths plus 1 label-specific `predictions/<label>.prediction.json` per receipt.

**A9** sets up the clone (exit 0, origin count 0, HEAD = REV):
`D=$(mktemp -d /tmp/kr18w2-mmr-XXXXXX) && echo "D=$D" && git clone -q --no-local /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$D/c" && git -C "$D/c" remote remove origin && git -C "$D/c" remote -v | wc -l && git -C "$D/c" rev-parse HEAD && echo "clone_exit=0"`

It created D=/tmp/kr18w2-mmr-5Fz0yh. The F1 demo then ran as follows. The script exit was 0. The step exits were step2_exit=**0**, with `{"exit":0,"counts":{…"valid":1},"codes":[]}`; step3_exit=**0**; and step4_exit=**1**, with `"codes":["mid_map_sha256_mismatch","sha256_mismatch"]`. The clone map was `6e048012…`; the recorded value is `6b4957f9…`.
```bash
set -u
D=/tmp/kr18w2-mmr-5Fz0yh; C=$D/c; R=.ufo/waves/round-18/runs/real-kimi-webbridge; LANE=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
cd "$C" || exit 2
printf ' ' >> $R/pins/mid-1.json
echo "clone map sha256 = $(/usr/bin/sha256sum $R/pins/mid-1.json | cut -d' ' -f1)"
echo "recorded map_sha256 = $(/usr/bin/jq -r '.steps.analyze.pin_checks[0].map_sha256' $R/receipt.json)"
echo "recorded map_path = $(/usr/bin/jq -r '.steps.analyze.pin_checks[0].map_path' $R/receipt.json)"
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $R/receipt.json | /usr/bin/jq -c '{exit, counts, codes: [.receipts[].findings[]?.code]}'; echo "step2_exit=${PIPESTATUS[0]}"
python3 -I -B .ufo/waves/round-17/tools/pins.py compare <(/usr/bin/jq '.pins_pre' $R/receipt.json) "$(/usr/bin/jq -r '.steps.analyze.pin_checks[0].map_path' $R/receipt.json)" >/dev/null 2>&1; echo "step3_exit=$?"
/usr/bin/jq --arg L "$LANE" --arg C "$C" '(.steps.analyze.pin_checks[].map_path) |= sub("^" + $L; $C)' $R/receipt.json > $D/receipt.relocated.json
python3 -I -B .ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $D/receipt.relocated.json | /usr/bin/jq -c '{exit, counts, codes: [.receipts[].findings[]?.code]}'; echo "step4_exit=${PIPESTATUS[0]}"
```
(Each `echo "-- stepN …"` banner line of the run is omitted above.)

**A10** hides the lane path. It printed `lane hidden in this namespace`, then `{"exit":1,"counts":{"invalid":15,"receipts":15,"unreadable":0,"valid":0},"mid_codes":{"mid_map_missing":22},"all_codes":{"binding_mismatch":15,"mid_map_missing":22,"missing_file":262}}`, `validator_exit=1` and `bwrap_exit=0`:
```bash
set -u
C=/tmp/kr18w2-mmr-5Fz0yh/c
bwrap --dev-bind / / --tmpfs /home/vgpnk/Projects/shokunin/kaidoku-shokunin -- /usr/bin/bash -c '
  C=/tmp/kr18w2-mmr-5Fz0yh/c
  [ -e /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo ] && echo "lane visible" || echo "lane hidden in this namespace"
  python3 -I -B $C/.ufo/waves/round-17/tools/receipt-validate.py --require-mid-maps $C/.ufo/waves/round-18/runs/*/receipt.json | /usr/bin/jq -c "{exit, counts, mid_codes: ([.receipts[].findings[]? | select(.code|startswith(\"mid_\")) | .code] | group_by(.) | map({(.[0]): length}) | add), all_codes: ([.receipts[].findings[]?.code] | group_by(.) | map({(.[0]): length}) | add)}"
  echo "validator_exit=${PIPESTATUS[0]}"
'
echo "bwrap_exit=$?"
```
Cleanup: `rm -rf /tmp/kr18w2-mmr-5Fz0yh && ls -d /tmp/kr18w2-mmr-*` reported "No such file or directory".

**A11** compares mid instants with the Ghidra log window. It printed `TOTAL mids before ghidra window: 15 inside: 7 after: 0` and `labels with no mid map inside the ghidra.log window: 9 [s1246-noswiss-methods, s1246-noswiss-nomethods, s1246-swiss-methods, s1246-swiss-nethttp, s1246-swiss-nomethods, s1250-noswiss-methods, s1250-noswiss-nomethods, s1250-swiss-methods, s1250-swiss-nomethods]`. Exit 0.
```python
import json, subprocess, re
from datetime import datetime, timedelta, timezone
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; REV = "b2aad08ceeee8dd125ce0d316056d8bd766c7f94"; RUNS = ".ufo/waves/round-18/runs"
def show(p): return subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"], capture_output=True, check=True).stdout
tree = subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only", REV, "--", RUNS], capture_output=True, text=True, check=True).stdout.split()
TZ = timezone(timedelta(hours=-3))  # INFERENCE: ghidra.log local time = lane offset -03:00
tot_in = tot_before = tot_after = 0; single_none = []
for lab in sorted({p.split("/")[4] for p in tree if p.endswith("/receipt.json")}):
    rc = json.loads(show(f"{RUNS}/{lab}/receipt.json"))
    mids = [datetime.fromisoformat(c["taken_at_utc"]) for c in rc["steps"]["analyze"]["pin_checks"]]
    logs = [p for p in tree if p.startswith(f"{RUNS}/{lab}/logs/") and p.endswith("/ghidra.log")]
    stamps = []
    for g in logs:
        for l in show(g).decode("utf-8", "replace").splitlines():
            m = re.match(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d) ", l)
            if m: stamps.append(datetime.strptime(m.group(1), "%Y-%m-%d %H:%M:%S").replace(tzinfo=TZ))
    lo, hi = min(stamps), max(stamps) + timedelta(seconds=1)  # second resolution: window [first, last+1s)
    before = sum(t < lo for t in mids); inside = sum(lo <= t < hi for t in mids); after = sum(t >= hi for t in mids)
    tot_in += inside; tot_before += before; tot_after += after
    if inside == 0: single_none.append(lab)
    print(f"{lab}: logs={len(logs)} ghidra_window_utc={lo.astimezone(timezone.utc).time()}..{hi.astimezone(timezone.utc).time()} mids={len(mids)} before={before} inside={inside} after={after} first_mid_lead_s={(lo - mids[0]).total_seconds():.3f}")
print("TOTAL mids before ghidra window:", tot_before, "inside:", tot_in, "after:", tot_after)
print("labels with no mid map inside the ghidra.log window:", len(single_none), single_none)
```

**A12** checks clock consistency and the start-to-mid-1 timing. Per label it printed `start_to_mid1_s` 0.045–0.053 for 98,605,533–117,092,834 pinned bytes, then `max |d(utc)-d(monotonic)| across pre->mid*->post pairs = 0.006 ms`. Exit 0.
```python
import json, subprocess
from datetime import datetime
LANE = "/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; REV = "b2aad08ceeee8dd125ce0d316056d8bd766c7f94"; RUNS = ".ufo/waves/round-18/runs"
def show(p): return subprocess.run(["git", "-C", LANE, "show", f"{REV}:{p}"], capture_output=True, check=True).stdout
tree = subprocess.run(["git", "-C", LANE, "ls-tree", "-r", "--name-only", REV, "--", RUNS], capture_output=True, text=True, check=True).stdout.split()
worst = 0.0; rows = []
for lab in sorted({p.split("/")[4] for p in tree if p.endswith("/receipt.json")}):
    rc = json.loads(show(f"{RUNS}/{lab}/receipt.json"))
    snaps = [rc["pins_pre"]] + [json.loads(show(c["map_path"][len(LANE)+1:])) for c in rc["steps"]["analyze"]["pin_checks"]] + [rc["pins_post"]]
    for a, b in zip(snaps, snaps[1:]):
        du = (datetime.fromisoformat(b["taken_at_utc"]) - datetime.fromisoformat(a["taken_at_utc"])).total_seconds()
        dm = (b["monotonic_ns"] - a["monotonic_ns"]) / 1e9
        worst = max(worst, abs(du - dm))
    tot = sum(e["size"] for e in rc["pins_pre"]["entries"].values())
    car = rc["pins_pre"]["entries"][rc["carrier"]["path"]]["size"]
    lead = (datetime.fromisoformat(snaps[1]["taken_at_utc"]) - datetime.fromisoformat(rc["steps"]["analyze"]["started_at_utc"])).total_seconds()
    rows.append((lab, car, tot, lead, tot / lead / 1e9))
for r in rows: print(f"{r[0]}: carrier_bytes={r[1]} pinned_bytes_total={r[2]} start_to_mid1_s={r[3]:.3f} implied_min_hash_GBps={r[4]:.2f}")
print(f"max |d(utc)-d(monotonic)| across pre->mid*->post pairs = {worst*1000:.3f} ms")
```

**A13** searches for claims (exit 0 for both commands); only retention statements are present:

- `git -C LANE grep -n -i -E 'pin|instant|unchanged|identical bytes|stable' REV -- corpus/knowledge/2026-10-20-r18-swiss-map-replay.md corpus/lessons/round-18.md .ufo/waves/round-18/runs/run-log.txt | cut -c1-400; echo "exit=${PIPESTATUS[0]}"`
- The same pattern over `SCORECARD.md LOG.md`, filtered to SCORECARD lines ≥2400 and LOG lines ≥2110 via `python3 -I -B -c` (exit 0 0).
  - Round-18 hits: `LOG.md:2125,2131,2143,2149,2165` and `SCORECARD.md:2428,2438`. These are revision-pin (C2) wording, "byte-identical" r17 outputs, the registry row and the R17-PINMAP correction; none states stability during a run.
  - The other hits are r17-section lines: `LOG.md:2113,2114,2122` and `SCORECARD.md:2400,2403,2408`.

**A14:** `git -C LANE log --format='%H %cI %s' REV -- .ufo/waves/round-18/runs` printed one line, `b2aad08… 2026-10-20T13:38:07-03:00 round-18: carrier runs, …`. Exit 0.

**A15** re-snapshots kimi's pinned paths today (read-only). It printed `pass1 … 63.7 ms; now-vs-pins_pre equal=True changed=0 missing=0 errors=0`, then pass2 60.3 ms and pass3 60.1 ms, both equal=True. `exit=0`.
```bash
cd /home/vgpnk/Projects/shokunin/kaidoku-shokunin && git show b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-18/runs/real-kimi-webbridge/receipt.json | python3 -I -B -c '
import json, sys, subprocess, time
rc = json.load(sys.stdin)
ns = {"__name__": "pins_at_rev"}
exec(compile(subprocess.run(["git","show","b2aad08ceeee8dd125ce0d316056d8bd766c7f94:.ufo/waves/round-17/tools/pins.py"],capture_output=True,check=True).stdout,"pins.py","exec"), ns)
paths = list(rc["pins_pre"]["entries"])
for i in range(3):
    t = time.perf_counter(); s = ns["snapshot"](paths); dt = time.perf_counter() - t
    c = ns["compare"](rc["pins_pre"], s)
    print(f"pass{i+1}: snapshot of {len(paths)} pinned paths took {dt*1000:.1f} ms; now-vs-pins_pre equal={c["equal"]} changed={len(c["changed"])} missing={len(c["missing"])} errors={len(c["errors"])}")
'; echo "exit=${PIPESTATUS[1]}"
```
(The first attempt of A15 used `\"` inside an f-string and failed with a SyntaxError, exit 1. It was rerun as shown.)
