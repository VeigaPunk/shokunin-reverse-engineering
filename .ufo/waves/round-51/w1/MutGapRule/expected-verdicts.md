# R51-C1 gap-rule mutation battery — expected-verdict table

Seat: MutGapRule (round 51, wave 1). Base revision `f04b51ddb8d5fedb234a5e40a2c38b016f07a4ab`.
All data read at that revision from the lane tree (read-only): the four committed
REA 6.5.0 receipts `corpus/evidence/round-50/c1/<id>/after.json` and the four frozen
`tools/round-50/oracle/<id>.nonregular.tsv` census tables.

Two independent implementations of the three-family disposition clause agree on every
cell: this seat's own evaluator (an independent re-implementation of the clause
semantics at `tools/round-50/c1-counter.py:1458-1569`) and the frozen counter's own
`gap_rule_model` + `disposition_check`, imported read-only from
`tools/round-50/c1-counter.py` (sha256 `9820811bf29f2de988f8ddb2513cf365f30a89a36f2bb465f96f1926ef9bd813`).
Agreements: **36/36**, disagreements: **0**.

Verdict is the **disposition-clause** verdict for that carrier under that rule
(`gaps_ok`), not the whole-carrier match: the counter's other clauses (carrier bytes,
rerun projection, freshness) are out of scope for this table and are the L1's.

| Mutation | c6430 (Cable) | c6490 (Cable) | g7581 (FRITZ!Box) | g7582 (FRITZ!Box) | carriers green | clause that fires on the red carriers |
|---|---|---|---|---|---|---|
| **M0** the round-50 frozen rule (committed tools/round-50/gap-rule.json) | green | green | **red** | **red** | 2/4 | required-disposition |
| **M1** require char-device, silent whitelist 247:0 only (== the round-50 frozen rule) | green | green | **red** | **red** | 2/4 | required-disposition |
| **M2** require char-device, silent whitelist of all thirteen details | green | green | green | green | 4/4 | (none — green everywhere) |
| **M3** require char-device, silent whitelist = 247:0 plus 136:0-136:7 (strict subset) | green | green | **red** | **red** | 2/4 | required-disposition |
| **M3b** require char-device, silent whitelist = 136:0-136:7 only (the other strict-subset reading) | **red** | **red** | **red** | **red** | 0/4 | required-disposition |
| **M4** drop the symlink-removal diagnostic clause entirely | **red** | **red** | **red** | **red** | 0/4 | required-disposition |
| **M5** require symlinks, but only the gap may discharge them (removed.kinds excludes symlink) | **red** | **red** | **red** | **red** | 0/4 | removal |
| **M6** the claims' law encoding (required.char-device=false, no device whitelist) | green | green | green | green | 4/4 | (none — green everywhere) |
| **M6s** advisory: law with device kinds admitting NO gap kind (a device gap would be red) | green | green | green | green | 4/4 | (none — green everywhere) |

## Unaccounted oracle entries per mutation

The exact set of oracle rows left with no disposition (the rows the rule fails to account for).

