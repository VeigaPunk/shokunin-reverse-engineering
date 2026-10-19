# RV-2 — C1 freshness census

Chain: c1. Scope: `PROVINCE.md:50` patch text and a census of other unqualified perishables in that row. This artifact records measurements only; no source, gate, or tracked file was edited. HEAD: `947091d6b6f52684faf9ca53adf94ff8a0f6b006`.

## First-hand measurements

On 2026-10-19 (`date -u +%Y-%m-%d` → `2026-10-19`):

```text
$ ls /var/cache/pacman/pkg/*.pkg.tar.zst | wc -l
1350
$ ls /var/cache/pacman/pkg/*.sig | wc -l
1350
$ ls /var/cache/pacman/pkg/*.pkg.tar.zst.sig | wc -l
1350
```

Independent filename pairing and arithmetic:

```text
archives=1350
signature_files=1350
archives_without_matching_sig=0
orphan_signature_files=0
live_minus_2026-10-13=-206
```

The calculation uses the 1,556 historical snapshot value recorded at `corpus/knowledge/2026-10-13-pacman-packages.md:21-25` only as the dated comparison baseline; the live 1,350 count and −206 delta above were remeasured here. The target pointer in the patch below is the existing append-only erratum at `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`, not evidence borrowed from another seat.

The installed-jq state was also rechecked:

```text
$ pacman -Q jq
jq 1.8.2-1
$ pacman -Qo /usr/bin/jq
/usr/bin/jq is owned by jq 1.8.2-1
$ pacman -Qkk jq
jq: 25 total files, 0 altered files
installed_sha256=e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
archive_member_sha256=e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
```

Correction: the two SHA-256 strings above are identical (`/usr/bin/jq` versus `usr/bin/jq` extracted to stdout from `jq-1.8.2-1-x86_64.pkg.tar.zst`). This verifies current byte equality with the cached archive member and `pacman -Qkk`; this seat did not cryptographically re-verify the detached signature.

## Row census and verdicts

- **Live archive count — VERIFIED:** 1,350 `.pkg.tar.zst` paths, with 1,350 matching `.sig` files and no missing/orphan filenames, as measured above. The historical 1,556 is a dated 2026-10-13 snapshot, not a current count.
- **Unqualified Province count — REPRODUCED / DISCREPANCY:** `grep -n '1556' PROVINCE.md` returns a match at line `50` (full exact row below); the row still states `1556 signed archives` without an as-of qualifier. The current measured count is lower by 206.
- **`available:true` — UNVERIFIABLE:** the same row says ``(`available:true` in live session)``. This is a time-sensitive live capability value, but this seat has no attached `binary_session {}` MCP session to re-probe it. The row supplies no dated receipt. Do not treat the old value as freshly verified.
- **Installed `jq` byte-equality result — VERIFIED as of 2026-10-19:** `pacman -Qkk jq` and the identical digests above reproduce the current state. This is another stateful result, though the row's past-tense “verified” is not an assertion that it is still current. If the row is intended as a current claim, date this verification too.
- **`.MTREE` per-file sha256 / `pacman -Qkk` verify / `binary_session {}` capabilities — NOT PERISHABLE VALUES:** these are descriptions of data format, command, or probe method, not live numeric/status values in the row.

Exact current line from `grep -n '1556' PROVINCE.md`:

```text
| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
```

## Required one-line patch text (not applied)

```diff
-| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1556 signed archives; `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
+| Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in live session); pacman `.pkg.tar.zst` corpus 1,350 signed archives (re-count 2026-10-19; −206 vs 2026-10-13 snapshot; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member |
```

This replaces only the count fragment on line 50; it adds no lines. `wc -l PROVINCE.md` → `162`, so the proposed same-line change holds 162. `grep -n '1556' PROVINCE.md` reproduced the pre-patch source; no source patch was applied under this seat's write-scope restriction.

## Census-gate disposition

Instrument identity: `sha256sum .ufo/gates/c1-census-v10.py` → `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`.

Command and exact output:

```text
$ python3 .ufo/gates/c1-census-v10.py --quiet
live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
PROVINCE.md    lines=162  loci=6
SCORECARD.md   lines=1870 loci=11
SKILL.md       lines=413  loci=2

SCOPE-ERRORS (marker assertions): []
FRONTIER register (G21): 14 rows asserted, errors: []
UNREADABLE (could-not-evaluate): []
G2 positive-assertion guard: ok (current-ok loci per file: PROVINCE.md=20, SCORECARD.md=17, SKILL.md=3; total loci=19; floor=1/file)
G7 configured!=held warnings: []
G11 current-ok without receipt language: []
DECLARED FAIL CLASSES: []
VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
gate_exit=1
```

The JSON identifies the sole failure as `SCORECARD.md` block `1833-1839`, pin `6.7.0` at line 1834 with `scope: null`. The gate's SCORECARD scope ends at line 1813 (instrument `SCOPE`); the appended round-8 pointer narrative is outside it. This is independent of the proposed Province count edit. Therefore the frozen “census PASS held” condition is **DISCREPANCY / NOT MET at the measured baseline**; no PASS-after-patch claim is made. Re-keying the gate or altering SCORECARD is outside RV-2's permitted write scope.
