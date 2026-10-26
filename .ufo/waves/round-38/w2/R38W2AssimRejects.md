# R38W2AssimRejects — the two assimilation refusals, attacked

**Verdict: DEFECTS FOUND.** Both refusals are correct as *decisions* — neither entry can be
admitted on the bytes the lane holds — but three of the stated grounds are misdated or
overstated, one closing premise is refuted by a weaker witness than the available one, and the
theme pass leaves undispositioned the single entry against which none of its grounds applies.

Scope: `corpus/lessons/round-38.md` `## Gate` → `### Assimilation — theme sasquatch / unblob`
(lines 36–66), against the staged package
`/home/vgpnk/Projects/shokuknow/merge/kaidoku/knowledge/corpus/knowledge/` (11 theme files).
Everything below re-derived on this host, 2026-10-26. The two refusal bullets are byte-identical
in the working tree and at the landed commit `0fc6113376a156fddc3ec385386d71c3a4a9f690`
(section diff: the only hunk is the admitted `unblob-format-matrix` corrections paragraph), so
the critique holds for both. Raw outputs:
`.ufo/waves/round-38/w2/artifacts/R38W2AssimRejects/{host-and-upstream-checks.txt,branch-argv.txt}`.

## Axes

1. dated truth of a host-state claim (snapshot vs present tense)
2. pin identity (does "unpinned" mean different bytes?)
3. provenance reachability (is the cited byte obtainable anywhere?)
4. direction and depth of a sibling "conflict"
5. flip testability and its cost
6. theme coverage (silent skips, superseded chains)
7. premature saturation (refusing a re-measurable fact)

## Findings — refusal 1 `sasquatch-unblob-compatibility-precondition`

**D1 — ground (a) attacks a snapshot that was true when taken.** The lesson says the claim
"Neither tool is present on the lane host" "is false here", listing the binaries. It is false
*here and now*, but not when measured: `~/.local/bin/sasquatch` and `sasquatch-v4be` have mtime
**2026-10-26 01:22:37** and the `unblob` uv-tool link **2026-10-25 18:10:59** — i.e. installed by
*this* lane (round 36), after the staged campaign. The rough digests and sizes in the lesson are
exact (`382824`, `436232`, sha256 `ad02d27a…4754`, `fac88740…14c6`), and they equal the ones the
lane already carries (`2026-10-26-r36-sasquatch-squashfs-recursion.md:137`,
`2026-10-26-unblob-sasquatch-dependency.md` point 3 — which already says the staged sentence was
"true at the package's 2026-10-23 snapshot and … false from 2026-10-26"). The entry's own
`Caveats` calls itself "a 2026-10-24 snapshot of this host". Worse for re-checking: two of the
three locations the entry enumerates **still verify today** — `ls /usr/bin/sasquatch
/usr/local/bin/sasquatch /usr/bin/unblob /usr/local/bin/unblob` → all four "No such file or
directory" (exit 2), and `python3 -c 'import unblob'` on the host default Python **3.14.8** →
`ModuleNotFoundError` (exit 1). Only the "absent from PATH" clause flipped (`~/.local/bin` is on
`PATH`). A wave-2 re-runner following the entry's own words finds it two-thirds true.
*Axis 1. Smallest correction:* date the ground — "false from 2026-10-26T01:22:37 (binaries'
mtime); true when taken" — and put provenance first, host state second.

