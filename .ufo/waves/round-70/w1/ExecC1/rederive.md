# ExecC1 independent R70-C1 re-derivation

Axes: base acceptance; frozen rejection; mutation-consistent named clauses; evidence reproducibility.

## Method

Own six-shape builder, each a single-field mutation of the supplied round-69 genuine receipt. No declared forged-receipt battery was run or imported. Readers extracted with read-only git show at exact required revisions. No production code edited; no builds, linters, formatters, or unrelated tests run. No tools installed. LSP unavailable in mounted tools; no symbol refactor required.

```sh
python3 -I -B /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-70/w1/ExecC1/independent.py
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 4737a542ae3b1b910d8fe43efbd572bc578b07c6:tools/round-70/packed-elf.py
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin show 5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d:tools/round-69/packed-elf.py
```

## Frozen bytes

- frozen: `1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880` (4737a542ae3b1b910d8fe43efbd572bc578b07c6:tools/round-70/packed-elf.py)
- base: `4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc` (5cc845ca88c90e3e8ceb816f75fe44ddb6758a6d:tools/round-69/packed-elf.py)

Source SHA256: `7f25e2b117e730228106854a25fc413fdc687dc4c0f64f9c32b34ffa9a976411`.

## Per-shape observations

| Shape | Base rc / met | Frozen rc / met | Exact mutation-consistent clause |
|---|---|---|---|
| base-genuine | 0 / True | 1 / False |  |
| wrong-revision | 0 / True | 1 / False | rev 0000000000000000000000000000000000000000 != 4737a542ae3b1b910d8fe43efbd572bc578b07c6 |
| zeroed-instrument | 0 / True | 1 / False | instrument.sha256 0000000000000000000000000000000000000000000000000000000000000000 != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880) |
| relabelled-source | 0 / True | 1 / False | jq: source /usr/bin/exec-c1-relabelled != registry /usr/bin/jq |
| underived-ratio | 0 / True | 1 / False | jq: before_ceiling_ratio 0.5 != ceiling/orig 0.0599 |
| packed-over-ceiling | 0 / True | 1 / False | jq: packed 11 > ceiling 10 |
| unknown-carrier | 0 / True | 1 / False | unknown carrier id exec-c1-unknown |

## Attribution limitation

The unmodified round-69 receipt is itself rejected by the frozen round-70 reader (producer binding and target/carrier-set migration). Therefore rejection alone is not isolated evidence for each mutation. The table records the required mutation-consistent clauses, with all ambient failures retained below and in results.json. This does not establish the full ten-shape predicate, identity-probe arms, battery pin/floor/work-dir/validate arms, or acceptance of a genuine four-carrier landing receipt. Those are outside this six-shape seat assignment. The supplied base genuine control passes the base reader.

## Exact command transcripts

### base-genuine

Mutation: `null`

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/base.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/base-genuine.json
exit: 0
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R69-C3",
 "failing": [],
 "kinds": [
  "executable",
  "shared-object"
 ],
 "met": true,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/base-genuine.json",
 "target": 3
}
stderr:

```

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/frozen.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/base-genuine.json --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
exit: 1
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R70-C3",
 "failing": [
  "instrument.path tools/round-69/packed-elf.py != tools/round-70/packed-elf.py",
  "instrument.sha256 4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)",
  "rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a != 4737a542ae3b1b910d8fe43efbd572bc578b07c6",
  "target 3 != 4",
  "carriers_matched 3 != 4",
  "carrier rows 3 != 4",
  "carrier kinds ['executable', 'executable', 'shared-object'] != ['executable', 'executable', 'shared-object', 'static-exe']",
  "carrier ids ['jq', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']"
 ],
 "instrument_sha256": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc",
 "kinds": [
  "executable",
  "executable",
  "shared-object"
 ],
 "met": false,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/base-genuine.json",
 "rev": "4737a542ae3b1b910d8fe43efbd572bc578b07c6",
 "target": 3
}
stderr:

```

### wrong-revision

Mutation: `{"field": ["rev"], "before": "5ee94c56ce7490938ee38c2e5c10930a1fd1330a", "after": "0000000000000000000000000000000000000000"}`

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/base.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/wrong-revision.json
exit: 0
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R69-C3",
 "failing": [],
 "kinds": [
  "executable",
  "shared-object"
 ],
 "met": true,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/wrong-revision.json",
 "target": 3
}
stderr:

