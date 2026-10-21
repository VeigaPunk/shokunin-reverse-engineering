HOLDS — the correction for the C3 first-failure comparison reproduces the retained rerun records for all 19 frozen, included labels.

**Observation.** F's `predictions/carriers.tsv` lists 20 carriers; `t1246-link` is explicitly excluded before analysis because the emulator returned exit 2 (`predictions/decision-rule.json:19-27`; `run-carriers.sh:278-281`). The 19 remaining labels each have a frozen `swiss-misread-v2/<label>.json` forecast and a receipt-bound log. I selected each log from the `bound_sessions` / `retained_logs` entry in its receipt at S. `evidence/compare-rerun/summary.txt:1-19` records `exit=0` and `logsha_ok=y` for all 19.

The frozen comparator, extractor and v2 predictions are identical from F to S (`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 808cbb31a1e24656da5ba4967497e602fbca7415 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/tools/compare-first-failure.py .ufo/waves/round-20/tools/first-failure-extract.py .ufo/waves/round-20/predictions/swiss-misread-v2`; exit 0). The runner, carrier inventory and exclusion rule are also unchanged F→S (same command with `run-carriers.sh`, `predictions/decision-rule.json`, and `predictions/carriers.tsv`; exit 0). The local command inputs, S run logs and retained comparison files match S (`git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --quiet 5c0b46c4d35f7256f340ab3f53a8b1a66a2aa5d9 -- .ufo/waves/round-20/tools/compare-first-failure.py .ufo/waves/round-20/tools/first-failure-extract.py .ufo/waves/round-20/predictions/swiss-misread-v2 .ufo/waves/round-20/runs .ufo/waves/round-20/evidence/compare-rerun`; exit 0).

I ran this exact command once for each row below; each process returned **exit 0**, `match:true`, and its output JSON reproduced the retained JSON at `evidence/compare-rerun/<label>.json:1`:

```text
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/compare-first-failure.py --prediction /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/predictions/swiss-misread-v2/<label>.json --log /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/runs/<label>/logs/rea-ghidra-<session>/ghidra.log --extractor /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-20/tools/first-failure-extract.py
```

| Label | Receipt-bound session | Result |
|---|---|---|
| t1246-addr2line | P9tyVR | exit 0; match |
| t1246-asm | 15p1Vy | exit 0; match |
| t1246-buildid | qGQ7Im | exit 0; match |
| t1246-cgo | I0zRdH | exit 0; match |
| t1246-compile | Q6goA3 | exit 0; match |
| t1246-covdata | 314Y9f | exit 0; match |
| t1246-cover | mFkiDF | exit 0; match |
| t1246-doc | wQaOa9 | exit 0; match |
| t1246-fix | Zvh0Na | exit 0; match |
| t1246-go | 2PFXTv | exit 0; match |
| t1246-gofmt | jjj6WB | exit 0; match |
| t1246-nm | xpz849 | exit 0; match |
| t1246-objdump | uLjgCv | exit 0; match |
| t1246-pack | Dhu23X | exit 0; match |
| t1246-pprof | hCPl3X | exit 0; match |
| t1246-preprofile | JcCFCG | exit 0; match |
| t1246-test2json | tU5R8R | exit 0; match |
| t1246-trace | Vwh31x | exit 0; match |
| t1246-vet | AW49O8 | exit 0; match |

A first `t1246-nm` attempt had my path typo (`/home/vgpnk/Projects/shokurin/...`) and returned exit 2 (`log_not_found`); the corrected exact command above was rerun and returned exit 0. This typo attempt is not included in the 19 results.

**Inference / scope.** Mistake 6 describes the wrong in-run prediction shape and the corrected v2 file path (`corpus/lessons/round-20.md:105` at S). The rerun supports closure of that comparison defect: eight non-silent forecasts matched their `invalid_index` and index, and eleven forecasts matched silence. Comparator equality is intentionally only kind+index (or both null), not VA/phase (`tools/compare-first-failure.py:28-34`); a null extractor result is bounded to the final line of its log, not proof of later analysis success (`tools/first-failure-extract.py:6-8,134-135`). No Go toolchain binary, REA command, or Ghidra analysis was run; this finding is limited to comparison against the already-bound logs.