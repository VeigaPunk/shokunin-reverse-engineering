# W2Skill — round 49 wave 2 (post-landing): SKILL.md decision table and PROVINCE Core row

Revision attacked: `29883d4ec35a31a8393c4ffb220888c44c0bb022` (lane `main`), read only from git objects.
Scope: `SKILL.md` decision table, queue-drain craft section, SquashFS triage table v4 (the table the
reader is routed to from `Firmware blob`), and the `squashfs_v1`/`squashfs_v2` row in `PROVINCE.md`.
Not run by this seat: the frozen C1/C2 counters (other seats own them); no REA run on any image.
Scratch receipts and copied artifacts: `.ufo/waves/round-49/w2/W2Skill/` (`receipts.tsv`,
`receipts-triage.tsv`, `probes/`, `*.at-29883d4e*`).

## Verdict

**Does not pass the skill-surface check as landed.** The landing did not touch `SKILL.md` at all
(its sha256 at the base `e4f2cfa5` and at the landing is identical), so the decision table still
routes SquashFS through a generic `Firmware blob` row with status `held r4u`, and the only
SquashFS-specific guidance is the v4 triage table. Two measured defects follow from that:

1. **The v4 triage table mis-routes `squashfs_v2_nonstandard`.** Its `legacy-body-failure` row
   matches every `squashfs_v[123]*` handler, including the v2ns handler that has no independent
   reader. On a healthy v2ns body both independent readers fail, so the row's own rule would call
   the body damaged.
2. **The landed PROVINCE Core row is wider than the scored claim and not actionable.** It says
   "SquashFS v1 and v2, gzip bodies, both byte orders", with no v1.0/v2.0 limit, no v2.1 exclusion,
   no command, no expected result and no refusal signature. The README row and the entry state the
   narrower scope; PROVINCE does not.

Further items (F2, F5–F10) are dated-supersession or wording fixes. Proposed wording for every
SKILL line that needs a note is in section 3; nothing was edited.

## 1. Findings table

Each row names what it attacks, the exact command, exit code, and the sha256 of the captured output
(`receipts.tsv` / `receipts-triage.tsv` hold the same values with UTC times, 2026-10-28T22:45Z).

