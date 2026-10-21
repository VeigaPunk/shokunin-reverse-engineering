# ResidualSources — same-seat follow-up to CriticSourcesFinal

Seat: KaidokuR23.CriticSourcesFinal, the same W2 identity; this is not a new seat. Source F=`9d64b95393bb7134e9fe0dfa9f68df91338a3665`, previous C=`2838351450ff1ee4baa620c962a1153450d53311`.

Method:
- Read `git show F:` for the read set: `corpus/SOURCES.md`, both r23 knowledge entries, `corpus/lessons/round-23.md`, `PROVINCE.md` and `SKILL.md`.
- Ran `git diff C F` on those files.
- Ran `git diff --stat C F -- .ufo/waves/round-23/evidence/c1 corpus/README.md`, which was empty. The envelopes I observed at C are therefore byte-unchanged at F, and my C observations carry forward.
- No tests, counters, producers, fetches or installs. `CriticSourcesFinal.md` is preserved unchanged.

Anything not run below is unverified.

## Original defects, rechecked

| C defect | F repair | Decision |
|---|---|---|
| 1. S058 samplerate attribution | S062 `teaches`: "The synthetic call alone sets samplerate explicitly; the public session call obtains it from recording metadata, as S060's records show." The signal entry's W2 bullet cites `input_format:null`. The appended note says 960000 Hz is a "caller-declared interpretation". The SKILL row says the synthetic values are "not defaults for arbitrary recordings" | **Repaired.** This matches the C observation: the public decode has `parameters.input_format:null` and no `--input-format` in `tool.arguments`. The S062 docs row now attributes run facts to S060 explicitly |
| 2. S061 necessary versus sufficient condition | S063 `teaches` names four symbols, kind-3 headers and two hash sources. The Dart W2 section says "Exporting the four names alone does not guarantee…". The SKILL row heading is narrowed the same way | **Repaired.** Matches the envelope's `limitations[2]` at C |
| 2b. Overall partial coverage | Dart W2 section: "`normalized_result.coverage` is **partial** … three distinct coverage fields". The PROVINCE table and SKILL row say "overall/string_pool partial" | **Repaired** in prose. The quote used for it has a problem (Finding 2) |
| 3. Excluded guide had no locator | The signal W2 bullet gives a URL (`morluto/rea/main/docs/signal-recordings.md`), a retained copy and sha `8997ec52…5fa9`. The lesson says the guide stays non-authority for 6.5.0 | **Partly repaired.** See Finding 3 (census) and the unverified-bytes risk |
| 4. "legacy" label | Dart W2 section: "descriptive terminology borrowed from the connector's proposal, not an admitted SDK-generation or version mapping". S063 and PROVINCE use "four-symbol". The producer's "Dart2.14" text is "retained but not adopted" | **Repaired.** The immutable S061 name and the filename keep the word, and that is explicitly qualified |
| Copied versus recomputed fields | Dart W2 section: describe-dart "extracts and reports … does not recompute"; the earlier "recomputed" sentence is superseded | **Repaired** for Dart. The signal entry never claimed recomputation (it says "retained by the `recheck:` producer"), so no gap |

## Residual checks requested

| Check | Evidence at F | Decision |
|---|---|---|
| Explicit current T1 readiness supersession | `PROVINCE.md` "### Round-23 current T1 readiness — explicit supersession after W2" names the R22 section's "unexercised" and "no recording decode" lines and the earlier R23 paragraph. Its six-row table holds 4 verbs and marks both debugger verbs not held. The signal W2 bullet withdraws "Dart parsing … remain unheld" | Holds |
| Caller-declared rate | Signal W2 note: "raw carrier contains no absolute sampling-rate metadata; 960000Hz is a caller-declared interpretation … 100 samples per planted bit" | Holds |
| Only explicit env overrides retained | Signal W2 note: "'environment' means retained explicit env_overrides only; ambient environment was not captured". At C, run.json had only `env_overrides` (signal: `REA_SIGROK_COMMAND`; Dart: `{}`) | Holds. The header line 2 "argv/environment/…" stays, but it is superseded by the appended note |
| Requested limits | Signal W2 note: prlimit values are "requested or provider-declared … not a retained kernel readback"; "measured" is superseded | Holds |
| Warning filter and output tail | The signal W2 notes say `uart=rx-data` excludes warning classes, and that tail truncation and range overhang have unknown causes. They are non-lossless and "not 'parsed-and-empty'" | Holds. The OriginalPublic bit analysis is cited as separate, non-REA source analysis and was not read here |
| First admitted versus first successful | Dart W2 section: "'First successful' … means **first admitted holding** … the unadmitted connector and synthetic schema probes ran earlier" | Holds |
| Unresolved ABI, SDK and authentication | Dart W2 section: the R22 refusal "does not echo its selected ABI"; there is no causal SDK boundary; the fetch record is "not an authenticated network transcript". PROVINCE and SKILL repeat the ABI caveat | Holds |

