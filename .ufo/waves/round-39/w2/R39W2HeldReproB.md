# R39W2HeldReproB — provenance reproduction of committed held-out envelopes H06–H10

**Verdict: CONFIRMED.** All five committed R39-C2 held-out envelopes (H06–H10) reproduce
from their carriers: carrier sha256 matches the manifest for 5/5, a fresh REA 6.5.0
`extract-firmware` run in the manifest arm yields the identical feature payload (chunk
handler, `extraction_failed`, gap kinds, gap dependencies, diagnostics `__typename__`,
MaliciousSymlinkRemoved, published-file count **and** published relative-path/sha256 set),
and the frozen interpreter labels each fresh envelope with the manifest label (5/5).

## Table

| id | class | label (manifest) | fresh label (frozen sqfs-triage) | payload match |
| --- | --- | --- | --- | --- |
| H06 | escaping-symlink-removed | escaping-symlink-removed | escaping-symlink-removed (rule 6) | match: H=`squashfs_v4_be`, EF=false, G=∅, D=∅, SR=yes, P=8, 8/8 identical rel-path+sha256 |
| H07 | in-tree-symlink-metadata | in-tree-symlink-metadata | in-tree-symlink-metadata (rule 7) | match: H=`squashfs_v4_be`, EF=false, G=`unpublished-entry`, D=∅, SR=no, P=3, 3/3 identical |
| H08 | in-tree-symlink-metadata | in-tree-symlink-metadata | in-tree-symlink-metadata (rule 7) | match: H=`squashfs_v4_be`, EF=false, G=`unpublished-entry`, D=∅, SR=no, P=6, 6/6 identical |
| H09 | dep-missing-be | dep-missing-be | dep-missing-be (rule 2) | match: H=`squashfs_v4_be`, EF=true, G=`missing-extractor-dependency`, D=`sasquatch-v4be`, DIAG=`ExtractorDependencyNotFoundReport`, SR=no, P=0 |
| H10 | dep-missing-be | dep-missing-be | dep-missing-be (rule 2) | match: same as H09; P=0 |

"Payload match" = no difference in any of the keys `{H, EF, G, D, DIAG, SR, P, sasquatch
commands, file relative-path+sha256 multiset}` between the committed `envelope.json` and the
fresh envelope — computed over the whole `data` object, i.e. `normalized_result` **and**
`raw_result` (see `cross-checks.json`, `fresh-labels.json`).

## Method (exact)

Scratch `S=/fast/scratch/hyaku/kaidoku-r39/R39W2HeldReproB` (removed at end; nothing under
`/tmp`; no `find`/`du` under `/fast/scratch`).

1. Copies + digests — all five matched `manifest.json` exactly:

   ```
   cp corpus/evidence/round-39/c2/heldout/<id>/carrier.sqsh $S/<id>/carrier.sqsh
   sha256sum $S/<id>/carrier.sqsh
   H06 d7d1c6f5977613de0ea1dad4b9a5640a9d220c13cc6af07edd4987f2190dc85c
   H07 3130c5f9193e38ee089644ed09fc940f8db920cfb482ad3689f637a1db070d6c
   H08 2a4b40777ecb839d8fea16e0c2674640a5ab4b3386a444f6419072b8a86fcc8c
   H09 d9d49304ca7a293dfce6b2941951bc0b9a626cfd6eafab9c4e580a83d93f774c
   H10 93d445c2f7453e370914bc49aa1822d9edb32921ddd2541b1300209dc8c90d12
   ```

   Carrier magics (`head -c 4`) are `sqsh` for all five, consistent with the declared
   big-endian class; `tree.json` for each names `"endian": "be"` and seed
   `8fcda41c…faba0b`.

