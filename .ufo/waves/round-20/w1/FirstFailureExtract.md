# First-failure extractor (C3)

Axes: calibration, coverage, depth. **Observation:** added `.ufo/waves/round-20/tools/first-failure-extract.py`; it preserves the C3 `first_failure` shape (`kind/index/va/phase`), reports the Go failure summary line separately from its cause line, bounds null/absence with `last_line`, and keeps every other structured `ERROR` record in `other_errors`. See tool `.ufo/waves/round-20/tools/first-failure-extract.py:36-39,84-131,134-195`; the `last_line` bound is computed at `:142-149`; C3 shape is specified at `.ufo/waves/round-20/contract.md:76-81`.

**Synthetic selftest:** command `python3 -I -B /tmp/kr20-FirstFailureExtract-2/.ufo/waves/round-20/tools/first-failure-extract.py --selftest` → exact final line `SELFTEST: CLEAN cases=4`; exit 0. Cases and stable ids are in tool `:199-293`.

**Observed log sweep:** 30 logs (16 round-19, including pass2; 14 round-18), all emitted. `other_errors` is the count of retained ERROR records, not only NPEs. `none through N` means no qualifying Go failure through the final scanned line N.

| label | first failure | summary line | cause line | last line | other_errors |
|---|---|---:|---:|---:|---:|
| r19/t1250-asm | none through 227 | — | — | 227 | 0 |
| r19/t1250-cgo | none through 180 | — | — | 180 | 0 |
| r19/t1250-compile | none through 432 | — | — | 432 | 1 |
| r19/t1250-cover | none through 250 | — | — | 250 | 0 |
| r19/t1250-go | none through 576 | — | — | 576 | 0 |
| r19/t1250-gofmt | none through 182 | — | — | 182 | 0 |
| r19/t1250-preprofile | none through 163 | — | — | 163 | 0 |
| r19/t1250-vet | invalid_index, index=13902080, phase=markup | 186 | 229 | 282 | 0 |
| r19/pass2/t1250-asm | none through 227 | — | — | 227 | 0 |
| r19/pass2/t1250-cgo | none through 180 | — | — | 180 | 0 |
| r19/pass2/t1250-compile | none through 432 | — | — | 432 | 1 |
| r19/pass2/t1250-cover | none through 250 | — | — | 250 | 0 |
| r19/pass2/t1250-go | none through 576 | — | — | 576 | 0 |
| r19/pass2/t1250-gofmt | none through 182 | — | — | 182 | 0 |
| r19/pass2/t1250-preprofile | none through 163 | — | — | 163 | 0 |
| r19/pass2/t1250-vet | invalid_index, index=13902080, phase=markup | 186 | 229 | 282 | 0 |
| r18/calib-aether | eof, index=17645861, phase=markup | 97 | 177 | 244 | 6 |
| r18/calib-notesmd-cli | none through 127 | — | — | 127 | 0 |
| r18/real-kimi-webbridge | invalid_index, index=15606016, phase=markup | 73 | 206 | 263 | 3 |
| r18/s1246-noswiss-methods | none through 5721 | — | — | 5721 | 5495 |
| r18/s1246-noswiss-nethttp | none through 10242 | — | — | 10242 | 9843 |
| r18/s1246-noswiss-nomethods | none through 5723 | — | — | 5723 | 5495 |
| r18/s1246-swiss-methods | none through 5828 | — | — | 5828 | 5601 |
| r18/s1246-swiss-nethttp | invalid_index, index=22386945, phase=markup | 408 | 451 | 504 | 64 |
| r18/s1246-swiss-nomethods | none through 5829 | — | — | 5829 | 5601 |
| r18/s1250-noswiss-methods | none through 5937 | — | — | 5937 | 5705 |
| r18/s1250-noswiss-nethttp | none through 10516 | — | — | 10516 | 10113 |
| r18/s1250-noswiss-nomethods | none through 5937 | — | — | 5937 | 5705 |
| r18/s1250-swiss-methods | none through 6051 | — | — | 6051 | 5821 |
| r18/s1250-swiss-nethttp | none through 10651 | — | — | 10651 | 10250 |
| r18/s1250-swiss-nomethods | none through 6052 | — | — | 6052 | 5821 |

