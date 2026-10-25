# R35Audit17 — Reopen live S125 and hash bytes (round 35, wave 1)

- Seat: `R35Audit17` (executor, leaf). Item: "Reopen live S125 and hash bytes. Read-only or private /tmp only; no lane writes."
- Read: `plans/round-35-claims.md`, `.ufo/waves/round-35/claims-canonical.json`, `.ufo/waves/round-35/w1-dispatch.json`, `.ufo/waves/round-35/w1-spec.json`, `.ufo/waves/round-35/assimilation/quarantine-verdicts.md`, `.ufo/waves/round-35/prep/jsc-sources/*`.
- Identity: S125 is the **jsc2js README** (external source, repo `xqy2006/jsc2js`), captured at prep as `.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md` (the second admitted jsc2js source is S129 = GitHub releases pages). S125/S129 rows do not exist yet in `corpus/SOURCES.md` (they land with C1 data); the capture is the frozen source artifact.

## Evidence (commands + outputs)

1. Captured bytes hashed (read-only):
   - `sha256sum prep/jsc-sources/jsc2js-readme.md` → `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3` (8,996 B)
   - `sha256sum prep/jsc-sources/releases-page1.json` → `4a5199ddf709ec41b6a1109b5d5598356892d6a4aad227dc873fe3869a0f813c` (631,043 B)
   - `sha256sum prep/jsc-sources/releases-page7.json` → `499e2b227a6eb2c3053a8df280e52dc7dd5c597d50a1cdbabc1ff98a20e199fc` (487,166 B)
2. Live repo metadata (GitHub API, 2026-10-25):
   - `curl -fsSL https://api.github.com/repos/xqy2006/jsc2js` → `default_branch=main`, `full_name=xqy2006/jsc2js`, `pushed_at=2026-10-21T08:53:24Z`, `updated_at=2026-10-25T09:16:56Z`
3. Live S125 bytes reopened and hashed:
   - `curl -fsSL https://raw.githubusercontent.com/xqy2006/jsc2js/main/README.md` → `/tmp/r35audit17/readme-live.md`
   - size 8,996 B; `sha256sum` → `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`
   - `diff -q prep/jsc-sources/jsc2js-readme.md /tmp/r35audit17/readme-live.md` → exit `0` (byte-identical)
4. Commit identity at instrument revision `d2729cba` (the prep commit, 2026-10-25T16:05:46-03:00):
   - `git show d2729cba:.ufo/waves/round-35/prep/jsc-sources/jsc2js-readme.md | sha256sum` → `df85060f38fd9ba5a15df5c86b4fbc9aa988c4d6faab8d8aa8d8b91f9ffeade3`
   - blob id `62876f3e135466093d3bd001669dd5408cb9f3f8`
   - ⇒ live == capture == committed instrument blob (all `df85060f…`).
5. Anchor presence in live bytes (same bytes as capture):
   - line 1 `# jsc2js`
   - line 117 `` `jsc2js` reverses **V8‑generated JSC bytecode** into readable (approximate) JavaScript. ``
   - lines 64–66 V8 5.1 lower bound / 5.1–11.9 + 14.7.84+ source-aware patches / 12.0–14.7.83 stable patch
   - line 75 V8 14.7.84–15.3.25 57 exact failed tags

## Verdict / findings

- **S125 live reopen: HOLDS.** Live bytes fetched 2026-10-25 hash identically to the prep capture and to the object committed at the instrument revision; no drift between capture time and now.
- **First falsifications (advisory):**
  - F1 — The capture filename pins no commit/tag; the S125 row must pin the fetched-at SHA-256 (or a commit) with its `opened=2026-10-25` date, else a future README edit silently invalidates the anchor. Safe today: hash is fixed at open date.
  - F2 — Anchor must quote the **raw** README lines (the capture is raw Markdown). If the mapper-contract entry quotes the rendered GitHub HTML page instead, byte comparison will differ (HTML boilerplate). Recommended anchor set (present in live raw bytes): line 117 (English overview), lines 64–66 and 75 (V8 coverage bounds).
  - F3 — Line numbers are stable today (byte-identical), but verify again at release/score time; the frozen counter reads immutable git objects only, so worktree drift cannot affect scoring.
  - F4 — README line 200 states Node-compiled JSC may fail to decompile while Electron works (`由于没有node环境…electron则正常`); any entry must keep this boundary, not generalize to all `.jsc` carriers.

## Limits

- Read-only on the lane; only private `/tmp/r35audit17/` used; only network touched: GitHub API + raw.githubusercontent.com. No lane writes except this report. No subagents spawned (leaf).
- S129 release-page byte verification and pagination is out of scope here (Audit02/Audit03).
