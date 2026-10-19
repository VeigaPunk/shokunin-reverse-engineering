# EX-22 evidence — fixtures and instruments (how to rebuild)

Scratch root: `/var/tmp/ex22` (never `/tmp`, standing EDQUOT rule). All fixture
files were copied with `cp`; no custody path was written.

## Instruments

| instrument | sha256 | builder |
|---|---|---|
| `c1-census-v10.pre.py` | `6f1d19ff…` | `git show HEAD:.ufo/gates/c1-census-v10.py` |
| `c1-census-v11.preview.py` | `a81893fc770a05424f2427749427367a7dd9cfd307afdd200e8c2fbe6c887c18` | pre-round file + RV-11 H1 + CR-5 H3 patch texts applied verbatim (line-anchored string replacements; all 5 hunks asserted exactly-once) |
| `c1-census-v11.landed.py` | `82fb807e79963f6dc6b9d055ab7378464b3636adfb498e5b615393f5f47c57aa` | first landing (mid-wave revision, later superseded); `cp` of the real target while stable across two polls 15 s apart |
| `c1-census-v11.r2probe.py` | `c95a5cf30201a1f862849b04701330e65b3777c877fb9467e4ee38656bbb0d4f` | in-flight intermediate whose floor counted current-ok BLOCKS per file — the revision that false-FAILed the ordinary run; frozen copy in `evidence/instr-blockfloor-intermediate.py` |
| `c1-census-final.py` | `df9ffdf963efa549f55c65770bca25120513015fe3b01c150a1087e0cf8e6b43` | FINAL r9 revision (601 lines; EX-16 `receipts/after/after-sha256.txt` names the same hash); `cp` of the real target after 5 stable polls 09:12:05→09:13:25 |
| `c1-census-v10.blind.py` | `7d7a54b283d25483e79c2f3915272a4f662f3c85f0ff233d555dc1f99d3caeeb` | pre-round file with the three needle lines `PIN =`/`VER =`/`PTR =` replaced by `re.compile(r"(?!)")` (line-based, 3/3 asserted) |
| `c1-census-v11.blind.py` | `b305c6afdb02d5d0aa8bdfa0a4f4ff3af859947c3c9be79e1d10d06e24e46e2d` | same rule on the preview |
| `instr-landed-blindall.py` | `5a65a315f8a4efbad299cc2fa1b27c92f3414163d6869eeda67c94097bc5d54d` | same rule on the landed bytes |
| `instr-landed-blindpin.py` | `ebd651f9a80a5d789fb31aded3a70257d0ba2bb2541e75fde3419da723afa344` | same rule, only `PIN =` neutered (partial-blindness control) |
| `c1-census-v10.blindpin.py` | `7f4ef99edcc7170edb9528d2bdb7330257ce8f35ea30b2ddea4a7bd51847d4b6` | same rule on the pre-round file |
| `instr-final-blindall.py` | `4b6e37e5f847d0143f4da232955291039046df0f6f5aa565e368b81567d75b7f` | final bytes, all three needles neutered via `evidence/blind-derive.py PIN,VER,PTR` (copy kept in `evidence/`) |
| `instr-final-blindpin.py` | `d3df7511fb4733f899ec4829dbb4ef6279f456186bc7286bd207d8dd581a24fe` | final bytes, `PIN` only — partial-blindness control (copy kept in `evidence/`) |
| `run.sh` | `30435b4e37537a6098d2d8b81849390fc0b57f69bd514f5194f716fcd196c7ba` | runner: `python3 <instr> --root <tree> [args]`, writes `<label>.out` + `<label>.exit` |

## Trees (three scoped files each: PROVINCE.md, SKILL.md, SCORECARD.md)

| tree | built from | file hashes |
|---|---|---|
| `tree-pre` | `git show HEAD:<f>` (HEAD `14b1682`) | PROVINCE `d075a3c67e17ae…`, SKILL `483b0eba27458c…`, SCORECARD `a7c72950094eca…` (identical to the worktree at seat start) |
| `tree-r1work` | `git show fbbbd45:<f>` (round-1 work commit) | PROVINCE `d075a3c6…`, SKILL `483b0eba…`, SCORECARD `30129a98d6f3f3…` (1336 lines) |
| `tree-r1pre` | `git show e845c2b:<f>` (round-1 pre-work HEAD) | PROVINCE `d075a3c6…`, SKILL `5c93c7c1bf45c7…`, SCORECARD `30129a98…` |

Injection trees: `tree-absent-skill` / `tree-absent-prov` (file removed),
`tree-empty-skill` (SKILL.md truncated to 0 bytes), `tree-trunc-skill`
(SKILL.md = first 10 lines), `tree-isdir-skill` (SKILL.md replaced by a
directory), `tree-eacces-skill` (SKILL.md `chmod 000`, probe run as its owner),
`tree-nullskill` (SKILL.md 371 lines, rows 10-20 stripped of every needle via
`evidence/nullskill-build.py` — readable and gate-clean, zero loci, EX-14's
fixture rebuilt independently).

## Real-target revision history observed in this seat's window

| time (-03) | sha256 of `.ufo/gates/c1-census-v10.py` | note |
|---|---|---|
| 09:05:05 | `7b5a0e88…` | header-only (doc block), behaviour still `d3da7509…` |
| pre-09:08 | `1431620f…` | header-only revision |
| pre-09:10 | `076bd621…` | H1+H3 code landed (global floor) |
| 09:11:05→09:11:45 | `c95a5cf3…` | per-file floor in the BLOCK unit — false-FAILs the ordinary run (`SKILL.md=0`) |
| 09:12:05→09:13:25 | `df9ffdf9…` | FINAL: per-file floor in the DET unit (EX-14's variant B) |

Poll log: `evidence/runs/` labels `v11landed-*` = `82fb807e…`,
`v11r2probe-*` = `c95a5cf3…`, `v11r3probe-*` = `df9ffdf9…`,
`v11final-*` = `df9ffdf9…`.

## Run protocol

Every run: `TMPDIR=/var/tmp/ex22/tmp python3 <instrument> --root <tree> [args]`,
stdout captured to `runs/<label>.out`, exit code to `runs/<label>.exit`.
`--json` runs are captured as `runs/<label>.json`. Labels encode
`<instrument>-<tree>`; the `v11landed-worktree` and `v11final-worktree` runs
used the real repo root.
