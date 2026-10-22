# Wave 2 scout — carrier and package-root drift since the round-27 runs

Item: freshness of the R27-C1 and R27-C2 inputs, lane tip 4084d8975b684a8837b1c858eea0008ce9ab49e0.
All times UTC; local zone is -03:00. **Verdict: holds** — no drift on any of the six named inputs. Observations unless labelled inference.

## Checks

C1. Carrier hashes vs claims.json carriers — `sha256sum /usr/bin/jq /usr/bin/tinyxxd /fast/scratch/hyaku/kaidoku-r27/carrier/renamed/*.dat`, 15:35:56Z, exit 0
```
e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806  /usr/bin/jq
7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65  /usr/bin/tinyxxd
e8156675…  carrier/renamed/jq-r27-renamed.dat      (same hash as /usr/bin/jq)
7b1e5d0c…  carrier/renamed/tinyxxd-r27-renamed.dat (same hash as /usr/bin/tinyxxd)
```
Matches claims.carriers.{jq,tinyxxd}.sha256, sizes 30800 / 38928, plain files (links=1, readlink -f resolves to themselves). `pacman -Q jq tinyxxd` exit 0: 1.8.2-1, 1.3.17-1 as claimed. `pacman -Qkk jq tinyxxd` exit 0, 15:37:06Z: "25 total files, 0 altered" / "12 total files, 0 altered". `cmp` renamed-vs-carrier both exit 0, 15:36:37Z, byte-identical.

C2. Package files vs c2 FROZEN_FILES and the claim — `sha256sum <2 roots>/{package.json,dist/domain/evidence.js}`, 15:35:56Z, exit 0
```
a500302319c1214a8bb6c9a8b4a4a090806e95eef884204a9d9fbb4003050a6c  ad9a3fdbcad992c6/…/package.json      6.5.0
f992d93eaf228bf8d7c6bc3bf566f4ff4554b53299f35cd7ff29e3b18a78dcff  …/dist/domain/evidence.js            6.5.0
3f6c47fb12c8388f291a21e7f99a876495d03aee671b3b6a0708dd12d6ebb570  a1722018f28f9df2/…/package.json      6.7.0
a3fb9f028e04e3a14f4c2269048e194ad2a8acb884b0e403212bb977d329c0fb  …/dist/domain/evidence.js            6.7.0
```
Exact match on all four FROZEN_FILES entries (c2-xpin-check.py:56-61) and the claim's pkg_json_sha256 (a5003023…).

C3. The checker's own gate, invoked as its function instead of a rewrite — `python3 -I -B -c "import importlib…; m.frozen_files_ok()"`, 15:36:37Z, exit 0
```
FROZEN_FILES entries: 4
mismatches: []
```
Same call the checker makes at c2-xpin-check.py:225-232.

C4. Installed trees vs the published npm artifacts — tree hash = sha256 of the sorted per-file sha256 listing; 15:37:34Z (6.5.0), 15:37:52Z (6.7.0), both exit 0
```
6.5.0 tarball, from cache   c9e45447785e3fbf0697fbdd3d97497a9345e6645278d38aeb5d1e8cf3ae1b0f
6.5.0 installed            c9e45447…  equal=yes  files 1650/1650
6.7.0 tarball, registry    d2fa81400750df4222db9564235a5f145bdbdbc771cd1adaa4b9d8502ce632e0
6.7.0 installed            d2fa8140…  equal=yes
6.7.0 tarball sha512-b64 = yhIx2ioJYYT1C/tONfYeitC6LhnKmCh+ZwRUOgYuhSc733lGhkkt73zhug9WmLgxoMdKuqIYGCoBfD4fXkOhFw==
  = npx package-lock.json integrity, match=yes
```
Ordinary means only: the 6.5.0 tarball came from the local npm content cache addressed by its integrity; the 6.7.0 tarball by plain HTTPS GET of https://registry.npmjs.org/rea-agents/-/rea-agents-6.7.0.tgz (curl exit 0, 6276963 bytes, sha256 20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90). No browser, no challenge bypass. Both roots are therefore the artifacts npm published, not merely self-consistent.

