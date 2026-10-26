# R40C1Counter — `c1-counter.py` for P40-C1 (pre-freeze build)

**Verdict: DONE** — the round-40 C1 counter is written, self-tested (70 cases, 5 green / 65 red, every
one of the 17 per-carrier clauses and 10 bindings has at least one red witness), and exercised against
real REA 6.5.0 runs; integrating it at `tools/round-40/c1-counter.py` is the L1's remaining step.

Axes named (Godspeed): **coverage** = the five things a receipt cannot fake cheaply (carrier layout
bytes, oracle publication, gap rule, evidence-id rule, and the rerun comparison) are each a separate
clause with its own red witness; **depth** = two routed defects were turned into executable limits
(R39-CL5 fabrication → rerun projection; R39-CL4 control tables → frozen-table validation), and the
two defects this seat found *in the predicate* (oracle-closed `core`, and the un-replayed extraction
depth) are measurable and closed.

## Deliverables

| path (under `.ufo/waves/round-40/w1/artifacts/R40C1Counter/`) | sha256 / size |
|---|---|
| `c1-counter.py` (the tool; integrate at `tools/round-40/c1-counter.py`) | `39e47e872e9c716d5fa1af6eb8dcf09ba3ed20b8f560875f2e905241a76b6c33`, 103 KB |
| `c1-contract.md` — frozen-table + documentation contract for the L1/harness/recon/scribe | 182 lines |
| `selftest.log`, `selftest-detail.log` — 70 cases, per-case exit/clause attribution | 85 B / 70 DETAIL lines |
| `selftest-rea.log` — real-REA end-to-end on the development AVM image | 1.4 KB |
| `cli-smoke.json`, `cli-smoke.err` — CLI exit paths on a fixture lane (real runner) | 25 KB |
| `projection-stability.json` — 3 real runs of one carrier: 48 envelope fields vary, projection equal | 6.2 KB |
| `projection-profiles.json` — all four profiles stable across those runs | 2.1 KB |
| `projection-agreement.json` — counter projection == `R40C1Projection/projection.py` on 6 real envelopes × 4 profiles | 2.1 KB |
| `depth-replay.json` — depth-1 vs depth-3 receipts and the counter's parameter replay | 1.5 KB |
| `dev-avm-be-4096.squashfs` — copy of the development input used by `--selftest-rea` | `c7f74691b3e8d76777322f568cea640e08b7d52c994b6bc53a01388faed32d32` |

Report: `.ufo/waves/round-40/w1/R40C1Counter.md`

## What the counter enforces

