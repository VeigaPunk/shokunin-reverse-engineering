# SquashFS `extract-firmware` outcome triage v4, scored on a fresh held-out set under a generator that cannot declare the unobserved (round 43)

source: S112 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/handlers/filesystem/squashfs.py — `SquashFSExtractor` :24-70 (`EXECUTABLE = "sasquatch"` :25, `V4BE_EXECUTABLE = "sasquatch-v4be"` :26, the `match endian, self.version` argv decision :39-54, AVM marker branch :42-50, the 4-token argv tail :56-64, `get_dependencies` :68-69), the seven v1-v3 handler `NAME` lines :102,:159,:200,:245,:319,:364,:410, the three v4 `NAME` lines :455,:514,:549 with their extractors :527,:553 — re-read 2026-10-27 from the installed unblob 26.6.4 tree (`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob/`), whose `handlers/filesystem/squashfs.py` sha256 `2d7b901b54e2ad28c28df2cbbdaeb4bcedb58670fb4c4478f9578a0dd5599287` equals the S112 row pin
source: S118 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/extractor.py — `is_recursive_link` :42-47, `fix_symlink` :50-92 (loop :58-65, empty-target branch :67-69, containment :79-87, kept-link rewrite :88-91), `carve_unknown_chunk` :116-127 (`extension = "unknown"` :119, `<start>-<end>.<ext>` :123) — re-read 2026-10-27 from the installed tree (`extractor.py` sha256 `1bb498119429ed80ae29caf9772d2b6210c22b6a8a2c8beb6cfea94550bcd23a`, tag 26.6.4 = commit `1fcc7a0a584a70a96c31f5a276c20944d199a089` as the S118 row records)
source: S119 — https://registry.npmjs.org/rea-agents/-/rea-agents-6.5.0.tgz — `dist/firmware/FirmwarePublication.js`: `GAP_CONTINUATIONS` :14-19 (`unpublished-entry` continuation :18, `depth-limited` :19), `MAX_EXTRACTION_DEPTH = 10` :23, `depthContinuation` :24-29, `emptyGap` :39-46, `gapSortKey` :47, `dependencyExtractionGaps` :152 with its body :161-201 (`chunk_missing_dependencies` :161, standalone `missing_dependencies` :195), `chunkGaps` :225-238, `unknown-chunk-handler` chunk gap :286, `encrypted-chunk` :287, `extractor-failure` stage gaps :275-284 and chunk gaps :288-293, `depth-limited` :294-299, `unpublished-entry` :301-307; `dist/domain/firmware/firmwareAnalysis.js` gap kinds :88-90 and `unpublished_entries` :137-141; `dist/firmware/FirmwareRelease.js:27-32` — re-fetched this round as `npm pack rea-agents@6.5.0`, tarball sha256 `531717a06e92ca651aab52691190f916fac044272c01f875e22c5e293218e699` equal to the S119 row pin; the tarball's `dist/firmware/FirmwarePublication.js` (322 lines) is sha256 `bb4f3246bee70a5b32b048e5ef956e649626b6449b1d457454440739a8d51029`. The host's global `rea-agents` install is 6.7.0 and is **not** the measured package: its `FirmwarePublication.js` shifts the same clauses to :293/:301/:310/:317, so no anchor in this entry is read from it
source: S120 — https://raw.githubusercontent.com/onekey-sec/unblob/26.6.4/python/unblob/report.py — `ExtractCommandFailedReport` :91-98 (`command` :95), `ExtractorDependencyNotFoundReport` :118-122, `ExtractorTimedOut` :125-138 (`cmd` :129), `MaliciousSymlinkRemoved` :133-138; `extractors/command.py` raise sites :59-77 and `Command.get_dependencies()` :101-102 — re-read 2026-10-27 from the installed unblob 26.6.4 tree
source: S121 — https://raw.githubusercontent.com/onekey-sec/sasquatch/sasquatch-v4.5.1-6/squashfs-tools/unsquashfs.c — `-be` sets the swap flag and `read_block` swaps the block-length header only when it is set; `debian/rules` builds the same tree a second time as `CFLAGS=-DFIX_BE` and ships it as `sasquatch-v4be` — row pointer only this round (the inherited AVM row's citation), not re-fetched
source: S130 — https://github.com/onekey-sec/unblob/tree/26.6.4/tests/integration/filesystem/squashfs (LFS payload base `https://media.githubusercontent.com/media/onekey-sec/unblob/refs/tags/26.6.4/tests/integration/filesystem/squashfs/`) — the MIT-licensed unblob 26.6.4 SquashFS test fixtures the held-out generator embeds, pinned by `tools/round-42/fixtures.json` (sha256 `9f957663c1f21940ec17e32f98485425145b6c4e7eb265a7b12327b629c3da9b`, 14 pins, tag commit `1fcc7a0a584a70a96c31f5a276c20944d199a089`) with committed copies under `corpus/evidence/round-42/c2/fixtures/` — opened 2026-10-26 (`.ufo/waves/round-42/w1/R42SrcUnblob.md`), re-verified this round only as the pin file's sha256 above
source: S135 — unblob 26.6.4 license text, the basis on which the carriers may embed S130's fixtures — read this round from the installed distribution's metadata (`~/.local/share/uv/tools/unblob/lib/python3.13/site-packages/unblob-26.6.4.dist-info/licenses/LICENSE`): 1068 B, sha256 `67303bbde385e13f69e8019f6f8bc77d4ebfce58c2a409952645e3fe4f4d922e`, MIT text; the row is opened by the round-43 L1 at 2026-10-27T08:08Z (HTTP 200, same 1068 B, same sha256 `67303bbd…`). Scope: the license grant only, never a statement about fixture content
verified-at: 2026-10-27
recheck: 180d — `python3 -I -B tools/round-42/sqfs-triage-v4.py --skill SKILL.md --table-only` -> `marker line: 521  actions line: 522  table line: 523  rules: 15`, exit 0 (run at the base `6b9e64fe` this round; the frozen interpreter's own sha256 `497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9` is unchanged at `d1681696` and at the round-43 base); the score recheck is `python3 -I -B tools/round-43/c1-counter.py --root <LANE> --rev <<L1:measured-revision>> --freeze <<L1:freeze-commit>> --json-out <OUT>` -> exit `<<L1:counter-exit>>`, and a re-fetch of the S119 tarball that lands bytes other than `531717a0…` means the gap-clause anchors in this entry are re-read
status: R43-C1 (R42-V5 ordering kept: provenance trio first) — scored on the fresh round-43 held-out set by `tools/round-43/c1-counter.py` at `<<L1:measured-revision>>`, `matched <<L1:matched>>/<<L1:n>>`, exit `<<L1:counter-exit>>` (`<<L1:score-artifact>>`); this line states the score that the freeze's own counter run produced, never a target, and if that exit is not 0 it is replaced by the honest stop — exit code, `bindings_false` list, receipt — and the PROVINCE row with it, exactly as round 42's `C02` stop replaced its row

**What stopped at round 42, in one paragraph.** Round 42 froze the v4 table and generated a held-out set of 78
carriers whose manifest declared, per carrier, the six-field feature tuple the table reads; on 2026-10-26 the
round-42 C2 counter scored that set at `eb8215ac87860f0e52745a4f842485bf8a6fe3b8` and returned exit 1 with
`bindings_false ["observed_features_match_declared"]` although the table's (label, action) pair matched its
independent evaluator on 78 of 78 carriers (`.ufo/waves/round-42/l1/scores/c2-at-eb8215ac.json`, blob
`9989e1c41d0fd393a03647ee128c04c8cdf1d1ee` at HEAD, sha256
`0b4e6026e1d92f3d4a5e4c73da6a0ee4574998fc40d58edbd5ca8ab9997f21eb`, committed at `d4b4b4fb`; the stop commit
message records `78/78 matched but observed_features_match_declared false (combo C02 declared gap set lacks
depth-limited), exit 1`). The one carrier that differed was the combo `C02`: the manifest declared
`gap_kinds ["extractor-failure","unpublished-entry"]` and REA 6.5.0's own envelope carried
`["depth-limited","extractor-failure","unpublished-entry"]` — one failing chunk beside a sibling extraction that
reached the depth ceiling, which REA mints per `depth-limited` path (S119 `FirmwarePublication.js:294-299`) —
so the declared-versus-observed difference was exactly one extra observed kind, the receipt's
`declared_features.mismatch[0]` (`differ ["gap_kinds"]`), and the round stopped on the binding rather than relabel
the carrier. That mistake is recorded as M42-2 (`corpus/lessons/round-42.md:26`) and routed as R42-CL1.

**What changed: the generator may no longer declare what it did not observe (QUALITY 85).** The round-43
generator `tools/round-43/heldout-gen-v4r43.py` (a port of `tools/round-42/heldout-gen-v4.py`, which is frozen at
sha256 `c2b1641ad6beec0d8eead002520174fb596c574efe44220c4a440917be03a5e1` and unchanged at the base) measures
instead of predicting: in its `--run` pass it extracts every carrier with REA 6.5.0, reads the observed six-field
tuple out of the envelope it just produced, and, before finalizing the manifest, compares that tuple with the one
the manifest would declare for that carrier. Any difference refuses the manifest — exit 3
`declared_tuple_unobserved`, no manifest written, a per-carrier declared-versus-observed diff on stdout — so a
manifest that exists at all is one whose declared tuples were observed by the same run that wrote it. That is the
QUALITY 85 rule as stated in `corpus/lessons/round-42.md:26` ("the generator must refuse to write a manifest whose
declared tuple differs from the observed one in its own `--run` pass … red: this manifest; green: a manifest built
after that check") and `:81`. The manifest additionally records the check's own verdicts under
`generator.tuple_check` (`<<L1:tuple-check-verdicts>>`), so the counter binds the generator's report of its own
refusal rather than trusting the generator's silence. The set's class structure is round 42's: 27 named classes at
two carriers each plus 24 combo carriers, n = 78, each carrier declaring the single-key `declared_features`
contract (R41-CL1), seeded by the round-43 freeze commit `<<L1:freeze-commit>>` and committed first in a commit
descending from that freeze (`<<L1:heldout-dir-commit>>`). Combo `C02`'s round-42 shape — a failing chunk beside
a sibling extraction at the depth ceiling — is required to appear among the new seed's combos with the manifest
declaring what was observed, `depth-limited` included; whether it did is a property of the seed the generator
used, not of this entry.

**The table is unmoved, and the claim does not touch it.** The region `SKILL.md` gives the v4 marker — from the
line containing `<!-- sqfs-triage-table v4 -->` through the end of the first markdown table after it, 15 rule
rows, 13 856 bytes — is byte-identical at the round-42 freeze `d1681696dd63ca4f9b8a09ffa8fa3e2de5e2b51b`, at the
round-43 base `6b9e64fe7e0de202d9383baad5792fbfe039a743` and at the measured revision: sha256
`92540586b8c03dcde511652c0d76ba93cbde8e5f4e79e0b94509192c19b101f2` at each, versus
`<<L1:region-sha256>>` at `<<L1:measured-revision>>`. The two frozen readers are unmoved with it:
`tools/round-42/sqfs-triage-v4.py` (interpreter) sha256
`497bab6766a0b0c6d6f36cb58cadc531bddf9dd3231f6100bf46cf6ff552a2e9` and `tools/round-42/indep-eval-v4.py`
(evaluator) sha256 `7a135dd36b3cab29d4dfa5b5d6dcf2199c026989549683933f4e6c1fa64dd301` are identical at `d1681696`,
at the base and at the measured revision, and `tools/round-42/fixtures.json` still hashes
`9f957663c1f21940ec17e32f98485425145b6c4e7eb265a7b12327b629c3da9b`. The only `SKILL.md` edit between the freeze
and the base is one prose line above the block, made at `46486e7a` (the round-42 bullet now names
`corpus/knowledge/2026-10-26-r42-sqfs-triage-v4.md` as its pointer), and `6b9e64fe..HEAD` touches no
`SKILL.md` at all; the line lies outside the region, which is why the region hash does not move while the file's
blob does.

**The new held-out score.** At `<<L1:measured-revision>>` the frozen interpreter assigned every one of the 78
fresh envelopes the same (label, action) pair as the frozen evaluator: `<<L1:matched>>` of `<<L1:n>>`, counter
exit `<<L1:counter-exit>>` (`<<L1:score-artifact>>`). The receipt's own bindings carry what the pair count cannot:
`combo_unseen_majority` `<<L1:combo-unseen-count>>` of 24 combos unseen in the dev arm (the binding needs at least
12), the lookup control `<<L1:lookup-score>>` of 24, and `observed_features_match_declared` true for every
carrier — the round-42 stop binding, which the generator's own `<<L1:tuple-check-verdicts>>` record must
corroborate. The table still offers the 15 rows and the 16 (label, action) pairs the round-42 set exercised,
because its bytes did not change; which of them this seed's 78 carriers reach is a property of the draw, not of
the table.

**The controls, scored at the freeze, before any claim data.** Each control's committed receipt is the pointer;
the sentences below state what the control is built to show, and every exit code and score is a fill token so a
divergence between the expectation and the measured arm is visible in the installed entry rather than absorbed
into prose. CTL-C1-0 is the do-nothing arm: the round-43
counter run at the freeze revision exits 2 with `no_manifest_at_rev` and writes no score, because no manifest
exists yet at that revision (`<<L1:ctl-c1-0-exit>>`, `<<L1:ctl-c1-0-receipt>>`). CTL-C1-1 plants the round-42
held-out manifest at the round-43 path and shows the counter goes non-zero on it — the seed is the round-42 freeze,
not this round's, and the manifest was not first added after this round's freeze
(`<<L1:ctl-c1-1-exit>>`, `<<L1:ctl-c1-1-receipt>>`) — so a counter that greens on a copied prior set is a
defect, not a pass. CTL-C1-2 is the refusal's red/green: the round-42 `C02` declaration fed to the frozen
generator's tuple check exits 3 and writes no manifest (red), while the green is the manifest the claim's own
data run must produce after the same check (`<<L1:ctl-c1-2-exit>>`, `<<L1:ctl-c1-2-receipt>>`). CTL-C1-3
re-scores the round-42 shortcut controls with the frozen round-43 counter on the frozen dev arm and shows none of
them reaches 78 (`<<L1:ctl-c1-3-summary>>`, `<<L1:ctl-c1-3-receipt>>`): the lookup table, the catch-all and the
rotated-action controls that round 42 scored below target stay below it, so a table that merely memorized the dev
arm cannot pass this counter.

**Limits.** (1) The blindness round 42 disclosed is unchanged: agreement between the frozen interpreter and the
frozen evaluator cannot tell this table from any other table that labels the same envelopes the same way; the
claim measures that the frozen table implements the frozen precedence on real REA envelopes under a generator
that cannot declare the unobserved, not that the precedence is the best triage. (2) The `C02` shape is a property
of REA 6.5.0's gap minting beside a failing chunk at the depth ceiling (S119 `FirmwarePublication.js:294-299`),
not a property the table chooses; the observed tuple is authoritative, whatever it turns out to be, and a seed
that draws the shape with a different extra kind would still score the same table. (3) One seed, n = 78, is one
draw from the combined-shape space: the counter binds that every declared tuple was observed, but it cannot bind
that the 24 combos cover every reachable combination, and a row that no carrier reaches is exercised only by the
round-42 controls, not by this set. (4) The recheck command's `--table-only` leg proves the table parses to the
same 15 rules; it does not re-run REA, so a later unblob or REA release that changes gap minting would leave the
table parsing and this entry's anchors valid while the envelopes' shapes moved — the S119 tarball pin and the
S112/S118/S120 file pins are the guard, and they are re-hashed, not re-derived. (5) The S135 license basis
supports embedding S130's fixtures in the carriers; it says nothing about the content claims of any other row, and
no third-party firmware image is embedded anywhere in this claim's inputs.
