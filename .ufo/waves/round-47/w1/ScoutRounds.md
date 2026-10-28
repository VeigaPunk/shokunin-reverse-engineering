# ScoutRounds — last two `## Round N` sections at the freeze

Seat: ScoutRounds. Read-only on the lane. No install.

## How this was measured

- Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`
- Freeze (assigned, and re-derived): `5017e1f7299c3a812e87e7950148f54313dd279e`
  - Command, UTC `2026-10-28T17:49:05Z`: `git -C <lane> log --format=%H -1 -- plans/round-47-claims.md`
  - Observed stdout line: `5017e1f7299c3a812e87e7950148f54313dd279e`
- `SCORECARD.md` blob at that commit: `1a296cdc8aec809146d0f3bd3568c448cacc3fb6`
  - Command: `git -C <lane> rev-parse 5017e1f7299c3a812e87e7950148f54313dd279e:SCORECARD.md`
  - File sha256 of `git show` of that blob: `e1fbea5d48b383a50415d5f7161c47d07a56013e3affb7910dfb79d4ac53ff52` (355376 bytes, 3661 lines)
- Worktree `HEAD` at measurement time was `3186f69b49798f2cc05727bbfd1604505fcee03b`, which is **not** the freeze. Every path and revision check below names the freeze commit. Nothing was read from the worktree copy of `SCORECARD.md`.
- Batch UTC for the git show / rev-parse / merge-base / `git log` rows: `2026-10-28T17:50:18Z`. Receipts: `receipts.jsonl` in this directory.
- Empty stdout (and empty stderr) sha256, called EMPTY below: `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`
- Counter cross-check (not a substitute for the rows): `python3 -I -B <lane>/tools/round-47/record.py --root <lane> --rev 5017e1f7299c3a812e87e7950148f54313dd279e --no-battery`
  - UTC `2026-10-28T17:52:13Z`, exit **1**, stdout sha256 `7c93ef7e37dab44c5c29ae0cf99c58df97c34ef43074104f55138fae92897218` (1409 bytes). Copy: `record-no-battery.json`.
  - `sections` = `["round-45","round-46"]`. `atoms` 50 = seats 2, window 1, path 12, rev 33, axes 2. `verified` 46. `corrections` 0.
  - In-scope mismatches are exactly the round-45 seat pair and the round-46 window. Axes mismatches were emitted by that run and were **not** re-derived by this seat.

`tools/round-47/record.py` `sections()` keeps the last two matches of `^## Round (\d+)`. The freeze blob has 33 such headings. The last two are `## Round 45` (line 3519) and `## Round 46` (line 3599 through EOF, no later `## ` heading). Round 46 is lines 3599–3661.

## Verdict in one paragraph

Two `Wave`/`Waves` sentences carry seat counts. Round 46 `Waves: 40 + 40 = 80 seats` is verifiable and matches `w1`/`w2` `counts.spawn` (40 and 40); there is no `w3-dispatch.json`. Round 45 `Wave 1: 40 seats; wave 2: 32 seats` is verifiable and **false**: dispatch spawn is 40 and 36, and the results files the same sentence cites also say `seats` 40 and 36. A third sentence, `Wave 1 found …`, asserts no count; the counter does not treat it as a seat atom. One `is empty` sentence exists; it is **unverifiable** because the window is `0425224..<tip>`. Twelve `.ufo/waves/` tokens that the counter's `WAVE_DIR` regex actually captures all `git show` exit 0, but one of those twelve is a truncation of a brace path that itself does not exist. All 33 backticked 7–40 hex tokens (24 distinct) resolve and are ancestors of the freeze.

## Seats

Counter patterns (whole section, not line-bound): `Waves?:\s*(\d+)\s*\+\s*(\d+)\s*=\s*(\d+)\s*seats` and `Wave 1:\s*(\d+)\s*seats;\s*wave 2:\s*(\d+)\s*seats`. Derivation is `.ufo/waves/round-<N>/w<i>-dispatch.json` → `counts.spawn`, `i` from 1 until the file is absent.

