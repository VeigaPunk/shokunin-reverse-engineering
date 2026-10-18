# Caller-independent services for long Ghidra analyze runs

Domain: REA/Ghidra analyze runs on this host whose wall-clock exceeds a wave's
lifetime. Not general service management.

## The round-4 incident and its correction

Round 4's 91.6MB run was launched with `systemd-run --user --scope`. The
containment itself worked — the run OOM-killed at its own 7G cap with zero
bystander kills (kernel `CONSTRAINT_MEMCG`, journal-verified) — but a `--scope`
is bound to the launching process's lifetime: when the launching shell exited,
the scope tore down and REA's envelope read `cancelled`. The kernel cause never
reached the record; only systemd's journal held it. The correction, used in
rounds 6-7: `systemd-run --user` as a transient SERVICE unit (no `--scope`) —
caller-independent, survives the launcher, and still carries
`MemoryMax`/`MemorySwapMax` containment plus `StandardOutput=file:` envelope
capture.

## Standing rules (this host, this domain)

1. Long analyze runs are transient user services with an explicit unit name,
   a memory cap (+ swap cap), a disk-backed `TMPDIR` (`/var/tmp/<run>` —
   never the quota-full tmpfs, and no dot-prefixed name, which REA's session
   root silently discards), and `StandardOutput=file:` so the envelope
   survives unit collection.
2. Containment and unit type are independent claims: the r4 verdict stands
   that the memcg cap did its job (one in-scope victim, zero bystanders);
   what failed was lifetime, not containment. Do not let the corrected story
   erase the validated part (`SCORECARD.md`, arc2-loop1-round4 section).
3. The journal is the terminal record for collected units
   (`journalctl --user-unit <unit>`); a unit's post-collection `Result` field
   is residue, not evidence. Capture the envelope out of `/var/tmp` into the
   round's receipts before any cleanup.
4. Whether a service survives its CALLER's kill (as opposed to natural
   exit) is untested — recorded unknown, do not assert it.

## Evidence

r4 scope teardown and containment account: `SCORECARD.md` arc2-loop1-round4;
r6 service-form refusal (7.554s) and mid-rung hold: `corpus/knowledge/2026-10-18-arc2-r6-pe-midrung.md`; r7 service-form 91.6MB hold: `corpus/knowledge/2026-10-18-arc2-r7-pe-wall.md`. (arc2-loop1-round7; adjudicated against the round-6 CR14 generic-advice attack — artifact-anchored, domain-bounded.)