Adapted from `tools/round-39/c1-counter.py` with its spine kept: lane bytes only through
`git show REV:path`, a private scratch under `$HYAKU_SCRATCH/kaidoku-r40`, the frozen evidence-id
recompute (`tools/round-27/xpin-attribute.mjs`, the package's own `semanticProjection`), freeze-integrity
exit 2 `frozen_path_changed` over `FREEZE..REV` (a later restore does not un-block), exit 0 met / 1 not
met / 2 unevaluable, `--json-out`, `--selftest`.

New per-carrier clauses (all 17 in the module docstring, with reasons):

- `layout_ok` — the layout test implemented here, not borrowed: BE `sqsh` magic, v4.0,
  `mkfs_time == bytes_used`, `0 < bytes_used <= size`, and the 2-byte metadata block header at
  `inode_table_start` decoding as a little-endian length in 1..8192 while the BE decode is not
  plausible; when both decodes are plausible the single-block identity
  `inode_table_start + 2 + len_le == directory_table_start` settles it, otherwise the carrier is
  ambiguous and red. The marker alone never passes a carrier (`gen-squashfs.py --endian avm` and a
  marker-stripped genuine body are both red witnesses).
- `gaps_ok` — the gap rule is **data** (`.ufo/waves/round-40/c1/gap-rule.json`): path-resolved gaps must
  land on exactly one non-regular entry whose `allowed` list holds their kind; required kinds need one;
  pub­less structural gaps (`unknown-chunk-handler`, `depth-limited`) need their own frozen per-carrier
  allowance; `nonregular_unpublished_ok` refuses a materialised symlink/device.
- `projection_ok` — the rerun binding (below).
- `receipt_fresh` strictly after the freeze; receipts are deliberately not frozen.

Bindings: province Core section/row (handler in the first cell + `AVM[ _-]layout` + entry path),
one-line round-40 frontier note, entry presence, `sourced` (S-id opened 2026-10-26 whose used-by lists
the entry), README coverage-map row, carrier-spec well-formedness (4 ids, 4 distinct pins, `target`
consistency), `gap_rule_ok` (schema + every reader kind covered), `compression_coverage` (gzip leg and
xz leg), `frozen_tables_valid` (both tables parse at the freeze commit, R39-CL4).

## The rerun clause, and the two predicate defects it exposed

The counter re-runs each pinned carrier with `npx -y rea-agents@6.5.0 extract-firmware --format json
--full-output <bytes> <fresh outdir>` (`REA_UNBLOB_COMMAND` absolute, cwd and `TMPDIR` in scratch) and
compares a semantic projection with the committed receipt. Two things had to be fixed for that binding
to be true rather than decorative.

**1. `core` is oracle-closed — measured, then closed by the L1's profile ruling.** The draft's six
fields (subject digest, files suffix/sha/size, chunks handler/start/end/failed, gaps kind/suffix/deps,
unpublished kind/suffix, diagnostic typenames) are all derivable from `oracle.tsv` + `nonregular.tsv` +
the claim: a tables-literate forger needs no run. Two selftest witnesses record both sides — an
explicit `core` lane accepts a receipt whose only difference is `published_bytes`, while the default
lane refuses the same receipt naming `published_bytes`. The L1 ruled `plus-extractor` for every carrier;
the counter now defaults to it, takes it from the optional frozen `projection` key, echoes
`projection_profile` in the score JSON, and keeps all four profiles implemented. All four were stable
across three real runs of one carrier, and my inline implementation is byte-identical to
`R40C1Projection/projection.py` on six real envelopes (three live runs + round-39 K1/K5/K6) for every
profile.

**2. REA's default depth would have redded every carrier under the ruling.** The L1 ruled receipts at
`--max-depth 1`; a depth-1 extraction is `partial` with a different published set and an extra
`depth-limited` gap. A rerun at REA's default depth 3 therefore cannot match, whatever the profile: on
the round-39 K5 copy, depth-1 vs depth-3 differs in `files`, `extraction_gaps` and `derivations` under
every profile, while depth-1 vs depth-1 (different outdir, different staged name) is equal. The counter
now replays the receipt's recorded `parameters` (`max_depth`, `max_output_bytes`,
`max_output_files`) and records what it replayed; measured, its own runner on a depth-1 receipt's
parameters reproduces that receipt under both `core` and `plus-extractor`.

Projection stability, measured (three real runs of the retained development image, different input
names and output dirs): 48 envelope fields vary — `evidence_id`, `chunks[].provider_id`,
`derivations[].provider_blob_id`, every `files[].path`, `output_directory`, `parameters.path`,
`raw_result` subtask/blob paths and args, `subject.name`/`local_path` — and the projection is equal
across all three runs for all four profiles. Excluding the chunk `*_extract` directory is load bearing:
the counter stages the carrier as `carrier.bin`, the receipts as `carrier.sqsh`.

## Evidence (exact commands, outputs, exit codes)

```
# fast selftest (offline; simulated runner), cwd = lane root
TMPDIR=/fast/scratch/hyaku/kaidoku-r40/R40C1Counter HYAKU_SCRATCH=/fast/scratch/hyaku \
  python3 .ufo/waves/round-40/w1/artifacts/R40C1Counter/c1-counter.py --selftest \
  --pkg65 /home/vgpnk/.npm/_npx/ad9a3fdbcad992c6/node_modules/rea-agents
  -> {"selftest": "c1-counter", "cases": 70, "green_ok": 5, "red_ok": 65, "failures": []}   exit 0
  -> C1_SELFTEST_DETAIL=1 adds 70 DETAIL lines (per-case exit, failing clauses, bindings, projection_diff)

# real-REA end-to-end: two real runs of the development AVM image, then an oracle-only fabrication
… c1-counter.py --selftest-rea --pkg65 <rea-agents 6.5.0 root> --rea-timeout 300
  -> green: carriers_matched 1, failing [], projection_diff [], bindings_false ["compression_coverage"]
     (the one-carrier fixture lane has no gzip leg; the binding is a 4-carrier property)
  -> fabrication: met_target false, failing ["handler_ok","projection_ok"], diff ["files","chunks","derivations"]
  -> layout_ok true, meta_signal "plausibility", hdr 7400 -> LE 116 / BE 29696, identity 239
     (image sha256 c7f74691…d32, 4096 B)                                            exit 0

# CLI exit paths on a fixture lane (own git repo in scratch, real REA runner)
  frozen files only            -> exit 1, matched 0, all boolean bindings true
  receipts + real rerun        -> exit 1, projection_ok false on all four carriers, diff
                                  ["files","chunks","gaps","diagnostics"]  (synthetic carriers extract to nothing)
  --no-rerun                   -> exit 2, {"reason": "rerun_disabled"}
```