| id | sentence (SCORECARD line) | shape | claimed | verifiable? | derived | command |
|---|---|---|---|---|---|---|
| S45 | `Wave 1: 40 seats; wave 2: 32 seats (counts from \`.ufo/waves/round-45/{r45-w1,r45-w2}-results.json\`).` (3527–3528) | pair | 40, 32 | yes, and the claim is false | dispatch `[40, 36]` | `git show <freeze>:.ufo/waves/round-45/w1-dispatch.json` exit 0, stdout sha256 `fec3d2b055d0fcbbe94fcc1ab476efb00c23d3a01fe75397ce1869705b7b4087` (84634 bytes), `counts.spawn=40`. `…/w2-dispatch.json` exit 0, sha256 `0dfade1b643085d0a8d507a886b695a21adc107134e70c847f304e0b5e0da5a8` (70139 bytes), `counts.spawn=36`. `…/w3-dispatch.json` exit 128, stdout EMPTY, stderr sha256 `d45e62b49b2f4099fcfc645cfae20dee9820331a67e2a447f0200efed4f05540` |
| S45-source | same sentence's cited results files (not what the counter reads) | prose source | 40, 32 | yes, and the citation contradicts the number | `seats` 40 and 36 | `git show <freeze>:.ufo/waves/round-45/r45-w1-results.json` exit 0, sha256 `6773b1777c3f377cbb752e53ab8186e88d1a899f814fcb8162e08ff8fd4649d9` (89800 bytes), top-level `seats=40`, `results` length 40. `…/r45-w2-results.json` exit 0, sha256 `65492e04e2cad1f6546cf8554a4870595d0106c9ad098b17251189d45d048be6` (303275 bytes), `seats=36`, `results` length 36 |
| S46 | `Waves: 40 + 40 = 80 seats.` (3606) | sum | 40, 40, 80 | yes, and the claim holds | dispatch `[40, 40]`, sum 80 | `git show <freeze>:.ufo/waves/round-46/w1-dispatch.json` exit 0, sha256 `2e6693484d1509fc6a7418b0e69f77c459bb40978afdb88812de78ce82999697` (102751 bytes), `counts.spawn=40`. `…/w2-dispatch.json` exit 0, sha256 `b0d334a4e2504db5a3eb27e65fa382e31e79b782d6072b0c94b8350352a0c4ba` (84755 bytes), `counts.spawn=40`. `…/w3-dispatch.json` exit 128, stdout EMPTY, stderr sha256 `b9aa9511197c1527d5278a69acb901e493fb9fa02624cb6b9bcd6901b71ab861` |
| S46-narr | `Wave 1 found two HIGH instrument defects that the round closed: …` (3652) | not a seat pattern | none | not a count. Counter `seats` atoms are 2, not 3. Spawn is not asserted | n/a | no `counts.spawn` comparison applies. Round 46 `w1` spawn 40 is the row above, not a claim of this sentence |

The counter receipt's only seat mismatch is `key=45`, claimed `[40,32]`, derived `[40,36]`, dispatch `[40,36]`. Round 46's sum is among the 46 verified atoms.

## `is empty`

One line in the two sections contains `is empty`. The counter scans **per line**, so the atom is line 3635 only. Line 3634 is the other half of the wrapped command and is not part of the atom.

- Line 3634: `` `git log --name-status ``
- Line 3635: `` 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` is empty at every measurement above. ``

`WINDOW` is `([0-9a-f]{7,40})\.\.([0-9a-f]{7,40})`. `<tip>` is not hex, so the pair is `None`. Counter detail: `unverifiable` / `the claimed window names no concrete A..B revisions`. That matches the receipt.

| window | verifiable? | exit | stdout sha256 | stdout |
|---|---|---|---|---|
| as written: `git log --name-status --format= 0425224..<tip> -- tools/round-46 plans/round-46-claims.md` | **no** | 128 | EMPTY (stderr sha256 `30433d50fa60db50ded453deb214da1bee9e0aff67289c983e641e239d7dc85a`, `fatal: bad revision '0425224..<tip>'`) | empty |
| `<tip>` as a commit: `git rev-parse --verify --quiet <tip>^{commit}` | no | 1 | EMPTY | empty |

