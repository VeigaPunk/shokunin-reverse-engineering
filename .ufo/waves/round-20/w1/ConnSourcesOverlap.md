# ConnSourcesOverlap — sibling SOURCES rows for the round-20 scribe subjects

Clock read immediately before this write: `2026-10-20T17:53:23-03:00` (`date -Iseconds`, exit 0). No tool installed.

Axes: calibration (C1), coverage (C2), depth (C3). One move below. It makes the go1.24.6 index row visible to the census without an E04, and it leaves the five uncovered subjects free to open.

## Evidence

Registry under test is the baseline blob. `git -C kaidoku-shokunin rev-parse refs/heads/main` → `d1d981d2cc041dda4656c5b01d2c8445d8d17124` (exit 0). `git status --porcelain -- corpus/SOURCES.md` empty (exit 0). `git rev-parse 14f0260ad319ecc26994381b2415d5a999003375:corpus/SOURCES.md` and `git hash-object corpus/SOURCES.md` both `ef109212b4f4c058cb526f2aa8b181042c5c25bd` (both exit 0).

Ids `S001`–`S039` are contiguous (39 rows). `grep -cE '^\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' kaidoku-shokunin/corpus/SOURCES.md` → `39` (exit 0). Gap awk printed only `max 39` (exit 0). Next free id is `S040`.

### Sweep

Authoritative command: per-file `grep -n -E -i -e 'wabt|WebAssembly|wasm|rizin|objdump|HarmonyOS|harmony|go1\.24\.6|go-1\.24\.6|go\.dev|binutils|openharmony|webassembly\.github|rizinorg'` on `*-shokunin/corpus/SOURCES.md`. Loop exit 0. `files=21 hit_files=2`.

| lane | grep exit | registry row for these subjects |
|---|---|---|
| audio, chousa, game-dev-2d, game-dev-3d, kagi, kake, kama, kasegi, kengaku, kotoba, kumitate, lore, mado, mori, revenger, souji, tabi, tameshi, tsukuroi | 1 each | none |
| kaidoku | 0 | go.dev / go-1.24.6 rows below; no WABT, wasm spec, rizin, objdump, or HarmonyOS row |
| kotodama | 0 | not a row — see false hit |

A earlier `grep` of the unfiltered glob `*/corpus/SOURCES.md` exited 2 (`GREP_EXIT:2`): ripgrep also received non-directories (`AXES.md/corpus/SOURCES.md`, `os error 20`). That exit is the bad glob, not an absence result.

`scripts/sources-census.sh shared --root /home/vgpnk/Projects/shokunin` filtered with `grep -E -i` for `wabt|webassembly|wasm|rizin|objdump|binutils|harmony|openharmony|huawei|go\.dev|golang.org`: census exit 0, filter exit 1. No shared URL across two lanes carries those tokens.

`scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku` (exit 0):

```
kaidoku	W04	S033 duplicate url github.com/NationalSecurityAgency/ghidra/pull/9348 across scopes
kaidoku	ok	/home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md
```

W04 does not fail validation (`scripts/sources-census.sh:33`).

### kaidoku rows (observation)

Registry hits only:

| id | line | what it is | cross-cite use |
|---|---|---|---|
| S024 | `corpus/SOURCES.md:30` | go.dev `debug/buildinfo` at go1.27.3 | not the go1.24.6 archive |
| S025 | `:31` | go.dev/doc/devel/release | release-train dates, not the tarball digest |
| S026 | `:32` | go.dev linker / `buildcfg` at go1.27.3 | `X:` suffix, not the archive |
| S028 | `:34` | go.dev/doc/go1.27, status `rejected` | not go1.24.6 |
| S031 | `:37` | go.dev/doc/go1.25#dwarf5-support | DWARF opt-out, not the archive |
| S034 | `:40` | go.dev/doc/go1.24 Swiss-map notes | map semantics for 1.24, not the 1.24.6 digest |
| S035 | `:41` | installed `go-1.24.6` / `go-1.25.0` `internal/abi` (byte-identical map structs) | layout bytes, not archive provenance |
| S038 | `:44` | `https://go.dev/dl/?mode=json&include=all`, entry **go1.25.0** | same index document as a go1.24.6 entry |

`grep -n -E 'go-1\.24\.6|1\.24\.6' *-shokunin/corpus/SOURCES.md` (exit 0) hits only kaidoku `:41` (S035) and `:71` (round-18 search log, not a row). The go1.24.6 digest already sits in prose at `corpus/lessons/round-19.md:71-73` (`bbca37cc395c974ffa4893ee35819ad23ebb27426df87af92e93a9ec66ef8712`, 78583176 bytes) and is not a registry row.

