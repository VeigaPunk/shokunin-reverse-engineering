# ExecFreshSource — independent measurement of S321 (held-out arm, second fresh source)

Seat: ExecFreshSource, round-96 attempt-1 lane kaidoku. Clone HEAD: `3baac2ef4b9b2830d299125b8184ca06d9e6584d` (supersession commit over declaration `e4d1f7de9deae83e6d5f78d2d7f0157196002af0`, base `0ea695e826f2dca53dd55ac0bafead93de26b173`).

Axes named: coverage (second-source byte measured), depth (byte-identical repro vs committed base receipt), calibration (exit/label exact-match), freshness (host sha256 re-measured this round).

## 1. Host SHAs (fresh, this round)

```
$ sha256sum /usr/bin/printf /usr/bin/env /usr/bin/head
b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7  /usr/bin/printf
a9ba02dcad338ee7f0b03e58a1cf44009b2bd645b09c2b423242e9791d202301  /usr/bin/env
313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1  /usr/bin/head

$ file /usr/bin/printf /usr/bin/env /usr/bin/head
/usr/bin/printf: ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=e7eb13c0620dda16d8b82cd2b7ab2ac854a0355a, for GNU/Linux 4.4.0, stripped
/usr/bin/env:    ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=0643d2009289281a0847fa2d38bce244239b9755, for GNU/Linux 4.4.0, stripped
/usr/bin/head:   ELF 64-bit LSB pie executable, x86-64, version 1 (SYSV), dynamically linked, interpreter /lib64/ld-linux-x86-64.so.2, BuildID[sha1]=5b565ae9d7f974ad89df4b302cf77da8f2eea891, for GNU/Linux 4.4.0, stripped
```

`/usr/bin/printf` sha256 matches the S321 claim pin `b2265abe04a2c237be085f12c14d3c70969f34ab3370a56f399727e4b38374d7` exactly; `/usr/bin/env` present (first fresh source, sha256 `a9ba02dc…`); `/usr/bin/head` recorded for step 4.

## 2. Independent repro of the S321 check (own clone, own scratch)

```
$ git -C clone rev-parse HEAD
3baac2ef4b9b2830d299125b8184ca06d9e6584d

$ python3 -I -B clone/tools/round-96/fresh-source2-check.py --root clone --work $S/fs2 --rev 3baac2ef4b9b2830d299125b8184ca06d9e6584d --json-out $S/fs2-repro.json
exit=0
fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0
```

Verdict: **PASS** — exit 0, label matches the frozen expectation `fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True` exactly. Receipt key fields: `packed_sha256 95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6`, `blocks 5`, `deterministic true`, `collides_public_packed false`, `intact_identity true`, `counts {near:2, repaired:2, far:2, far_refused:2}`, `met_target true`, cells near ±7 repaired (rc 0, `box_after [in,out]`), far ±40 refused (rc 2, `box_after [in]`).

Byte-identity vs committed base receipt (`.ufo/waves/round-96/pre/s321-fresh-source2-at-base.json`, measured at base `0ea695e82…`): field-by-field diff after rewriting `revision` to the clone HEAD — **identical** (`diff` clean; every non-revision field equal: blocks, cells, collides_public_packed, counts, deterministic, exit, intact_identity, label, met_target, packed_sha256, source, source_sha256, tool). The supersession commit did not change this check's output.

## 3. Determinism probe + public-carrier collision

Independent double-pack of `/usr/bin/printf` with the same tool (`upx --best`) in scratch:

```
$ cp /usr/bin/printf p1 && cp /usr/bin/printf p2
$ upx --best -o p1.upx p1 >/dev/null 2>&1
$ upx --best -o p2.upx p2 >/dev/null 2>&1
$ sha256sum p1.upx p2.upx
95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6  p1.upx
95f2beb30d459f3080a542d29430e91f8b55664efb5c7920c8c3fa880672adb6  p2.upx
$ cmp p1.upx p2.upx  # BYTE-IDENTICAL: yes
```

Both digests equal the check's `packed_sha256` (`95f2bebe…`) and the base receipt's — pack determinism confirmed independently of the check's own double-pack.

Public carriers from `CARRIERS` in `tools/round-92/stop-boundary-battery-v2.py` (jq, xxd, libz, dinit, xz-unseen), each packed with the same `upx --best`:

```
e8b6c9e76b542435a476a584bbe0fdff813c4b05b6d6e9a8e8405b7c7975268a  jq
1727faf91c38130249156aa1cdecc0845d67d49add0d89cc363ed3ad24eb89ff  xxd
a9c544e6da4f93418f15b768873f9ce5177d490e8de7f2e0c30a3f8e0065da5b  libz
b67ce1bdda27880a3448e25d519bcc7af2ffb073bf2ea2867a1d16dbb9f14bc7  dinit
a7b4d929441c01673bb336d69052bb362faa0a9d10504a30b691ce0fd43a889b  xz
```

`95f2bebe…` (printf packed) matches **none** of the five; `collides_public_packed false` confirmed.

Tool versions (pre-existing, no install): upx 5.2.0 (UCL 1.03, zlib 1.3.1.1-motley, LZMA 4.43), python 3.14.8. No tool was installed or upgraded by this seat (RULES.md read; nothing to install).

## 4. Supplementary diversity: /usr/bin/head through the same check

```
$ sha256sum /usr/bin/head
313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1

$ python3 -I -B clone/tools/round-96/fresh-source2-check.py --root clone --work $S/fs2-head --rev 3baac2ef4b9b2830d299125b8184ca06d9e6584d --source /usr/bin/head --source-sha 313bf1f0c296d63fa9534394e22a502cfe29d9fe9e110c5b45f3c070b9ddf3e1 --json-out $S/fs2-head-repro.json
exit=0
fresh-source2 repaired 2 of 2; far-refused 2 of 2; intact 1 of 1 met True exit 0
```

**Holds** — supplementary only (not part of any claim): `packed_sha256 b93ac38db8b61a8739adf596268e44b6b36c8e0ffdaaa7d6df0902beef4e9cc0`, `blocks 5`, `deterministic true`, `collides_public_packed false`, `intact_identity true`, `counts {near:2, repaired:2, far:2, far_refused:2}`, `met_target true`; near ±7 repaired at block 21888 (stored_sz_cpr 321), far ±40 refused (rc 2). Its packed digest also matches none of the five public carriers above, and differs from printf's packed digest (the two sources are distinct carriers).

## Files written

- This seat report: `.ufo/waves/round-96/w1/ExecFreshSource.md` (the only lane write).
- Scratch (removed after receipts copied out): `/fast/scratch/hyaku/kaidoku-r96/ExecFreshSource/` held the clone (`git clone --shared`), `fs2-repro.json`, `fs2-head-repro.json` (+ stdouts) and the double-pack artifacts. Scratch removal: per seat bounds the scratch tree was removed before finishing; the receipt JSONs were reproduced above field-by-field — their full bytes equal the committed base receipt (printf) and the printed stdout (head), so no content is lost by the removal.

## Blockers / risks

None. No lane file was edited; the only lane write is this report. No host mutation; no `~/.local/bin` writes; no fleet-root writes.
