# PROVINCE.md repair — Frontier bullet "Recorded crashes >32 MiB": "all 3 organic cores exceed the cap" is falsified

Authored by SEAT EX-13 (chain c2, executor), wave `arc3-loop1-round4`, 2026-10-19.
**Patch text only** — seats never write `PROVINCE.md`; the parent applies.

## Stale item (census-checked, falsified first-hand this wave)

`PROVINCE.md` Frontier bullet `Recorded crashes >32 MiB`, current bytes:

> mechanism held (Core); all 3 organic cores exceed the cap (waybar 434MB).

Two clauses are falsified by measurement on this host, 2026-10-19:

1. **"all 3 organic cores exceed the cap"** — an *organic* (not deliberately
   generated) core sits **under** the 32 MiB cap and inspects successfully.
   `core.chrome_crashpad.1000.f955c71647bf461e83eafa062d5376a7.1857.…zst`
   (SIGBUS, `/chrome_crashpad_handler`, recorded by `coredumpctl list`)
   decompresses to **17,608,704 B** — below `33554432`. First-hand run:

   ```
   coredumpctl dump 1857 --output=/var/tmp/ex13/core.crashpad.raw     # 17,608,704 B
   npx -y rea-agents@6.4.0 inspect-recorded-crash /var/tmp/ex13/core.crashpad.raw --format json
   ```
   → **exit 0**, `evidence_id ev_1c1cd827435d40c4a1559269ef93d12060986227b71f767e1ebc537cda629f6f`,
   `format: elf-core`, `architecture: x86_64-little-endian`, segment table emitted.
   Transcript: `claims/c2/EX-13/evidence/crashpad-probe.json`.

2. **"(waybar 434MB)"** — no waybar core exists on this host any more.
   `ls /var/lib/systemd/coredump/ | grep -i waybar` → empty; `coredumpctl list`
   shows the waybar entry with `COREFILE missing`. Retention decayed it — which
   the bullet's own final clause predicts.

The **>32 MiB class itself still refuses**, re-measured this wave on an organic
oversize core (`core.git…1214442…`, decompressed **36,360,192 B**):

```
{"code":"invalid_request","category":"invalid_input", … "reason":"out_of_range",
 "message":"Selected artifact exceeds 33554432 bytes: /var/tmp/ex13/core.git.raw"}
```
exit 1. Transcript: `claims/c2/EX-13/evidence/git-oversize-probe.json`.
So the headline (`>32 MiB`) stays; the *inventory* clause and the *implication*
that no organic crash can be inspected here are what the repair removes.

Cause of staleness: the bullet's inventory was frozen at r2
(`corpus/knowledge/2026-10-13-r2-crash-inspect-probe.md`: "every *organic* core
on this host (waybar 434M, localsearch 71.8M, godot ≥16M-compressed) exceeds
REA's fixed 32 MiB input cap") and was never re-derived as the coredump
directory churned.

## Change (same-line replacement, line count held at 3)

`PROVINCE.md`

```diff
# file: PROVINCE.md
-- **Recorded crashes >32 MiB** — mechanism held (Core); all 3 organic cores
-  exceed the cap (waybar 434MB). Needs a cap-raising knob or partial-core
-  intake — neither exists. Retention decays oldest-first.
+- **Recorded crashes >32 MiB** — mechanism held (Core); the oversize class
+  still refuses `out_of_range`, but an organic 17.6MB core inspects (arc3-r4).
+  No cap-raising knob or partial-core intake. Retention decays oldest-first.
```

## Census conformance

- Line-neutral: 3 → 3 lines; `PROVINCE.md` stays at 162 lines (DATED marker at
  line 119 does not shift).
- Needle-free: no `rea-agents@x.y.z`, no bare `6.x.y`, no `~`/`/`-absolute
  `path:line`. The block stays outside the census's needle vocabulary, so the
  UNDECLARED region (72–118) cannot read `FAIL (undeclared=1)`.
- `Retention decays oldest-first` is kept — it is now *confirmed* by the
  vanished waybar core rather than merely asserted.

## Note for the parent (rule #14 / admission boundary)

Clause 1's evidence is this seat's **first-hand measurement this wave**, not yet
an admitted corpus entry (`corpus/knowledge/` is 83 files; no arc3-r4 crash
entry has landed). The repair is worded to state the measured fact without
claiming a corpus admission. If the parent prefers corpus-only evidence for the
landing, either land the crash measurement as a corpus entry first, or apply
this patch's clause 1 only after it lands.
