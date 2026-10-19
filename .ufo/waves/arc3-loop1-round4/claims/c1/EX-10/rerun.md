# EX-10 — id-stability rerun (arc3-loop1-round4, 2026-10-19)

Seat EX-10 · chain c1 · role executor. Task (seat line): rerun id-stability —
repeat EX-06's exact invocation twice; compare envelopes; record id behavior
(per the r3 entry's path-sensitivity caveat).

Repo HEAD at work: `015e1bab914713568f339fd53999bc180459cc40`. No git mutations,
no repo writes outside this seat's dir; scratch `/var/tmp/ex10-r4` only. The
custody target (`.ufo/gates/custody-pair/`) was never touched.

## 1. Target and baseline (established before any rerun)

EX-06's r3 exact invocation, from
`.ufo/waves/arc3-loop1-round3/claims/c1/EX-06/evidence/probe-log.txt` (and
`battery-log.txt` line 1):

```
TMPDIR=/var/tmp/ex06-r3/tmpdir npx -y rea-agents@6.4.0 inspect-evm-interface \
  .ufo/waves/arc3-loop1-round1/claims/c1/RV-2/Rv2Token.runtime.hex hex --format json
```

cwd = repo root; relative argv; the r1 canonical recheck line. Target
`RV-2/Rv2Token.runtime.hex` read-only identity: 3,886 B, sha256
`d7f73058e2d9fb2563bf96b2f26902f233530de027a7943185e15bfdc4e1048f`, inode
36477115, mtime 2026-10-19 07:00:40 -0300.

Sealed baselines (read-only hashes, `evidence/analysis.txt` §A):

- r1 canonical capture `.ufo/waves/arc3-loop1-round1/claims/c1/RV-2/probe-runtime-hex-6.4.0.json`
  — sha256 `f2aec424c1edade81d7bbe58f0d99be7f5d2253749ffb09e9a2a4226425f42f8`,
  id `ev_45849c8b11794ea0b007bd01ea3241aa9b385ca7543e514a16e82c795a106eaf`
- EX-06 r3 recheck `…/arc3-loop1-round3/claims/c1/EX-06/evidence/recheck-rv2token-hex-6.4.0.json`
  — **byte-identical** to the r1 capture (same sha256, same id).

## 2. What was run

Five batteries, 22 envelopes, every leg's verbatim command in
`evidence/battery*-log.txt`; envelopes + stderr in `evidence/`.

- **Battery 1** (`run-battery.sh`): the EX-06 invocation repeated twice, plus
  TMPDIR (3 values incl. EX-06's own `/var/tmp/ex06-r3/tmpdir`), argv spelling
  (relative / `./`-prefixed / absolute) and cwd (`/var/tmp/ex10-r4/work`) variants.
- **Battery 2** (`run-battery2.sh`): scratch-copy controls — byte-identical copy
  at another path; symlink to the repo file; fixed scratch path with mutated
  bytes (+`0x00` to the hex text).
- **Battery 3** (`run-battery3.sh`): pin 6.7.0, same invocation, twice.
- **Battery 4** (`run-battery4.sh`): hard-link pair (same inode, two paths);
  path recreated (new inode, same bytes); mtime set to 2020; then bytes mutated.
- **Battery 5** (`run-battery5.sh`): EX-06's `probe-log.txt` line **verbatim**
  (TMPDIR=/var/tmp/ex06-r3/tmpdir included), twice.
- **Shape leg**: `--full-output` wrapper on the exact request (id identical;
  wrapper keys `{ok,data,meta}`).
- **Bounded formula probe** (`idformula.py`): 1,680 candidate hash forms.

## 3. Result — repeat/rerun behavior

**The two repeats (and four more exact reruns) re-derived the sealed envelope
byte-for-byte**: 9,399 B, sha256 `f2aec424…`, id `ev_45849c8b…` — equal to both
the r1 canonical capture and EX-06's r3 recheck. All six exact reruns landed in
one id group; the `--full-output` shape re-derived the same id. 6.7.0 repeated
twice also byte-identical (`12e5d171…`, `ev_19d7d3cb…`), matching r1's
`probe-6.7.0-rerun.json` (same sha256 and id, 4 h apart).

**id STABLE across**: repeat runs (×6), TMPDIR value (3 distinct dirs incl.
EX-06's), cwd (2 values), argv spelling (relative / `./`-prefixed / absolute),
**inode identity and link count**, **mtime**, and pin-internal rerun.

**id CHANGES with**: resolved path (byte-identical copy elsewhere → `ev_4899d147…`),
carrier bytes at a fixed path (→ `ev_8bff5c7d…`), encoding form, pin (6.4.0 vs
6.7.0), verb-family request (r3 measurements).

**Discriminator (new this round):** the hard-link pair — same inode, same bytes,
different path — minted **different ids** (`ev_ed1452cc…` vs `ev_4364a3bf…`),
while recreating the same path with a **new inode** re-derived the **same id**
(`ev_ed1452cc…`). The id's path input is therefore the **resolved path as recorded
in `parameters.path` / `subject.local_path`** — not the raw argv spelling, not
the inode, not mtime. This sharpens the r3 caveat from "path-sensitive" to a
measured path-keyed (not inode- or content-keyed) identity.

**Content-identity anchor:** every leg's decoded
`normalized_result.bytecode.sha256` equals `c1081a56…` for the pinned carrier
bytes, including the altpath and hard-link legs where ids differ — so the
r3 entry's advice (compare by decoded bytecode sha256 + payload, not by `ev_`
id) is exactly right and now demonstrated on the same carrier where the ids
*do* diverge.

**Normalized payloads:** 0 field diffs vs `exact-r1` for every same-path leg;
the altpath/hard-link legs differ only in the three path fields (+`subject.name`
when the basename changes).

## 4. Attacks / refutations attempted, with verdicts

- **"Is the rerun id-stable, or does it drift with time/run?"** — REFUTED as a
  drift source: six exact reruns across ~2 minutes, plus r1's own reruns ~4 h
  earlier, all byte-identical.
- **"Does the id key on inode/mtime rather than path?"** — **REFUTED**: hard-link
  pair (same inode, different path) → different ids; recreate (new inode, same
  path) → same id; mtime 2020 → same id. Path-keyed, not stat-keyed.
- **"Is `ev_` a content-addressed id?"** — REFUTED again (byte-identical copy at
  a different path mints a new id; mutated bytes at a fixed path mint a new id).
  Content identity must be read from `normalized_result.bytecode.sha256`.
- **"Can the id be derived from the request fields?"** — **HONEST NEGATIVE**:
  1,680 candidate forms (11 fields × 7 algorithms × 7 separators, plus JSON
  canonicalizations, singles through 4-tuples) — **0 hits** (`idformula.txt`).
  No formula claimed; derivation unproven, consistent with the r3 honest-stop form.
- **Symlink input** — NEW typed finding: a symlink pointing at the target is
  refused fail-closed, `invalid_request` / `invalid_format`, message "Expected a
  regular file without a symlink", exit 1, no id minted (`b2-symlink.json`).
  A symlinked carrier path cannot be probed at all.
- **Mutated bytes at a fixed path** — the id moves and the decoded bytecode sha
  moves with it; the file's own sha256 is re-reported in `subject.digest.sha256`
  (`93d6d335…`) — so a stale id cited against a re-written file is detectable
  from the envelope alone.
- **r3 entry's path-sensitivity caveat** — CONFIRMED and extended, not falsified.
  The caveat's "compare by decoded bytecode sha256 + payload" remedy is
  re-verified as the correct comparison discipline.

## 5. Before → after for the chain's C1 claim

- **Before** (seat start 14:04Z): the id-stability question rested on r3's
  measurements (repeats within one sitting); the r1→r3 cross-round re-derivation
  had been observed once (EX-06, SC-2) but never at r4; the id's path-input was
  described as "path-sensitive" without an inode/mtime discriminator; symlink
  behavior was unmeasured.
- **After** (14:04–14:07Z): 6 exact reruns + 1 `--full-output` shape leg + 2
  6.7.0 legs re-derived sealed envelopes byte-for-byte; the path-vs-inode-vs-mtime
  discriminator is resolved (path-keyed); the symlink refusal is a typed class;
  the id formula is falsified as derivable among 1,680 tested forms (honest
  negative). All measurements are re-derivable from the sealed manifest
  (`evidence/MANIFEST.sha256`, 60 entries, `sha256sum -c` all OK).
- **Repo effect:** none — this seat wrote only under its own claims dir; command A
  and the corpus are untouched by construction (0 repo writes outside the seat dir).

## 6. Blockers

None. Gaps named: (a) the id derivation is not proven — only its sensitivity axes
are measured; the honest-stop form stands; (b) the symlink refusal's scope is
measured on one verb family only; (c) the path key's normalization (symlink
resolution is impossible to observe since symlinks are refused; `..`-containing
spellings untested) remains an Unknown.