| ID | Sev | Attacks | Finding | Evidence (command → exit, stdout sha256) |
|---|---|---|---|---|
| F1 | HIGH | SKILL.md:535 `legacy-body-failure` row, failing-handler glob `squashfs_v[123]*` | Glob matches `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`, `squashfs_v3_nonstandard`. Entry `corpus/knowledge/2026-10-28-r49-squashfs-v1v2-core.md:102-104` says these have no independent reader or only a partial one. Row text: "if the independent readers fail where sasquatch failed the body is damaged and the failure stands". On a **healthy** v2ns body both readers fail, so the rule condemns a good body. | `/usr/bin/unsquashfs -lls v2ns-le--squashfs_v2.0_le.bin` → **1** (`Can't find a valid SQUASHFS superblock`); stdout sha `e3b0c442…` (empty), stderr sha `4bca0ea7…`; `7z l -tSquashFS v2ns-le…` → **2**, stdout sha `af93eab0…`. `v2ns-be…`: unsquashfs **1** (stdout `e3b0c442…`, stderr `c774bb13…`), 7z **2** (stdout `495276…`). Fixture sha256: v2ns-le `f25cf3ea531de5c1…`, v2ns-be `6560be64cb26ed19…`. Interpreter on a synthetic probe (healthy v2ns envelope, `files` emptied, one `extractor-failure` gap with handler `squashfs_v2_nonstandard`): `sqfs-triage-v4.py --skill SKILL.md --json synthetic-v2ns-body-failure.json control-v2ns-clean.json` → **0**; probe → `legacy-body-failure` / `cross-read-legacy`; control → `clean` / `none`; stdout sha `976207e0…`. The probe is a relabelled healthy envelope: it shows the label, not a real REA failure. |
| F2 | MEDIUM | SKILL `clean` row (craft table v4) | The `clean` row says "nothing to install or fix; match files to the oracle". For `squashfs_v2_nonstandard` there is no oracle (F1), yet the four committed v2ns recon envelopes at `ddefault` (`squashfs_v2_nonstandard_squashfs_v2.{0,1}_{le,be}_ddefault`) label `clean`/`none`. PROVINCE says the same family is Frontier. Two sections of the reader's own guidance disagree. | `sqfs-triage-v4.py --skill SKILL.md --json <126 R42C2ReconLegacy envelopes>` → **0**, stdout `labels-r42-recon.json` sha `0d4a269f…`; the four v2ns `_ddefault` rows read `clean`/`none`. |
| F3 | HIGH | PROVINCE.md:436 Core row, surface cell and r49 frontier note (line 438) | Surface says "SquashFS v1 and v2, gzip bodies, both byte orders", unscoped. Scored set is v1.0 and v2.0 only (`tools/round-49/carriers.json` `scope.target_ids` = v1le, v1be, v2le, v2be). The v2.1 pair is "UNBOUND exploratory data, NOT scored" (`scope.exploratory_ids` v21le, v21be). Round-42 recon labels v2.1 envelopes under handler `squashfs_v2` (`squashfs_v2_squashfs_v2.1_le_ddefault`: `chunks[0].handler = squashfs_v2`, 4 files, gaps `[]`), so a v2.1 reader is routed to Core by this row. The landed README row (`corpus/README.md:105`, "v1.0 le/be, v2.0 le/be; 4 KiB each") and the entry (`:119`, "Four 4 KiB fixtures… not that every v1/v2 image extracts") are narrower; PROVINCE is the only landed surface that is not. The entry's "What stays Frontier" list does not name v2.1 either. | `git show 29883d4e:tools/round-49/carriers.json` sha `829e3392…`; `sqfs-triage-v4.py --json …squashfs_v2.1_le_ddefault/envelope.json` label `clean`. PROVINCE sha `3964d90d…`, README sha `2636ff42…`. |
| F4 | HIGH | PROVINCE.md:436 Core row, "Probe" and "Ports / keys" cells | Not actionable. (a) Probe cell names only the counter `tools/round-49/c1-counter.py`, which a reader cannot run on their image. (b) No command: the frozen counter's REA argv is `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output …` with `REA_UNBLOB_COMMAND` = unblob 26.6.4 and a child PATH holding sasquatch 4.5.1 (`tools/round-49/c1-counter.py:1893-1897`); none of it is in the row. (c) No expected result: `chunks[].handler` = `squashfs_v1`/`squashfs_v2`, `extraction_gaps == []`, published `firmware.bin_extract/` regular files equal to the `unsquashfs -lls` census (3/3/4/4 files). (d) No refusal signature: `missing-extractor-dependency` with `dependencies: ["sasquatch"]` (→ `install-extractor-le`); `extractor-failure` with zero files (→ `legacy-body-failure`). (e) No depth note: scored receipts used `max_depth: 3` (`corpus/evidence/round-49/c1/v1le/after.json` parameters), and the round-42 recon shows `depth-limited` at `--max-depth 1` for both v1 and v2 (`squashfs_v1_squashfs_v1.0_le_d1`, `squashfs_v2_squashfs_v2.0_le_d1` → `depth-limited` / `raise-depth`). The entry's "Commands" table lists only the `unsquashfs`/`7z` probes, not the REA argv. | `c1-counter.py` argv lines 1893–1897 (rev); `labels-r42-recon.json` sha `0d4a269f…`. |
| F5 | MEDIUM | SKILL.md:57 decision-table row `Firmware blob` | Status `held r4u` is unscoped. The decision table has no SquashFS row. A reader who routes a SquashFS image through this row sees `held r4u` for the whole `extract-firmware` verb, which after r49 still excludes v2.1, v2ns, v3 broadcom/nonstandard, LE AVM and kernels, and says nothing about the s_minor-0 v1/v2 promotion. | `grep -in 'firmware\|unblob' SKILL.md` → lines 3, 57, 64, 73, 95, 97; none is a per-family SquashFS status. SKILL sha unchanged (F7). |
| F6 | LOW-MED | SKILL.md:64 decision-table row `AppImage inner` | Route "unblob carve → `7z` on squashfs → inner asar analyze", status `held r4`. After r49 a reader may take `7z` as the extraction route for v1/v2 payloads. The entry (`:56`) says 7-Zip is corroboration only. AppImage-embedded v1/v2 is not measured. | `7z l -tSquashFS v2-le--squashfs_v2.0_le.bin` → **0** (4 files); a listing, not an extraction oracle. Stdout sha `5a6698a2…`. |
| F7 | LOW | Landing scope: SKILL.md unchanged; PROVINCE.md:156–157 sasquatch bullet | `git show e4f2cfa5:SKILL.md` and `git show 29883d4e:SKILL.md` both sha `d6f4e265…`; `git diff --stat e4f2cfa5 29883d4e -- SKILL.md` empty. PROVINCE +8 lines, README +3. The round-4 sasquatch bullet says "7z fallback covers the carved-image path today" and carries bracketed dated supersessions for v4 only, none for v1/v2. | `git diff --stat …` → PROVINCE 8, README 3, SKILL 0. |
| F8 | LOW | SKILL.md:523 table-v4 status line | "Status — unscored claim … round 43 re-scores it under P43-C1". The only later mention in SKILL is the registry row (`:1742`); no result is linked, so a reader cannot tell whether table v4 is still unscored. Not an r49 defect; flagged because the landing is the first SKILL-surface review since. | `grep -n 'P43-C1\|unscored' SKILL.md` → 523 only, plus the registry row. |
| F9 | LOW | SKILL.md:535 `legacy-body-failure` action "if either lists the tree … reinstall the extractor" | 7-Zip lists the LE broadcom fixture (2 files, entry `:103`) while `unsquashfs` refuses it. A 7-Zip listing of a damaged or mis-read body would send the reader to "reinstall sasquatch" when the body is at fault. [INFERENCE: not measured on a damaged broadcom body.] | Entry `:103` (receipt `v3-readers`); not re-run by this seat. |
| F10 | LOW | PROVINCE.md:424–430 `## Round-44 measured, not promoted` | Heading and row still read "measured, not promoted"; the supersession is only in the r49 frontier note at line 438. Dated and explicit there, so acceptable. An arrow in the r44 heading would make it findable. | `sed -n 424,438p PROVINCE.md` at rev. |

