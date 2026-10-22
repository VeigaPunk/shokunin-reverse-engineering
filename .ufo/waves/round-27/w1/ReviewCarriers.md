# R27 wave 1 — ReviewCarriers: carrier-fact attack on R27-C1 (claims.json)

Seat KaidokuR27.ReviewCarriers, 2026-10-22. Scope: attack the frozen carrier facts of
R27-C1 in .ufo/waves/round-27/claims.json. No REA invocation was made (per assignment);
only the two carriers and their renamed copies were touched, read-only. Lane writes:
this report file only. Tooling: no installs were needed or performed (sha256sum/stat/cmp
coreutils, binutils readelf/file, pacman -Qo/-Qi queries only — pacman guard respected).

## Findings

### F1 — sha256 and size of carriers and copies — HOLDS (observation)
Command: `sha256sum` + `stat -c '%n %s'` over the four paths; 2026-10-22T14:56:54Z; exit 0.
- /usr/bin/jq = e815667571d07cb7a7be98eb6e9920a9e7e20d64074c132882e7fc94984f7806, 30800 B — equals claims.
- /usr/bin/tinyxxd = 7b1e5d0c970afe686c8d6b60fcf0298981e16adf08c3f0f128ee007a0403ae65, 38928 B — equals claims.
- renamed jq copy: same sha256, 30800 B; `cmp -s` base vs copy exit 0 → byte-identical.
- renamed tinyxxd copy: same sha256, 38928 B; `cmp -s` exit 0 → byte-identical.
The "byte-identical copy" premise of the C1 rename rows is true on disk right now.

### F2 — tinyxxd is an ELF PIE; entry 0x3d40 maps to 0x103d40 — HOLDS (observation + inference)
Command: `file`, `readelf -hW`, `readelf -lW`; 14:56:54Z; exit 0.
`file /usr/bin/tinyxxd`: "ELF 64-bit LSB pie executable"; readelf Type: DYN. Entry point 0x3d40;
first LOAD vaddr 0x0 with 0x1000 alignment, so the file's fixed vaddrs are base-relative.
Image base REA uses: 0x100000 is inference, cross-validated two ways without running REA:
(1) the frozen pre_freeze_probe (claims.json, 14:45:23Z, exit 0) has REA's `function` verb
report "procedure entry at 0x103d40, 38 bytes" for a file whose ELF entry is 0x3d40;
0x100000 + 0x3d40 = 0x103d40. (2) Independent: `readelf --debug-dump=frames /usr/bin/tinyxxd`
shows `FDE cie=00000000 pc=0000000000003d40..0000000000003d66` — an eh_frame FDE starting
exactly at 0x3d40 spanning 0x26 = 38 bytes, matching the probe's "38 bytes" and the frozen
address rebased. A C1 rule also requires subject.name equal to the file name, and the probe
records ".data.subject.name is the file name 'tinyxxd'".

### F3 — jq: 0x103fa0 is a function entry, not the ELF entry; does it matter — HOLDS (observation + inference)
`readelf -hW /usr/bin/jq`: Type DYN (PIE), Entry point 0x3cf0 → rebased 0x103cf0 ≠ 0x103fa0.
So 0x103fa0 is NOT an entry. It IS a function entry: `readelf --debug-dump=frames /usr/bin/jq`
gives `FDE cie=00000000 pc=0000000000003fa0..00000000000044a9`, an FDE whose pc_begin is
exactly 0x3fa0, inside .text (readelf -SW: .text vaddr 0x2020, size 0x2529, range
0x2020..0x4549). jq is stripped (no .symtab; only 74 dynamic FUNC symbols), so eh_frame is
the strongest symbol-free witness available. Does it matter? For the claim as frozen, no
(inference): claims.json asserts only "one address per carrier" and feed it to the five
address-taking verbs; it never calls either address the ELF entry, and its limits say "Any
verdict counts as complete; the claim is that the 16 verdicts re-derive". The asymmetry
(tinyxxd address = ELF entry and function entry; jq address = function entry only) is
cosmetic unless a future write-up calls 0x103fa0 "the entry point" — it must not. No defect.

### F4 — pacman ownership — HOLDS (observation)
Command: `pacman -Qo /usr/bin/jq /usr/bin/tinyxxd` (read-only query); 14:56:54Z; exit 0.
"/usr/bin/jq is owned by jq 1.8.2-1" and "/usr/bin/tinyxxd is owned by tinyxxd 1.3.17-1";
`pacman -Qi` confirms Version 1.8.2-1 / 1.3.17-1. Matches claims.json packages exactly.
Both carrier paths are pacman-owned files, i.e. the pinned hashes are distribution bytes.

### F5 — renamed paths differ in directory, file name and extension — HOLDS (observation)
Command: dirname/basename/extension expansion; 14:57:23Z; exit 0.
- jq: /usr/bin + name "jq" + no extension  vs  /fast/scratch/hyaku/kaidoku-r27/carrier/renamed
  + "jq-r27-renamed.dat" + "dat". Directory, name, and extension all differ.
- tinyxxd: /usr/bin + "tinyxxd" + none  vs  .../carrier/renamed + "tinyxxd-r27-renamed.dat"
  + "dat". Directory, name, and extension all differ.
Both renamed files exist, are regular readable copies (F1), and were not modified.

## Verdict summary
All five carrier-fact checks hold. No counterexample found against R27-C1's frozen carrier
facts: hashes, sizes, byte-identity of copies, PIE status, the 0x100000-based mapping for
tinyxxd's entry/function address, jq's address being a genuine function entry, pacman
ownership with exact package versions, and the directory/name/extension triple difference.

## Residual risk
- "The image base REA uses = 0x100000" is inference from the frozen probe plus my FDE
  corroboration, not a live REA observation; a different pinned provider could in principle
  rebase differently. If wave 2 wants it nailed, one REA call (or the analyze envelope's
  image_base field, exposed per ReaGhidraBridge.java:492/608) settles it — out of my scope.
- 0x103fa0's FDE proves a function entry in eh_frame terms but gives no name (jq stripped);
  whether REA itself resolves a named function there was not re-derived (no REA allowed).
- Carrier facts were verified at 14:56–14:58Z today; nothing prevents later host changes
  (e.g. a pacman upgrade) between now and the C1 runs. Re-hash at run time is the counter's
  own job (subject sha256 rule), so risk is contained.

## Verification gaps
- REA not run (per assignment): the live `function` outputs for both carriers are not mine.
- C1 counter logic, table.tsv, envelopes, and entry_ok were not examined (other seats).
- No pacman file-list audit beyond -Qo/-Qi; no check that /fast/scratch copy metadata
  (mtime/permissions) is preserved — only byte identity matters to the claim.

## Artifacts
- /fast/scratch/hyaku/kaidoku-r27/seats/ReviewCarriers/raw/carrier-facts.txt
  sha256 a1f8df6901a1f8b7b4bddec4134287faafe897304677ad5fbf0c8a52ad0666f6 (4309 B, raw outputs)
- This report: .ufo/waves/round-27/w1/ReviewCarriers.md
