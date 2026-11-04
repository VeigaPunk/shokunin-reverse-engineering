# ExecC1 — independent six-shape reader measurement

Detailed report: [ExecC1/rederive.md](ExecC1/rederive.md).
Machine evidence: [ExecC1/results.json](ExecC1/results.json).
Own harness: [ExecC1/independent.py](ExecC1/independent.py).

Observed all six assigned shapes accepted by the base reader (exit 0, met true) and rejected by the exact frozen reader (exit 1, met false), each naming its mutation-consistent clause: rev, instrument.sha256, source, before_ceiling_ratio, packed, unknown carrier id. All 14 invocations retain complete argv, status, stdout and stderr. Both extracted reader SHA256 values match the container pins. No declared forged-receipt harness run or imported. Scratch removed in finally; no tool installs, production edits, mutating git commands, or unrelated checks.

Limitation: the supplied unmodified round-69 receipt also fails the frozen reader on producer binding and the three-to-four carrier migration. Thus failures are not isolated mutation-only experiments. Full R70-C1 additionally requires ten shapes, identity-probe and mutation-battery arms, and a genuine landing receipt; this scoped six-shape result does not assert those unmeasured arms.

Self-evaluation: accuracy 4/5 (full raw evidence, but ambient failures limit causality); completeness 5/5 (all six requested shapes and transcripts); clarity 4/5 (detailed transcripts are necessarily long); actionability 5/5 (parent can integrate exact JSON results); conciseness 4/5 (summary separates the large evidence appendix). Overall 4.4/5. Highest-impact improvement for claim-level confidence is integrating the parent's full predicate and genuine landing control; not an expansion of this seat's assignment. The user should agree with the explicitly limited observation.

VERDICT: met — six independent base-accepted forgeries rejected by frozen reader with matching clauses; full R70-C1 not independently established.
