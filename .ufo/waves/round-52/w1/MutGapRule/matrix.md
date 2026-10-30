# R52 gap-rule mutation battery — expected-verdict matrix (MutGapRule)

Seat: MutGapRule, kaidoku round 52 wave r52-w1. Table math only: no counter run,
no REA, no carrier bytes. Every verdict below is computed from the COMMITTED
lane bytes (round-50 rule, round-50 oracle tables, round-50 envelopes,
the committed round-50 score receipt) by `gap-rule-mutants.py` in this dir.

Reproduce: `python3 -I -B gap-rule-mutants.py > battery.json` (exit 0 = the
computed matrix equals the independently derived EXPECTED matrix).


## Anchor

The ported clause math applied to the FROZEN round-50 rule reproduces the
committed round-50 receipt exactly — same `gaps_ok` AND byte-identical
`gaps_note` — on all four carriers:

| carrier | computed gaps_ok | committed gaps_ok | note identical |
|---|---|---|---|
| c6430 | True | True | True |
| c6490 | True | True | True |
| g7581 | False | False | True |
| g7582 | False | False | True |

The round-50 rule is RED by `law_shape_ok` (removed.silent lists char-device details ['247:0']).

## Cross-validation

The ported clause math was compared with the FROZEN counter's own
`disposition_check` (`tools/round-50/c1-counter.py`, imported as a module)
over 40 rule x carrier pairs: agree=True, including byte-identical notes.

## Matrix

`shape` = `law_shape_ok` of the rule (the claims' rule-shape clause: no
char-device/fifo/socket/block detail under `removed.silent`, and `allowed`
for those kinds is the empty list). `red clauses` names every clause that
makes the rule red.

| mutant | shape | c6430 | c6490 | g7581 | g7582 | red clauses | overall | expected match |
|---|---|---|---|---|---|---|---|---|
| M6 | True | green | green | green | green | - | green | True |
| M1 | False | green | green | red | red | shape,R | red | True |
| M1b | True | red | red | red | red | R | red | True |
| M2 | False | green | green | green | green | shape | red | True |
| M3 | False | green | green | red | red | shape,R | red | True |
| M3b | False | red | red | red | red | shape,R | red | True |
| M4 | True | red | red | red | red | R | red | True |
| M5 | True | red | red | red | red | F3,R | red | True |
| M5b | True | red | red | red | red | F1,R | red | True |
| R50-FROZEN | False | green | green | red | red | shape,R | red | True |

### Mutant descriptions

- **M6** — the round-52 device-accounting law rule (the CTL-NEW arm: required char-device=false, allowed device kinds empty, no device detail under removed.silent)
  - `law_shape_ok`=True (None) | `law_shape_ok_strict`=True
  - c6430: gaps_ok=True — 568 gaps (1 structural), 1 removals, 0 silent, on 824 non-regular entries
  - c6490: gaps_ok=True — 613 gaps (1 structural), 1 removals, 0 silent, on 914 non-regular entries
  - g7581: gaps_ok=True — 637 gaps (1 structural), 3 removals, 0 silent, on 1001 non-regular entries
  - g7582: gaps_ok=True — 637 gaps (1 structural), 3 removals, 0 silent, on 1001 non-regular entries