**D2 — ground (b) "No published source states the compatibility … contradicted by S110 line 49
and S112" holds only under a loose reading.** I fetched both at the pin: README sha256
`6544d60f…3716`, 235 lines, line 49 verbatim "For SquashFS support, also install
[sasquatch](https://github.com/onekey-sec/sasquatch):" — an install instruction. S112 is
`EXECUTABLE`/`V4BE_EXECUTABLE` plus the argv builder (lines 25–26, 40–64). Neither states that the
*pair* works at any version; they state the producer's declared dependency on it. The lane's
actual observations of the pair are its own after-arms. I added one at the pin on lane bytes: on
committed `K4` (`corpus/evidence/round-37/c1/K4/carrier.bin`) unblob 26.6.4 runs
`sasquatch-v4be -be -no-exit-code -f -d …` and all four files come out byte-identical to
`K4/oracle.tsv` (4/4 sha256 MATCH, exit 0). So the entry's load-bearing sentence — "running them
requires the operator's own installation … currently unobtainable from the lane host" — is
falsified by lane-held bytes alone. *Axis 1/7. Correction:* "no published source states the
version-pair condition; unblob declares the dependency (S110:49, S112) and the lane has observed
the pairing itself (r36 LE; r38 after-arm K1–K4; K4 4/4 reproduced at the pin)."

**D3 — "Flip: none" is right in kind, but the lesson gives no reason.** A pure snapshot claim has
a natural flip (the host loses the binaries again). What makes this entry unrecoverable is
provenance, and that is stronger than "the lane does not hold": **the cited tsv exists nowhere on
this host** — `ls -d /home/vgpnk/Projects/shokunin/lanes` → No such file or directory (exit 2);
`find /home/vgpnk/Projects/shokunin -name 'r7-local-measurements.tsv' -o -name
'lead2-avm-branch.tsv'` → no output (exit 0). *Axis 3.* The decision stands; say that.

## Findings — refusal 2 `sasquatch-unblob-avm-branch`

**D4 — "S189 is the unpinned `unblob/main` handler, while lane S108/S112 pin tag 26.6.4" is a
policy defect with no content behind it.** `main` and `26.6.4` are **byte-identical**:
`curl …/26.6.4/python/unblob/handlers/filesystem/squashfs.py | sha256sum` → `2d7b901b…9287` (the
S108/S112 digest, 590 lines); the same fetch from `main` → the same digest; `diff` → empty. The
unpinned ref is disqualifying because it can move, not because it says something else. *Axis 2.
Correction:* state the policy ground and add "identical to the pin today (sha256 `2d7b901b…`)", so
the refusal is not read as a version disagreement.

**D5 — the sibling "conflict" is shallower than the lesson says, and a better falsifier is
available.** `avm-image-extraction.md` does not show that the host *has* an AVM-capable tool; it
shows the tool is *buildable* from a tarball that is still served. Its closing premise ("a real
AVM image still needs a tool this host does not have") is nonetheless false, for a cheaper
reason: AVM publishes the real image. `https://download.avm.de/fritzbox/fritzbox-6490-cable/
other/fritz.os/` → HTTP 200, 592 B, listing `FRITZ.Box_6490_Cable-07.57.image`. *Axis 4.
Correction:* cite the published firmware index as the falsifier; cite the round-11 build as
"the tool is buildable, too" rather than as a contradiction.

**F1 — the flip is testable, cheaply, and half of it is already discharged.** "The branch is
re-measured on a lane-built AVM carrier with the source repinned to 26.6.4."
(i) *Branch half:* I copied `K4`, set the big-endian `mkfs_time` (offset 8) equal to `bytes_used`
(offset 40, = 307; four bytes changed), and ran unblob 26.6.4 with a PATH shim logging the child
argv. Control → `-be` present, 4/4 oracle files. Marker → **`-be` absent**, 0 files,
`ExtractCommandFailedReport` (child exit 1), stderr exactly the round-9 text: "…suggests a
SquashFS image of a different endianess / read_id_table: failed to read id table block / FATAL
ERROR: File system corruption detected". Decision logic and loud failure both reproduce at the
pin with no campaign byte and no build.
(ii) *Strict half:* `squashfs4.3.tar.gz` from the SourceForge path downloads (182550 B) with md5
**`d92ab59aabf5173f2a59089531e30dbf`** — the entry's own pin, exact — and Freetz-NG's pinned
`613-avm_format_as_option.patch` fetches (sha256 `9af3b3de…93f8`, contains `AVM_FORMAT_AS_OPTION`
and `-no-mkfs-time`). So "lane-built AVM carrier" is reachable too.
*Axis 5:* the flip is **not** untestable; it is a few seconds' work plus an optional build. The
"source repinned to 26.6.4" half is trivially satisfiable (main == pin anyway).

**F2 — ground (d) is true, verified.** The round-38 BE entry already carries the rule verbatim —
"It drops `-be` when `header.bytes_used == header.mkfs_time`, which is the AVM-BE marker (S114)"
— the pin's code has it at lines 48–50, and `AVM-BE-format.txt` re-fetches with the lesson's
digest `c1c43f6f…a5d5` carrying the equivalence at line 14. Nothing is lost by refusing the
staged entry; the refusal does not lower coverage.

## Findings — theme scan: the one skip no ground covers

**F3 — `sasquatch-prebuilt-package-inventory.md` is the only theme entry with zero provenance
defect, and it was skipped silently.** Its sources are public GitHub URLs, no campaign tsv. Every
claim reproduces live (2026-10-26): `releases.atom` (HTTP 200, 16794 B) lists **8** `sasquatch-v*`
tags (v4.5.1-6, -5, -4, -3, -2, -1, v1.0.1, v1.0), newest updated 2026-01-27T11:54:41Z;
`releases/expanded_assets/sasquatch-v4.5.1-6` (HTTP 200) lists exactly six assets,
`sasquatch_1.0_{amd64,arm64,armhf}.deb` plus `sasquatch-dbgsym_1.0_{amd64,arm64,armhf}.deb`. The
lane's delta if admitted: the release count, the architecture matrix, and the
package-version(`1.0`)/upstream-version(`4.5.1`) split — S107's scope cell carries only "asset
set, publish date and the amd64 package digest". Two counter-considerations a Gate row must
answer, not ignore: its `Caveats` still says the compatibility question "stays an operator
action" (stale — the lane observed it in rounds 36 and 38), and its `recheck` command hits the
GitHub API, which is **rate-limited today** (`http=403`, "API rate limit exceeded"), so admission
needs an unauthenticated recheck (atom feed + `expanded_assets`).
*Smallest correction:* add one Gate line — either admit with the caveat corrected and an
atom-based recheck, or refuse explicitly on duplication with S107's asset-set scope. Silence is
the only indefensible disposition, because it is indistinguishable from "not looked at".

**Coverage, stated honestly.** The theme is 11 files: 1 admitted (`unblob-format-matrix`),
2 refused (above), 1 is the staged twin of the lane's r36 `unblob-sasquatch-dependency`, and **7
carry no disposition line**. Six of the seven are tsv-sourced or unpinned-main
(`sasquatch-unblob-compatibility`, `avm-image-extraction`, `avm-image-build-blocker`,
`avm-le-variant-reachability`, `avm-le-image-genuine-marker`, `avm-firmware-image-unblob`), so
refusal-by-silence is defensible; but two of them are **actively falsified** rather than merely
unproven, and the Gate says neither: `avm-image-build-blocker`'s "not served from any mirror this
lane could reach" is false (I downloaded the exact tarball, md5 match), and
`avm-le-variant-reachability` is overturned by its own sibling `avm-le-image-genuine-marker`
("the round-12 conclusion … is wrong on both counts"). A reader of the Gate alone cannot
reconstruct that chain. One line per entry would close it.

## What I did not find

- No wrong refusal. Both entries fail on provenance the lane cannot repair from its own bytes
  (`F3`'s tsvs exist nowhere under `/home/vgpnk/Projects/shokunin`), and both carry premises that
  are false independently.
- No premature saturation introduced by this pass: AVM stays on the Frontier
  (`PROVINCE.md:157`), and F1 shows the frontier item is one cheap measurement away, not
  unreachable.
- No identity change: the binaries the lesson lists are the binaries on disk (sha256 match), and
  the `K4` carrier digest is unchanged (`a29ddc15…56ed`).

## Smallest safe corrections (in priority order)

1. Refusal 1, ground (a): date it. "False from 2026-10-26T01:22:37; true when taken (the entry's
   own caveat says snapshot). The refutation that matters is provenance."
2. Refusal 1, ground (b): replace "contradicted by S110:49 and S112" with the dependency reading,
   and add the lane's own observation (r36 LE; r38 after-arm; K4 4/4 at the pin).
3. Refusal 1, flip: say *why* it is none — the sole source is unreachable on this host, not merely
   outside the lane.
4. Refusal 2, ground (a): append "main is byte-identical to the pin today (`2d7b901b…`)".
5. Refusal 2, ground (c): cite the published AVM firmware index as the falsifier of the closing
   premise; keep the round-11 build as a secondary witness.
6. Refusal 2, flip: record that it is cheap — a 4-byte patch on `K4` reproduces the branch, and
   the strict route's tarball still matches its pin — so a later round can discharge it instead of
   re-refusing.
7. Gate: add disposition lines for the 7 undispositioned theme entries, naming the falsified two.

## Reproduction (all read-only; no REA, no VCS mutation, nothing installed)

```
S=/fast/scratch/hyaku/kaidoku-r38/R38W2AssimRejects   # removed at exit
ls -la --time-style=full-iso ~/.local/bin/{sasquatch,sasquatch-v4be,unblob}; sha256sum ~/.local/bin/sasquatch*
~/.local/bin/unblob --version; ~/.local/bin/unblob --show-external-dependencies
python3 -V; python3 -c 'import unblob'                       # 3.14.8 / ModuleNotFoundError, exit 1
curl -fsS https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/README.md | sha256sum
curl -fsS https://raw.githubusercontent.com/onekey-sec/unblob/{26.6.4,main}/python/unblob/handlers/filesystem/squashfs.py
# branch: copy K4 -> control.bin; patch BE u32@8 := BE u64@40 (=307) -> avm-marker.bin
# shim dir first on PATH logging argv, then:
unblob -e out --report rep.json --log log.txt control.bin    # argv has -be, 4/4 oracle MATCH
unblob -e out2 --report rep2.json --log log2.txt avm-marker.bin  # argv has no -be, 0 files
curl -fsSL https://downloads.sourceforge.net/project/squashfs/squashfs/squashfs4.3/squashfs4.3.tar.gz | md5sum
curl -sS https://github.com/onekey-sec/sasquatch/releases.atom
curl -sS https://github.com/onekey-sec/sasquatch/releases/expanded_assets/sasquatch-v4.5.1-6
ls -d /home/vgpnk/Projects/shokunin/lanes; find /home/vgpnk/Projects/shokunin -name 'r7-local-measurements.tsv'
```

No frozen predicate, counter, carrier, oracle or staged file was modified; nothing was written
outside this report and its two artifacts; scratch removed on exit. No tool was installed or
upgraded (unblob 26.6.4, sasquatch 4.5.1 already present; GitHub API left rate-limited rather
than authenticated).
