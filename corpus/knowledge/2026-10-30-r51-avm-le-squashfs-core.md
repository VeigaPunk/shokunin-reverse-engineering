source: S250 — https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/unsquashfs.c :1287-1318,:1320-1363 (tag 4.7.5)
source: S251 — https://raw.githubusercontent.com/plougher/squashfs-tools/4.7.5/squashfs-tools/mksquashfs.c :7113 and companion mksquashfs_help.c :467
verified-at: 2026-10-30 (source review and committed-receipt inspection only; no R51 REA data run)
recheck: Open the S250/S251 tag-pinned URLs and compare the named branches; for registry scope run python3 -I -B tools/round-51/census3.py --root . --rev <REV> --check

# LE AVM accounting prerequisites — NOT promoted (round 51 honest stop)

**Status:** the filename was declared before the build wave; it is not a Core claim.
R51-C1's four-carrier measurement was not completed. LE AVM members (`hsqs`)
remain Frontier. This entry preserves the source corrections discovered while
constructing the proposed re-freeze, not an extraction capability acquisition.
R51-C2's triage v6 and its independent falsification are also unverified.

## Device kinds are not interchangeable

At tag 4.7.5, `unsquashfs.c:1287` enters `if(root_process)` before attempting
`mknod` with `S_IFCHR` or `S_IFBLK` (`:1296-1297`). The other branch reports
`not superuser` and goes to `failed` (`:1313-1318`). This is an explicit
**char/block-device privilege boundary**, not a rule about every non-file inode.

FIFO (`:1328`) and socket (`:1349`) creation call `mknod` outside this root test.
Thus the proposed explanation “an unprivileged extraction cannot mknod, so
char-device/fifo/socket rows all disappear” is rejected. The source does not
prove those two kinds disappear. The lane must distinguish the mechanisms and
observe the operative extractor before assigning a disposition to an untested kind.

S250 is upstream source, not REA's result schema and not proof of the installed
sasquatch binary's behavior. The wave's synthetic non-root probe corroborates the
char-device refusal only (`.ufo/waves/round-51/w1/ExecRuleDerive/probe.md`).

## What the existing carriers show, and what they do not

The committed round-50 nonregular tables have one char-device on each Cable
carrier and thirteen on each FRITZ!Box carrier. The existing envelopes have no
published-file, gap or removal disposition for those device rows. These are
**historical observations**, not a new run:

- Inputs: `tools/round-50/oracle/*.nonregular.tsv` and
  `corpus/evidence/round-50/c1/{c6430,c6490,g7581,g7582}/after.json`.
- Counting command and output: `python3 -I -B .ufo/waves/round-51/w1/ExecOfflineGrammar/disposition-dryrun.py`
  (2026-10-30), receipt `.ufo/waves/round-51/w1/ExecOfflineGrammar/dryrun.stdout`.
  Old disposition rule: 2/4; proposed relaxed rule: 4/4. That is a rule-scoped
  comparison, **not** the full carrier predicate or a new extraction result.
- The round-50 miss also contains `g7581:projection_ok false`, separately from
  its gap-accounting miss. The ENOENT/readlink diagnostic does not by itself
  establish a retry-safe environmental race. No new retry policy is admitted.
- A depth-limited receipt does not prove a device-only subtree was visited.
  The absence of a published path cannot alone establish why it is absent.

## Padding is a producer option, not a reader witness

S251's actual upstream option is **`-nopad`**, not `-no-pad`.
`mksquashfs_help.c:467` says “do not pad filesystem to a multiple of 4K”.
This describes the writer's output padding. It does not identify the producer
of a shipped image, certify a DD-WRT body as readable, or provide a discriminator
inside a normalized REA envelope that lacks those bytes.

The proposed v6 routing needs an explicit reader-support/provenance mapping.
A clean extraction is not independent-reader success; the failed DD-WRT body's
route cannot be repaired by asserting that its other readers succeeded.

## Registry census scope is separate

`census2.json` is correct under its historical claims-naming scope; it is not
made false by later registry rows. The new `census3.py` inventories the marker-bound
registry in both directions against `census3.json`. It diagnoses registry inventory
only. It neither replaces the frozen `meanings.py` consumer nor makes R51-C2's
triage/executability target pass. See `corpus/lessons/round-51.md`.
