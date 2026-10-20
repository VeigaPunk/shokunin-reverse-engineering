# Wave 2 — MutDeadseat findings

## Finding — Medium: DEADSEAT-RECORD binds structure, not cause authenticity

**Observation.** At the clone-time main tip `279e8b19c51658bfd05b9e31a1c0894ab2e70537`, unmodified `routed-r18.py --strict` reported `R18-DEADSEAT-RECORD` named/substance `true`, `open_count: 0` (exit 0). Three independent clone commits were then correctly caught: deleting `GateSUMSRUNLOG.cause` produced `substance:false`, `seats without cause/source: ['GateSUMSRUNLOG']`; removing `ShonenLines` produced `got != recomputed missing-report set`; adding `InventedSeatR19` produced the same set-mismatch failure. Each had `R18-DEADSEAT-RECORD` open (named correction remained true).

**Observation.** In a separate clone commit, I replaced only `GateSUMSRUNLOG.cause` with `synthetic non-empty cause without transcript support`, retaining its `(wave,name)` and the original non-empty `source`. At commit `48aba6ba88d667baac036e305a49537fef564f7a`, the router still reported `R18-DEADSEAT-RECORD` `substance:true`, with the normal `4 seats without a report at a245bb0, each with cause and source` reason. Therefore, **yes: an arbitrary non-empty cause passes**.

**Inference, grounded in implementation.** `.ufo/waves/round-19/tools/routed-r18.py:236-245` recomputes the expected missing-seat identities from round-18 registration members minus `.md` report filenames at fixed `A18`; `:253-255` compares only sets of `(wave,name)`. Lines `:256-260` require `cause` and `source` only to be non-empty after trimming. No cause text is compared with a transcript, and the source string is not resolved or authenticated. Thus the check supplies structural binding and field-presence checks, not evidence authenticity. The same code implies arbitrary non-empty `source` text would also pass if the seat set and cause field remain valid; that source mutation was not separately exercised. The correction text says causes have transcript pointers (`corpus/lessons/round-19.md:60`), but that claim is not validated by this substance check. The original evidence has cause/source strings at `.ufo/waves/round-19/evidence/r18-dead-seats.json:17,34`.

## Mutation commands and results

**Observation — setup.** `git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main` returned `279e8b19c51658bfd05b9e31a1c0894ab2e70537` (exit 0) when clones were made; a post-run read returned the same hash (exit 0). An earlier tip read in this session returned `d0690fd44f46d8a7fe9da5f01c6be723d12abd41`; I pinned the actual test clones and all result claims below to the later clone-time hash. Clone root: `/tmp/kr19-w2-mutdeadseat-main.J8ECot`. The four `git clone -q --no-hardlinks /home/vgpnk/Projects/shokunin/kaidoku-shokunin "$tmp/$v"` invocations (`v=no-cause,no-seat,invented-seat,arbitrary-cause`) each exited 0 and began at the stated tip on branch `main`.

Each clone staged only `.ufo/waves/round-19/evidence/r18-dead-seats.json` (`git add ...`, exit 0) and committed on its clone's `main` branch (`git -c user.name='R19 mutation test' -c user.email='r19-mutation@example.invalid' commit -q -m ...`, exit 0):

| Mutation | Clone commit | Router result |
|---|---|---|
| Remove the `cause` field from `GateSUMSRUNLOG` | `cae61f4de218f7ee1b854b46cf10a218f54d39d9` | `R18-DEADSEAT-RECORD` substance false; cause/source missing; strict exit 1 |
| Remove the `ShonenLines` seat | `469950454e6811ed1cd7631482f80dbba046a509` | Substance false; actual identity set lacks `('wave2','ShonenLines')`; strict exit 1 |
| Add invented `wave2/InventedSeatR19` with non-empty cause/source | `3ea68127cfa1b95d5acfd14b08db40bdd721ca1a` | Substance false; actual set contains invented identity; strict exit 1 |
| Replace cause with arbitrary non-empty text; retain original source | `48aba6ba88d667baac036e305a49537fef564f7a` | Substance true, ordinary four-seat reason; strict exit 1 for another defect (below) |

Commands (each router invocation ran from the corresponding clone; reported exit is the actual command exit):

```sh
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root . --rev 279e8b19c51658bfd05b9e31a1c0894ab2e70537 --strict
# exit 0; baseline open_count=0
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root . --rev cae61f4de218f7ee1b854b46cf10a218f54d39d9 --strict
# exit 1; DEADSEAT-RECORD substance=false, cause/source missing
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root . --rev 469950454e6811ed1cd7631482f80dbba046a509 --strict
# exit 1; DEADSEAT-RECORD substance=false, missing ShonenLines identity
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root . --rev 3ea68127cfa1b95d5acfd14b08db40bdd721ca1a --strict
# exit 1; DEADSEAT-RECORD substance=false, extra InventedSeatR19 identity
python3 -I -B .ufo/waves/round-19/tools/routed-r18.py --root . --rev 48aba6ba88d667baac036e305a49537fef564f7a --strict
# exit 1; DEADSEAT-RECORD substance=true; arbitrary non-empty cause accepted
```

## Residual risk / verification gap

**Observation.** Each mutation-revision router output also reported `R18-HEAD-ALIASES` substance false (`refs/heads/main also refused (always-red)`); this made total `open_count` 2 for the first three mutations and 1 for the arbitrary-cause mutation. The per-defect `R18-DEADSEAT-RECORD` fields and reasons above were used rather than attributing the overall strict exit solely to DEADSEAT. The unmutated baseline command was clean. No production files were changed; all four mutation commits remained in `/tmp` clones. No tools were installed or updated.