```

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/frozen.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/wrong-revision.json --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
exit: 1
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R70-C3",
 "failing": [
  "instrument.path tools/round-69/packed-elf.py != tools/round-70/packed-elf.py",
  "instrument.sha256 4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)",
  "rev 0000000000000000000000000000000000000000 != 4737a542ae3b1b910d8fe43efbd572bc578b07c6",
  "target 3 != 4",
  "carriers_matched 3 != 4",
  "carrier rows 3 != 4",
  "carrier kinds ['executable', 'executable', 'shared-object'] != ['executable', 'executable', 'shared-object', 'static-exe']",
  "carrier ids ['jq', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']"
 ],
 "instrument_sha256": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc",
 "kinds": [
  "executable",
  "executable",
  "shared-object"
 ],
 "met": false,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/wrong-revision.json",
 "rev": "4737a542ae3b1b910d8fe43efbd572bc578b07c6",
 "target": 3
}
stderr:

```

### zeroed-instrument

Mutation: `{"field": ["instrument", "sha256"], "before": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc", "after": "0000000000000000000000000000000000000000000000000000000000000000"}`

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/base.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/zeroed-instrument.json
exit: 0
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R69-C3",
 "failing": [],
 "kinds": [
  "executable",
  "shared-object"
 ],
 "met": true,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/zeroed-instrument.json",
 "target": 3
}
stderr:

```

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/frozen.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/zeroed-instrument.json --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
exit: 1
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R70-C3",
 "failing": [
  "instrument.path tools/round-69/packed-elf.py != tools/round-70/packed-elf.py",
  "instrument.sha256 0000000000000000000000000000000000000000000000000000000000000000 != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)",
  "rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a != 4737a542ae3b1b910d8fe43efbd572bc578b07c6",
  "target 3 != 4",
  "carriers_matched 3 != 4",
  "carrier rows 3 != 4",
  "carrier kinds ['executable', 'executable', 'shared-object'] != ['executable', 'executable', 'shared-object', 'static-exe']",
  "carrier ids ['jq', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']"
 ],
 "instrument_sha256": "0000000000000000000000000000000000000000000000000000000000000000",
 "kinds": [
  "executable",
  "executable",
  "shared-object"
 ],
 "met": false,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/zeroed-instrument.json",
 "rev": "4737a542ae3b1b910d8fe43efbd572bc578b07c6",
 "target": 3
}
stderr:

```

### relabelled-source

Mutation: `{"field": ["carriers", 0, "source"], "before": "/usr/bin/jq", "after": "/usr/bin/exec-c1-relabelled"}`

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/base.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/relabelled-source.json
exit: 0
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R69-C3",
 "failing": [],
 "kinds": [
  "executable",
  "shared-object"
 ],
 "met": true,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/relabelled-source.json",
 "target": 3
}
stderr:

```

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/frozen.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/relabelled-source.json --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
exit: 1
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R70-C3",
 "failing": [
  "instrument.path tools/round-69/packed-elf.py != tools/round-70/packed-elf.py",
  "instrument.sha256 4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)",
  "rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a != 4737a542ae3b1b910d8fe43efbd572bc578b07c6",
  "target 3 != 4",
  "carriers_matched 3 != 4",
  "carrier rows 3 != 4",
  "carrier kinds ['executable', 'executable', 'shared-object'] != ['executable', 'executable', 'shared-object', 'static-exe']",
  "jq: source /usr/bin/exec-c1-relabelled != registry /usr/bin/jq",
  "carrier ids ['jq', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']"
 ],
 "instrument_sha256": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc",
 "kinds": [
  "executable",
  "executable",
  "shared-object"
 ],
 "met": false,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/relabelled-source.json",
 "rev": "4737a542ae3b1b910d8fe43efbd572bc578b07c6",
 "target": 3
}
stderr:

```

### underived-ratio

Mutation: `{"field": ["carriers", 0, "before_ceiling_ratio"], "before": 0.0599, "after": 0.5}`

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/base.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/underived-ratio.json
exit: 0
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R69-C3",
 "failing": [],
 "kinds": [
  "executable",
  "shared-object"
 ],
 "met": true,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/underived-ratio.json",
 "target": 3
}
stderr:

```

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/frozen.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/underived-ratio.json --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
exit: 1
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R70-C3",
 "failing": [
  "instrument.path tools/round-69/packed-elf.py != tools/round-70/packed-elf.py",
  "instrument.sha256 4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)",
  "rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a != 4737a542ae3b1b910d8fe43efbd572bc578b07c6",
  "target 3 != 4",
  "carriers_matched 3 != 4",
  "carrier rows 3 != 4",
  "carrier kinds ['executable', 'executable', 'shared-object'] != ['executable', 'executable', 'shared-object', 'static-exe']",
  "jq: before_ceiling_ratio 0.5 != ceiling/orig 0.0599",
  "carrier ids ['jq', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']"
 ],
 "instrument_sha256": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc",
 "kinds": [
  "executable",
  "executable",
  "shared-object"
 ],
 "met": false,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/underived-ratio.json",
 "rev": "4737a542ae3b1b910d8fe43efbd572bc578b07c6",
 "target": 3
}
stderr:

```

