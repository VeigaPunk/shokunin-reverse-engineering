# RunBefore: R23-C1 counter run

Lane root: `/home/vgpnk/Projects/shokunin/kaidoku-shokunin`.
Candidate: `2838351450ff1ee4baa620c962a1153450d53311` ("round-23: retain measured four-of-six coverage and refusal controls").
Baseline B: `aa1450b82f9ede35aada63efe8a34e01c6e02f72` ("round-22: record thirty passing checks and finite claim verdicts").

## Findings

1. **Wrong revision measured (my error; observed).** The expected result (incomplete 1/6, "before" semantics; frozen claims `before: 1`) corresponds to measuring B, i.e. `--rev aa1450b…`. I read "against B" as the baseline comparison and passed `--rev 2838351…` (the candidate). The single run therefore measured the candidate. Its output self-labels `rev`=2838351…, `historical_rev`=aa1450b…. **The B-revision measurement was not run and is not passed.** I did not re-run, per the once-only rule.

2. **Observed result (candidate revision).** `finding`=`c1_incomplete`, `t1_exercised_count`=4, `t1_total`=6, exit 1 (tool-reported; see Incident).
   - Exact T1: the six frozen verbs, in order (observed).
   - Historical identify: exercised by B-baseline R22 witnesses `ev_6a84742a9749692a3c6b59678c83d50b4741761f996c723995fa799b1bbca0b6` (`.ufo/waves/round-22/evidence/c1/identify-flutter-build-saber.envelope.json`) and `ev_3458b996b71e3dccde0177728ba60ef94800dd373db5a704048e18526d9d866b` (`.ufo/waves/round-22/evidence/c1/identify-godot.envelope.json`) (observed).
   - Exercised by round-23 witnesses: inspect-dart-aot, inspect-signal-decoders, decode-signal-recording. Not exercised: debug-with-gdb, debug-with-rizin (observed).

   | verb | entry (`corpus/knowledge/…`) | evidence_id | evidence (`.ufo/waves/round-23/evidence/c1/…`) |
   |---|---|---|---|
   | decode-signal-recording | `2026-10-21-r23-offline-signal-envelopes.md` | `ev_1d361f25aeaa07b5c03ffbbd43c61d061407b96c6c62bf783913d03a62c67e5c` | `decode-official-uart.envelope.json` |
   | decode-signal-recording | `2026-10-21-r23-offline-signal-envelopes.md` | `ev_bcadf773da826e70bfb79c492ddf111cd3f226fdd30addb4a15aabdc3602bd3e` | `decode-uart-hi.envelope.json` |
   | inspect-dart-aot | `2026-10-21-r23-dart-legacy-layout-boundary.md` | `ev_d2ff19d7100f34b52e4b2bc52ee115e48428624f7da57814e5f184b4bd4c7491` | `inspect-dart-legacy-saber.envelope.json` |
   | inspect-signal-decoders | `2026-10-21-r23-offline-signal-envelopes.md` | `ev_940cf7bbd6ba6e8def3e7f29dad9dc03bccbd0f39a094a4787d3dd563164fdd0` | `inventory.envelope.json` |

   - `catalog_mentioned_count` 137 of `catalog_total` 153; `catalog_zero_count` 16 (observed; not a claim input).

3. **Expectation vs observed.**
   - Exact T1: matched.
   - Historical identify: matched.
   - Count 1/6: **not matched.** The candidate-side count is 4/6, which agrees with the candidate commit subject ("four-of-six") (observed).
   - B-revision count: unobserved. [INFERENCE] A `--rev aa1450b…` run would reuse the same historical identify binding and find no round-23 witnesses. Observed basis: at B, all four bound entries/evidence are absent (`git cat-file -e`: both knowledge entries absent; `.ufo/waves/round-23/evidence/c1/inventory.envelope.json` absent), `round-23/evidence/c1` holds 0 files at B vs 27 at the candidate, and `round-23/tools/count-c1.py` is absent at B. Predicted: incomplete, 1/6, exit 1. Not observed; not passed.

