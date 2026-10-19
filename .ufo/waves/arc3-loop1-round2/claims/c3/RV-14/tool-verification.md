# RV-14 — independent tool-side verification of `.ufo/gates/custody-pair/`

Seat RV-14, chain c3, reviewer. This is the pre-row half of the review: every
behaviour the registry row may claim must exist in the actual tool, so the
tool's surface is measured here independently of any row text.

Tool under test: `.ufo/gates/custody-pair/custody-pair.py`, 883→887 lines,
sha256 `112d01dc034c2d54324e7703e2d03d1d83b0c3930ed5d4f688546968b73ecefa`
(stable across the whole battery; the file was still being revised earlier —
`4862f642…` → `b10ad1c8…` → `112d01dc…` — so every measurement below is pinned
to `112d01dc…`). `README.md` landed mid-wave; `__pycache__/` present (write-scope
note below).

Battery: `independent-battery.sh`, output `receipts/independent-battery.out`
(self-sha256 `0b9a774d…`); extra edges in `receipts/` and `/var/tmp/rv14/battery/`.
Every command below was run by this seat; nothing is quoted from EX-31's outputs.

| # | Claim tested | Command | Result |
|---|---|---|---|
| 1 | fixture selftest passes | `python3 custody-pair.py selftest --scratch /var/tmp/rv14/selftest-scratch` | `CLEAN cases=15 passed=15 failed=0 exit=0` (rc 0) |
| 2 | live capture is read-only, 5/5, exit 0 | `... capture --out -` | 5 stanzas, `paths=5/5 exit=0` |
| 3 | sha256 fields match independent ground truth | `os.lstat` + `hashlib.sha256` vs receipt stanzas | all 5 agree (sha256, size, mode, uid, gid, inode, mtime/ctime epoch+ns) |
| 4 | UTC render is correct and TZ-independent | `TZ=UTC / UTC+5 / UTC-3 ... capture --paths ~/.profile` | `MTIME_UTC_RENDER: 2026-10-15T06:12:07Z` identical under all three TZs; local render moves (`+00:00`, `-05:00`, `+03:00`) |
| 5 | label defect reported when a v1 receipt carries it | `verify <round-1>/config-pre-pair.txt --live` | rc 12; 5× `LABEL-DEFECT ... localtime(epoch …); gmtime(epoch) is …`; `SHA256-CONTRACT: 5/5` |
| 6 | pipe-v1 shape handled the same way | `verify <round-1>/config-pre-pair-metadata.txt --live` | rc 12; 10× LABEL-DEFECT (mtime+ctime per path); `SHA256-CONTRACT: 5/5` |
| 7 | same-content in-place rewrite detected | synthetic fixture, bytes rewritten in place, mtime restored, `verify --live` | rc 11 `REWRITE-DRIFT ... moved=ctime_ns`, sha256 unchanged |
| 8 | rename-based rewrite detected | selftest case 3 (`same-content-rewrite-rename-inode-pin`) | PASS (inode moves) |
| 9 | absent path → exit 13, receipt still written | `capture --paths <missing>` | `PARTIAL paths=0/1 exit=13`, receipt + sidecar written |
| 10 | extra-path class | `verify present-rec absent-rec` | `METADATA-DRIFT ... moved=EXTRA-PATH`, overall `ABSENT exit=13` (severity precedence holds) |
| 11 | usage errors → exit 2 | no subcommand; `verify` with no operand | rc 2 both |
| 12 | write-guard refuses a receipt over a custody path | `HOME=<sandbox> ... capture --out <sandbox>/.bashrc` | rc 2, `USAGE: refusing to write a receipt over a custody path`, sandbox file unchanged |
| 13 | round-trip idempotence | own capture → `verify --live` ×2 | `MATCH paths=5/5 exit=0` both times |
| 14 | the round's own live pair verifies | `verify EX-31/capture-pre.txt EX-31/capture-post.txt` | `MATCH paths=5/5 drift=0 exit=0`; capture-pre self-hash `3f3db73e…` reproduces EX-31's recorded digest |

Declared exit map (source, `custody-pair.py:119-134`): 0 MATCH, 10 CONTENT-DRIFT,
11 REWRITE-DRIFT, 12 METADATA-DRIFT (incl. EXTRA-PATH, LABEL-DEFECT), 13 ABSENT,
2 USAGE, 3 SELFTEST-FAIL; severity CONTENT-DRIFT > ABSENT > REWRITE-DRIFT >
METADATA-DRIFT > MATCH. Every class above was exercised except CONTENT-DRIFT
(selftest case 4 covers it; my run of case 4 passed inside the 15/15).

## Notes for the row review (to be confronted with EX-36's text)

- **v1 compatibility has two outcomes, not one.** sha256 is the contract and is
  reported (`SHA256-CONTRACT: 5/5`) for every v1 shape; but a *real* round-1
  stanza/pipe receipt still exits **12**, not 0, because it carries the very
  label defect this tool reports. Only sums-v1 (`sha256sum` output) exits 0
  (`MATCH-V1-PARTIAL`). A row sentence like "v1 receipts remain verifiable"
  without this split would be a row-vs-tool mismatch.
- **Exit map is non-standard for a gate** (10–13, not 0/1/2). A row must state
  the real map or say nothing.
- **Write scope, measured:** normal capture writes only `--out` + `<out>.sha256`;
  selftest writes only under `--scratch` (or `$CUSTODY_PAIR_SCRATCH`/`/dev/shm`/
  `/var/tmp`); `__pycache__/custody-pair.cpython-314.pyc` exists inside the tool
  directory (created by whoever *imported* it as a module, not by `python3
  custody-pair.py` runs — my runs did not touch it), which is the one residue a
  "writes only its receipt" claim would have to blacklist.
- **Risk note (not a defect):** the selftest's guard case (`refuses-to-write-
  over-custody-path`) attempts a capture whose `--out` is the *real* `~/.bashrc`
  and relies on the refusal branch; if that branch ever regressed, the selftest
  itself would overwrite a custody path. My re-run of the same semantics used a
  sandboxed `HOME`, so the refusal is verified without that exposure.
- **Tool churn:** the row must name the revision it describes; the tool changed
  three times in ~3 minutes (`4862f642…` → `b10ad1c8…` → `112d01dc…`). Any row
  sentence describing a feature that only existed in an earlier revision would
  be a stale-identity defect (C1's rule applied to C3).
