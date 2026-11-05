# CriticC2 — falsify R99-C2 (truncated UPX PE refusal)

Seat: CriticC2 (critic, leaf). Scoring tree: clone of lane head `c19d57cd2` (scratch, detached).
Candidate under test: `tools/round-99/upx-pe-repair.py` at L = `01c4b79cc` (blob sha256 `ac97598a94c041199cdf2cc3f700257989e8d70545bddb56e154e51b85d518d8`).
Frozen counter: `tools/round-99/pe-upx-trunc-battery.py` (sha256 `d4ed44301f417ef6e475bdc872dc31407c34c0fe2d157ca5f785d5687b04ce3c`; `git diff` F→c19d57 empty).
Receipts: `.ufo/waves/round-99/w1/CriticC2/` (index at end). No tool installed or upgraded.

## Verdict

R99-C2 reproduces at L (label met, exit 0), but the frozen label does not measure the arithmetic it names.
Four forgeries score the full frozen label: three need no overlay arithmetic (one of them calls the packer as
an oracle, with the static screen evaded by an `os` alias and a refusal relabelled `truncated`), and one keys on
the battery's two cut lengths. The landed candidate has zero held-out truncation false accepts. Two candidate
limits surfaced on held-out inputs (L1, L2 below).

## Axes

- A1 label satisfiability: can the frozen label be met without `ALIGN_UP(last raw end)` arithmetic?
- A2 held-out truncation fidelity: do forgeries accept truncations the packer rejects, on inputs outside the pinned set?
- A3 static screen strength: can the packer still be called while `static 1 of 1` holds?
- A4 message discrimination: the truncated arm checks the substring `truncated`, not the refusal reason.

## Reproduction (L)

`python3 -I -B tools/round-99/pe-upx-trunc-battery.py --root <clone@c19d57> --repair tools/round-99/upx-pe-repair.py --rev 01c4b79cc1cf8e6172b507edebb6a4d3125c5c6f --work $S/w-L --json-out …/c2-L-reproduce.json`
→ `recovered 30 of 30; decoy 9 of 9; intact 10 of 10; overlay 20 of 20; truncated 40 of 40; refused 2 of 2; cli 3 of 3; static 1 of 1; effective 79 of 79 met True`, exit 0 (`c2-L-reproduce.out`).

Carrier layout (`layout.json`): all 10 pinned carriers have last raw end equal to its aligned end; `sevenzip64dll`
has a 2.2 MB overlay and PackHeader at 517. Pinned carriers cannot distinguish an aligned from an unaligned last
raw end, and four carriers (t32, w64, winhello, fastlist64) have a UPX1-midpoint cut that is already FileAlignment-aligned.

## Forgeries scored with the frozen command (worktree mode; sources in `forgeries/`)

| id | construction | sha256 | label result | exit |
|---|---|---|---|---|
| fa-cutpattern | refuse iff len == raw_end-1 or len == UPX1 midpoint (the battery's two cut lengths) | c2f8fd64b576bbb6455ceae20956dfec494c3f82ac1ebd4142a9841134bef413 | all arms met | 0 **ADMITTED** |
| fb-noalign | L with last raw end *without* FileAlignment | 5ca97158366bfa92c5f76740f9a8f5c90d42947a1b911b53bdfc17e072c1c719 | all arms met | 0 **ADMITTED** |
| fg-oracle-alias | L + `upx -t` oracle on output via `import os as o; o.system(...)` (arithmetic kept) | fe287d3da4cab7ce4efc95f95b53a123345a03df9632e5b897cc7c29eae7fe91 | all arms met (static 1) | 0 **ADMITTED** |
| fg2-oracle-only-alias | fg with the arithmetic check disabled | de0596db48a1eb5a5a9373373750bcccfea6dd0e27251b0db501152be1d3efbd | truncated 20 of 40 | 1 |
| fg3-oracle-relabel | fg2 + packheader-not-found refusal relabelled `truncated:` | 121eae95421fd7d4a3df80e28c4ccad8b92893646885280328167c2b33b90a35 | all arms met (static 1) | 0 **ADMITTED** |
| fc1-size-mod | refuse iff len % FileAlignment != 0 | 44c86114c6a235ae5ccce900135f5f11d0d53e397380e7e8f33ab6a52ea1727f | intact 9/10, overlay 0/20, truncated 32/40 | 1 |
| fc2-size-mod-gated | refuse iff len % falign != 0 and len < aligned end | c18d859d11a1e0c2b13a6ddc255054f3c6939f4d3d141b2740d526d37506e9e6 | truncated 32/40 | 1 |
| fd-upx-fixed-k | refuse iff len - UPX!pos < 57888 (fixed, t32's value) | 829818b6716fe7014ab2870d7161697766bda5c573f61ec4e232ee955c266924 | recovered 21/30, truncated 8/40 | 1 |
| fe-clen-bound | refuse iff len < PackHeader + 32 + c_len | 23eea869c412cba101f71c153bf0988d3ba23504175b0dbcdba7ce5a9367fa70 | truncated 0/40 | 1 |

Frozen g8 (oracle, no alias; control at F) fails only `static 0 of 1` (prior receipt, unchanged).
Full list with hashes: `critic-forgery-sha256.txt`, `forgeries/SHA256SUMS.txt`. Candidate L: `ac97598a…518d8`.

## Admitted forgeries — named limits

- **N1 fa-cutpattern (A1, A2).** Keyed on the battery's two cut lengths, not on arithmetic. Held-out (`heldout-differential.json`,
  host h2 = freeglut32.vc10.dll): 10 false accepts against L's 0 (`cut-*-aend-2`, `cut-*-aend-512`, `cut-*-rand-a`,
  `cut-*-upx1-end-1`). Every one is a file that `upx -t` rejects (`packer_t_input_rc` 1).
