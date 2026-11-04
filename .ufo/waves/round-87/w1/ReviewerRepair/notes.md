# notes — ReviewerRepair (round 87)
- Read-only review of upx-magic-repair.py (f4ebd152…) and upx-tamper-battery.py (0f2d2bd8…) at b5c7a49e; the working tree matches both pins.
- Commands, all under /fast/scratch/hyaku/kaidoku-r87/ReviewerRepair (deleted before yield):
  - `TMPDIR=<scratch>/tmp python3 -I -B tools/round-87/upx-tamper-battery.py --root <lane> --repair-cmd <lane>/tools/round-87/upx-magic-repair.py --upx /usr/bin/upx --work <scratch>/work --json-out counter-norea.json --no-rea` → exit 1 (REA disabled); non-REA arms 8/8, controls all true.
  - jq: `upx --best` → T1 (every UPX! → 00000000) → repair → `upx -t` OK → `upx -d` gives the pin → REA analyze: 167 (rea-jq-restored.json).
  - Out-of-population probe (probe-out-of-population.txt).
- Files: review.md, counter-norea.json, rea-jq-restored.json, probe-out-of-population.txt, notes.md, DONE; report at ../ReviewerRepair.md.
- No VCS mutation, no tool installs, no frozen files touched.
