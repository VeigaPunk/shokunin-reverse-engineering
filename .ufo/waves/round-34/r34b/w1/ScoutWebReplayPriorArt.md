# ScoutWebReplayPriorArt — bounded prior-art search (R34-C2 province)

- Seat: `L1Kaidoku34-2.ScoutWebReplayPriorArt` (leaf, no dispatch).
- Round: 34, run-6 re-dispatch, wave 1. Lane: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
- Lane rev at survey time: `c79bbe7b` (`git rev-parse --short HEAD` exit 0, `REV_EXIT=0`; full `c79bbe7b0959132b9873ff3431cf5eb313b58b33`) — the frozen revision, so nothing read here is post-freeze drift.
- Mode: read-only. No lane VCS write, no jj mutation, no ELF carrier/fixture/reader executed, no counter run, no build/lint/suite. Wrote only this file and `/fast/scratch/hyaku/kaidoku-r34b/w1/ScoutWebReplayPriorArt/` (created, empty).
- Window: all fetches and receipts below occurred in this session before `2026-10-25T07:20:26Z`. The `read` tool does not expose per-fetch timestamps; I report the window rather than inventing per-request clock values.
- Tooling: **no installs, no upgrades**. No `pacman`, no `uv`, no `npx`, no binary added to `~/.local/bin`. The `read` tool was sufficient; `/home/vgpnk/.omp/agent/RULES.md` needed no new-tool branch because no tool was added.

## Axes

1. **Control-structure fit** — does the source describe an *admission gate with a positive control* (the structural reader meets target, the shortcut readers do not), not merely a plausibility argument?
2. **Shortcut-class specificity** — does it name a mechanism by which an input's identity (size, name, whole-file digest, record order, printable runs) survives into a reader and substitutes for decoding?
3. **Transformation legibility** — can the lane state its invariance test as a metamorphic relation over *this* fixture family (rename inputs, permute records, pad bytes) with a located method reference?
4. **Province distance** — ML-benchmark vs program-analysis vs binary-metadata parser.

Kept moves: sources scoring on 1+2 (control structure, shortcut class) or 3 (MR legibility) without requiring the lane to adopt ML vocabulary. Sources that only supply vocabulary were kept as *rejected-with-flip* so the frontier does not drift into modelling the gate as a learned model.

## Fetch ledger (8 attempts; 7 usable, 1 dead)

| # | URL | Result |
|---|---|---|
| 1 | `https://arxiv.org/abs/2009.07235` | ok, arXiv metadata |
| 2 | `https://arxiv.org/abs/2004.07780` | ok, arXiv metadata |
| 3 | `https://arxiv.org/abs/2207.07048` | ok, arXiv metadata |
| 4 | `https://www.usenix.org/conference/raid2020/presentation/fioraldi` | **HTTP 404 — dead lead.** WEIZZ is ISSTA 2020, not RAID 2020; the RAID 2020 USENIX page does not exist for it. |
| 5 | `https://andreafioraldi.github.io/assets/weizz-issta2020.pdf` | ok, full text (extended version) |
| 6 | `https://tmpout.sh/3/13.html` | ok, full text |
| 7 | `https://arxiv.org/abs/1810.03292` | ok, arXiv metadata |
| 8 | `https://eprints.whiterose.ac.uk/id/eprint/110335/1/segura16-tse.pdf` | ok, accepted-version full text (IEEE TSE) |

