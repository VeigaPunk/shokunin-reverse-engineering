# Round 35 — assimilation quarantine verdicts (kaidoku slice)

Source register: `/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md`
(header and `## By lane` summary totals are stale; slice derived from data rows only).
Extraction command (round prompt §10):

    A=/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-35/assimilation; mkdir -p "$A"
    R=/home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
    awk -F'|' -v l='kaidoku' '$2 ~ ("`" l "`") && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ \
      {print $4, $5}' "$R" > "$A/quarantine-slice"

Slice rows: 5 (every line carries an S-id). Each row is hand-checked this round; none of
the frozen rows is appended (no admitted entry cites them).

| staged row | register class | this round's hand check | verdict |
|---|---|---|---|
| S150 (round5) | `payload-absent` | Live fetch 2026-10-25 of https://zenn.dev/yasu01/articles/7370bd5d414ec4 (174,088 B, saved to prep capture): the quoted section heading 「シンボルがない場合のヒント」 is absent from the served bytes; the substring 「ヒント」 occurs 0 times; the article exists and is about no-symbols reading (title 「実バイナリを逆アセンブルして読む——シンボルなしの世界に踏み込む」; `strip` walkthrough at data-line 69), but the quoted heading is not there | **REFUSE** (fabrication class). Flip: re-anchor the row to a real contiguous quote from live bytes (e.g. the title, or the strip section text) and re-open |
| S113 (round1) | `unreachable` | Live fetch 2026-10-25 of https://developer.android.com/tools/adb?hl=en (368,063 B): page returns 200; `<link rel="alternate" hreflang>` matrix carries 17 locales plus x-default; `tools/adb?hl=ja` alternate link present (count 1) — the row's teaches/anchor verify | **verifiable-now** (unreachable at campaign time ≠ fabrication); still not adopted (no admitted entry cites it) |
| S117 (round1) | `unreachable` | Fetch attempt 2026-10-25 of https://doi.org/10.1109/SP46214.2022.9833799 → HTTP 202 with empty body (IEEExplore wall); no quote checkable | **unverifiable** (unreachable, not fabrication) |
| S136 (round4) | `named no locator` | Row is own-work against `corpus/knowledge/2026-10-13-r4u-06-adb-surface.md`; the location is now supplied: heading 「kaidoku-r4u / 06 — ADB surface: client present, zero devices」; quote `2 of 24 verbs are` present in the committed file (grep -c → 1) | **verifiable**, anchor locatable; still not adopted (no admitted entry cites it) |
| S147 (round5) | `named no locator` | Row is own-work against `~/.agents/skills/reverse-engineer-anything/HOST-CONTRACT.md` (exists, 3,386 B); `rea-agents@6.7.0`, skill v42, 207 tools at lines 18/41/53 | **verifiable**, anchor locatable; still not adopted (no admitted entry cites it) |

Verdict summary: 1 refuse (fabrication class), 2 verifiable-now, 1 unverifiable (unreachable), 1 verifiable with locator supplied.
No row is appended; adoption stays closed to the admitted jsc2js entries (S125/S129).