Checks that passed (so the reader can trust the rest):

- **Triage table v4 parses.** `python3 -I -B sqfs-triage-v4.py --skill SKILL.md --table-only` at rev →
  **0**, 15 rules, marker line 525, table line 527, stdout sha `f0bc0a9b…`.
- **Frozen fixtures match the PROVINCE and entry pins.** `git show 29883d4e:corpus/evidence/round-42/c2/fixtures/<f> | sha256sum`:
  v1-le `b45925fa…`, v1-be `529e1077…`, v2-le `7c62dbe3…`, v2-be `79c0f388…`, identical to the Core row's
  `V1LE`/`V1BE`/`V2LE`/`V2BE` pins and to `carriers.json`. Expected member counts 3/3/4/4 match.
- **Reader agreement on the scored family.** `unsquashfs -lls v2-le…` **0**, `7z l -tSquashFS v2-le…` **0** (4 files).
- **Entry is careful where PROVINCE is not**: its "What stays Frontier" list (`:96–105`) names v2ns, v3 broadcom/nonstandard and gzip v3 correctly.

## 2. Answers to the attack questions

- **Does any row mislead now?** Yes, two. `legacy-body-failure` (F1) and `clean` (F2) both give v2ns actions that the landed Frontier status contradicts. `Firmware blob` (F5) and `AppImage inner` (F6) do not say what changed for v1/v2. No row says v1/v2 needs a 7z fallback: the 7z mention is the AppImage route (F6) and the cross-read action.
- **Does the PROVINCE Core row give an actionable decision?** No (F3, F4). It gives the handler names and the counter; it gives no command, no expected result and no refusal signature, and it is unscoped to s_minor 0.
- **Which SKILL lines need a dated supersession note?** Section 3.

## 3. Proposed dated supersession notes (not applied)

Nothing below was edited. Each is wording for the L1 to place. Machine-read table cells are unchanged;
any note must sit outside the table and after its last row, and `sqfs-triage-v4.py --table-only` must be
rerun after the edit.

**SKILL.md:57 (`Firmware blob`, status cell)** — append:
> ; SquashFS, per handler (2026-10-28, round 49): `squashfs_v1` and `squashfs_v2` at s_minor 0 on the standard fixtures are Core (PROVINCE `## Round-49 additions to Core`). v2.1, `squashfs_v2_nonstandard`, `squashfs_v3_broadcom`/`_nonstandard`, LE AVM and the other rows in PROVINCE Frontier stay Frontier. This status is not a per-family claim.

**SKILL.md:64 (`AppImage inner`)** — append:
> [2026-10-28] For a squashfs_v1/v2 payload, 7-Zip is a listing corroborator (r49 entry, oracle section), not the extraction route. The r49 Core route is REA `extract-firmware` on a bare image; no v1/v2 measurement exists inside an AppImage.