4. **Read-only cross-check of bound envelopes** (candidate blobs via `git cat-file blob`). All six bound files (four new, two historical) have top-level keys `data`, `meta`, `ok` with top `ok: true`; no `"ok": false` substring (observed). One `refus` substring hit in `inspect-dart-legacy-saber.envelope.json` (byte offset 86055, line 1): prose limitation text "a payload without exported snapshot symbols is refused rather than guessed". This is not a refusal envelope, and the binder bound it (observed).

5. **Not assessed:** source relevance and ownership (counter `limit`: "manual source relevance"); authentication; the semantics of `r21.refused` were not read.

## Produced files and hashes

Ignored runtime directory: `.ufo/waves/round-23/runtime/KaidokuR23.RunBefore/`
- `clone/`: private clone (`git clone --no-hardlinks --no-checkout`), detached at `2838351450ff1ee4baa620c962a1153450d53311`. Status clean; B is an ancestor; retained.
- `count-c1.argv`, sha256 `66e1df80f6c3efb4625051da14758e9e6b39613a4c5f0b1151d57fcd678f5c06`
- `count-c1.stdout`, sha256 `dcc2d3a2fff54d46212fab81571d653a34179e13b666321cfebbe7dd7bf1766a` (1 line, 2347 bytes)
- `count-c1.stderr`, sha256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855` (0 bytes)
- `count-c1.exit-note.txt` (no `count-c1.exit` exists; see Incident)

Counter source (candidate): `.ufo/waves/round-23/tools/count-c1.py`, blob `0f966a50018bba2fa5af3d6f9af1541f660c43c2`, sha256 `f4b8d16ac195ca106a99cbb9236d36d1283dee349c6fef3a49567de0bbea0cc2`. Identical in the clone worktree.
Legacy R22 counter `.ufo/waves/round-22/tools/count-c1.py`: sha256 `c925918fb871151f86065aa5b3e9d10334ab845ed67c265ae0977f05e09b1879`, equal to the script's pinned `LEGACY_SHA256`.

Command as executed, once (cwd = clone; wall time 3.61 s):
`python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root /home/vgpnk/Projects/shokunin/kaidoku-shokunin/.ufo/waves/round-23/runtime/KaidokuR23.RunBefore/clone --rev 2838351450ff1ee4baa620c962a1153450d53311`

Exit: 1, from the tool's "Command exited with code 1" for that invocation.

## Incident

My clone-setup command had set `set -e` in the persistent shell. The counter's non-zero return (1) aborted the shell before `echo $? > count-c1.exit`, so no `.exit` file exists and the echo printed nothing. Exit 1 is the tool-reported status of that same invocation and matches the stdout finding. `set +e` was applied before further commands. There was one execution: one argv, one stdout, one stderr, one wall-time.

## Installs

None. Observed versions, no install: Python 3.14.8, git 2.56.0.

## Open risks and decisions for L1

- The assigned before-measurement (B) is unrun. To obtain it, L1 must designate a Run seat for: `python3 -I -B .ufo/waves/round-23/tools/count-c1.py --root <clone at 2838351…> --rev aa1450b82f9ede35aada63efe8a34e01c6e02f72`. Predicted (inference above): incomplete, 1/6, exit 1.
- The candidate count of 4/6 is counter arithmetic over author-side witnesses. Source relevance and ownership remain manual.
- Exit 1 is also the code for "incomplete", and an uncaught exception would also yield 1. Here stderr is empty and stdout is the expected JSON, so the run completed normally.
- The clone is retained at `.ufo/waves/round-23/runtime/KaidokuR23.RunBefore/clone` (ignored) for L1's use and may be removed.
- W1 proposal re-evaluation: not applicable to this run seat.

Report: `.ufo/waves/round-23/w2/RunBefore.md`