2. Fresh REA run per manifest arm, `cd $S/<id>/work` (fresh, REA refuses an existing outdir):

   ```
   # after (H06, H07, H08)
   REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
     npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
     $S/<id>/carrier.sqsh $S/<id>/work/out
   # before (H09, H10): PATH with every entry resolving to $HOME/.local/bin removed
   env PATH="$NEWPATH" REA_UNBLOB_COMMAND=$HOME/.local/bin/unblob \
     npx -y rea-agents@6.5.0 extract-firmware --format json --full-output \
     $S/<id>/carrier.sqsh $S/<id>/work/out
   ```

   Exit codes: 0 / 0 / 0 / 0 / 0; stderr empty (0 bytes) for all five; `ok: true`;
   durations 2217 / 2138 / 2156 / 2124 / 2116 ms.
   `NEWPATH` verification: `env PATH="$NEWPATH" bash -c 'command -v sasquatch || echo NONE'`
   → `NONE` (both sasquatch binaries live only in `~/.local/bin`; `sasquatch -version` and
   `sasquatch-v4be -version` both report `unsquashfs version 4.5.1 (2022/03/17)`).
   Fresh runs record `engine.unblob 26.6.4`,
   `executable_sha256 0ce7b624f540c2191ff144892584997fe3fb6ab28ab6ef6b88639f8a7cba1d09`,
   and `selection.sha256` equal to the manifest carrier sha256 for all five.

3. Labelling with the frozen interpreter:

   ```
   python3 -I -B tools/round-39/sqfs-triage.py --skill SKILL.md \
     .ufo/waves/round-39/w2/artifacts/R39W2HeldReproB/H0{6,7,8,9}-fresh-envelope.json \
     .ufo/waves/round-39/w2/artifacts/R39W2HeldReproB/H10-fresh-envelope.json
   ```

   One label line per envelope, exit 0 → `escaping-symlink-removed`,
   `in-tree-symlink-metadata`, `in-tree-symlink-metadata`, `dep-missing-be`,
   `dep-missing-be`. `--selftest` → `SELFTEST cases=35 pass=35 fail=0`, exit 0.

## Freeze provenance of the surfaces used

| surface | freeze `8fcda41c96cbf00b113d2c8e136cc14e7fcaba0b` | worktree/HEAD `e40a25df…:round-39 wave-2 spec…` | same |
| --- | --- | --- | --- |
| `tools/round-39/sqfs-triage.py` | `ef4a8a8b7428cf7221dd3aa16bc587507d308b1eacf01074def276e744beacf2` | same | **yes** |
| `SKILL.md` (whole file) | `29372524a963f5d05012b552f095eaf6a3b81b37f73a72f22aa9bcc95f40890d` | `f31ebd633e9fff3396e04886acd65f5a283ffb14b3136e17499493b5dbe23b78` | **no** |
| triage table block after `<!-- sqfs-triage-table v1 -->` (10 rows) | `56bc6204ee597cb9d06978b024a290d71bb1dc982246650ce538523922fcef4f` | same | **yes** |

The SKILL.md difference is exactly the 28-line `### Round-35/37/38/39 instrument registry`
appended by the later commit `52b0eb2907c704ed5f184c47b14c723208e5cbbc` (post-freeze,
documented in the assignment) — `diff -u` shows no other hunk. The frozen triage table the
interpreter reads is byte-identical at freeze and worktree, so labelling against the
worktree `SKILL.md` is labelling against the frozen table.

## Retained evidence (artifacts dir)

`/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-39/w2/artifacts/R39W2HeldReproB/`

```
32623183b524377cc0cd6e3409a7e88a054a3658927a1285a53f842a46367cc7  H06-fresh-envelope.json
d3c215549556e4af67479087d1400e7c5e08d7959fafadeea8c0d215e38955ff  H06-fresh-full.json
e0e79a11054569b47fc636e4da9beed1d9bc8469a0ed7e8740fd61ae61f86a1b  H07-fresh-envelope.json
686d36e44fbcd7916544b3ce949befe4e028e25e06084180e262df60acf9fea2  H07-fresh-full.json
9b3c6a6150f6bd4f52d62d0e53d5b39bf82dd15be0025b918cab9c7f64804f7d  H08-fresh-envelope.json
671fc8463a5d7802bfca9ba732bfcb183278932fc7c4dc5edb15197b277a3bf0  H08-fresh-full.json
6f399fbe0b852d22027bd6437a48c5c9885982cb9be8304c59b89b3b36c9cb63  H09-fresh-envelope.json
ab675857079ae60d634e4126f5a21e63f5d313e89a5f82e74e86dff72b2edb4d  H09-fresh-full.json
6063b8406e648182c45714fdfa579ef409fe597dcc570d070f9f4b30fc5cdabb  H10-fresh-envelope.json
0cca47e128746dca036997a2c1e3a930e57f9c36ee27ecb4ec74c2c0af0c88da  H10-fresh-full.json
a0b11e3a3714a6e2d91642d8681e4d721ec4a51310bdaefab3f91247b94b7de2  cross-checks.json
a71a0d28e1493c8eb7a30e192d0c1a76908cdcac92deae2e19c125d291ebf060  fresh-labels.json
```