**SKILL.md:523 (table v4 status)** — either link the round-43 P43-C1 result, or keep the line and append:
> [2026-10-28] No round-43 result is linked here; the status stays "unscored claim" until one is.

**SKILL.md, after the last row of the v4 table (`sqfs-triage-table v4`)** — insert a dated note:
> **Note, 2026-10-28 (round 49).** `squashfs_v[123]*` also matches `squashfs_v2_nonstandard`, `squashfs_v3_broadcom` and `squashfs_v3_nonstandard`. These have no independent reader or only a partial one (r49 entry, "What stays Frontier": on the healthy `v2ns` fixtures `unsquashfs` 4.7.5 exits 1 and 7-Zip 26.04 exits 2). For those handlers the cross-read cannot decide: if both readers fail on a healthy image, the "damaged" clause of `legacy-body-failure` does not apply. Route to Frontier and keep the envelope; never read a both-fail cross-read as proof of body damage. The `clean` row presumes an independent oracle; for a handler with none, a clean envelope is unverified, not Core. `squashfs_v2_nonstandard` envelopes that label `clean` are unverified.

**PROVINCE.md:157 (round-4 sasquatch bullet)** — append:
> [2026-10-28 round 49: `squashfs_v1`/`squashfs_v2` at s_minor 0 on the standard fixtures are Core, `## Round-49 additions to Core`; there 7-Zip is corroboration, not the route.]

**PROVINCE.md:436 (Core row, surface cell)** — the scope and the action cell it needs:
> Surface: `squashfs_v1` and `squashfs_v2` at s_minor 0 (SquashFS v1.0/v2.0, gzip bodies, both byte orders) on the four standard 4 KiB single-block fixtures. v2.1, `squashfs_v2_nonstandard` and every other SquashFS handler are not claimed.
> Action: `REA_UNBLOB_COMMAND=<unblob 26.6.4>` and a child PATH holding `sasquatch` 4.5.1, then `npx -y rea-agents@6.5.0 extract-firmware --format json --full-output <image> <fresh-outdir>` (argv prefix from `tools/round-49/c1-counter.py:1893-1897`). Expected: every chunk handler is `squashfs_v1` or `squashfs_v2`, `extraction_gaps` is empty, and the published `firmware.bin_extract/` regular files equal the `unsquashfs -lls` census by path and sha256. Refusals: `missing-extractor-dependency` with `dependencies: ["sasquatch"]` → install sasquatch 4.5.1 on that PATH (SKILL `install-extractor-le`); `extractor-failure` with zero files → SKILL triage v4 `legacy-body-failure`; `depth-limited` → raise `--max-depth` (the scored receipts used 3; `--max-depth 1` gives `depth-limited` on v1/v2 recon envelopes).

**PROVINCE.md:424 (round-44 heading)** — optional arrow:
> ## Round-44 measured, not promoted (R44-C1 honest stop) — SquashFS v1/v2 superseded 2026-10-28, see `## Round-49 additions to Core`

## 4. Limits of this seat

- No REA run and no frozen-counter run by this seat. F3/F4 are about the text, not a re-score.
- The synthetic v2ns probe (F1) relabels a healthy envelope; it shows the interpreter's label for that shape. It does not show REA behaviour on a damaged v2ns image; none is committed.
- F9 is an inference from a listing result (entry `:103`), not measured on a damaged broadcom body.
- I did not read the queue-drain craft section (SKILL lines 130–330) line by line; I grepped it for `squashfs`, `firmware`, `v1`, `v2`, `legacy`, `unsquashfs`, `7z` and read lines 1–130 and 415–545 in full. The grep found no v1/v2 or Frontier statement there.
- Scratch `$S` (`/fast/scratch/hyaku/kaidoku-r49/W2Skill`) is removed before yield, after the receipts above are copied.

## 5. Tooling

No tool was installed. Every command used the host's `/usr/bin/unsquashfs` 4.7.5 (sha256 `461e1fd9…`), `7z` 26.04, `python3 -I -B`. No pacman, no `~/.local/bin` write.

Receipt note: `W2Skill/receipts.tsv` has three `triage-v4-*` rows with exit 2 from a first attempt in which the interpreter was copied under the wrong file name. They are superseded by `W2Skill/receipts-triage.tsv` (same commands, exit 0, the values quoted above). The `unsquashfs-version` row (`/usr/bin/unsquashfs -version`) exits 1; the version line prints on stdout. [INFERENCE: the exit 1 is the binary's no-action exit; not checked against source.] The `unsquashfs -version` exit does not bear on any finding.