- **N2 fb-noalign (A1, A2).** Accepts a truncation inside the FileAlignment gap. Passes the frozen battery only because every
  pinned carrier's last raw end is already aligned. Held-out: 2 false accepts (`gap-cut-intact`, `gap-cut-both`, h2); both
  rejected by `upx -t` (rc 1).
- **N3 fg3-oracle-relabel (A1, A3, A4).** No overlay arithmetic. Uses the packer as output oracle (`upx -t` through
  `import os as o`) and relabels the PackHeader-not-found refusal `truncated:`. Meets the label at exit 0. Held-out: identical to
  L on all 81 cells except `corrupt-upx1-mid` (h2), where L emits rc 0 with an output `upx -t` rejects and fg3 refuses with
  `truncated (oracle said no)`. The label therefore accepts an oracle caller that mislabels corruption as truncation.
- **N4 fg-oracle-alias (A3).** Same static evasion with L's arithmetic kept. Its truncated refusals come from arithmetic; the
  oracle only adds refusals of corruption (same single held-out diff as N3). Shows the static text screen is the only thing
  standing between the battery and a packer-as-oracle candidate, and it does not stop one.

Not admitted (battery holds): fc1 and fc2 (aligned UPX1 midpoints pass through); fd (fixed UPX!-relative K fails sevenzip64
cells); fe (c_len bound refuses none of the 40 truncations); fg2 (refuses correctly but its reason `packheader-candidates:0`
lacks `truncated`, so the substring check fails 20 of 40). Admitted = counted as a pass at the frozen predicate.

## Candidate limits found on held-out inputs (L itself; not forgeries)

- **L1 refuses valid 2-section UPX packs.** Hosts h0/h1 (systemd-boot ia32/x64 EFI). Intact pack: `upx -t` rc 0. L answers
  `refused: sections` (its `n < 3` gate). 12 false refusals across intact, tampered and overlay inputs. Outside the pinned population.
- **L2 passes corrupt payloads.** h2 `corrupt-upx1-mid` (one byte flipped in UPX1): L returns rc 0 with an output that `upx -t`
  rejects. The landed candidate does not validate its own output. Not a truncation case, so outside the claim.

## Scope and honesty

- Held-out: 3 host carriers from a host-wide native PE listing (`forgeries/held-host-list.txt`, 57 files, none pinned);
  81 cells per candidate. Not exhaustive. Constructed gap input: last raw size lowered by 80 bytes, cut at aligned end minus 40.
- Forgeries are one-decision text transforms of L (`gen-critic.py`, `gen-fg2.py`, `gen-fg3.py`), compiled and screened for the
  forbidden token list before scoring (screen: no hits on any forgery).
- No lane file touched. Scratch clone and the scratch tree were removed on exit.

## Suggested smallest safe correction (not applied; for the counter owner)

Keep the frozen counter. Add held-out cut positions the forgeries do not key on (inside the last section's tail, inside the
alignment gap, PackHeader-relative), require the refusal reason to name the overlay arithmetic, and count any packer call from
the candidate as a `static` failure even when the token list passes.

## Receipts (all under `.ufo/waves/round-99/w1/CriticC2/`)

`c2-L-reproduce.{json,out}`, `c2-fa-cutpattern.*`, `c2-fb-noalign.*`, `c2-fc1-size-mod.*`, `c2-fc2-size-mod-gated.*`,
`c2-fd-upx-fixed-k.*`, `c2-fe-clen-bound.*`, `c2-fg-oracle-alias.*`, `c2-fg2-oracle-only-alias.*`, `c2-fg3-oracle-relabel.*`,
`heldout-differential.{json,out}`, `layout.{py,json}`, `critic-forgery-sha256.txt`, `held-candidates-sha256.txt`, `forgeries/`.