- **M1** — require char-device, silent detail 247:0 only (the round-50 rule's device clause on top of the law)
  - `law_shape_ok`=False (removed.silent lists char-device details ['247:0']) | `law_shape_ok_strict`=False
  - c6430: gaps_ok=True — 568 gaps (1 structural), 1 removals, 1 silent, on 824 non-regular entries
  - c6490: gaps_ok=True — 613 gaps (1 structural), 1 removals, 1 silent, on 914 non-regular entries
  - g7581: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6', 'dev/pts/7']
  - g7582: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6', 'dev/pts/7']
- **M1b** — require char-device with NO silent allowance at all (the claims' F3 "required-true variant")
  - `law_shape_ok`=True (None) | `law_shape_ok_strict`=False
  - c6430: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led']
  - c6490: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led']
  - g7581: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led', 'dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6']
  - g7582: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led', 'dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6']
- **M2** — whitelist ALL THIRTEEN observed char-device details
  - `law_shape_ok`=False (removed.silent lists char-device details ['247:0', '136:0', '136:1', '136:2', '136:3', '136:4', '136:5', '136:6', '136:7', '230:0', '3:0', '3:1', '3:2']) | `law_shape_ok_strict`=False
  - c6430: gaps_ok=True — 568 gaps (1 structural), 1 removals, 1 silent, on 824 non-regular entries
  - c6490: gaps_ok=True — 613 gaps (1 structural), 1 removals, 1 silent, on 914 non-regular entries
  - g7581: gaps_ok=True — 637 gaps (1 structural), 3 removals, 13 silent, on 1001 non-regular entries
  - g7582: gaps_ok=True — 637 gaps (1 structural), 3 removals, 13 silent, on 1001 non-regular entries
- **M3** — whitelist a STRICT SUBSET: 247:0 plus 136:0-136:7 only (the M50 partial-widening trap)
  - `law_shape_ok`=False (removed.silent lists char-device details ['247:0', '136:0', '136:1', '136:2', '136:3', '136:4', '136:5', '136:6', '136:7']) | `law_shape_ok_strict`=False
  - c6430: gaps_ok=True — 568 gaps (1 structural), 1 removals, 1 silent, on 824 non-regular entries
  - c6490: gaps_ok=True — 613 gaps (1 structural), 1 removals, 1 silent, on 914 non-regular entries
  - g7581: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/tiatm', 'dev/ttyp0', 'dev/ttyp1', 'dev/ttyp2']
  - g7582: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/tiatm', 'dev/ttyp0', 'dev/ttyp1', 'dev/ttyp2']
- **M3b** — variant of M3: 136:0-136:7 only, 247:0 dropped
  - `law_shape_ok`=False (removed.silent lists char-device details ['136:0', '136:1', '136:2', '136:3', '136:4', '136:5', '136:6', '136:7']) | `law_shape_ok_strict`=False
  - c6430: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led']
  - c6490: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led']
  - g7581: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led', 'dev/tiatm', 'dev/ttyp0', 'dev/ttyp1', 'dev/ttyp2']
  - g7582: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led', 'dev/tiatm', 'dev/ttyp0', 'dev/ttyp1', 'dev/ttyp2']
- **M4** — DROP the symlink removal diagnostic (the rule no longer names MaliciousSymlinkRemoved)
  - `law_shape_ok`=True (None) | `law_shape_ok_strict`=True
  - c6430: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkKept) on ['usr/www/avm/cgi-bin/system_status']
  - c6490: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkKept) on ['usr/www/avm/cgi-bin/system_status']
  - g7581: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkKept) on ['dev/log', 'usr/www/avm/cgi-bin/system_status', 'usr/www/avme/cgi-bin/system_status']
  - g7582: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkKept) on ['dev/log', 'usr/www/avm/cgi-bin/system_status', 'usr/www/avme/cgi-bin/system_status']
- **M5** — require symlinks with ONLY THE GAP allowed (removed.kinds no longer admits a symlink)
  - `law_shape_ok`=True (None) | `law_shape_ok_strict`=True
  - c6430: gaps_ok=False — removal at 'usr/www/avm/cgi-bin/system_status' names a 'symlink' entry; removed.kinds is ['dir']
  - c6490: gaps_ok=False — removal at 'usr/www/avm/cgi-bin/system_status' names a 'symlink' entry; removed.kinds is ['dir']
  - g7581: gaps_ok=False — removal at 'dev/log' names a 'symlink' entry; removed.kinds is ['dir']
  - g7582: gaps_ok=False — removal at 'dev/log' names a 'symlink' entry; removed.kinds is ['dir']
- **M5b** — variant of M5: no gap kind is allowed for a symlink row
  - `law_shape_ok`=True (None) | `law_shape_ok_strict`=True
  - c6430: gaps_ok=False — gap kind 'unpublished-entry' not allowed for 'symlink' entry 'bin/ash' (allowed [])
  - c6490: gaps_ok=False — gap kind 'unpublished-entry' not allowed for 'symlink' entry 'bin/ash' (allowed [])
  - g7581: gaps_ok=False — gap kind 'unpublished-entry' not allowed for 'symlink' entry 'bin/adsl' (allowed [])
  - g7582: gaps_ok=False — gap kind 'unpublished-entry' not allowed for 'symlink' entry 'bin/adsl' (allowed [])
