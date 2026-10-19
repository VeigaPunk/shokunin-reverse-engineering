# PL-3 — C1 freshness: pacman row census

## Scope and evidence identity

Read-only worktree at `git rev-parse HEAD` → `947091d6b6f52684faf9ca53adf94ff8a0f6b006`. The source row is `PROVINCE.md:50`; its table introduction says each surface was verified on this host on 2026-10-13 (`PROVINCE.md:40`). No source, gate, corpus, or tracked file was changed. The proposed replacement below was tested only in a temporary `/var/tmp` tree, which was removed at exit.

## Re-derivations and per-item verdicts

- **VERIFIED — stale row value and current archive inventory.** `Grep("1556", PROVINCE.md)` returns `PROVINCE.md:50` with “pacman `.pkg.tar.zst` corpus 1556 signed archives”; the number has no same-row as-of qualifier. `wc -l < PROVINCE.md` → `162`. I independently enumerated the live cache and matching detached-signature filenames:

  ```text
  python3 - <<'PY'
  from pathlib import Path
  import json
  root = Path('/var/cache/pacman/pkg')
  archives = {p.name for p in root.iterdir() if p.is_file() and p.name.endswith('.pkg.tar.zst')}
  sigs = {p.name[:-4] for p in root.iterdir() if p.is_file() and p.name.endswith('.pkg.tar.zst.sig')}
  print(json.dumps({
      'archive_files': len(archives),
      'matching_detached_sig_files': len(archives & sigs),
      'archives_without_matching_sig': sorted(archives - sigs),
      'sig_files_without_archive': sorted(sigs - archives),
      'delta_vs_dated_2026_10_13_count_1556': len(archives) - 1556,
  }, sort_keys=True))
  PY
  ```

  ```text
  {"archive_files": 1350, "archives_without_matching_sig": [], "delta_vs_dated_2026_10_13_count_1556": -206, "matching_detached_sig_files": 1350, "sig_files_without_archive": []}
  ```

  The `1556` comparison input is the dated 2026-10-13 source record, not a re-use of a prior seat's live measurement (`corpus/knowledge/2026-10-13-pacman-packages.md:21-25`). The current count and sidecar pairing were freshly enumerated. This does not cryptographically validate all 1,350 detached signatures; the patch wording therefore claims matching sidecar files, not a full signature sweep.

- **VERIFIED — the installed-jq byte-identity observation is still true when rechecked.** Commands/results from this run:

  ```text
  pacman -Q jq: jq 1.8.2-1
  matching cached archives: ['jq-1.8.2-1-x86_64.pkg.tar.zst']
  pacman -Qkk jq: jq: 25 total files, 0 altered files
  installed /usr/bin/jq sha256: e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
  archive usr/bin/jq sha256: e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806
  byte-identical: True
  gpg verify exit: 0
  gpg: Good signature from "Felix Yan <felixonmars@archlinux.org>" [full]
  ```

  GPG also printed an unsafe-homedir-ownership warning and “trustdb not writable”; verification nevertheless exited 0 and reported a good signature. The one archive checked is not evidence that every cache signature is valid.

- **CENSUS — other perishable facts in the whole row.** Besides the cache count, `available:true` for `inspect_artifact`/`extract_artifact` is a session-scoped value. The row/table dates it to the 2026-10-13 survey, but its current session state is **UNVERIFIABLE** here (no REA session tool is exposed to this seat); it must not be presented as a fresh availability check. The installed-`jq` byte-identity statement is also time-sensitive, but it was independently rechecked above. `.MTREE` per-file sha256, `pacman -Qkk` as a verification command, and `binary_session {}` as a probe are capability/method descriptions, not additional live inventory counts. The patch makes the dates of both volatile observations explicit.

- **CORRECTED (proposed text only; not applied).** Same-line replacement for `PROVINCE.md:50`:

  ```text
  | Archive/package inventory | `inspect_artifact`/`extract_artifact` (`available:true` in the live session as recorded for the 2026-10-13 host survey); pacman `.pkg.tar.zst` cache: 1,556 signed archives (2026-10-13 snapshot); current cache: 1,350 archive files, each with a matching `.sig` sidecar (arc3-loop1-round9 recount; −206 vs snapshot; see `corpus/knowledge/2026-10-13-pacman-packages.md:73-83`); `.MTREE` per-file sha256; `pacman -Qkk` verify | `binary_session {}` capabilities | installed `jq` verified byte-identical to signed archive member (re-verified in arc3-loop1-round9) |
  ```

  A scratch test applied exactly this text to a copied `PROVINCE.md`: `PROVINCE.md lines=162`, and the row retained the same table shape. The live source remains unmodified. The historical `1,556` snapshot and current `1,350` recount differ by `−206`.

- **DISCREPANCY — census gate does not PASS on HEAD or the proposed scratch row.** Independently measured gate identity: `sha256sum .ufo/gates/c1-census-v10.py` → `e4fb740cb8153f15c623f3b9f7ca781e270053b0557be5393010359b2213b7b4`. Both `python3 .ufo/gates/c1-census-v10.py --quiet` on HEAD and a full run against the scratch replacement report `VERDICT: FAIL (stale=0 ambiguous=0 undeclared=1 unresolved=0)`, exit 1. The full output identifies the unrelated locus:

  ```text
  -- UNDECLARED (1) --
    SCORECARD.md block 1833-1839 [scope None]
        :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
  ```

  The gate's declared SCORECARD scope ends at line 1813 (`.ufo/gates/c1-census-v10.py:264-276`); its classifier emits `UNDECLARED` outside scope (`:574-576`). Changing only `PROVINCE.md:50` cannot make this gate PASS. Under the frozen write boundary, I did not edit the gate or `SCORECARD.md`; the required PASS remains blocked for the integrator to disposition.