| Mutation | c6430 | c6490 | g7581 | g7582 |
|---|---|---|---|---|
| **M0** | — | — | 12 row(s): `dev/pts/0`, `dev/pts/1`, `dev/pts/2`, `dev/pts/3`, `dev/pts/4`, `dev/pts/5`, `dev/pts/6`, `dev/pts/7`, `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` | 12 row(s): `dev/pts/0`, `dev/pts/1`, `dev/pts/2`, `dev/pts/3`, `dev/pts/4`, `dev/pts/5`, `dev/pts/6`, `dev/pts/7`, `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` |
| **M1** | — | — | 12 row(s): `dev/pts/0`, `dev/pts/1`, `dev/pts/2`, `dev/pts/3`, `dev/pts/4`, `dev/pts/5`, `dev/pts/6`, `dev/pts/7`, `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` | 12 row(s): `dev/pts/0`, `dev/pts/1`, `dev/pts/2`, `dev/pts/3`, `dev/pts/4`, `dev/pts/5`, `dev/pts/6`, `dev/pts/7`, `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` |
| **M2** | — | — | — | — |
| **M3** | — | — | 4 row(s): `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` | 4 row(s): `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` |
| **M3b** | 1 row(s): `dev/led` | 1 row(s): `dev/led` | 5 row(s): `dev/led`, `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` | 5 row(s): `dev/led`, `dev/tiatm`, `dev/ttyp0`, `dev/ttyp1`, `dev/ttyp2` |
| **M4** | 1 row(s): `usr/www/avm/cgi-bin/system_status` | 1 row(s): `usr/www/avm/cgi-bin/system_status` | 3 row(s): `dev/log`, `usr/www/avm/cgi-bin/system_status`, `usr/www/avme/cgi-bin/system_status` | 3 row(s): `dev/log`, `usr/www/avm/cgi-bin/system_status`, `usr/www/avme/cgi-bin/system_status` |
| **M5** | — | — | — | — |
| **M6** | — | — | — | — |
| **M6s** | — | — | — | — |

## Mutation definitions (each is a complete gap-rule.json)

- **M0** — the round-50 frozen rule (committed tools/round-50/gap-rule.json)
  - rule sha256 `43f7c8d712f7e460a13f88b2efffced461bc9081f92bf1fe7eef0c3a900fa0ef`
- **M1** — require char-device, silent whitelist 247:0 only (== the round-50 frozen rule)
  - rule sha256 `930cd675921e9eb3e99d1ef0d9e3be3d342b502212898d9eca3f6e5937f2c2bb`
- **M2** — require char-device, silent whitelist of all thirteen details
  - rule sha256 `522231f0627602702e8da6012609068dceea7b7567c356ac5df6f78c2bde941c`
- **M3** — require char-device, silent whitelist = 247:0 plus 136:0-136:7 (strict subset)
  - rule sha256 `00e7ac6cd94a470a62c8dffd338beed8772c41cec81606d1fd19323cb6ad8869`
- **M3b** — require char-device, silent whitelist = 136:0-136:7 only (the other strict-subset reading)
  - rule sha256 `1a718a018e6902c3f90da32ec0414b70da99a2b10c8a4bc2fc129499d7ab757a`
- **M4** — drop the symlink-removal diagnostic clause entirely
  - rule sha256 `6d6545bd7612303cee0e192eeec42d9a81e18c806edeab3d65393afd0abca241`
- **M5** — require symlinks, but only the gap may discharge them (removed.kinds excludes symlink)
  - rule sha256 `b296f8b958674d7a3fd0a7b2ffde7c5eb3b7a6e12a36c9623888fb1cba96bf63`
- **M6** — the claims' law encoding (required.char-device=false, no device whitelist)
  - rule sha256 `4720c60833ec9cccb1b03ebcb20739224eb56f4ca842d609f96956abe83a6583`
- **M6s** — advisory: law with device kinds admitting NO gap kind (a device gap would be red)
  - rule sha256 `9fbd1b012e0dbc353bb7f6489e0a9570b74fdba7147d4f968e3426e99129d28c`

## Per-carrier data census (from the committed receipt + frozen table)

| Carrier | class | extract root | non-regular rows | by kind | gaps | diagnostics | removal targets |
|---|---|---|---|---|---|---|---|
| c6430 | Cable | `firmware.bin_extract` | 824 | char-device=1, dir=255, symlink=568 | depth-limited=1, unpublished-entry=567 | MaliciousSymlinkRemoved | `usr/www/avm/cgi-bin/system_status` |
| c6490 | Cable | `firmware.bin_extract` | 914 | char-device=1, dir=300, symlink=613 | depth-limited=1, unpublished-entry=612 | MaliciousSymlinkRemoved | `usr/www/avm/cgi-bin/system_status` |
| g7581 | FRITZ!Box | `firmware.bin_extract` | 1001 | char-device=13, dir=349, symlink=639 | depth-limited=1, unpublished-entry=636 | MaliciousSymlinkRemoved, MaliciousSymlinkRemoved, MaliciousSymlinkRemoved | `dev/log`, `usr/www/avm/cgi-bin/system_status`, `usr/www/avme/cgi-bin/system_status` |
| g7582 | FRITZ!Box | `firmware.bin_extract` | 1001 | char-device=13, dir=349, symlink=639 | depth-limited=1, unpublished-entry=636 | MaliciousSymlinkRemoved, MaliciousSymlinkRemoved, MaliciousSymlinkRemoved | `dev/log`, `usr/www/avm/cgi-bin/system_status`, `usr/www/avme/cgi-bin/system_status` |