- **R50-FROZEN** — the committed round-50 gap rule (the CTL-OLD arm: it must yield 2 of 4 dispositions over the committed round-50 envelopes, reproducing the round-50 miss)
  - `law_shape_ok`=False (removed.silent lists char-device details ['247:0']) | `law_shape_ok_strict`=False
  - c6430: gaps_ok=True — 568 gaps (1 structural), 1 removals, 1 silent, on 824 non-regular entries
  - c6490: gaps_ok=True — 613 gaps (1 structural), 1 removals, 1 silent, on 914 non-regular entries
  - g7581: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6', 'dev/pts/7']
  - g7582: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6', 'dev/pts/7']

## Probes

**Probe 14th device** (g7581 census + synthetic row dev/ttyS0 4:64; expected match=True).

- M1: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6', 'dev/pts/7']
- M1b: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/led', 'dev/pts/0', 'dev/pts/1', 'dev/pts/2', 'dev/pts/3', 'dev/pts/4', 'dev/pts/5', 'dev/pts/6']
- M2: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/ttyS0']
- M3: gaps_ok=False — required entry with no disposition (no gap, no MaliciousSymlinkRemoved) on ['dev/tiatm', 'dev/ttyS0', 'dev/ttyp0', 'dev/ttyp1', 'dev/ttyp2']
- M6: gaps_ok=True — 637 gaps (1 structural), 3 removals, 0 silent, on 1002 non-regular entries

**Probe device-gap fail-closed** (expected match=True). synthetic unpublished-entry gap injected on the committed c6430 device row dev/led; the law rule (allowed[char-device] empty) must go RED, the round-50 rule tolerates it

- M6: gaps_ok=False — gap kind 'unpublished-entry' not allowed for 'char-device' entry 'dev/led' (allowed [])
- R50-FROZEN: gaps_ok=True — 569 gaps (1 structural), 1 removals, 0 silent, on 824 non-regular entries

## Restoration evidence

The battery is read-only on the lane tree; these hashes were taken before
and after the run and are identical (`identical`=True):

| lane path | sha256 (before == after) |
|---|---|
| .ufo/waves/round-50/l1/scores/c1-after-attempt2.json | e1e0ac176a9ccd71876bfe3ce2032eb94067c29c86922ee56d7db211b7c62816 |
| corpus/evidence/round-50/c1/c6430/after.json | 30db72bdf2aa84e6d470b98acf5224c147eab5c070f845b38bc91b453f11c64c |
| corpus/evidence/round-50/c1/c6490/after.json | 2c21f26464235334c330d42058c4b92485a688db65c05438b56c7690a0381aed |
| corpus/evidence/round-50/c1/g7581/after.json | ff481957b42cb418c2264771c60ebf5c4fda2db76f225d86606b2c0bf96c74a7 |
| corpus/evidence/round-50/c1/g7582/after.json | f250f31585f6137755815062243a4fd5881affa794da583c5c64910e3dc19665 |
| tools/round-50/c1-counter.py | 9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813 |
| tools/round-50/gap-rule.json | 43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef |
| tools/round-50/oracle/c6430.nonregular.tsv | cb691b4420cb2232eee6018af2776b59376a1116482066fc2d9834f85ed77594 |
| tools/round-50/oracle/c6490.nonregular.tsv | 74f171744d1ce28bd3e4cfc85dd07b30a9ba1604d8c4eef6dc8feef4c50b345c |
| tools/round-50/oracle/g7581.nonregular.tsv | e8706799c39f470903c06596631c5b6dfb9a6ec4866e74bfaa305c26a5c58b92 |
| tools/round-50/oracle/g7582.nonregular.tsv | eff3f15ec9107159f9ba9e6067ebbfd959bc05828d0729f23356f7e0f6ae0306 |