Evidence anchors: the round-19 vet summary/cause are at `.ufo/waves/round-19/runs/t1250-vet/logs/rea-ghidra-CSKBVG/ghidra.log:186,229` and pass2 at `.ufo/waves/round-19/runs/pass2/t1250-vet/logs/rea-ghidra-PEkTou/ghidra.log:186,229`. Round-18 EOF is `.ufo/waves/round-18/runs/calib-aether/logs/rea-ghidra-HtDopV/ghidra.log:97,177`; invalid-index examples are `.ufo/waves/round-18/runs/real-kimi-webbridge/logs/rea-ghidra-ZSUHpG/ghidra.log:73,206` and `.ufo/waves/round-18/runs/s1246-swiss-nethttp/logs/rea-ghidra-zHRS1l/ghidra.log:408,451`. The deferred `AnalysisTaskWrapper` NPE remains a separate `other_errors` record (one per compile log), observed at `.ufo/waves/round-19/runs/t1250-compile/logs/rea-ghidra-uEQQSP/ghidra.log:347` and `.ufo/waves/round-19/runs/pass2/t1250-compile/logs/rea-ghidra-07WMDZ/ghidra.log:347`.

**Commands and exits** (no tools installed):

- `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin /tmp/kr20-FirstFailureExtract-2 && git -C /tmp/kr20-FirstFailureExtract-2 checkout -q --detach 14f0260ad319ecc26994381b2415d5a999003375 && git -C /tmp/kr20-FirstFailureExtract-2 rev-parse HEAD` — exit 0; observed base `14f0260ad319ecc26994381b2415d5a999003375`.
- `mkdir -p /tmp/kr20-FirstFailureExtract-2/.ufo/waves/round-20/tools` — exit 0.
- `command -v jq && jq --version` — exit 0; output `jq`, `jaq 3.1.1`.
- `python3 -I -B /tmp/kr20-FirstFailureExtract-2/.ufo/waves/round-20/tools/first-failure-extract.py --selftest` — exit 0; final line `SELFTEST: CLEAN cases=4`.
- Log-sweep command — exit 0; output is the 30-row table above:

```sh
set -o pipefail; shopt -s nullglob; tool=/tmp/kr20-FirstFailureExtract-2/.ufo/waves/round-20/tools/first-failure-extract.py; r19=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-19; r18=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-18; printf 'LABEL\tKIND\tINDEX\tPHASE\tFAILURE_LINE\tCAUSE_LINE\tLAST_LINE\tOTHER_ERRORS\n'; for f in "$r19"/runs/*/logs/*/ghidra.log "$r19"/runs/pass2/*/logs/*/ghidra.log "$r18"/runs/*/logs/*/ghidra.log; do case "$f" in "$r18"/*) rel=${f#"$r18"/runs/}; label="r18/${rel%/logs/*/ghidra.log}" ;; *) rel=${f#"$r19"/runs/}; label="r19/${rel%/logs/*/ghidra.log}" ;; esac; printf '%s\t' "$label"; python3 -I -B "$tool" "$f" | jq -r '[.first_failure.kind // "none", (.first_failure.index | if . == null then "-" else tostring end), (.first_failure.phase // "-"), (.first_failure_line | if . == null then "-" else tostring end), (.cause_line | if . == null then "-" else tostring end), (.last_line | tostring), (.other_errors | length | tostring)] | @tsv'; done
```

- `mkdir -p /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches` — exit 0.
- `git -C /tmp/kr20-FirstFailureExtract-2 add -A` — exit 0.
- `git -C /tmp/kr20-FirstFailureExtract-2 diff --cached --stat 14f0260ad319ecc26994381b2415d5a999003375` — exit 0; `.ufo/waves/round-20/tools/first-failure-extract.py | 316 +++++++++++++++++++++` (1 file changed, 316 insertions).
- `git -C /tmp/kr20-FirstFailureExtract-2 diff --cached --binary 14f0260ad319ecc26994381b2415d5a999003375 > /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/w1/patches/FirstFailureExtract-2.patch` — exit 0.

**Risk/blocker:** input-to-run/carrier binding is assumed from the supplied log path, not independently authenticated here. `va` is null because the relevant log records expose an index/EOF pair rather than a VA; phase is taken from visible stack frames where possible. No blocker.
