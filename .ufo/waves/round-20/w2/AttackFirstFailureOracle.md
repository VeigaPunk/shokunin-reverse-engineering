HOLDS — C3 first-failure observations agree with the captured Ghidra logs for all 19 labels, at the declared kind/index-or-silence granularity.

## Evidence

Observed from the Git tree at S (`5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9`), not the working tree. The line-number search over all 19 `runs/**/ghidra.log` files found eight first `Go analysis failure` entries, each followed by `Caused by: java.io.EOFException: Invalid index: N`; no `Failed to read Go info` entry occurred. The other 11 logs had no matching Go failure/cause text. Their comparison observations are `null` (extractor documentation says null means no qualifying failure through `last_line`, not proof that analysis succeeded: `tools/first-failure-extract.py:4-8`).

All paths below are relative to `.ufo/waves/round-20/`. `runs/` log anchors give the first failure line and its cause line; `evidence/compare-rerun/<label>.json:1` gives the recorded observed object and `match` result.

| Label | Ghidra log: first failure / cause | Log-derived observation | Recorded observed object |
|---|---|---|---|
| t1246-addr2line | `runs/t1246-addr2line/logs/rea-ghidra-P9tyVR/ghidra.log:112,186` | `EOFException: Invalid index: 22078465` | `invalid_index / 22078465`; match=true |
| t1246-asm | `runs/t1246-asm/logs/rea-ghidra-15p1Vy/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-buildid | `runs/t1246-buildid/logs/rea-ghidra-qGQ7Im/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-cgo | `runs/t1246-cgo/logs/rea-ghidra-I0zRdH/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-compile | `runs/t1246-compile/logs/rea-ghidra-Q6goA3/ghidra.log:332,384` | `EOFException: Invalid index: 36421889` | `invalid_index / 36421889`; match=true |
| t1246-covdata | `runs/t1246-covdata/logs/rea-ghidra-314Y9f/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-cover | `runs/t1246-cover/logs/rea-ghidra-mFkiDF/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-doc | `runs/t1246-doc/logs/rea-ghidra-wQaOa9/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-fix | `runs/t1246-fix/logs/rea-ghidra-Zvh0Na/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-go | `runs/t1246-go/logs/rea-ghidra-2PFXTv/ghidra.log:527,593` | `EOFException: Invalid index: 35082496` | `invalid_index / 35082496`; match=true |
| t1246-gofmt | `runs/t1246-gofmt/logs/rea-ghidra-jjj6WB/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-nm | `runs/t1246-nm/logs/rea-ghidra-xpz849/ghidra.log:121,195` | `EOFException: Invalid index: 22070273` | `invalid_index / 22070273`; match=true |
| t1246-objdump | `runs/t1246-objdump/logs/rea-ghidra-uLjgCv/ghidra.log:122,196` | `EOFException: Invalid index: 13816064` | `invalid_index / 13816064`; match=true |
| t1246-pack | `runs/t1246-pack/logs/rea-ghidra-Dhu23X/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-pprof | `runs/t1246-pprof/logs/rea-ghidra-hCPl3X/ghidra.log:381,472` | `EOFException: Invalid index: 27091201` | `invalid_index / 27091201`; match=true |
| t1246-preprofile | `runs/t1246-preprofile/logs/rea-ghidra-JcCFCG/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-test2json | `runs/t1246-test2json/logs/rea-ghidra-tU5R8R/ghidra.log` — no matching line | no qualifying failure | null; match=true |
| t1246-trace | `runs/t1246-trace/logs/rea-ghidra-Vwh31x/ghidra.log:502,577` | `EOFException: Invalid index: 25696001` | `invalid_index / 25696001`; match=true |
| t1246-vet | `runs/t1246-vet/logs/rea-ghidra-AW49O8/ghidra.log:187,230` | `EOFException: Invalid index: 13791488` | `invalid_index / 13791488`; match=true |

The 19 line-numbered entries in `evidence/compare-rerun/summary.txt:1-19` each report comparator `exit=0` and `logsha_ok=y`. The eight error observations and eleven null observations agree with the direct log search. The comparator contract is specifically both-null or equal `kind` and `index`; it ignores `va` and `phase` (`tools/compare-first-failure.py:28-34`). Thus this supports 19/19 at the C3 claimed granularity, not equality of every object field.

## Artifact-path caveat

The requested `runs/<label>/compare-ff.json` files do not exist in the S tree. Instead, all 19 `runs/<label>/compare.json` records contain `prediction: missing first_failure.h1` with null observed values (e.g. `runs/t1246-addr2line/compare.json:1`; grep found this for all labels). S's `measure.py:38-41` explicitly says the in-run input was wrong and that `evidence/compare-rerun/<label>.json` supersedes those files when present. I used those rerun records above; treating the stale `runs/*/compare.json` files as the comparison would be a false falsification.

## Commands and limits

- Read-only revision snapshot: `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 .ufo/waves/round-20/runs .ufo/waves/round-20/tools | tar -x -C /tmp/kaidoku-r20-firstfailure.jmBoPb`; and `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin archive 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 .ufo/waves/round-20/evidence/compare-rerun .ufo/waves/round-20/predictions .ufo/waves/round-20/measure.py | tar -x -C /tmp/kaidoku-r20-firstfailure.jmBoPb`. Both completed without reported errors; the Bash wrapper did not expose numeric pipeline statuses. Direct `git show` checks at S for the addr2line log, rerun summary, and root-level `measure.py` each printed `git show exit=0`.
- Search used the dedicated `functions.grep` query `Go analysis failure|Failed to read Go info|Invalid index|EOF` (case-insensitive) over the S snapshot's `runs/**/ghidra.log`; it returned the line anchors above. The tool exposes findings but no process exit code. Search of `runs/**/compare.json` for `prediction: missing first_failure.h1` returned all 19. No `lsp` device was mounted, so these source references use literal search and file reads rather than semantic LSP results.
- A path probe `git show S:.ufo/waves/round-20/tools/measure.py` returned 128 (the file is at `.ufo/waves/round-20/measure.py`); the corrected path returned 0. No tools were installed.