`*-fresh-envelope.json` = the `data` object of the fresh run (same shape the committed
`envelope.json` has); `*-fresh-full.json` = the whole `{ok, data, meta}` CLI envelope.

## Observed detail behind the table

* **Chunk handler + extraction_failed.** All five: one chunk, `handler=squashfs_v4_be`.
  `extraction_failed=false` for H06/H07/H08; `true` for H09/H10 (dependency unresolvable in
  the `before` arm).
* **Gaps.** H06: none. H07/H08: exactly `{unpublished-entry}`, dependencies `∅`, one gap
  each, and every oracle file is published with the oracle sha256 (3/3 and 6/6). H09/H10:
  exactly `{missing-extractor-dependency}` with dependencies `{sasquatch-v4be}`, 0 published
  files.
* **Diagnostics `__typename__`.** H06: `MaliciousSymlinkRemoved` only (fresh report link
  basename `dupzyk73w`, target basename `alt` — identical shape to committed). H07/H08: no
  diagnostics. H09/H10: `ExtractorDependencyNotFoundReport` (severity `ERROR`) only.
* **sasquatch `command` / `-be`.** **No envelope in H06–H10 records any `command` naming a
  sasquatch binary** — the only `command` members present are the unblob invocation
  (`/home/vgpnk/.local/share/uv/tools/unblob/bin/unblob`, twice, in `raw_result`). So the
  "-be in child argv" feature is `n/a` for all five, in both the committed and the fresh
  envelopes; the `-be` sub-check is vacuous on this surface for these ids (it is exercised
  by H13/H14, outside this seat's range). This is consistent with the labels' rule cells:
  rules 6/7 specify `n/a`, rule 2 specifies `n/a`.
* **Internal consistency.** For all five, the committed `run.json` (`handlers`,
  `gap_kinds`, `diagnostics`, `files`) equals both the committed and the fresh envelope
  features, and `subject_sha256`/`digest_matches_carrier` are consistent with the carrier
  bytes.
* **H09/H10 oracle vs published 0/6 and 0/7** is expected by construction of the
  `before` arm (the label asserts "unmeasured, not unreadable"), not a defect.

## Limits / notes

* Reproduction used the npx-cached `rea-agents@6.5.0` package root
  `/home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents` as recorded by the
  environment (`command`/version provenance is the recorded unblob
  `executable_sha256 0ce7b624…` plus REA 6.5.0's own `meta`).
* The `before` arm was reproduced as the generator defines it
  (`tools/round-39/heldout-gen.py:390-399`: drop every PATH entry whose realpath is
  `$HOME/.local/bin`, keep the rest), not as the literal example
  `PATH=/usr/local/bin:/usr/bin:/bin`, because `npx`/`node` on this host live under
  `/run/user/1000/fnm_multishells/…/bin` and the literal example would fail before REA
  starts. The property that matters — unblob's child PATH cannot resolve `sasquatch` or
  `sasquatch-v4be` while `REA_UNBLOB_COMMAND` stays absolute — was verified directly
  (`command -v sasquatch` → `NONE`), and the resulting envelopes match the committed
  `before`-arm payloads, which is itself the control that the arm was faithful.
* No tool was installed, upgraded, or moved (no pacman, no uv, no npx install beyond the
  cached `-y rea-agents@6.5.0` resolution); no VCS mutation; nothing written outside this
  report and the artifacts directory. Scratch `$S` removed.