Substitutions are **not** the atom. They show what a concrete correction would re-derive. Same pathspec `tools/round-46` `plans/round-46-claims.md`, command shape `git log --name-status --format= 0425224..<tip> -- …`.

| substituted tip | exit | empty? | stdout sha256 | stdout (52 bytes when non-empty) |
|---|---|---|---|---|
| `0425224` | 0 | yes | EMPTY | |
| `7bf33e31` | 0 | yes | EMPTY | |
| `1e32827b` | 0 | yes | EMPTY | |
| `332f4884` | 0 | **no** | `f7ace3d35eb91c95df996df7551a8b65b132400cd97b0c45fc25eaa81483a282` | `M tools/round-46/attest.py` / `M tools/round-46/gate.py` |
| `58eb04b6` | 0 | **no** | same `f7ace3d3…` | same two paths |
| freeze `5017e1f7299c3a812e87e7950148f54313dd279e` | 0 | **no** | same `f7ace3d3…` | same two paths |

So a correction `empty in 0425224..58eb04b6 -- tools/round-46 plans/round-46-claims.md` (the amendment's measured revision) would stay red. `empty in 0425224..7bf33e31 -- tools/round-46 plans/round-46-claims.md` does re-derive empty. `empty in 0425224..332f4884 -- …` does not. This seat did not pick a landing correction.

## `.ufo/waves/` path tokens

Prose tokens (cut at whitespace or a closing backtick) versus the counter's `WAVE_DIR` = `\.ufo/waves/round-[0-9]+/[A-Za-z0-9._/-]*`, then `rstrip(".,;:)`")`. `{` is outside that class, so the round-45 results citation is truncated to the directory.

Existence command, every row: `git -C <lane> show <freeze>:<token>` and `git -C <lane> cat-file -t <freeze>:<token>`. `cat-file -t` stdout sha256 `bc103b4a84971ef6` is `blob\n`; `f27e01fe7624cca3` is `tree\n`. UTC `2026-10-28T17:50:18Z`.

| token | who sees it | show exit | type | stdout sha256 | bytes | verifiable? |
|---|---|---|---|---|---|---|
| `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json` | prose only (line 3528) | 128 | absent | EMPTY (stderr sha256 `29216881cee6f9a8e648b110e10d1455917da11669ea8fb243e9540cc8ca0a49`) | 0 | yes: the literal path does **not** exist |
| `.ufo/waves/round-45/` | counter only, truncation of the row above | 0 | tree | `f810a98a1057e798de4957e390ea8059038e7f8352b29c48ef746c34c81057c5` | 228 | yes: the directory tree exists. The counter therefore counts this citation as a present path. The cited brace path does not. |
| `.ufo/waves/round-45/controls/ctl-c1-0-do-nothing.json` | both | 0 | blob | `5cf74c78468785e429075d5f6b6ce98ece64debb986c64d8a47ff28e3aa57fcf` | 667 | yes, exists |
| `.ufo/waves/round-45/l1/scores/c1-at-1f4b27f8.json` | both | 0 | blob | `da9d99b4d1388e8274ef49e0735a38622308b5b411bc344f370ab8df417936de` | 529 | yes, exists |
| `.ufo/waves/round-45/controls/ctl-c2-0-do-nothing.json` | both | 0 | blob | `f61c6b997f6151ea3cd086bce9625ad6e1a27e558c5c3c74961023d705d2c630` | 953 | yes, exists |
| `.ufo/waves/round-45/controls/ctl-c2-0-base-unevaluable.json` | both | 0 | blob | `9c09b1d76b1a3bf1df8b934ca0e851a5eb0bbf27ce83c395fb1ef208ee36c9f3` | 102 | yes, exists |
| `.ufo/waves/round-45/l1/scores/c2-at-1f4b27f8.json` | both | 0 | blob | `0daf63d3d13068a376af8adce4e37c9830f312d21cdaf2649d98478bf3c0abb9` | 732 | yes, exists |
| `.ufo/waves/round-45/l1/scores/c1-at-A2.json` | both | 0 | blob | `3fa65f25351e9ed399d34431052313cc011a16d52136c07e5e550ca88a306bdf` | 529 | yes, exists |
| `.ufo/waves/round-45/l1/scores/c1-at-A3.json` | both | 0 | blob | `5663b064282f72215c9bbf28666a53a0dd48739d7a6166fe39560a3d072edc89` | 529 | yes, exists |
| `.ufo/waves/round-46/controls/ctl-c1-0-do-nothing.json` | both | 0 | blob | `dc40761582361a81ca2cb5739b3f8c70981ef8940a1a1ea60f2b518f90637a42` | 548 | yes, exists |
| `.ufo/waves/round-46/l1/scores/c1-at-F4.json` | both | 0 | blob | `5811bfe0d6e439c95d8edc9f7aa33d7be48ba4ab7fb323682324ec4f9114ed33` | 3289 | yes, exists |
| `.ufo/waves/round-46/controls/ctl-c2-1-v1-scope.json` | both | 0 | blob | `aff4ecc59e85690f25abe4d0f0ccd6ea3e8b2c5b07dfd88cbc04f56a0f8bd006` | 732 | yes, exists |
| `.ufo/waves/round-46/l1/scores/c2-at-F4.json` | both | 0 | blob | `d3869553edf79e572238c1aecac68ccbe408c0daa8b28f51b5971d7314539ac1` | 3144 | yes, exists |

That is 11 prose `.ufo/waves/` tokens plus 1 counter-only truncation = the counter's `path` count of 12. None of the 12 is in `mismatches`, so the counter accepted the truncated directory.

The brace members, which the prose brace would name if expanded, do exist, and they are the S45-source rows above: `r45-w1-results.json`, `r45-w2-results.json`. Expanding the brace is this seat's reading, not a token in the file.

### Citations that are not `.ufo/waves/` tokens

The path class does not see these. They are listed so they are not mistaken for missed tokens. Existence of a reconstructed path is marked inference.

| written citation | why it is outside the class | reconstruction checked? |
|---|---|---|
| `` `…/c2-at-A2.json` `` (round 45, beside `c1-at-A2.json`) | leading ellipsis, no `.ufo/waves/` | inference: `.ufo/waves/round-45/l1/scores/c2-at-A2.json` show exit 0, blob, sha256 `be8a7a74a872cc1a2c084f0c1c0fd8c3cbb0b4625bc71c747a128161ac777812`, 732 bytes |
| `` `…/l1/preflight-round45-frozen-both.json` `` | same | inference: `.ufo/waves/round-45/l1/preflight-round45-frozen-both.json` show exit 0, blob, sha256 `ca59dd525309b0e1cfb19ed60d972d21bbad6f14991caa04124eae2f027dcbe4`, 373 bytes |
| `` `…/c2-at-A3.json` `` | same | inference: `.ufo/waves/round-45/l1/scores/c2-at-A3.json` show exit 0, blob, sha256 `6c322c7c375e81a87726d2761b0333b2b3b8cc05f29b6cf142ecae316851dc76`, 732 bytes |
| `` `l1/scores/{c1,c2}-at-A4.json` `` (round 46) | no `.ufo/waves/` prefix; brace | inference: both `.ufo/waves/round-46/l1/scores/c1-at-A4.json` (sha256 `0b3d8c3f88f87b2cdf1bdfeb7b74cbf36c1f1835b3e830612b97f331fd28d3e6`, 3289) and `c2-at-A4.json` (sha256 `f4a0c39bf424b80e0dd77a5b2e8dac06c2ca3143c9cc988a0162565573c5ff6d`, 3144) show exit 0, blobs. The brace literal was not a path atom |

## Backticked commits

Counter: `` `([0-9a-f]{7,40})` ``, then `git rev-parse --verify --quiet <token>^{commit}` and `git merge-base --is-ancestor <oid> <freeze>`. Ancestor exit 0 with stdout EMPTY for every row below. Each short name is unambiguous: `rev-parse` exit 0 (an ambiguous abbreviation would not). 33 occurrences, 24 distinct, all ancestors. None are in the counter's `mismatches`.

Command prefix: `git -C <lane> rev-parse --verify --quiet <token>^{commit}`. Stdout is `<oid>\n` (41 bytes).

| round | n | token | oid | rev-parse exit | stdout sha256 |
|---|---|---|---|---|---|
| 45 | 1 | `149133d47aa7e90796f96047afe6d251a3e65b2c` | `149133d47aa7e90796f96047afe6d251a3e65b2c` | 0 | `ed3637cb583b244bad2c1d786a450d8f85d40c3f49c85b2a3401668faf25b935` |
| 45 | 1 | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | `f762b7273e3f6ca3c710bb37d5de92a4a4417aec` | 0 | `97150e76f53a53146147fe3d2c3d6318d1e08cd3e8d23cadde679512bf85b67f` |
| 45 | 1 | `e715263cb51b713c342ab992d527fe9d61d6f8ff` | `e715263cb51b713c342ab992d527fe9d61d6f8ff` | 0 | `a7dd8f10c26a7eb747679a733d98cd802a2a90db637304e2ccb89c72ad839f11` |
| 45 | 1 | `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` | `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` | 0 | `6d12cc5cbbcdfc2e607d5a985b2ae7f36eb9301b12bc0056bfb65051f17c6be8` |
| 45 | 6 | `1f4b27f8` | `1f4b27f82353d6544dc0c8048b3cfdadd8525d12` | 0 | `6d12cc5cbbcdfc2e607d5a985b2ae7f36eb9301b12bc0056bfb65051f17c6be8` |
| 45 | 1 | `c86ea508` | `c86ea508188c50e2645b1f9bba65df4177cda6b1` | 0 | `63ea2c1b985bfbaa1475ee8b0f7fc49e1f2576c21ab8e5097ce9acc417fb3896` |
| 45 | 1 | `fedd11bf5ff9fe42d061169f78d77df59af4eca1` | `fedd11bf5ff9fe42d061169f78d77df59af4eca1` | 0 | `8990e43ce03950d9c13c027433932bf2937aac1796dfc2145d3b0901f405d9f9` |
| 45 | 1 | `f59565b782c18b0eb691bec12f52d2f80d9f5032` | `f59565b782c18b0eb691bec12f52d2f80d9f5032` | 0 | `51eb2f22739242355fbde17443f908746894b27faeb1419d681fe9542e3dccd4` |
| 45 | 1 | `e715263c` | `e715263cb51b713c342ab992d527fe9d61d6f8ff` | 0 | `a7dd8f10c26a7eb747679a733d98cd802a2a90db637304e2ccb89c72ad839f11` |
| 45 | 1 | `fedd11bf` | `fedd11bf5ff9fe42d061169f78d77df59af4eca1` | 0 | `8990e43ce03950d9c13c027433932bf2937aac1796dfc2145d3b0901f405d9f9` |
| 46 | 1 | `5382acc85f9d8617fe242fc116819b8055dfc4c7` | `5382acc85f9d8617fe242fc116819b8055dfc4c7` | 0 | `508d2e19fe158a94e759917b68967f65d7f1633b6c01bfe5fd2ecb9882cdcee2` |
| 46 | 1 | `31820472784284727546808acc31b3ea1e73919b` | `31820472784284727546808acc31b3ea1e73919b` | 0 | `9757eb4b209616da445117438ef0eca8989765d9b70c7f61764efe954dd925d7` |
| 46 | 1 | `50862e4a` | `50862e4a041499dd2ce0da68d10301b765bb9997` | 0 | `7ef033eb2c31e03a75f51a6dc50962a0da6fe97b199e441bc098f50fb9cd262f` |
| 46 | 1 | `65678df0` | `65678df0f1666e83cdeea7233bfb31ffe73ec709` | 0 | `e6d0c8c0e4eb9e60aec581dd10c643f6bc73a9d47bee2c6c053a1e00b5c1dd39` |
| 46 | 1 | `0425224756791b414454df28a9abf93dcdf154ce` | `0425224756791b414454df28a9abf93dcdf154ce` | 0 | `b2784a6989e3a1308244829f2322bf947d843f39ce7ec8efda4d4735e043ce9e` |
| 46 | 4 | `0425224` | `0425224756791b414454df28a9abf93dcdf154ce` | 0 | `b2784a6989e3a1308244829f2322bf947d843f39ce7ec8efda4d4735e043ce9e` |
| 46 | 1 | `227d6982` | `227d698281c015cb3944ef19b542473c0ffdc16d` | 0 | `7459fe1d06aecf843f6cccc13ca65b13f1ab03057a28bc3478af46d8d7d0ee2b` |
| 46 | 1 | `87578656` | `8757865679e62dac1f50efb33f583de0be884bf3` | 0 | `c464873b4bf1b7410bd6d675db17be6f90817de911f1f0372f303eefb53b43be` |
| 46 | 1 | `6e018068` | `6e018068aaf9beb3c66ed270aeee08b300531976` | 0 | `b3b6fb341cab82a8d8a801338b1415d201cf0d60af0c5f04e0fc186221efc3f6` |
| 46 | 2 | `7bf33e31` | `7bf33e312d75ad09d55df399814e9ae3ef7cee49` | 0 | `b61e0ec50303e3c67a18c1457621bda99c530007f59dd423dceada148e4dd596` |
| 46 | 1 | `781e19ae` | `781e19ae674225b6be0b5de56ee8574679bac0b6` | 0 | `799d175813e5d7dc5bb26d7a41abe81fc60df4cdaed56acc6c1cb1c9b410dbd0` |
| 46 | 1 | `1e32827b` | `1e32827bd05328ee3b1e439d116008f40f078049` | 0 | `dc89c5c01bea80051e1320350b8f09450cc6a38566ff0c23d2b8018fec9aefcf` |
| 46 | 1 | `332f4884` | `332f48849966073e2f165c13f952eb4c8e165e39` | 0 | `33ea20216800eb6318c2e36e40b4559bf877f36a4d2442f3a547e29e118b0c64` |
| 46 | 1 | `58eb04b6` | `58eb04b6e5e886078121bb5e13fb95c687fe41bc` | 0 | `633ff47d1872479d0661a155be2f2e1f1f9f93e7920ba546ebbeb617a8df529b` |

Same-object pairs: `1f4b27f8` = `1f4b27f82353d6544dc0c8048b3cfdadd8525d12`; `e715263c` = `e715263cb51b…`; `fedd11bf` = `fedd11bf5ff9…`; `0425224` = `042522475679…`.

## What is wrong with the frozen path check

The round-45 sentence cites `` `.ufo/waves/round-45/{r45-w1,r45-w2}-results.json` ``. That literal path is absent (`git show` exit 128). `WAVE_DIR` stops at `{` and records `.ufo/waves/round-45/`, which `git show` accepts as a tree (exit 0). `gate.show` treats any exit 0 as existence, so the path atom is green. The counter receipt has `path: 12` and no path mismatch. A citation of the form `.ufo/waves/round-<N>/{anything-missing}` is satisfiable whenever the round directory exists. The live scorecard line is the fixture; frozen bytes were not edited.

The window check has the same shape of hole in the other direction: a placeholder makes the atom unverifiable (red, correctly), but only the line that contains the words `is empty` is parsed. The `git log` opener on line 3634 is invisible to it. That did not change the verdict here, because `<tip>` is already on the `is empty` line.

## Not run

- `record.py` battery (`--no-battery` was set). Axes fractions `138/138` and `23/23` are the counter's derivation, not an independent recount by this seat.
- No mutation of `SKILL.md`, `SCORECARD.md`, `plans/`, or `tools/`. No commit.