### packed-over-ceiling

Mutation: `{"field": ["carriers", 0, "packed_counts", "procedure_count"], "before": 3, "after": 11}`

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/base.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/packed-over-ceiling.json
exit: 0
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R69-C3",
 "failing": [],
 "kinds": [
  "executable",
  "shared-object"
 ],
 "met": true,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/packed-over-ceiling.json",
 "target": 3
}
stderr:

```

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/frozen.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/packed-over-ceiling.json --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
exit: 1
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R70-C3",
 "failing": [
  "instrument.path tools/round-69/packed-elf.py != tools/round-70/packed-elf.py",
  "instrument.sha256 4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)",
  "rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a != 4737a542ae3b1b910d8fe43efbd572bc578b07c6",
  "target 3 != 4",
  "carriers_matched 3 != 4",
  "carrier rows 3 != 4",
  "carrier kinds ['executable', 'executable', 'shared-object'] != ['executable', 'executable', 'shared-object', 'static-exe']",
  "jq: packed 11 > ceiling 10",
  "carrier ids ['jq', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']"
 ],
 "instrument_sha256": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc",
 "kinds": [
  "executable",
  "executable",
  "shared-object"
 ],
 "met": false,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/packed-over-ceiling.json",
 "rev": "4737a542ae3b1b910d8fe43efbd572bc578b07c6",
 "target": 3
}
stderr:

```

### unknown-carrier

Mutation: `{"field": ["carriers", 0, "id"], "before": "jq", "after": "exec-c1-unknown"}`

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/base.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/unknown-carrier.json
exit: 0
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R69-C3",
 "failing": [],
 "kinds": [
  "executable",
  "shared-object"
 ],
 "met": true,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/unknown-carrier.json",
 "target": 3
}
stderr:

```

```text
$ python3 -I -B /fast/scratch/hyaku/kaidoku-r70/ExecC1/frozen.py --check-receipt /fast/scratch/hyaku/kaidoku-r70/ExecC1/unknown-carrier.json --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin --rev 4737a542ae3b1b910d8fe43efbd572bc578b07c6
exit: 1
stdout:
{
 "before_ceilings": [
  {
   "ceiling": 10,
   "ceiling_ratio": 0.0599,
   "id": "jq",
   "orig_procedures": 167
  },
  {
   "ceiling": 10,
   "ceiling_ratio": 0.101,
   "id": "xxd",
   "orig_procedures": 99
  },
  {
   "ceiling": 120,
   "ceiling_ratio": 0.6522,
   "id": "libz",
   "orig_procedures": 184
  }
 ],
 "carriers_matched": 3,
 "check": "R70-C3",
 "failing": [
  "instrument.path tools/round-69/packed-elf.py != tools/round-70/packed-elf.py",
  "instrument.sha256 4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc != blob at 4737a542ae3b1b910d8fe43efbd572bc578b07c6 (1601a5b8c91bac4cf3484ac6f1b0a74bd2a7c59590b7c42f149b510e7d021880)",
  "rev 5ee94c56ce7490938ee38c2e5c10930a1fd1330a != 4737a542ae3b1b910d8fe43efbd572bc578b07c6",
  "target 3 != 4",
  "carriers_matched 3 != 4",
  "carrier rows 3 != 4",
  "carrier kinds ['executable', 'executable', 'shared-object'] != ['executable', 'executable', 'shared-object', 'static-exe']",
  "unknown carrier id exec-c1-unknown",
  "carrier ids ['exec-c1-unknown', 'xxd', 'libz'] != registry ['dinit', 'jq', 'libz', 'xxd']"
 ],
 "instrument_sha256": "4ac0d83baee352e42f63b9ced91df01c2ee01f508a35798e400f13478f8aebcc",
 "kinds": [
  "executable",
  "executable",
  "shared-object"
 ],
 "met": false,
 "receipt": "/fast/scratch/hyaku/kaidoku-r70/ExecC1/unknown-carrier.json",
 "rev": "4737a542ae3b1b910d8fe43efbd572bc578b07c6",
 "target": 3
}
stderr:

```

## Evidence and handoff

Retained: independent.py; results.json (argv/rc/stdout/stderr for all 14 checks); base-genuine.json; six exact mutated receipts; this report. Scratch readers and fixtures removed in finally. No frozen instrument writes or git mutations. Parent should integrate this limited independent evidence with the full frozen predicate evaluation.

VERDICT: met — six independent shapes accepted by base and rejected by frozen reader with mutation-consistent clauses; full R70-C1 not independently established.
