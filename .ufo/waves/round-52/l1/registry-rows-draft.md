# instrument-registry v2 rows for tools/round-52/ (draft; land in SKILL.md registry at the freeze/landing)

Shape (per protocol §Gate standard): name, gate|probe, entry command, verdict map,
self-test command + spelling, pinned-value path, write scope, owner.

| `tools/round-52/c1-counter.py` | gate — R52-C1 coverage: carriers_matched + law_shape_ok + census_rederived_ok + depth_gap_recorded + bindings | `0` met (carriers_matched == 4, every binding true, frozen_path_changed []); `1` not met (semantic red, incl. mutants); `2` could-not-evaluate (missing args, unknown revision, frozen-path drift, oracle_env_error) | `python3 -I -B tools/round-52/c1-counter.py --selftest` — flag `--selftest`; N isolated fixture cases (v1 battery carried + new: drift exit-2, ENOENT-retry-exhausted red, law_shape red, census fail, prior-pin allow-list receipt, depth-gap recorded, wrong-carrier-set), exit 0 iff no case fails | expected values: plans/round-52-claims.md constants + tools/round-52/gap-rule.json + fixtures in the selftest | read-only over the lane; REA rerun writes only under /fast/scratch/hyaku/kaidoku-r52/ | kaidoku |

| `tools/round-52/c1-controls.py` | gate — R52-C1 pre-freeze control battery (offline, committed round-50 envelopes) | `0` all controls show their expected verdicts; `1` a control disagrees (kill rule); `2` could-not-evaluate | `python3 -I -B tools/round-52/c1-controls.py --selftest` — flag `--selftest` | EXPECTED.md table (frozen at the freeze) + per-control JSON receipts | read-only; receipts to --out dir | kaidoku |

| `tools/round-52/c1-run.sh` | probe — R52-C1 data harness (after arm = REA run; oracle arm = three producers) | `0` ok; `2` usage/environment/precondition; `3` tool failure or producer disagreement (never 1: the counter judges) | no selftest (probe; exercised by the data run + ExecOracleDry synthetic receipt) | tool pins rea-agents@6.5.0 / unblob 26.6.4 / sasquatch 4.5.1 / unsquashfs 4.7.5 | writes receipts to corpus/evidence/round-52/c1 (after --data-run only) + scratch | kaidoku |

| `tools/round-52/fetch-vendor.py` | probe — pinned-chain carrier fetch (image sha → member sha → cache) | `0` fetched+pinned; `2` usage; `3` pin mismatch / guard refusal | `python3 -I -B tools/round-52/fetch-vendor.py --selftest` — offline, proves https-scheme/allowed-host/redirect guards fail closed (deleted-guard fixture copies) | tools/round-52/carriers.json (pins); --plan mode prints without network | writes cache only under the given --cache-dir (kaidoku-r52); never the lane tree | kaidoku |

| `tools/round-52/sqfs-triage-v6.py` | gate — R52-C2 depth: triage v6 labels + executability audit + census clause | `0` clean (pair_mismatches 0, evaluator_missing 0, executability_violations 0, census_outside 0); `1` violation (audit/mismatch/census); `2` could-not-evaluate (table missing/malformed, frozen-path drift) | `python3 -I -B tools/round-52/sqfs-triage-v6.py --selftest` — v5's 18-case battery + new-row-deleted/action-swapped/audit-guard-deleted/census-guard-deleted/do-nothing mutants | reader-census table + expected verdicts frozen in the instrument; corpus manifest .ufo/waves/round-42/w1/artifacts/R42C2ReconLegacy/envelopes/ | read-only | kaidoku |

| `tools/round-52/misroot-sweep.sh` | probe — read-only fleet-root stray classifier (misroot clause helper) | `0` classified (report printed); `2` usage; --apply performs copy+cmp+delete for lane strays only after showing | `tools/round-52/misroot-sweep.sh --selftest` — fixture-repo cases (planted stray classified; non-lane stray untouched) | fixture receipts | read-only by default; --apply deletes only fleet-root copies it classified as kaidoku's | kaidoku |

| `tools/round-52/gap-rule.json` | data — the frozen law-derived gap rule (consumed by c1-counter.py; claim R52-C1) | n/a (data) | validated by the counter's rule parser + ExecRuleFixtures grammar receipt | this file | read-only | kaidoku |

NOT registered (seat-side or wave evidence, not lane instruments): check-dispatch.py,
wave-accounting.py (live in .ufo/waves/round-52/; wave evidence).
