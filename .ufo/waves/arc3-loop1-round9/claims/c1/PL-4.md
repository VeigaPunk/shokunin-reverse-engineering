# PL-4 — C1 freshness: pacman row census

Scope: evidence and patch text only. I did not edit `PROVINCE.md`, the census gate, or any tracked file. Worktree source identity: `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`.

## Re-derived count and line patch

**CORRECTED — live archive inventory.** I counted direct-child regular files in `/var/cache/pacman/pkg/` two ways; neither result is taken from an earlier seat or round.

```text
$ python3 -c 'from pathlib import Path; p=Path("/var/cache/pacman/pkg"); fs=[x for x in p.iterdir() if x.is_file()]; a=[x for x in fs if x.name.endswith(".pkg.tar.zst")]; s=[x for x in fs if x.name.endswith(".pkg.tar.zst.sig")]; print(f"archive_regular_files={len(a)}"); print(f"matching_signature_regular_files={len(s)}"); print(f"archive_without_matching_sig={sum(not Path(str(x)+".sig").is_file() for x in a)}"); print(f"direct_child_regular_files={len(fs)}")'
archive_regular_files=1350
matching_signature_regular_files=1350
archive_without_matching_sig=0
direct_child_regular_files=2700

$ bash -c 'shopt -s nullglob; a=(/var/cache/pacman/pkg/*.pkg.tar.zst); s=(/var/cache/pacman/pkg/*.pkg.tar.zst.sig); printf "shell_glob_archives=%d\nshell_glob_matching_signatures=%d\n" "${#a[@]}" "${#s[@]}"; printf "dated_1556_delta=%+d\n" "$(( ${#a[@]} - 1556 ))"'
shell_glob_archives=1350
shell_glob_matching_signatures=1350
dated_1556_delta=-206
```

The historical baseline is the source's 2026-10-13 receipt at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` (it records 1,556 archives and the original count recipe); it is not a live measurement. The independently measured path-count delta is `1,350 - 1,556 = -206`. Matching `.sig` path counts do **not** prove signature validity, and this recount did not verify signatures or archive integrity. The existing append-only erratum at `corpus/knowledge/2026-10-13-pacman-packages.md:73-83` is the requested durable pointer, not the source of my live count.

**PROVINCE.md:50 proposed one-line replacement** (only the pacman phrase changes; retain all other row text):

```diff
-| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
+| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1,556 signed archives (2026-10-13 snapshot; live archive count 1,350, −206; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
```

**VERIFIED — same-line constraint.** Applying exactly that replacement to a `/var/tmp` scratch copy kept `PROVINCE.md` at 162 lines (`province_lines=162`; `province_patch_lines=162`). No source file was changed.

## Census of the rest of line 50

- **UNVERIFIABLE as current — `available:true in live session`.** This is a volatile availability boolean. The phrase identifies a session but does not identify its capture time in the cell; the containing table says surfaces were verified on-host 2026-10-13 (`PROVINCE.md:40`), and the gate classifies the encompassing `PROVINCE.md:45-62` range as DATED (`.ufo/gates/c1-census-v10.py:259`). I had no live REA MCP session evidence to re-probe it, so do not read the old observation as present availability. Treat it as a second freshness candidate if the row is meant to make a current availability claim; explicitly date/link the captured result or re-probe before asserting current status.
- **DATED, not a current result — `installed jq verified byte-identical to signed archive member`.** This is past-tense verification, not a present-tense equality assertion; it sits in the table whose header dates host verification to 2026-10-13 (`PROVINCE.md:40`). I did not re-run the jq byte comparison as part of the pacman path recount.
- **Not perishable values — `.MTREE per-file sha256`, `pacman -Qkk verify`, and `binary_session {}` capabilities.** These are respectively a package-metadata property, a verification procedure, and a probe name, not dated live counts/results.
- The only numerical archive inventory value in the row is the `1556` count addressed above. The `available:true` boolean is the only other status-like volatile value I found; the current census gate's token families do not grade either this boolean or the pacman count (`.ufo/gates/c1-census-v10.py:310-316,499-516`).

## Census-gate result / integration blocker

**DISCREPANCY — the checked-in gate is not PASS on this checkout, even before the proposed province-line replacement.** Gate identity: `.ufo/gates/c1-census-v10.py`, SHA-256 `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`.

```text
$ python3 .ufo/gates/c1-census-v10.py --root . --json
exit=1
verdict=FAIL
counts: PROVINCE.md 162 lines / 6 loci; SCORECARD.md 1870 lines / 11 loci; SKILL.md 413 lines / 2 loci
undeclared: SCORECARD.md block 1833-1839; pin 6.7.0 at line 1834 (scope null; no client token in clause)
frontier_rows=14; frontier_errors=[]; g2_ok=true
```

The unscoped block is in the current round-8 SCORECARD record (`SCORECARD.md:1815-1870`); the gate's last SCORECARD range ends at 1813 (`.ufo/gates/c1-census-v10.py:276`). Applying the proposed province line in scratch left the same FAIL and same undeclared locus. As a diagnostic only, I copied the gate to `/var/tmp`, added the bounded DATED row `("SCORECARD.md", 1815, 1870, "DATED", 1815, r"arc3-loop1-round8")`, and re-ran it against the scratch tree containing the province replacement: exit 0 / `PASS`, undeclared `[]`, with the same `162/6`, `1870/11`, `413/2` file counts. This demonstrates the province text does not create the gate failure; it does **not** mean the checked-in gate currently passes. The gate source was not modified. The proposed range is tied to the currently measured SCORECARD extent and needs re-keying if the landing changes that extent.

## Verdicts

- Live pacman path count: **REPRODUCED / CORRECTED** — 1,350 archives, −206 versus the dated 1,556 receipt; path count only.
- One-line province replacement: **VERIFIED** — preserves 162 lines and points to the dated receipt plus its erratum.
- Other row perishables: **UNVERIFIABLE as current** for `available:true`; the cell is session-scoped but lacks its own capture stamp/current-session recheck. The remaining row items are dated evidence or procedures/properties, not additional current numeric counts.
- Current census acceptance: **DISCREPANCY** — gate fails on unscoped SCORECARD line 1834 independently of this one-line replacement; no claim of an actual-tree PASS is made.
