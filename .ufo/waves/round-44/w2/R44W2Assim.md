# R44W2Assim — assimilation falsification (round 44, wave 2)

Seat `R44W2Assim`. Lane `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`. Date 2026-10-28.
Axes: slice byte-identity, live S113/S150 reopen, structural absence, record match.
No tool installed. No VCS mutation. Scratch `/fast/scratch/hyaku/kaidoku-r44/R44W2Assim` removed before yield.
Artifacts: `.ufo/waves/round-44/w2/artifacts/R44W2Assim/`.

**Verdict: CONFIRMED.** `Assimilation: none` is accurate. The five-row kaidoku quarantine slice re-derives byte-identical to round 43. S150 stays fabrication-class refuse. S113 stays present with the 21-locale + `x-default` correction, not adopted. `.ufo/waves/round-44/assimilation/` is empty. `considerthese/` is absent. No staged subject is in `corpus/knowledge/`. No numbered defect for the L1.

Record checked, not edited:

- `plans/round-44-claims.md:290-292` — `Assimilation: none`; slice hand-checked in round 43 and re-derived; `considerthese/` does not exist.
- `corpus/lessons/round-44.md:34-41` — reject, no adoption; slice sha256 `7383a90e…28e6a`; S150 heading absent from a 174,088-byte page; S113 count is 21 + `x-default`; `considerthese/` absent.

## 1. Slice

Command (register read-only; awk form from `.ufo/waves/round-44/w1/R44Quarantine.md:38-39`):

```
awk -F'|' -v l='kaidoku' '$2 ~ l && $3 ~ /round[0-9]+/ && $4 ~ /S[0-9]+/ {print $4, $5}' \
  /home/vgpnk/Projects/shokuknow/.ufo/waves/corpus-expansion-1/absent-defect-register.md
```

| check | exit | stdout sha256 | wall | observed |
|---|---|---|---|---|
| awk slice (stdout = artifact `quarantine-slice`, 5 lines, 306 bytes) | 0 | `7383a90e7c04c7238dfa3d19d2f9e857852bd24288c5ff9e9873bce697c28e6a` | 1.939 ms | equals round-43 copy and its stored `.sha256` (`…  my-slice.txt`) |
| `diff -u` vs `.ufo/waves/round-43/w1/artifacts/R43Quarantine/quarantine-slice` | 0 | `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (empty) | 0.511 ms | byte-identical |
| `cmp -s` same pair | 0 | empty | 0.386 ms | identical |
| `sha256sum` staged register | 0 | file `register.sha256` | — | `5afe1810a6c3d62f37987b575a954f5b1197daa23005d4bb2f1d982f64bad833`, 83621 bytes (unchanged from the wave-1 record) |

Five lines, same stray trailing backtick on the four never-checked ids: `S150` `payload-absent`; `S113`` / `S117`` fetch-failed; `S136`` / `S147`` no locator.

## 2. Live reopen (S150, S113 only)

S117, S136, and S147 were not re-fetched. Their wave-1 standing labels are not re-claimed here.

### S150 — FABRICATION-CLASS, stays refused

`curl -sSL --max-time 90 -o s150-zenn.html -w 'http=%{http_code} bytes=%{size_download} url=%{url_effective} redir=%{num_redirects}\n' https://zenn.dev/yasu01/articles/7370bd5d414ec4`

| | |
|---|---|
| exit | 0 |
| stdout sha256 | `1eec7df6ed75583c027e2fd538cf1a354545a7e2b1893c39395a199cd7884b8a` (`http=200 bytes=174088 … redir=0`) |
| wall | 1065 ms |
| body | 174088 bytes, sha256 `e4ea23c5793ced12c10e90eb894627b2a9e4fac8cb64be0b8b4771e839d7312c` |

Counters (python3 over the saved body, html-unescaped; exit 0, stdout sha256 `8d0c11b6203c7b3a95729775c382601649773f5bc2281acfcb35b437f0f5ac8c`, wall 17.4 ms):

- `シンボルがない場合のヒント` = 0, `ヒント` = 0, `シンボルがない` = 0
- `llvm-objdump` line count = 6, occurrences = 16
- `<h2>` (8): はじめに / 道具の準備 / 実例：小さなプログラムを逆アセンブルする / パターン認識のコツ / AArch64 で同じバイナリを読む / 読み進めるためのワークフロー / まとめ / シリーズを終えて

The quoted heading is in none of them. Size matches the lesson (174,088). Body sha differs from wave 1 (`17fedf14…`); wave 1 already recorded that this sha is not stable across fetches. The counters, not the sha, are the verdict.

