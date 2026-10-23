# Round-30 routed defect 7 — correction draft

Report assembled 2026-10-23T04:12:26Z. Scope: correct the restore-time statement in `w1/RevOracleVsReadobj.md:15` using the cited round-30 lesson, verifier spotcheck, and all `CtlC1*.md` reports.

## Finding

**Observation:** `RevOracleVsReadobj.md:15` says the four carriers were restored “at ~02:46Z.” The verifier spotcheck instead says the restored files carried 02:44:00Z mtimes and reruns passed the input pin from 02:44:44Z (`round-30-verifier-spotcheck.md:37`). The control reports corroborate successful post-repair measurements beginning at 02:44:44Z, 02:44:52Z, 02:44:58Z, 02:45:05Z, and 02:45:41Z. **Inference:** the restore was complete no later than 02:44:44Z; the evidence does not support “~02:46Z.”

**Draft line for the end of `corpus/lessons/round-30.md` (not appended; lane remains read-only):**

Correction (round 31): The shared-carrier restore was complete no later than 02:44:44Z, not “~02:46Z”: restored-file mtimes are 02:44:00Z and the input pin passed from 02:44:44Z; the first post-repair C1 measurements began at 02:44:44Z (AllFalse), 02:44:52Z (JunkRow), 02:44:58Z (ShortcutIds), 02:45:05Z (NoReader), and 02:45:41Z (DoNothing) (`round-30-verifier-spotcheck.md:37`; `CtlC1AllFalse.md:113`; `CtlC1JunkRow.md:98`; `CtlC1ShortcutIds.md:73,147,195`; `CtlC1NoReader.md:90`; `CtlC1DoNothing.md:94,102`).

## Evidence and run records

The report excerpts below were obtained with local `functions.read` calls. That tool returns file excerpts but exposes neither a per-call process exit code nor a per-call UTC timestamp; the report assembly time above is recorded separately. For the underlying counter evidence, exact producing commands are recorded in the cited control reports; quoted run times and exit statuses below are those reports' observations, not newly executed runs.

- **Source statement:** `RevOracleVsReadobj.md:15` — “restored all 4 from wheel members at ~02:46Z and set chattr +i”.
- **Bound:** `round-30-verifier-spotcheck.md:37` — “The restored files carry 02:44:00Z mtimes, and reruns pass the input pin from 02:44:44Z.” `round-30-verifier-spotcheck.md:41` explicitly flags the ~02:46Z inconsistency. The lesson's M30-2 row (`corpus/lessons/round-30.md:45`) independently records restoration at 02:44:00Z (inode ctime).
- **Earliest passing-pin counter:** CtlC1AllFalse's exact command is recorded at `.ufo/waves/round-30/w1/CtlC1AllFalse.md:105` (`env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE TMPDIR=/fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/tmp timeout 900 python3 -I -B /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone/tools/round-30/c1-rust-positive.py --root /fast/scratch/hyaku/kaidoku-r30/seats/w1/CtlC1AllFalse/clone --rev main`). Its repaired run starts 2026-10-23T02:44:44+00:00, ends 02:44:58+00:00, counter exit 1 (`:113`); stdout proceeds to `P1-fail committed envelope absent or not added after the freeze` (`:128-129`), rather than stopping at PIN.
- **Other first post-repair measurements:** CtlC1JunkRow's command is `.ufo/waves/round-30/w1/CtlC1JunkRow.md:68`; its measured run is 02:44:52Z–02:45:07Z, exit 1 (`:98`), with a per-carrier P1 result (`:101`). CtlC1ShortcutIds' command is `.ufo/waves/round-30/w1/CtlC1ShortcutIds.md:150`; the report says the counter passed pinned-input checks (`:73`) and records the run at 02:44:58Z–02:45:12Z, exit 1 (`:147,195`). CtlC1NoReader's command is `.ufo/waves/round-30/w1/CtlC1NoReader.md:67`; its rerun is 02:45:05Z–02:45:18Z, exit 1 (`:90`) and reaches per-carrier P1 results (`:93`). CtlC1DoNothing's command is `.ufo/waves/round-30/w1/CtlC1DoNothing.md:99`; its rerun is 02:45:41Z–02:45:52Z, exit 1 (`:102`) and reaches per-carrier P1 results (`:107`). These are the documented passing-pin runs; the earlier PIN-blocked attempts are not treated as successful measurements.

## Gates and touched surfaces

- Read-only source review only; no subagents, REA, carrier/mutant access, build/test/lint, or external source fetch. No tools were installed or updated.
- Only this scoped report was written. `corpus/lessons/round-30.md` and all other lane files were left unchanged; no Git/jj writes were made.
- No scratch scripts, drafts, raw outputs, clones, or other artifacts were created under `/fast/scratch/hyaku/kaidoku-r31/seats/w1/`.
- No counter target was evaluated by this seat. The control measurements below are cited existing evidence, not executions by this seat.

## Local source provenance

Access date for these local source files: 2026-10-23. SHA-256 values were collected with `timeout 30 sha256sum` over the absolute paths below; the hash tool returned all listed digests, but its result did not expose a numeric exit-code field. Quotes are located excerpts (each ≤25 words).

| Source URL | SHA-256 | Located quote |
|---|---|---|
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/RevOracleVsReadobj.md` | `88b6aaf9e645bf9e472f4e0241c857359a3fe685afb5967bcb8c8731e8e14fac` | line 15: “restored all 4 from wheel members at ~02:46Z and set chattr +i” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-30.md` | `95817c8ac7f2fe0fce170e68c7983c1962fdd7318b787579996cc23f7c576068` | line 45: “Carriers restored from the verified wheel members and set chattr +i at 02:44:00Z” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/lessons/round-30-verifier-spotcheck.md` | `e9b49ccc2f29316d399b533374e59eec1bdbd046a2bb47f13d8ab4a16135ae75` | line 37: “The restored files carry 02:44:00Z mtimes, and reruns pass the input pin from 02:44:44Z.” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CtlC1AllFalse.md` | `b732e878bbbaec0eb05aa274e7cfc1922e7381ba443ab021816678f815e5790b` | line 113: “pristine-repaired … 2026-10-23T02:44:44+00:00 → 2026-10-23T02:44:58+00:00 | 1” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CtlC1DoNothing.md` | `500c9fc50e697a53c9d7e9699f54be801987f3bd8ab6c42ec018fa679db0aa90` | line 102: “UTC start: 2026-10-23T02:45:41+00:00. UTC end: 2026-10-23T02:45:52+00:00. Counter exit 1.” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CtlC1NoReader.md` | `e9af5526f5910b50dfdcb7fdeb1089b934594df13f907a9d99b54d31828e5f14` | line 90: “2026-10-23T02:45:05Z–02:45:18Z; counter exit 1.” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CtlC1JunkRow.md` | `f33fb54127dbf5a956649a31cb918eccbe859864af91ca0acd01f8dec8ff6279` | line 98: “2026-10-23T02:44:52Z–2026-10-23T02:45:07Z; counter exit 1.” |
| `file:///home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-30/w1/CtlC1ShortcutIds.md` | `203727e5dd6a86266ca548dc290d5dfc753bd50374820a4d002d36ea2fcd3708` | line 73: “The contaminated control counter run passed the pinned-input checks and measured all 16 carriers” |

Report: .ufo/waves/round-31/w1/ScribeR30Restore.md