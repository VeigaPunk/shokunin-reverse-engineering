# R70-C1 base-side rederivation and battery self-test

## Source and scope

Read `plans/round-70-claims.md` §R70-C1 and the round-70 claims container. R70-C1 specifies ten forgeries based on the round-69 three-carrier receipt and requires the base reader to accept them; this task independently probes that base defect and the frozen battery's self-test/validator. No tools were installed or updated.

## Independent base forgery

Source: `.ufo/waves/round-69/l1/scores/c3-at-landing.json`. Preserved its genuine `instrument` and `rev` fields and the carrier rows/arms, but changed jq `orig_counts.procedure_count` to 5000 and `packed_counts.procedure_count` to 1; retained `carriers_matched: 3`, `target: 3`, `met_target: true`, and `failing: []`. The resulting receipt is copied to `forged-base-receipt.json` in this findings directory.

Command: `python3 -I -B <scratch>/base-packed-elf.py --check-receipt <scratch>/forged.json` (reader extracted from base `5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d:tools/round-69/packed-elf.py`).

Observed: exit 0, `met: true`, `failing: []`, despite the invented counts. The base reader reports target/carriers matched 3 and kinds executable/shared-object. This reproduces M69-8: receipt claims pass without binding those counts to producer evidence.

An initial exploratory forgery also set jq `ok` and `arms.identity_ok` false; the reader correctly rejected it (`met:false`, `jq: not ok`, `jq:identity_ok false`, exit 1). This is not the retained claim demonstration; the successful forgery above changes fields the base checker does not derive.

## Frozen forged-receipts self-test

Command: `python3 -I -B tools/round-70/forged-receipts.py --selftest --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --base-rev 5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d --base-tool tools/round-69/packed-elf.py --work /fast/scratch/hyaku/kaidoku-r70/ExecC1Base`

Observed JSON: `cases: 7`, `failed: []`, `ok: true`; exit 0.

## Frozen mutation-check validator probes

Constant receipt `{ "mutants": [], "survivors": [] }`: `--validate` returned exit 1, `ok:false`, `mutants:0`; defects were `pristine_ok not true`, `target_sha256 absent`, `work_dir absent`, and `mutants absent or empty`. It does reject this empty constant receipt.

Historical `.ufo/waves/round-69/l1/scores/c1-at-landing.json`: `--validate` returned exit 1, `ok:false`, `mutants:5`; sole defect was `work_dir absent`. The historical receipt is a genuine r69-era receipt, predating `work_dir`; the r70 structural validator correctly distinguishes it from a valid r70-shaped receipt, but this result alone does not imply the old receipt's historical r69 result was invalid. The validator is shape/version-specific and does not establish provenance merely from nonempty structure.

## Limits / retained observations

No full forged-shapes battery was run; this seat's assigned battery check was `--selftest` plus validator probes. The successful base forgery is independently retained above. Scratch was removed by the shell EXIT trap. No build, lint, or general test suite was run.