## Findings (4)

1. **The counted entries still link only to the superseded rows (observed).**
   - The F headers are unchanged. The signal entry's line 1 is "source: S058 … S059 … S060", and the Dart entry's line 1 is "source: S061 …". Neither cites S062 or S063.
   - `SKILL.md` "Offline recording and carrier-layout envelopes — round 23" still says "(S058–S060)" and "(S061)". The `PROVINCE.md` paragraph "### Round-23 offline envelope additions" says the same, while the new PROVINCE table cites S063.
   - The C counter makes an entry eligible through *its first-line* row IDs (`count-c1.py:101–108` at C). The held Dart and signal witnesses are therefore still linked through S061/S058, whose `teaches` cells are now declared wrong. Both still read `mined`, because immutable cells were left unchanged.
   - Count effect: none, since both rows remain A/mined/opened 2026-10-21 with matching used-by. Provenance effect: the counted linkage points at the superseded wording.
   - Smallest correction: one of the following.
     - Append S062/S063 to the two `source:` lines. This is a first-line edit rather than append-only, but it doesn't change eligibility.
     - Or append one sentence to each entry, SKILL and PROVINCE saying the current row authority is S062 (with S059/S060) and S063, and that S058/S061 remain historical-only linkage.

2. **The S063 gate quote doesn't locate the field it cites (inferred from the C structure).**
   - The lesson's W2 gate row quotes `"coverage":"partial"` at `data.normalized_result.coverage`.
   - In the same compact envelope, `normalized_result.string_pool.coverage` is also `partial`. At C the parsed key order was `target, abi, libapp, string_pool, coverage`, with `string_pool` ending in `printable_run_count`. So the quoted bytes occur at least twice, and the quote fits the string-pool field equally well.
   - The envelope is unchanged C→F. I didn't grep it at F, because it is outside the read set.
   - Smallest correction: use a contextual quote that is unique, such as `"printable_run_count":50666},"coverage":"partial"`. This is inferred from compact serialization and must be confirmed by L1 with one grep.

3. **The SOURCES search log has no round-23 correction entry (observed).**
   - At F the only `corpus/SOURCES.md` changes are the S062 and S063 rows.
   - The round-23 search-log line (`SOURCES.md:113`) still lists "current upstream REA signal guide" with no locator, and still describes S061 as the "legacy-layout Dart envelope".
   - The precedent is the round-22 log line, which records the S057 "authority supersession" explicitly.
   - The guide's URL and sha now live only in the knowledge entry and in `guide-fetch.json`. The lesson says this reopen is "two corrections … not two new discoveries", but the registry's own log doesn't record that.
   - Smallest correction: append one round-23 W2 search-log bullet. It should cover S062/S063 as supersessions of already-opened families (identified 0 new), the guide's URL and sha as excluded, and a pointer to `evidence/sources/guide-fetch.json`.

4. **The retained guide copy is a later fetch of a mutable branch (observed wording; content unverified).**
   - The signal W2 bullet says the retained copy records "a new same-round access" of `…/main/docs/signal-recordings.md`.
   - The original claim, a "newer `invalid_request` description", was made from an earlier, unretained opening. No text in the read set states that the retained bytes actually contain that `invalid_request` description.
   - I didn't read `rea-signal-guide-main.md`, which is outside the read set, so the support is **unverified** here.
   - Smallest correction: add the located line or a ≤25-word quote from the retained copy that contains `invalid_request`. Otherwise say the earlier reading is unretained and the claim rests only on the later copy, if it matches.

## Not findings

- S062's gate quote is the same manual line as S058. That is enough, because its decision cell places the samplerate substance on S060's records.
- S059's "Release commit" wording is unchanged. It is still unknown without network access; no concrete defect.
- The immutable S058 and S061 cells are unchanged, which is consistent with the row-prefix freeze. Supersession follows the S057→S053 pattern.

## Produced files and installs

- `.ufo/waves/round-23/w2/ResidualSources.md` (this file). Its hash is computed outside the file.
- No scratch files. Nothing installed.