No registry line in the 21 files names WABT, `webassembly.github.io`, the wasm core spec, rizin's book or v0.8.2, GNU objdump / sourceware binutils, or HarmonyOS / OpenHarmony.

### False hit (observation)

`grep -o` on kotodama (exit 0) printed `163:rizin`. That span is inside "characterizing" at `kotodama-shokunin/corpus/SOURCES.md:163`, a lead bullet: "Solway and Lee 1990 (S036)". Kotodama `S036` is that article. Kaidoku `S036` is jj git-compatibility (`kaidoku-shokunin/corpus/SOURCES.md:42`). Bare ids are not fleet-unique.

### Census URL token (observation)

`url_of` keeps every non-space, non-pipe character (`scripts/sources-census.sh:600-605`). On S038 the first URL token is the backtick form plus the following comma. Python `re.search(r'https?://[^\s|]+', source)` on the S038 source cell returned `https://go.dev/dl/?mode=json&include=all`,` (backtick then comma).

Temp copies under `mktemp` (`/tmp/kr20-sources-*`, removed after; `--file` parent is the temp dir, so pre-existing mined rows emit E11 and the process exits 1 — `scripts/sources-census.sh:500-502`). S040 lines only:

| probe | source URL token vs S038 | scope vs S038 | teaches | S040 line |
|---|---|---|---|---|
| bare URL, different scope | unequal (`…all` vs `…all`,`) | different | `same index as S038 —` | none |
| backtick URL, no comma | unequal | different | same | none |
| S038 punctuation, different scope | equal | different | `same index as S038 —` (no `supersedes`) | `W04` `duplicate url go.dev/dl/?mode=json&include=all`, across scopes` |
| S038 punctuation, scope cell copied | equal | identical | `same index as S038 —` | `E04` within that scope |
| S038 punctuation, scope copied | equal | identical | `supersedes S038 —` | no S040 line |

E04 is `scripts/sources-census.sh:646-649`: same normalized URL and same scope, status not `rejected`, and `teaches` does not match `supersedes S[0-9]{3}`. W04 (`:644-645`) is the different-scope case and is not suppressed by `supersedes`.

## Inference

[INFERENCE] Sibling lanes have nothing to cross-cite for these six subjects. Copying kotodama `S036` or any foreign id would attach the wrong document. The only real collision is inside kaidoku: a go1.24.6 row on the download index is the same document as S038 and a different teach from S034 and S035. A bare URL hides that from `url_of`, so validate stays green while two tier-A rows describe one index. Matching S038's backtick-comma token makes the collision real: different scope → W04 (exit stays 0, same as today's S033 warning); identical scope without `supersedes` → E04 (exit 1); identical scope with `supersedes` → census-silent retirement of the go1.25.0 entry.

## Proposed move

Append the go1.24.6 archive as a new row (next free id `S040`, or the next id after the other new rows). In `source`, repeat S038's URL token including the closing backtick and comma (`` `https://go.dev/dl/?mode=json&include=all`, ``). Scope text is the go1.24.6 linux-amd64 archive only, not a copy of the S038 scope cell (`corpus/SOURCES.md:44`). `teaches` starts `same index as S038 —` and does not contain `supersedes S`. Leave S034 and S035 on the Swiss-map path. Status `queued`, `used-by` `—`, until the knowledge entry that names the new id exists (`CORPUS.md:103-108`); then flip to `mined` in that same change.

Open WABT 1.0.42, the wasm core import/export spec, rizin 0.8.x `iI`/`iS`/`ie`, GNU objdump `-i`, and HarmonyOS Stage/FA layout as five further rows. No sibling id goes in those cells. Keep the wasm spec row and the WABT release row separate (spec grammar vs tool-tarball identity). Both wasm knowledge entries can list both ids in `source:` so each row has a real `used-by` when it becomes `mined`.

## Risks

Matching punctuation with a pasted S038 scope cell is an E04 and `validate` exits 1 (observed on the temp copy). `supersedes S038` plus that same scope is census-silent (observed) and reads as retiring the go1.25.0 entry. A bare URL skips both codes (observed), so the duplicate is invisible. Pointing `used-by` at older objdump knowledge paths satisfies E11 (path exists) without those files citing the new id.

## Verification

Sweeps, live `validate` (exit 0, one W04 on S033), and the five temp-row probes above are the checks run. After integration, re-run `scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kaidoku`: expect the S033 W04 plus one new W04 on `go.dev/dl/?mode=json&include=all`,` , no E04, exit 0.