Selftest coverage: 70 cases covering every clause and binding, including an oracle-only fabrication with
a re-minted evidence id (refused on `projection_ok`), a fabrication differing in one published sha256,
one extra gap, a dropped diagnostics multiset, a marker-stripped genuine-LE-lengths carrier, a
standard-BE carrier, an ambiguous header settled and unsettled by the identity, all three frozen-path
restore cases (carrier, gap-rule, and a claims/counter edit), a path-less gap within/over/without its
allowance, the depth-replay plumbing, the profile witnesses, and the documentation bindings.

## Findings routed to the freeze (all messaged, in addition to this report)

1. **Gap-rule kind spellings (fixed).** Recon's first `gap-rule.json` keyed `device`/`hardlink`, but the
   frozen reader emits `dir|symlink|block-device|char-device|fifo|socket` and lists every directory, so
   `gap_rule_ok` would have been red with every per-carrier clause green. Recon re-emitted
   (`sha256 df05de05…722e`, 445 B); it now parses with zero problems and covers every reader kind.
2. **Structural gaps (fixed).** Without a frozen allowance, a genuine vendor member's path-less
   `unknown-chunk-handler`/`depth-limited` gaps red the predicate. Measured on recon's own development
   envelope: 88 gaps = 86 `unpublished-entry` + 1 + 1; passes with `{"unknown-chunk-handler": 1,
   "depth-limited": 1}`, fails without, fails at `depth-limited: 0`.
3. **`core` is oracle-closed (ruled).** L1 ruled `plus-extractor`; the counter default now encodes it.
4. **Depth replay (fixed).** See above; a receipt whose parameters the counter did not replay could
   never match under `plus-extractor`.

## Risks and residual limits

- **The rerun is necessary but not sufficient.** Under the ruled profile a receipt that does not come
  from a run of the pinned bytes cannot match without predicting the extractor's derivations, engine
  identity, published byte count and coverage. A forgery that reproduces all of that is semantically
  equal to a real run and cannot be refused by any projection — that is the bound R39-CL5 asked for,
  and it is now explicit rather than assumed.
- **Scoring environment.** The counter needs `npx`, `node`, `tools/round-27/xpin-attribute.mjs`, the
  rea-agents 6.5.0 package and an absolute `unblob`; a missing one is exit 2 (`rerun_env_error`), never
  met. Cost at scoring: one fresh REA run per carrier (4).
- **V2** depends on the vendor scout; if that fails, `TARGET`/`IDS` must change **before** the freeze —
  after the freeze the carrier table and the counter are both frozen paths and any edit is exit 2.
- **`compression_coverage`** needs one gzip-id carrier and one xz-id carrier; the draft's L1/L2 promise
  that, but a set of four xz members is red by design.
- Per-carrier `bytes_used <= size` assumes the carrier is the member, not a padded container; a carrier
  window longer than the member is fine, a truncated one is red.
- [INFERENCE] The frozen lane's judge runs `--selftest` (offline) rather than `--selftest-rea`; the
  latter needs the retained development image and network-free npx cache, both present here.

## Bounds compliance

Writes: only `.ufo/waves/round-40/w1/R40C1Counter.md` and the artifact directory above. No lane file in
`corpus/`, `tools/`, `plans/` or the top level was touched (a stray `detail.log` written to the lane
root by an early redirect was removed; `git status` shows only `.ufo/waves/round-40/` and the L1's own
untracked `plans/round-40-claims.md`). No VCS mutation: fixture repos were created with
`mktemp -d` + `git -C` under scratch, with `-c user.name=fx -c user.email=fx@fx` and a toplevel
assertion; the lane was only read (`git show`, `git log`, `git rev-parse`, `git status`).
**No REA or unblob run touched any C1 carrier**: every run was on the development AVM image
`round11/work/avm-be.squashfs` (copied into scratch), a round-39 K5 copy, or my own fixture bytes.
Shokuknow was read-only. No tool installed, upgraded or removed; no pacman transaction; `sasquatch`,
`sasquatch-v4be` and `unblob` untouched. Scratch `/fast/scratch/hyaku/kaidoku-r40/R40C1Counter` removed
at exit; cited bytes were copied into the artifact directory (4 KB image) or replaced by a digest plus
the command that rebuilds them (bulk envelopes).
