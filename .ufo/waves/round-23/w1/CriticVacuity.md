# CriticVacuity — R23-C1 numerator falsification (author-side critic, not verification)

Seat: `KaidokuR23.CriticVacuity`, read-only. Frozen claim `.ufo/waves/round-23/claims.json` (R23-C1, before 1/6, target k>=2, exact k).
Measured against production HEAD `a3c92eb6bc70984e90ae5b895412de978840b2c5` plus untracked R23 evidence present at 14:38–14:39Z.
Counter under attack: pinned `.ufo/waves/round-22/tools/count-c1.py` sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`, plus the planned R23 wrapper design `gen-wave1.py:19` (BuildCounter: legacy `measure` twice with the R22/R23 prefixes, union by verb, S058+ for new witnesses). The R23 `count-c1.py` does not exist in the lane yet, so I attacked the legacy measure + union design.

Method (observation): one `python3 -I -B -` harness, stdin only, no file writes. It loads `count-c1.py` and both helper sources from `git show a3c92eb:<path>`, re-checks the helper `HELPER_SHA256` pins in memory instead of writing the counter's tempdir, and patches `subprocess.run`. That makes `git show`/`git ls-tree` return the real tree plus virtual overlay blobs (knowledge entries, SOURCES rows, envelopes). Each scenario ran legacy `measure` per prefix and unioned exercised verbs. Exit 0, wall time 40 s. Results are below; the scenario letters are the harness labels.

## Findings

### 1. Duplicate same-verb witness: falsifier survives (no numerator inflation)
- Observation, A: honest overlay with 4 real R23 ok envelopes cited by one S058-eligible entry gives **k=3/6** (identify, inspect-signal-decoders, decode-signal-recording). Each verb has 2 witnesses.
- Observation, B: a second entry/S059 plus a byte copy `inventory-copy.envelope.json` gives inspect-signal-decoders 5 witnesses and decode-signal-recording 4, still **k=3**. The verb-set union in `count-c1.py:171` (`exercised = [verb for verb in T1 if ...]`) holds.
- Live instance: R23 `evidence/c1` already holds two ok inspect-signal-decoders envelopes (`inventory` ev_940cf7…, `uart-help` ev_4be137…) and two ok decode-signal-recording envelopes (`decode-uart-hi` ev_bcadf7…, `decode-official-uart` ev_1d361f…). These are 4 envelopes for 2 verbs, so the honest ceiling from current evidence is **k=3**, never "1 + 4 witnesses".
- Residual risk: only if the wrapper reports `before + new` (1 + new verbs) instead of the union. A new identify witness would then make 2. Correction: k = |union of verbs|, and report the per-verb witness list separately from k.

### 2. Inherited same evidence in new root: no inflation, but there are two identity hazards
- Observation, C1: a naive single prefix (R23 only, no copy) gives **k=2**, and identify-flutter-build is lost. Falsifier "inherited identify lost" is real for any counter that just swaps `EVIDENCE_PREFIX`.
- Observation, C2: the R22 Saber identify envelope byte-copied into the R23 root gives identify 3 witnesses (2 R22 + copy) and k=3. No inflation.
- Observation, C3: the same copy under a naive R23-only counter gives identify "preserved" by the copy alone (1 witness `id-copy.envelope.json`). The copy launders inherited evidence as new-root evidence and masks the C1 loss. Duplicate evidence_id across roots is not detected (`count-c1.py:153-164` keys only by path+id).
- Correction: union both prefixes, as designed. Reject any R23-root witness whose `evidence_id` or envelope sha256 already occurs under the R22 root (the inherited witness stays R22-attributed).

### 3. Copy erases parent refusal: defect, numerator inflatable to 4
- Observation, D1 (control): the R22 `inspect-dart-aot-saber.envelope.json` refusal (`ok:false`, `unsupported_target`) copied verbatim into R23 is **not counted** (k=3). Refusal ancestry survives verbatim copy.
- Observation, D2: the same refusal rewritten as `ok:true` with a fabricated minimal record (`evidence_id` = arbitrary `ev_<sha256>`, `operation:"inspect_dart_aot"`, Saber subject sha `de4813f9…`, meta copied) gives **k=4/6**. A self-consistent forged `.run.json` whose stdout equals the envelope was also present, so the "envelope == run.stdout" control (R22 final-suite style) would also pass.
- Why: `bind_cli` (`count-c1.py:69-98`) requires only `ok`, `data.evidence_id`, `data.operation`, `meta.command` and no refusal keys. `r21.bind` (`round-21/tools/verb-coverage.py:77-99`) checks id/operation equality only. There is no record-shape check, no link to an R22 refusal of the same verb on the same target sha, and no re-execution.
- Impact: this is not a theoretical gap for this round. The only route to inspect-dart-aot is the same Saber carrier that R22 saw refuse under the same REA 6.5.0.
- Smallest correction:
  - (a) In the wrapper, reject a new witness when the R22 root holds a refusal for the same `meta.command` and the same subject sha256, unless the argv differs and that difference is named.
  - (b) Require the full REA record members already present in every genuine envelope (`predicate_type`, `subject.digest.sha256`, `provider.id`, `confidence`, `limitations`).
  - (c) L1 admission must re-run the recorded `recheck` argv. A counter cannot authenticate; that is a tradeoff to declare, not a fixable defect.

### 4. Mention-only or source-line token: counter-level vacuity confirmed
- Observation, F5 (control): verbs named in prose with no envelope give **k=0**. The "mere mention counts" falsifier survives for a mention without evidence.
- Observation, F1–F4: each counted inspect-signal-decoders (k=1 alone) with the cited inventory path+id when the verb token occurs **only**:
  - F1: in the `source:` header line;
  - F2: in a negation ("was NOT exercised; ignore …");
  - F3: only in the `recheck:` header;
  - F4: only as the cited evidence filename `…/c1/inspect-signal-decoders.envelope.json`. `command_pattern` (`round-20/tools/verb-coverage.py:99-105`) allows `/` before and `.` after the token.
- Inference: the knowledge entry contributes nothing verb-specific. The envelope alone carries the count, so "entry names the verb" is not an independent knowledge requirement.
- Current R23 filenames (`inventory`, `uart-help`, `decode-*`) do not embed verb tokens, so F4 is not live yet.
- Correction: the wrapper requires a verb mention in the entry body (after the header block), outside every cited evidence path, and refuses entries whose only mention sits within a negation window. Alternatively, declare "entry mention" as non-semantic in the claim limit.

### 5. Source linkage: the eligibility rule is gameable, and the wrapper design cannot see the entry
- Observation, G3 (control): no source row gives k=0. Linkage absence is caught.
- Observation, G1: eligibility via a **pre-round S055 row with the new entry appended to used-by** (no S058) counts both signal verbs (k=2). The legacy rule is `>=51`, A/B, mined, opened `2026-10-21` (`count-c1.py:129`). R22's rows S051–S057 are all dated 2026-10-21, so the date gives zero round separation. The edit violates no_harm ("pre-round source rows unchanged"), but the counter does not detect it.
- Observation, G1 detail: the legacy witness tuple is `[evidence_id, evidence_path]` (`count-c1.py:162`). It carries no entry path or source id, so the BuildCounter instruction "newly counted witness comes from round23 entry citing S058+" **cannot be enforced from legacy output**. The wrapper must re-derive eligibility, which is exactly the "never duplicate binding policy" it is told to avoid, or else silently accept `>=51`.
- Observation, G2: an S058 row about Dart SDK snapshot symbols makes the *signal* entry eligible (k=2). Topical relevance is unchecked.
- Observation, G4: an own-work S058 whose location is the counted envelope itself is eligible (k=1). Circular linkage passes. R22 already does this (S055/S057 are own-work rows for the witness envelopes).
- Correction:
  - The wrapper computes its own S058+ entry eligibility as a narrower *additional* filter (a filter, not a binding-policy duplicate). Record the entry path and source id per new witness.
  - Diff `SOURCES.md` rows <=S057 against baseline `aa1450b` and require byte equality.
  - Require each eligible S058+ row's scope/claim to name the counted verb's subject class, or record relevance as manual-only in the limit.
  - Do not let an own-work row be the sole source for the witness it describes.

### 6. Boundary is not enforced by the counter
- Observation, E: a `debug-with-gdb` envelope (`operation:"gdb_console"`, `subject:null`) gives debug-with-gdb exercised. The counter would admit live debugger execution that the claim boundary forbids, and the pathless record passes: `r21.bind` computes `pathless` but `count-c1.py:96` discards it.
- Correction: the wrapper hard-fails if debug-with-gdb or debug-with-rizin is exercised at all this round. Surface `pathless` per witness.

### 7. Vacuity inside the real signal witnesses (observations on actual R23 files)
- **inspect-signal-decoders "complete" inventory is not complete:**
  - `inventory.envelope.json` (sha `5f8021…`) is `ok:true` with `output_window` examined=matching=returned=110 and `has_more:false`.
  - Yet `normalized_result.diagnostics` contains `srd: SyntaxError: Failed to load decoder signature … pd.py, line 138`.
  - The runtime decoder tree has 112 `__init__.py` dirs. Missing are `common`, which is a helper package [INFERENCE: not a decoder], and `signature`, which is a load failure.
  - The refusal walk only inspects structural keys (`round-21 verb-coverage.py:39-55`), so a free-text diagnostics failure is invisible.
  - Knowledge must say "110 loaded, 1 load failure", not "complete catalog".
- **Subject is the lane's own wrapper:**
  - Both inventory envelopes have the subject `tools/sigrok-cli.sh` (698 B, sha `50fe4359…`), and the producer labels it `authority:"shipped-artifact"`.
  - The actual binary/decoders under `.ufo/waves/round-23/runtime/squashfs-root` are git-ignored (`.ufo/waves/round-23/.gitignore:1:/runtime/`) and undigested by the envelope.
  - The wrapper `LD_PRELOAD`s host `/usr/lib/libgmodule-2.0.so.0`; the banner reports glib built 2.48.2 vs runtime 2.90.1 (mixed ABI).
  - Diagnostics also report `Could not find platform independent libraries` (embedded Python without its stdlib).
  - The target sha256 therefore identifies the launcher, not the decoder implementation. Reproduction needs AppImage sha `49d2f597…` via `tools/setup-sigrok.py` plus host libgmodule.
- **decode-uart-hi is circular:**
  - The carrier `uart-hi.bin` (sha `4a2e729f…`, 2500 B) is generated by lane-authored `tools/make-uart.py` (sha `e22a8f1f…`).
  - The decode `48`,`69` ("Hi") equals the generator's own payload.
  - This proves the decode path on an idealized self-authored signal, not recording semantics.
- **decode-official-uart is the non-circular witness:**
  - Carrier sigrok-dumps @`c8fad0528648ba58ceddbda9e34e4dfcd293a6b0` `uart/hello_world/8n1/hello_world_8n1_9600.sr`, sha `01b72610…` (matches `official-download.json`).
  - It decodes 12885 annotation lines. The first six bytes `BA BD C9 B1 91 85` precede `\r\nHello World!` [INFERENCE: pre-sync framing noise]. Knowledge must not claim every decoded byte is payload.
  - Prefer it as the counted decode witness; the synthetic one is a control.
- **Refusal control holds:** `decode-invalid-decoder.envelope.json` is `ok:false` `execution_failure` (nested `diagnostics.exit_code:1`), and the counter correctly blocks it. Note that REA classifies a nonexistent decoder as `execution_failure`, not invalid input.
- **Stdout equality:** observed `cmp` equality between `run.json.stdout` and the envelope for inventory and uart-help. This is local consistency only (see finding 3).
- **Production-path caveat:** these evidence files sit in the production lane's `.ufo/waves/round-23/evidence/c1/` (untracked), not a sandbox `output/`. Until committed, a `--rev` measurement counts none of them; any k reported before commit is not a counter result.

### Impacted axes
- coverage (numerator inflation: D2 and E; identity loss/masking: C1 and C3; eligibility: G1, G2, G4).
- calibration (false completeness: inventory 110/112 with a load failure; synthetic circular decode; launcher-as-subject provenance).
- depth (mention-only/header-token entries F1–F4 count with no verb-specific knowledge).

### Verdict as critic (not judgment)
- With the current real evidence and an honest union wrapper, the strongest supportable numerator is **k=3/6** (identify inherited from R22, inspect-signal-decoders, decode-signal-recording). Completeness stays incomplete.
- inspect-dart-aot, debug-with-gdb and debug-with-rizin have no legitimate R23 witness.
- Any k>3 this round is, by construction, one of the D2 or E patterns.
- Inflation is blocked for duplicates (A, B, C2). It is **not** blocked for refusal-flip forgery (D2), boundary-violating debugger envelopes (E), pre-round row edits (G1), or irrelevant or circular sources (G2, G4).

## Produced files
- `/home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/w1/CriticVacuity.md` (this report; sha256 not self-embeddable, compute post-write).
- No other files. The harness was stdin-only with no tempdir; helper loading was in-memory.

## Installs
None.

## Open risks
- The R23 `count-c1.py` did not exist when reviewed. Findings target the legacy code and the `gen-wave1.py:19` design; the real wrapper must be re-attacked once it lands.
- The overlay harness patches `subprocess.run` and synthesizes ls-tree entries with a zero object id. The counter never reads object ids (`tree_entries` returns them, unused in `count-c1.py`), so I infer it is faithful, but this is not a committed-fixture proof.
- Evidence in `round-23/evidence/c1` was changing during review (3 decode envelopes appeared mid-session). The file list and sha256s above are as observed at about 14:39Z.
- Authentication of any envelope remains impossible locally. Only L1 re-execution of the recorded argv against the recorded carrier sha distinguishes a genuine witness from the D2 pattern.
