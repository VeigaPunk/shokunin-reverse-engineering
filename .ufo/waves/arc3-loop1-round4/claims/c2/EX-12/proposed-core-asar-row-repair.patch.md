# PROVINCE.md repair — Core "Electron/ASAR/JavaScript" row (:49): asar inventory undercount + superseded file count

Authored by SEAT EX-12 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

Base: `PROVINCE.md` sha256
`d075a3c67e17ae428eb5a69e594171c6dcba88ec93c97bd3cf162a2f2b4dbdad` (162 lines,
HEAD `015e1bab914713568f339fd53999bc180459cc40`). The target line's own bytes:
sha256 `5719d6ff7f083cf23791bfd9071ebc5838728e1881054664e6786c04d755ab28`.

## Stale item (census-checked, re-derived first-hand)

Two falsified clauses in the same physical line:

1. **The pinned-asar inventory undercounts.** The row reads
   `asar archives pinned on host: obsidian ×2, signal, 1Password, electron39/43
   stubs, typora ×3 (r1 sweep missed them)` — 9 named archives. A live sweep
   (`find /usr/lib /usr/share /opt ~/.config ~/.local/opt -maxdepth 6 -name
   '*.asar'`) returns **12**:

   | archive | bytes |
   |---|---|
   | `/usr/lib/chatgpt/resources/app.asar` | 578,643,106 |
   | `~/.local/opt/zcode/squashfs-root/resources/app.asar` | 326,913,098 |
   | `/opt/1Password/resources/app.asar` | 40,708,328 |
   | `/usr/lib/signal-desktop/resources/app.asar` | 38,465,187 |
   | `~/.config/obsidian/obsidian-1.14.4.asar` | 27,477,966 |
   | `/usr/lib/obsidian/obsidian.asar` | 25,787,463 |
   | `/usr/share/typora/resources/node_modules.asar` | 15,077,447 |
   | `/usr/share/typora/resources/lib.asar` | 8,339,267 |
   | `/usr/lib/obsidian/app.asar` | 480,052 |
   | `/usr/share/typora/resources/app.asar` | 390,514 |
   | `/usr/lib/electron43/resources/default_app.asar` | 111,073 |
   | `/usr/lib/electron39/resources/default_app.asar` | 109,371 |

   The three not carried by the row: **chatgpt** (`pacman -Qo` → owned by
   `chatgpt-bin 26.1013.40934-1`, `Install Date: Fri 16 Oct 2026 11:53:28 PM
   -03` — after the r1 sweep), the **zcode** extracted `app.asar`
   (mtime 2026-10-10), and the **config-dir obsidian copy** (`~/.config/
   obsidian/obsidian-1.14.4.asar`, mtime 2026-10-13 14:18 — after the r1
   sweep's "~/.config contributes zero" observation in
   `corpus/knowledge/2026-10-13-asar-surface.md`). So `obsidian ×2` is now ×3
   and the total is 12, not 9.

2. **`423-file asar` is the superseded count.** The evidence cell reads
   `1Password 423-file asar + 188MB Rust N-API core (r4-06)`. The cited entry
   itself carries an append-only erratum:
   `corpus/knowledge/2026-10-13-r4-06-1password-asar.md:327-329` — "423
   inventory files" conflates REA's `relevant_files:423` with archive
   membership; the asar actually lists **480** files. Re-derived this seat by
   parsing the asar header directly: **486 entries = 480 files + 6 dirs**
   (415 `.js` + 6 `.html` among the files). The 188MB core is confirmed:
   `/opt/1Password/resources/app.asar.unpacked/index.node` = 187,997,016 B.

## Change (same-line replacement, line count held at 1)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-| Electron/ASAR/JavaScript | `analyze_javascript_application` on `.asar` or extracted tree; `inspect_analysis_view` paging; asar archives pinned on host: obsidian ×2, signal, 1Password, electron39/43 stubs, typora ×3 (r1 sweep missed them) | `analyze_javascript_application` `detail:"summary"` on a small asar | `default_app.asar` (electron43) → 5 files, 41 findings, evidence `ev_2628de89…`; 1Password 423-file asar + 188MB Rust N-API core (r4-06); AppImage inner asar via unblob/7z carve (r4-15) |
+| Electron/ASAR/JavaScript | `analyze_javascript_application` on `.asar` or extracted tree; `inspect_analysis_view` paging; asar archives pinned on host (12 live): obsidian ×2 + a config-dir copy, signal, 1Password, electron39/43 stubs, typora ×3 (r1 sweep missed them), chatgpt, zcode squashfs-root | `analyze_javascript_application` `detail:"summary"` on a small asar | `default_app.asar` (electron43) → 5 files, 41 findings, evidence `ev_2628de89…`; 1Password 480-file asar (count per the r4-06 erratum) + 188MB Rust N-API core (r4-06); AppImage inner asar via unblob/7z carve (r4-15) |
```

## Census conformance

- **Line-neutral:** 1 → 1 line (a table row); `PROVINCE.md` stays at 162 lines,
  so no declared row boundary moves (the DATED marker at :119 is untouched).
- **Needle-free:** the replacement adds no `rea-agents@x.y.z`, no bare `6.x.y`
  (the instrument's bare-version regex requires a literal `6.` with a
  non-digit/non-dot lookbehind — `26.1013` is not written into the row; the
  version strings stay in this patch text's evidence block), and no
  `~`/`/`-absolute `path:line`. The row sits inside the declared DATED scope
  row `("PROVINCE.md", 45, 62, "DATED", 45, r"2026-10-13")`.
- **DATED-class reading:** as with EX-13's Core-fallback repair, the row is
  inside a DATED range. The repair is offered on the reading that an inventory
  claim about the live host must not survive its own falsification; if the
  parent adjudicates the DATED class as sheltering it, record **NO-CHANGE with
  this cause** instead — both dispositions are defensible and the choice is the
  parent's. Measured either way: the census reads PASS on the patched tree
  (see the seat's `surface-census.md` §4).

## Scope note

This is the one Core-table row in this seat's mandate (Core table rows +
surface summary + drift-prone values) carrying a falsified clause that no peer
patch text repairs. The row's own source is
`corpus/knowledge/2026-10-13-asar-surface.md` (r1-era, 6 archives) plus the
r4-15/chatgpt-era additions; the r1 entry's `~/.config contributes zero`
observation is itself superseded by the config-dir copy's mtime.
