## CLAIM
Lane-B review of G-drafts 3–4: G3's inspection of E3D and G4's B-only `inspect_sqlite_database` entry text verify against tracked round-6 evidence; Z3 is accurate, Z4 misses one admission-relevant gap — G4's proposed body carries no `source:`/`verified-at:`/`recheck:` fields.

## METHOD
Read `G3.md`, `G4.md`, `Z3.md`, `Z4.md`; cross-read `E3D.md`, `E4D.md`, `E6D.md`, `corpus/QUALITY.md`, `/home/vgpnk/.kimi-code/skills/shokunin/protocol/CORPUS.md`, and tracked round-6 files (`receipts/leg-5.md`, `receipts/leg-6.md`, `receipts-B/leg-5.md`, `receipts-B/leg-6.md`, `SC3.md`, `SC4.md`, `CC5.md`, `CC6.md`, `CB3.md`, `RV3.md`). Read-only; no probe. Checks: `grep -n "source:\|verified-at:\|recheck:"` over E3D/E4D/G4 → zero matches (E6D.md:12-14 carries all three); `grep -rl "^- verified-at:" corpus/knowledge/ | wc -l` → 64/72.

## FINDINGS
- G3 verifies: E3D.md:8 has no metadata trio; `CORPUS.md:17-19` requires it verbatim; leg-5 receipts are HEAD-tracked (`git ls-files`); citations `receipts/leg-5.md:3-12`, `receipts-B/leg-5.md:8,48-52`, `CC5.md:13-16` all resolve. G3's `E3D.md:12-26` pointer is unresolvable (E3D is 14 lines); Z3's catch ("proposal is at line 8") is correct.
- G4 verifies: hash `3701a7e3…`, Evidence `ev_7572e622…`, path-only call, `inventory`/`rows:null`, pnpm byte-identity all match `receipts-B/leg-6.md:20-28,35,50-55`; lane-A exclusion is grounded (`CB3.md:12`; bytes/recipe absent at `receipts/leg-6.md:10-12,19`; criterion 12 = `QUALITY.md:22`). `Grep inspect_sqlite_database corpus/knowledge` → no matches (Z4's claim reproduced); Z4's line cites resolve.
- Gap: G4's entry body (G4.md:10-23) lacks `source:`/`verified-at:`/`recheck:` — the exact admission gap G3 caught in E3D; Z4's "admission-safe" omits it.

## THREATS
Receipts reviewed as retained records, not re-executed. Corpus field practice is uneven (`recheck:` appears only in `corpus/lessons/`, 3 files), so parent normalization is advisable. Map rows, Command A counts, prior-corpus byte-identity: outside this seat, unverified.

## VERDICT
FINDING: G3/G4 verify and Z3 is right, but G4's body must gain `source:`/`verified-at:`/`recheck:` before admission — Z4 missed it.
