# DRAFT (not landed) — SOURCES rows for `2026-10-27-sasquatch-release-matrix.md`

Lane schema — `corpus/SOURCES.md:5-6`:
`| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |`.
Registry at round-43 base `6b9e64fe`: **S001–S134** (S130–S134 landed by round 42: unblob fixtures,
OpenWrt 8.09.2/8.09, DD-WRT v24 ×2). **S135 is spoken for this round** (unblob 26.6.4 LICENSE, per
`plans/round-43-claims.md` `## Frontier step`), so the next free ids are **S136–S137**. Ids are
provisional: the L1 assigns them at landing.

The staged package's row for this entry is
`merge/kaidoku/SOURCES.append.md:31` — staged **S130**, `docs`, citing the **rendered page**
`https://github.com/onekey-sec/sasquatch/releases` as the asset authority. It is not appended
verbatim: staged S130 collides with the landed S130 (unblob 26.6.4 fixtures) and the page it cites
serves no asset filename (S137 anchor below). Rows are re-grounded by document.

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| S136 | onekey-sec/sasquatch releases API — https://api.github.com/repos/onekey-sec/sasquatch/releases | dataset | A | The release inventory as a machine-readable feed: 8 releases, per-release `assets[]` with name/size/`digest`, `published_at` and the release `body`; not unblob behaviour, not any carrier, not licence permission to redistribute | fetched 2026-10-27T08:18:38Z, HTTP 200, 107313 B, sha256 `cb42cd61728f994dc18e4937d2d173b543c6a976bea25fa922e50f7213a105d0`; pinned projection `[8,[6,6,6,6,6,6,6,2],[6,0,0,0,0,0,0,0]]` (2026-10-27T08:20:15Z, exit 0) | Count published assets per release before stating an architecture matrix: the matrix starts at `sasquatch-v1.0.1`, and `sasquatch-v1.0` is amd64-only; pin the projection, never the response digest | mined | 2026-10-27 | 180d | corpus/knowledge/2026-10-27-sasquatch-release-matrix.md |
| S137 | onekey-sec/sasquatch releases page — https://github.com/onekey-sec/sasquatch/releases | docs | A | The rendered page's tag links only (8 distinct tags); the page bytes carry no asset filename, so asset facts belong to S136 | fetched 2026-10-27T08:20:30Z, HTTP 200, 349255 B, sha256 `89e7377d92132bfa1bf1a004bf38a6f105dfe85ea99a753cccde49af29227a67`; second fetch 2026-10-27T09:05:48Z, same 349255 B, different digest `56632d0f19d7e7e81776e9a48e04f7ce4b89d32f9c79670617e5f2c888cb1cea`; round 42's retained fetch 349266 B, sha256 `71ebf1600a0a9764f62298976d0d2bd0e0700694e3e2ed5612386c7c370b734a`; `grep -c 'sasquatch_1.0_amd64.deb'` → 0 | Do not cite a rendered release page for its assets; cite the endpoint that serves them, and do not pin the page by digest — it moves per request | mined | 2026-10-27 | 180d | corpus/knowledge/2026-10-27-sasquatch-release-matrix.md |

Notes for the integrator:

- **There is now a second, validated copy of these rows — prefer it.** `R43AssimGround` published
  `artifacts/R43AssimGround/rows/normalized-rows.md` at 06:00 local: S136/S137, NF=13 on both rows,
  no literal or escaped pipe in any cell, `recheck` = `180d`, `used-by` = the single admitted entry,
  and a scratch mirror census `sources-census.sh validate --file` **exit 0** (0 E-lines, 13
  pre-existing W04) with the entry placed at `corpus/knowledge/2026-10-27-sasquatch-release-matrix.md`.
  Where its anchor cells differ from mine, take its: S136 quotes its own 08:18:09Z fetch (byte-identical
  to my receipt, `cb42cd61…`) plus the projection at two instants; S137 quotes its own page fetches
  (349255 / 349255 / 349251 B, three digests). My table below is the cross-check, not the preference.
- **Ordering constraint (E11).** `used-by` is resolved on disk for every `mined` row. The entry does
  not exist in the lane yet, so the **rows and the entry must land in the same commit** (rows after
  the entry), and if the entry lands under another filename both `used-by` cells move with it.
- **Do not append the staged rows.** `R43AssimGround` ran the staged file verbatim through the
  validator: **266 E-lines** (44 × E01 fields=12 from an escaped pipe, 88 × E09 recheck-not-a-cadence,
  2 × E03 duplicate id, 132 × E11 absent used-by) — the staged package is malformed for the fleet
  schema independently of the 29 id collisions.

- **Kind of S136.** Staged S130 said `docs`; this row is `dataset`, because every fact the entry uses
  (`assets[].size`, `assets[].digest`, `body`, `published_at`) is a field of the JSON response, while
  S137 holds the page. Held S107 is `code` for a tag page; if the L1 prefers family consistency, align
  S136 to `code` and keep S137 `docs`.
- **The page is cited for a negative.** S137's `teaches` cell is the correction, not an asset fact; if
  the L1 considers a negative-only citation not worth a row, drop S137 and keep the correction sentence
  in the entry, citing the fetch in the receipt `receipts/page-probe.txt`. The entry then has one
  source and its own `recheck:` still works (`recheck:` reads S136 only).
- **No other row.** The rejected candidates' staged rows (S183–S186) are not proposed; their content is
  either held (S108, S121) or wrong (round-42 verdicts, rows 3–4).
- **Collision guard, re-runnable** (registry side only; read-only git, scratch outside the lane).
  Result recorded in `receipts/id-collision.txt`: lane registry **134** rows, `S001..S134`; staged
  package 132 rows; `comm -12` → **29 collisions `S106..S134`**; and the column-0 pattern is
  sufficient for this file (`grep -c '^| S[0-9]'` = `grep -c '^ *| S[0-9]'` = 134).
  The narrower pattern was also **exercised on an indented fixture** this round
  (`receipts/id-guard-fixture.txt`): rows `| S001 |`, `  | S002 |`, `   | S777 |`, `| S003 |` → the
  column-0 pattern yields `S001 S003` (misses both indented rows) while `^ *\| S[0-9]+ ` yields
  `S001 S002 S003 S777`. So the equal-count test — not the pattern — is what licenses the narrow form
  on a given file, which is how round 36's and round 42's caveat is discharged here.

  ```
  S=$(mktemp -d /fast/scratch/hyaku/r43-ids.XXXX) && cd "$S" && L=/home/vgpnk/Projects/shokunin/kaidoku-shokunin
  git -C "$L" show 6b9e64fe:corpus/SOURCES.md | grep -oE '^\| S[0-9]+ ' | tr -d '| ' | sort > reg-ids
  grep -oE '^\| S[0-9]+ ' /home/vgpnk/Projects/shokuknow/merge/kaidoku/SOURCES.append.md | tr -d '| ' | sort > staged-ids
  wc -l < reg-ids; comm -12 reg-ids staged-ids | tr '\n' ' '; echo
  grep -c '^| S[0-9]' "$L/corpus/SOURCES.md"; grep -c '^ *| S[0-9]' "$L/corpus/SOURCES.md"; cd /; rm -rf "$S"
  ```