### S113 — PRESENT, count correction stands, not adopted

`curl -sSL --max-time 90 -o s113-adb.html -w '…' 'https://developer.android.com/tools/adb?hl=en'`

| | |
|---|---|
| exit | 0 |
| stdout sha256 | `e80b6757f431a5f2df4ecdc446f5027863c00b21242ee0330d5cab91010fcfc6` (`http=200 bytes=368120 … redir=0`) |
| wall | 1136 ms |
| body | 368120 bytes, sha256 `6b2bce9c9d127aab9937955e7b085f13523a83bdba29fe075c4dc079c8e04dff` |

Counters (exit 0, stdout sha256 `071ee8dfc1a82bdeb87a09748024b107edffdc27e7c4570714ec35e4d8329c15`, wall 18.3 ms):

- `hreflang="…"` unique = **22** = 21 locales + `x-default` (`ar bn de en es-419 fa fr he hi id it ja ko pl pt-BR ru th tr vi zh-Hans zh-Hant`)
- narrow `[a-z-]*` unique = 18 (misses `es-419`, `pt-BR`, `zh-Hans`, `zh-Hant`)
- `tools/adb?hl=ja` = 1

The staged "17 locales" is still not reproducible. Body is +4 bytes vs wave 1's 368,116 and +57 vs round 43's 368,063. Every content counter matches wave 1. Drift does not flip the standing verdict and does not adopt the row.

## 3. Structural absence

| check | exit | stdout sha256 | wall | observed |
|---|---|---|---|---|
| `ls -la .ufo/waves/round-44/assimilation` | 0 | `e87245ba5f17ce7ff09c6e64f10fa18e6f57cb21c4e4a244e4aff74c27e4fc24` | 0.801 ms | directory only (`.` / `..`), mtime 2026-10-28 07:59 |
| `find …/assimilation -mindepth 1 -print` | 0 | empty | 0.429 ms | 0 entries |
| `test -e considerthese` | 1 | empty | 0.347 ms | absent at lane root |
| `find <lane> /home/vgpnk/Projects/shokuknow -maxdepth 4 -name 'considerthese*'` | 0 | empty | 8.47 ms | no match |
| staged-subject grep in `corpus/knowledge/` (`7370bd5d414ec4`, `developer.android.com/tools/adb`, DOI `10.1109/SP46214.2022.9833799`, `HOST-CONTRACT`, the S150 heading, `yasu01/articles`) | 1 | empty | 2.09 ms | 0 files |
| `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}' corpus/SOURCES.md` | 0 | `690e07064753123c967bbac0180f32da6a753a5bd8b79a47644cef58e776d9f0` (`139\n`) | 0.792 ms | 139 rows, the lesson's after-count |
| `grep S150 corpus/SOURCES.md` | 1 | empty | — | no S150 row |

The round-44 knowledge entry `corpus/knowledge/2026-10-28-r44-squashfs-v1v2-core.md:12-14` cites S138, S139, and S112. None of those is a quarantine-slice id.

Literal id tokens `S113`, `S117`, and `S136` do appear in three older knowledge files (grep exit 0, stdout sha256 `732fe1e618de3fada209757981313905b91064c6120e2d66a745fd08b8ed6e69`). They are lane rows with different documents, not the staged subjects:

- `2026-10-26-r38-sasquatch-be-squashfs-recursion.md:4` — lane S113, unblob `squashfs_v4_be` fixture, not `developer.android.com/tools/adb`
- `2026-10-26-unblob-format-matrix.md:2` — lane S117, unblob README, not the IEEE DOI
- `2026-10-27-sasquatch-release-matrix.md:1` — lane S136, sasquatch releases API, not the staged adb-surface locator

`S150` and `S147` tokens are absent from `corpus/knowledge/`. The DOI string is only at `corpus/SOURCES.md:235` under `## Leads (unopened)`, stating the paper remains unopened. Wave 1 recorded that lead at `:232`; S138/S139 shifted it. The lesson does not cite `:232`. The lead is still not an admitted row.

## 4. Record match

`Assimilation: none` in the claims (`:290-292`) and the lesson (`:34-41`) matches this re-derivation: empty assimilation directory, no `considerthese/`, slice unchanged, S150 refused, S113 not adopted, no staged subject in knowledge. Nothing was appended from the slice.

No L1 defect. S113's +4 byte drift and S150's unstable body sha are the same fetch instability wave 1 already bounded; they do not change either standing verdict.