## Expectations (all 16 met)

- **MET** M0 reproduces the round-50 miss: Cable green, FRITZ!Box red — observed `{'c6430': 'green', 'c6490': 'green', 'g7581': 'red', 'g7582': 'red'}`, required `{'c6430': 'green', 'c6490': 'green', 'g7581': 'red', 'g7582': 'red'}`. the committed round-50 counter reported carriers_matched 2
- **MET** M1 (require char-device, 247:0-only whitelist) is red on the FRITZ!Box class — observed `['red', 'red']`, required `['red', 'red']`. the twelve non-247:0 char-devices have no disposition
- **MET** M1 is green on the Cable class (247:0 silently admitted) — observed `['green', 'green']`, required `['green', 'green']`. the Cable census has exactly one char-device, 247:0
- **MET** M2 (all-thirteen whitelist) is green on all four carriers — observed `['green']`, required `['green']`. a full detail whitelist discharges every char-device; the clause math cannot tell it from the law
- **MET** M3 (strict-subset whitelist) is red on the FRITZ!Box class (F10 trap) — observed `['red', 'red']`, required `['red', 'red']`. 230:0 and 3:0-3:2 fall outside the subset
- **MET** M4 (removal clause dropped) is red on all four carriers — observed `['red']`, required `['red']`. the symlinks that only a removal diagnostic discharges are left unaccounted
- **MET** M5 (only the gap may discharge a symlink) is red on all four carriers — observed `['red']`, required `['red']`. the removal diagnostic names a symlink entry that removed.kinds no longer covers
- **MET** M6 (the law) is green on all four carriers — observed `['green']`, required `['green']`. char-devices are exempt from the required-disposition clause
- **MET** the law fires no clause on any carrier — observed `['green']`, required `['green']`. the law must not rely on any of the three families for the device census
- **MET** M3 unaccounts exactly the four non-pts, non-led char-devices on the FRITZ!Box class — observed `[4, 4]`, required `[4, 4]`. dev/tiatm 230:0 and dev/ttyp0-2 3:0-3:2
- **MET** M1 unaccounts exactly the twelve non-247:0 char-devices on the FRITZ!Box class — observed `[12, 12]`, required `[12, 12]`. the claims name twelve other char-devices
- **MET** M4 unaccounts exactly the removal-discharged symlinks (1 Cable / 3 FRITZ!Box) — observed `[1, 1, 3, 3]`, required `[1, 1, 3, 3]`. the receipts carry 1/1/3/3 MaliciousSymlinkRemoved diagnostics
- **MET** M3b (136:0-136:7 only, no 247:0) is red on the Cable class too — observed `['red', 'red']`, required `['red', 'red']`. the Cable census has only 247:0, which the subset omits
- **MET** M3b unaccounts exactly the five char-devices outside the 136:0-136:7 subset (247:0, 230:0, 3:0-3:2) on the FRITZ!Box class — observed `[5, 5]`, required `[5, 5]`. the subset admits eight of the thirteen details
- **MET** M3b unaccounts exactly the one Cable char-device (247:0) — observed `[1, 1]`, required `[1, 1]`. the Cable census has only 247:0, which the subset omits
- **MET** no cross-check disagreement between the independent evaluator and the frozen counter — observed `0`, required `0`. the two clause implementations must agree on every (mutation, carrier) cell

