# CR6 — critic: separability attack (arc2-loop1-round6)

Seat CR6. Read-only on the repo except this report. No git mutation of the lane repo, no config edit, no signal to `arc2-r6-pe`. Scratch: `/var/tmp/arc2-l6r6-CR6-sim` (archive of `54bc9dd`, synthetic commits only). HEAD at measurement: `54bc9dd`.

Axes: causal separability (each claim verifiable without the other having landed), line-shift harm to the probe, command-A denominator integrity.

## 1. Verdict

**CONDITIONAL. Same file is not the coupling. A zero-newline in-cell map token is separable from C3. A new README row is not.**

Protocol bar: claims must be causally separable — each verifiable without the others having landed (`AXES.md` working-the-axes rule; this lane's copy is the shokunin protocol, not a repo file). Sharing `corpus/README.md` does not by itself fail that bar.

Measured:

- C1 alone, token appended inside `corpus/README.md:22` (the r4-12 cell the roster names) with a comma delimiter, plus a matching `corpus/knowledge/` file, zero newlines: command A `80/80` coverage `10.0`, probe `findings=0`, census `PASS`. `:177` and `:138` still hold. Verifies without C3.
- C3 alone, one lessons row after `:165` plus in-place `SCORECARD.md:69` `177`→`178`: probe `findings=0`, census `PASS`, command A `79/79`. Verifies without C1.
- Both of those hunks together (`good` `0f76153`): probe `findings=0`, command A `80/80`, census `PASS`. `:138` still the nits needle; the held-not-frontier needle moved to `:178` only.
- One new coverage-map row and nothing else (`plus1` `96b6d86`): probe `findings=2` (`sc69-readme-177` and `sc72-readme-nitrow`). C3's stated re-point does not own `:138`. That is an acceptance-test failure, not a merge conflict.
- That new row plus C3's hardcoded `:178` (`bad` `1bb3f38`): still `findings=2`. The re-point does not repair a C1 newline.
- A knowledge-table row before `## Lessons`, or a new frontier bullet, plus C3's `:178`: `findings=1` (`sc69` only). `:138` holds; `:177` does not land on the needle. C3's `+1` is wrong as soon as C1 also inserts one line above old `:177`.

Do not treat P7's "new 3-cell row is the line-neutral form" as the claim. It is the failing form. The roster form is the passing one (`.ufo/waves/arc2-loop1-round6/E26.md:40,61`: append the token to the existing r4-12 row, NOT a new row).

Big leg is already a typed refusal (`arc2-r6-pe` `failed` / `exit-code` / status 1, `NRestarts=0`, this seat). If the parent keeps the denominator at 79 for that leg, C1 writes neither README nor a knowledge file, and the shared file is unused. A later mid-rung HELD is still bound by the zero-newline rule. An in-place rewrite of the frontier bullet at `:172` does not shift pins; a new bullet does.

## 2. Evidence

### 2.1 Baseline pins (repo HEAD, not the scratch)

```
$ git rev-parse --short HEAD
54bc9dd
$ git status --porcelain -- corpus/README.md SCORECARD.md .ufo/gates
(empty)
```

- `SCORECARD.md:69` extracts `corpus/README.md:177`. That line holds `held, not frontier` (`corpus/README.md:177`).
- `SCORECARD.md:72` extracts `corpus/README.md:138`. That line holds `4 nits: 2 fixes applied at integration` (`corpus/README.md:138`).
- Lessons table ends at `corpus/README.md:165`. No `2026-10-18-wave-dispatch-counting` row. Deferral: `SCORECARD.md:981-984`.
- Probe entries `sc69-readme-177` and `sc72-readme-nitrow` read the number out of the citing line (`.ufo/gates/citation-drift/pointer-table.json:53-72`). They do not hard-pin 177.
- Command A takes tokens only from `## Coverage map` through the next `## ` (`SCORECARD.md:101-102`). A lessons-table row is invisible to it. Score is `|files ∩ mapped| / |files|`. A dangling token does not lower the score; a missing file does.
- Census `SCOPE` files are only `PROVINCE.md`, `SKILL.md`, `SCORECARD.md` (`.ufo/gates/c1-census-v10.py:86-108,376`). It does not read `corpus/README.md`. Last SCORECARD range is `:768-854`. Line 69 is outside SCOPE. An in-place `:69` edit with no `rea-agents@` / bare `6.x.x` token does not trip `UNDECLARED`.
- Landed citations of `corpus/README.md:N` with `N>=166`, excluding this wave's drafts: `SCORECARD.md:69` (live; C3 owns it), `SCORECARD.md:982` (the deferral record; must stay), `LOG.md:685` (already stale at HEAD — `:169` is the crash-cap frontier bullet, not the luna-round-3 evidence-id sentence). No other live pin moves when a line is inserted after `:165`.
- Service, read-only, not signalled: `ActiveState=failed SubState=failed Result=exit-code ExecMainStatus=1 NRestarts=0`.

### 2.2 Scratch (archive of `54bc9dd`, probe binary = repo copy)

`git archive 54bc9dd` into `/var/tmp/arc2-l6r6-CR6-sim/tree`, local commits only. Probe invocation each time:

```
python3 .ufo/gates/citation-drift/citation-drift-probe.py \
  --root /var/tmp/arc2-l6r6-CR6-sim/tree --rev <branch> \
  --table .ufo/gates/citation-drift/pointer-table.json \
  --expected .ufo/gates/citation-drift/expected.json
```

| Tree | What landed | README lines | Probe | Command A |
|---|---|---|---|---|
| `a453a6f` baseline | none | 187 | `findings=0 exit=0` | `79/79` coverage `10.0` |
| `5a3d0cb` c1-inline | token in `:22` cell + knowledge file, 0 newlines | 187; `:177` and `:138` hold | `findings=0` | `80/80` missing `[]` dangling `[]` coverage `10.0` |
| `52605f1` c1-concat | same stem jammed onto the old token with no delimiter | 187 | (not the coupling) | coverage `9.75`; missing both stems; dangling the merged token `2026-10-13-r4-12-godot-arm64-scale-2026-10-18-arc2-r6-pe-held` |
| `96b6d86` plus1 | one new map row inserted at old `:69` | 188; `:177` is old `:176` (PE reserve); `:138` is old `:137` (r14-02) | `findings=2` (`sc69`, `sc72`) `exit=0` | dangling token, files still 79, score still `10.0` |
| `446b8ee` c1-knowrow | one Knowledge-table row before `## Lessons` + file, no map token | 189 | `findings=1` (`sc69` only) | `mapped 79 / files 80 / missing [new] / coverage 9.88` |
| `47a7412` c3-pair | lessons row after `:165` + `:69` → `:178` | 188; `:138` nits holds; `:178` held-not-frontier holds; `:177` does not | `findings=0` | `79/79` |
| `0f76153` good | c1-inline + c3-pair | 188; `:22` carries both tokens; `:138` nits; `:178` held-not-frontier | `findings=0` | `80/80` coverage `10.0` |
| `1bb3f38` bad | new map row + lessons row + hardcoded `:178` | 190 | `findings=2` (`sc69` holds adb-device text; `sc72` holds r14-01) | dangling |
| `3b0c44f` front | one new frontier bullet + lessons row + `:178` | 189; needle is on `:179`, `:178` is PE reserve | `findings=1` (`sc69`) | — |

Census on `c1-inline`, `c3-pair`, and `good`: `VERDICT: PASS (stale=0 ambiguous=0 undeclared=0 unresolved=0)`.

Probe excerpts (observed):

```
plus1: citation_dead entry=sc69-readme-177 ... cites corpus/README.md:177-177, which lacks 'held, not frontier' (holds '- PE reserve: ARM64X hybrids; ...')
plus1: citation_dead entry=sc72-readme-nitrow ... cites corpus/README.md:138-138, which lacks '4 nits: 2 fixes applied at integration' (holds '| `2026-10-14-r14-02-final-sweep` | ...')
CITATION_DRIFT_VERDICT: reported findings=2 exit=0
```

`exit=0` with findings is the probe's non-strict default (`citation-drift-probe.py:69-78`). Gate-green means `findings=0`, not rc 0.

Delimiter law, observed: command A's class is `2026-10-\d{2}-[a-z0-9-]+` (`SCORECARD.md:102`). A hyphen between the old stem and the new stem is inside the class, so the two stems become one token and the old file drops out of `mapped`. The passing append used a backtick-comma break: `` `knowledge/2026-10-13-r4-12-godot-arm64-scale`, `2026-10-18-arc2-r6-pe-held` ``.

## 3. Verbatim-landable (parent applies; this seat did not edit these files)

```text
CR6 separability ruling (arc2-loop1-round6): C1 and C3 share corpus/README.md. That is not a coupling. Causal separability holds only if C1's README delta is zero newlines inside an existing Coverage-map cell, and C3's delta is exactly one inserted lessons row after line 165 plus an in-place SCORECARD.md:69 re-point 177→178. I measured that pair on an archive of 54bc9dd: C1 alone probe findings=0 and command A 80/80; C3 alone probe findings=0, census PASS, command A 79/79; both together probe findings=0, command A 80/80, census PASS. A new coverage-map row is not line-neutral: one inserted row (scratch plus1) makes probe findings=2, killing sc69 and sc72. C3 does not own sc72 (corpus/README.md:138, SCORECARD.md:72). A knowledge-table row or a new frontier bullet also makes the hardcoded :178 wrong (needle lands on :179; findings=1). Do not follow a "new 3-cell row" reading of the map-token form.

Landing constraints:
- Refusal/kill of the 91.6MB leg (arc2-r6-pe already failed, exit-code, status 1): do not add a knowledge file and do not touch corpus/README.md for that leg. Denominator stays 79.
- If a leg is HELD: append the new stem into the existing r4-12 cell at corpus/README.md:22 (or the line-68 cell; either is before :138). Zero newlines. Delimiter must be outside [a-z0-9-] — a comma and backtick, not a hyphen glued to the old stem. Stem must match corpus/knowledge/<stem>.md and the command-A regex. A second HELD leg appends into the same cell, still zero newlines.
- Do not add a Knowledge-table row. Command A does not read that table. README.md:9 does not require a dedicated row; multi-stem cells already exist.
- C3: insert exactly one line after corpus/README.md:165, before ## Frontier. Re-point only SCORECARD.md:69, in place, 177→178. Do not replace_all (line 982 is the deferral record and must stay). Do not insert a SCORECARD line anywhere above the census markers.
- Acceptance: after C1 and before C3, wc -l corpus/README.md is still 187 and probe findings=0. After C3, it is 188, SCORECARD.md:69 says :178, and probe findings=0. findings=0, not exit code 0.
```

## 4. Labels

- **Observation:** Write-set intersection of the declared claims is `corpus/README.md`. C2's probe files do not intersect it. At `54bc9dd`, README is 187 lines; `:177` holds `held, not frontier`; `:138` holds the nits needle; lessons index has no `2026-10-18-wave-dispatch-counting` row. Scratch `5a3d0cb` is probe `findings=0` and command A `80/80`. Scratch `47a7412` is probe `findings=0` and census PASS. Scratch `0f76153` is probe `findings=0`, command A `80/80`, census PASS. Scratch `96b6d86` is probe `findings=2`. Scratch `52605f1` is coverage `9.75`. Service `arc2-r6-pe` is `failed` / `exit-code` / status 1 / `NRestarts=0`. Lane-repo `corpus/README.md` and `SCORECARD.md` were not modified (`git status --porcelain` empty for those paths).
- **Inference:** The claim phrase "line-neutral README map-token append" is the separability condition. It means zero newlines and a delimiter outside the command-A character class. A new row fails C3's probe even if C3 lands exactly as specified. The two safe hunks do not overlap (`:22` cell vs insert after `:165` vs in-place `SCORECARD.md:69`), so order should not matter; I measured each alone and the combination, not two commit orders.
- **Inference:** Probe rc 0 is not gate-green. C3's "gates green" is `findings=0` plus census PASS plus command A with `missing=[]` and `dangling=[]`. A dangling map token keeps coverage at 10.0 and still fails that reading.
- **Unknown:** Whether the parent lands a mid-rung knowledge file after this measurement. Whether a concurrent seat has already drafted a new-row patch the parent might apply. Post-pair custody hashes (not this seat's scope; pre-pair file was not re-hashed).
- **Scope:** No tracked lane-repo file changed except this report. No git mutation of the lane repo, no config write, no install, no network, no signal to `arc2-r6-pe`.
