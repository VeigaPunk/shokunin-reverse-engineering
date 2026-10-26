# LOG.md round-42 entry skeleton (R42-C1 / R42-C2)

Target: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/LOG.md`, appended after the round-41 entry
(`## 2026-10-26 — round 41: …`). Shape copied from the round-41 entry: bold lead phrases, one bullet per
fact class, every number a fill token, dated 2026-10-26. Do not state a verdict the counter has not
produced: the two score bullets carry the exit code and the artifact path, and the coverage bullet names
`Frontier → Core` only if the counter met its target.

```markdown
## 2026-10-26 — round 42: SquashFS v3 handler family to Core on four published third-party images (R42-C1 `<<L1:c1-verdict-word>>`, `<<L1:carriers-matched>>`/4); triage table v4 `<<L1:c2-verdict-word>>` (`<<L1:c2-matched>>`/`<<L1:c2-n>>`)

- **Claims** (`plans/round-42-claims.md`, frozen `<<L1:freeze-commit>>`): R42-C1 coverage — the unblob 26.6.4 `squashfs_v3*` handler family (`squashfs_v3`, `_ddwrt` `tqsh`, `_broadcom` `qshs`, `_nonstandard` `sqlz`) Frontier → Core on four fresh frozen **published third-party** v3 images, scored by a port of the round-41 C1 counter against an oracle pair that is not sasquatch (`unsquashfs` 4.7.5 + 7-Zip 26.04); R42-C2 depth — SKILL rule block 21, table v4 over the whole SquashFS handler family, one `declared_features` key (R41-CL1), a legacy-failure row (R41-CL4) and combos a named-class lookup cannot reach.
- **Motivating evidence:** round-41 closure D1–D5 (`corpus/lessons/round-41-verifier-spotcheck.md` §5) and routed defects R41-CL1..CL4 (`corpus/lessons/round-41.md`).
- **Controls before data** (`<<L1:controls-commit>>`): C1 do-nothing `<<L1:ctl-c1-0>>`, relabelled round-41 receipts `<<L1:ctl-c1-1>>`, oracle-only fabricated receipt `<<L1:ctl-c1-2>>`; C2 counter at the freeze `<<L1:ctl-c2-0>>`, v3 table under the v4 marker `<<L1:ctl-c2-0b>>`, the shortcut set topping out at `<<L1:ctl-c2-max>>`, lookup control `<<L1:ctl-c2-7>>`. No control reaches a target.
- **Data:** C1 REA `extract-firmware --max-depth 1` receipts (`<<L1:c1-data-commits>>`) — `<<L1:carrier-1-id>>` `<<L1:carrier-1-published>>` files / `<<L1:carrier-1-gaps>>`, `<<L1:carrier-2-id>>` `<<L1:carrier-2-published>>` / `<<L1:carrier-2-gaps>>`, `<<L1:carrier-3-id>>` `<<L1:carrier-3-published>>` / `<<L1:carrier-3-gaps>>`, `<<L1:carrier-4-id>>` `<<L1:carrier-4-published>>` / `<<L1:carrier-4-gaps>>`, each + 1 `depth-limited`, no failed chunk. C2 held-out seed = freeze (`<<L1:c2-data-commit>>`), `<<L1:c2-n>>` carriers.
- **Scores at `<<L1:measured-revision>>`** (`<<L1:scores-dir>>`): C1 `<<L1:carriers-matched>>`/4, exit `<<L1:counter-exit>>`; `c1-extra` `<<L1:c1-extra-verdict>>`. C2 `<<L1:c2-matched>>`/`<<L1:c2-n>>` pairs, exit `<<L1:c2-exit>>`; `<<L1:c2-binding-failures>>`.
- **Re-verification (freshness):** every carrier re-fetched from its publisher and re-hashed at the freeze (`tools/round-42/fetch-carrier.py`, `<<L1:fetch-evidence>>`) and again in wave 2 (`<<L1:w2-refetch-report>>`); the v3 handler source re-read at the installed pin (sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287`); the oracle pair re-run on the fixtures.
- **Wave 2** (`<<L1:w2-seat-count>>` seats): `<<L1:w2-verdict>>`. Defects routed `<<L1:routed-ids>>` (`corpus/lessons/round-42.md`).
- **Frontier step:** SOURCES `<<L1:sources-before>>` → `<<L1:sources-after>>` (`<<L1:sources-rows-final>>`); assimilation `<<L1:assim-verdict>>`; QUALITY `<<L1:quality-n>>`; entry `corpus/knowledge/2026-10-26-r42-squashfs-v3-core.md`.
- **Tool installs:** `<<L1:installs>>` (channel, version, reason; "none" if none).
```

Writing discipline for this entry (learned from round-41's log and the round-39/40 corrections):

1. A bullet that reports a score names the counter, the revision, the exit code and the artifact path.
   Prose "met" without those three is not admissible.
2. Do not describe a control as "killed" unless the scored row shows fewer than the target; a control that
   reaches the target is the round's stop, and the entry says so in the same bullet.
3. The LOG records commits by short hash and by what they added, never by intention. If a repair commit
   reverted a wave-1 edit, say which bytes were restored.
4. "Tool installs" is mandatory even when empty: "No tools installed or updated by the L1 in round 42."