Search queries used (unbounded-count, no fetches): metamorphic parser testing; shortcut/trivial-baseline controls in program-analysis benchmarks; WEIZZ venue; metamorphic testing + binary format/ELF; Lipsitch negative controls; plus one query whose summaries I did **not** fetch (NIST MT-cybersecurity, Lipsitch negative controls, PLDI'14 EMI) — those appear only under *Unlocated leads* and carry no quote.

## Candidates

### C-01 — Deep Learning based Vulnerability Detection: Are We There Yet?
- URL: `https://arxiv.org/abs/2009.07235` · date **2020-09-03** (arXiv v1; a journal version exists but was not fetched).
- Quote: "Instead, they learn unrelated artifacts from the dataset (e.g., specific variable/function names, etc.)."
- Province verdict: **ACCEPT** (closest province of the seven — program analysis, not ML-vision). It establishes the exact failure the C2 gate refuses: a scorer whose apparent performance is carried by dataset artifacts rather than by the mechanism under test, and it prescribes the remedy as *report the artifact baseline and require the real method to beat it*.
- Flip if rejected: the replacement would have to be another program-analysis benchmark audit; nothing else fetched occupies this distance.
- Mapping to the frozen instrument: the counter's `shortcuts[]` list is the artifact-baseline suite; `green_positive_meets_target` (target 8) is "the real method must beat it". This source does not prescribe a *freeze* discipline — that part is the lane's own and is **not** in prior art I located.

### C-02 — Shortcut Learning in Deep Neural Networks
- URL: `https://arxiv.org/abs/2004.07780` · date **2020-04-16** (arXiv v1).
- Quote: "Shortcuts are decision rules that perform well on standard benchmarks but fail to transfer to more challenging testing conditions"
- Province verdict: **REJECT with flip** as a *method* source for this gate — it is a vision/ML perspective, its recommendations are about model interpretation and benchmark reporting, and importing its taxonomy would reframe a deterministic reader-side gate as a learned-model problem it is not.
- Flip (what the rejection buys): retain it only as the **terminology anchor** for the word "shortcut", and let the rejection force the stronger local rule — every shortcut class must be specified *operationally* by the input channel it keys on (basename / `st_size` / whole-file digest / record order / printable-run scan), which `gate-config-mini.json:shortcuts[].class` already does and which no ML taxonomy would give us.

### C-03 — Leakage and the Reproducibility Crisis in ML-based Science
- URL: `https://arxiv.org/abs/2207.07048` · date **2022-07-14** (arXiv v1).
- Quote: "we find 17 fields where errors have been found, collectively affecting 329 papers and in some cases leading to wildly overoptimistic conclusions"
- Province verdict: **ACCEPT, narrowed.** Its leakage taxonomy is pipeline-shaped (train/test contamination), which is *not* the C2 province. The one type that transfers is label leakage: an answer selected by an identifier that survives into the input. That is exactly `readers/label_replay_full.py` ("Returns a memorized answer for each fixture basename and nothing otherwise. It never decodes the file." — docstring, `tools/round-34/mini-fix/readers/label_replay_full.py:3-5`).
- Flip if rejected: the gate's rename-invariance requirement (the counter renames inputs so basename keying scores zero) would lose its located methodological warrant and become an in-house convention only.
- Confidence in the mapping: **medium** — the source never discusses binary metadata or replay counters; I am mapping one leakage *type*, not its evidence base.

### C-04 — WEIZZ: Automatic Grey-Box Fuzzing for Structured Binary Formats
- URL: `https://andreafioraldi.github.io/assets/weizz-issta2020.pdf` · venue **ISSTA '20, July 18–22 2020** (extended version © 2020; DOI `10.1145/3395363.3397372`).
- Quote: "“undisciplined” mutations make a fuzzer spend important time in generating many inputs that the initial parsing stages of some program typically rejects"
- Province verdict: **ACCEPT** — nearest binary-format province of the seven. It supplies the structure-blind vs structure-aware contrast as an evaluated methodological distinction (its Table 1 scores chunk/grammar awareness per fuzzer), which is the same axis as `naive-counter.py` vs `mini-counter.py` and `fixed_slice`/`string_scan` vs `structural`.
- Flip if rejected: no fetched source would then support the claim that structure-blind handling of binary records is a *measured, citable* deficiency rather than a lane-local intuition; the naive/red config's role would rest only on the lane's own `gate-config-naive.json`.
- Caveat: the extended PDF states that supplementary material "was not necessarily scrutinized during the reviewing process" — I quote only body text, and the quoted sentence is body text (Introduction).

### C-05 — Weird ELFs, or a tale of breaking parsers once again
- URL: `https://tmpout.sh/3/13.html` · date: **no date line on the fetched page**; internal anchor places it no earlier than **2023-04** (it reports CVE-2023-27734). tmp.0ut issue 3; author `g1inko`. **Do not cite as "2023" without that qualifier.**
- Quote: "OS is known to ignore section headers info, but debuggers and disassemblers parse it to name functions, sections, or apply DWARF data if any."
- Province verdict: **REJECT with flip** as a *control* source — a zine case study, not peer-reviewed, no baseline/gate methodology, and its subject is parser *differentials across tools*, whereas the C2 gate scores one reader against one predicate.
- Flip (what the rejection buys): keep exactly one concrete idea — the **metadata channel that the producer ignores but the consumer parses** is a legitimate place for a shortcut class to hide. If, and only if, the counter admits a differential mode, that suggests a future registered class ("reader that keys on a field the writer does not populate"). It must **not** be added to C2 now: the kill rule forbids changing the registered set after freeze (`claims.json:R34-C2.kill_rule`).

### C-06 — Sanity Checks for Saliency Maps
- URL: `https://arxiv.org/abs/1810.03292` · date **2018-10-08** (arXiv v1; NeurIPS 2018).
- Quote: "some existing saliency methods are independent both of the model and of the data generating process"
- Province verdict: **ACCEPT** — this is the methodological twin of the C2 mutant clauses. Its move is: build controls that a method *must* fail if it is not actually sensitive to the mechanism, and treat passing them as a precondition rather than a result. That is `always-clean gate mutant → red clause fails` and `gate whose positive control is all-false → green clause fails` in `claims.json:R34-C2.control_plan`.
- Flip if rejected: the gate's five-mutant plan would have no located precedent for "a gate must be killable by construction", and the `mutants_killed: 3` target would read as an arbitrary lane convention.
- Confidence: **medium-high** on the structural analogy, **low** on any claim that a reader-side gate is "the same technique" — the analogy is control-theoretic, not domain-identical.

### C-07 — A Survey on Metamorphic Testing
- URL: `https://eprints.whiterose.ac.uk/id/eprint/110335/1/segura16-tse.pdf` · **IEEE TSE 42(9):805–824, 2016** (accepted version).
- Quote: "correctness is not determined by checking an individual concrete output, but by applying a transformation to a test input"
- Province verdict: **ACCEPT** — supplies the formal shape the lane needs for its invariance checks: a metamorphic relation is (input transformation, output relation), with preconditions restricting which source cases it applies to. Directly usable to state the gate's own green/red invariants over the `mrec` fixtures (rename the input → output must be unchanged apart from name text; permute independent records → sorted output unchanged; append padding beyond the record array → unchanged), and the survey's warning that relations need stated preconditions matches the counter's need to say *which* fixture bytes may change.
- Flip if rejected: the lane would have to invent the "transformation + relation + precondition" vocabulary locally, and the report's claims about rename-invariance would be ungrounded assertions.
- Note: the survey found **no** primary study applying MT to binary-metadata/ELF parsing among its 119 papers (as reported in its domain breakdown: web services 16%, graphics 12%, simulation 12%, embedded 10%); I did **not** read the full 688-line text to confirm exhaustively — see gap G-2.

## Synthesis against the frozen claim

What the located prior art supports, for R34-C2:
1. **Control-first evaluation is published practice** — a candidate capability must be admitted only against baselines that could steal its score (C-01, C-06).
2. **Shortcut classes are best named by their input channel** — C-03 (label leakage) and C-05 (unpopulated metadata channel) give the channel vocabulary; C-02's taxonomy is deliberately not imported (see its flip).
3. **Structure-blind vs structure-aware is a measured axis in binary-format work** — C-04.
4. **Invariance-under-transformation is statable without an oracle** — C-07.

What the located prior art does **not** supply (and therefore remains the lane's own contribution):
- No fetched source describes a **pre-freeze admission gate** that (a) scores registered structure-blind readers *under the counter's own predicate*, (b) requires a registered positive control to meet the numeric target, and (c) freezes before the production run with a kill rule forbidding class removal. The closest structural analogues are C-06 (sanity controls) and C-01 (trivial-baseline parity), neither of which is a gate over an instrument's own admission predicate.
- Bounded novelty statement, to be used verbatim if the L1 wants it: *"In a bounded search of 8 fetches, no located source describes a freeze-time gate that admits a structural counter only if registered shortcut readers fail the counter's own predicate while a registered structural reader meets the target; the components (shortcut baselines, sanity controls, metamorphic relations) are each published, their composition as an admission gate was not located."* Confidence: **low-medium** — a bounded search is not a systematic review, and absence of a located source is not absence of the work.

## Province grounding (read-only, on-lane; supports the verdicts above)

- `tools/round-34/gate-config-mini.json` registers `positive_control.class=structural` and **seven** shortcut classes: `all-false`, `size-keyed`, `fixed-slice`, `digest-keyed`, `string-scan`, `record-order-replay`, `label-memorization` (→ `readers/label_replay_full.py`). `gate-config-naive.json` registers the identical set; only the `counter.argv` differs (`mini-counter.py` vs `naive-counter.py`).
- Hash check against the pins in `claims.json` — command and receipt:
  `sha256sum -c` over the five pinned instruments → all `OK`, `HASH_CHECK_EXIT=0`, at `2026-10-25T07:20:26Z` (full output captured in-session; configs match `4483f38…` / `72b1294…`, counter matches `41d5970…`, `label_keyed.py` matches `f727c15…`, `label_replay_full.py` matches `c772227…`).
- **Observation (pin/config asymmetry, `[INFERENCE]` on intent):** `tools/round-34/mini-fix/readers/label_keyed.py` is pinned in `claims.json:R34-C2.pins` but is referenced by **neither** gate config nor the counter — `grep -rn "label_keyed" tools/round-34 .ufo/waves/round-34` returns exactly one hit, the pin itself (exit 0). Its class name ("label-keyed") is therefore not a registered class; the same input-identity channel is registered transitively via `label_replay_full.py` (superset template, same basename lookup). This looks like registration bookkeeping, not a coverage hole — but it is a pinned instrument that no predicate exercises, and `claims.json:kill_rule` speaks of "any registered shortcut class", so the L1 should decide explicitly whether the pin set and the registered set are meant to coincide. I did not run the counter; this is a static reading.
- I did not read `replay-gate.py`, either counter's body, `mini-fix/build.py`, or any fixture. My verdicts are about source fit, not about the claim's six clauses.

## Unresolved gaps

- **G-1** Per-fetch UTC timestamps are unavailable from the `read` tool; only the enclosing window (≤ `2026-10-25T07:20:26Z`) is a receipt. Not fabricated per-request.
- **G-2** Segura 2016 fetched text was truncated at line 300 of 688 (`artifact://20402` holds the full conversion); the domain breakdown I quote is from the fetched portion, so "no MT study of binary-metadata parsing" is a **non-exhaustive** reading of that survey, not its finding.
- **G-3** tmp.0ut #3 has no located publication date; 2023-04 is a lower bound inferred from the cited CVE, not a printed date.
- **G-4** Three leads were seen only in search summaries and **not** fetched (NIST *Metamorphic Testing for Cybersecurity*; Lipsitch et al. 2010 *Negative Controls*, PMID 20335814; Le/Afshari/Su PLDI'14 *Equivalence Modulo Inputs*). They carry **no located quote** and are not candidates here. Negative controls are the most promising missing piece for the gate's "vacuous gate → UNEVALUABLE" clause and deserve a fetch in a later wave if budget reopens.
- **G-5** No source located on gallery/showcase shortcut controls specific to **ELF dynamic-metadata** extraction (DT_NEEDED / version-needs shape); the R34-C1 area stays stopped and I did not search or score it.

## Verdict

PRIOR_ART_BOUNDED: 7 located candidates, 5 accept (C-01, C-03 narrowed, C-04, C-06, C-07) and 2 reject-with-flip (C-02 → terminology only; C-05 → one channel idea, no C2 change allowed post-freeze); 1 dead lead (USENIX RAID-2020 WEIZZ URL, HTTP 404 — venue is ISSTA '20); no located source describes a freeze-time shortcut-replay admission gate, so the composition is a low-medium-confidence novelty claim and the components are attributable. Static on-lane observation for the L1: pinned reader `label_keyed.py` is registered in no config. No lane file other than this report was written.