C5. No shadow install — `ls -d ~/.npm/_npx/*/node_modules/rea-agents`, 15:38:52Z, exit 0: one 6.5.0 (ad9a3fdbcad992c6) and one 6.7.0 (a1722018f28f9df2) install; `npm root -g` holds no rea-agents.

C6. Nothing written into the 6.5.0 root during or after the runs — `find … -newermt "2026-10-22T11:30:00"` count 0, newest file mtime 05:22 local (08:22Z), 15:39:11Z, exit 0. Runs window from corpus/evidence/round-27/c1/runs.tsv: first utc_start 14:54:51Z, last utc_end 14:56:43Z; base commit 14:02:27Z. All 48 runs.tsv rows record 6.5.0 / a5003023…, an at-run pin of package.json that still holds. [inference] the 6.5.0 tree during the runs was byte-identical to the published artifact (unchanged mtimes plus C4 equality now).

C7. Renamed copies predate the runs — both mtime 14:51:33Z, ten seconds after the claims freeze commit (11:51:23 local) and about three minutes before the first run. Table subject_sha256 is the carrier hash on 8 jq + 8 tinyxxd rows; runs.tsv subject_sha256 likewise on 24 + 24 rows.

## Guard gaps found (neither is drift today)

G1. The R27-C1 counter never reads a live carrier. It reads envelopes from Git at REV and compares the recorded subject digest with the frozen CARRIERS[carrier]["sha256"] (c1-rename-identity.py:229-232, 308-310); /usr/bin/jq and the renamed path occur only as constants (lines 50, 56) and in selftest edits. Carrier drift between the runs and a later recount is invisible to it; C1 does that check externally and passes.

G2. FROZEN_FILES pins package.json and dist/domain/evidence.js, but xpin-attribute.mjs also imports dist/domain/canonicalDigest.js from each root (xpin-attribute.mjs:166-177). That file is unpinned. Its hash is f46d6bd4dd94835504d71b396cd9e1b995e5eff7da17a618d374c48765be81d9 in both roots — equal across pins, consistent with the cross-pin difference living in semanticProjection (evidence.js), not the digest code. C4's whole-tree equality closes G2 today; an edit to only that file would still pass FROZEN_FILES.

Minor: `_npx/ad9a3fdbcad992c6` directory mtime is 12:37 local (15:37Z) while no file in the package root is newer than 08:22Z — consistent with a concurrent npx call by another seat touching directory metadata only; content unaffected (C4, C6).

## Unknowns
- No per-file hash of evidence.js or canonicalDigest.js was recorded at run time; the at-run state rests on C4 plus unchanged mtimes (inference, not a record).
- The renamed copies live outside Git under /fast/scratch; the claim re-derives from the committed envelopes, but the copies themselves are unbacked. They exist now.

## Artifacts (/fast/scratch/hyaku/kaidoku-r27/seats/w2/ScoutCarrierDrift/)
```
26e9931bbb047e90aab20af3fb54aba0ce5de431e47a7634958a0961b3df3fd1  carrier-resolution.txt
9cb589a91ebe5f81d946feb19cbbea7883bf9eed430025a01f22532cbd0c49b0  evidence-log.txt
855836521f962f8346ff41c299839eccc0e4de897783ebcb87820cbb425ac747  frozen-files-ok.txt
a65a8cd795e81fc1e672f0c9622798728acfc144b6490d2110a4f9223aec1b86  npx-installs.txt
83b204f8bc126c135ba383382d036357afd68ff10f63acea529ada1efbc1babf  pkg65-tarball-path.txt
6a559b28230e6fba2064cce05777b9c02aae4c92b5c58b6f7c9bf5173ba97f7e  runs-subject-hashes.txt
237625aaa97dc050e805249a2d798681070d3997627899b7936e2327882d6553  tree-compare.txt
20958a66dba1a011e50a486beb9463a343128ed368c984f94065362c13f51f90  tar/rea-agents-6.7.0.tgz
```
Tooling: no installs or upgrades; checks used sha256sum, cmp, tar, curl, jq, python3 -I -B. No lane file was modified; only this report was written inside the lane.
