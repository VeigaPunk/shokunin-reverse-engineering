# Residual seat KagiR27-2.ResC1Instrument-2: falsification of R24-C1 counter (count-c1.py) at 69e82c48

Axes: coverage (C1 `t2_held`), calibration (does the instrument enforce its own declared falsifiers).

## Verdict

At 69e82c48 `t2_held` = 4/4 is **not inflated** by any vector I found: the five held envelopes
authenticate under REA6.5.0's own `parseEvidence`, bind on-boundary subjects, come from well-formed
`npx -y rea-agents@6.5.0 <verb>` producers, and cite S064–S067 rows with literal `opened` 2026-10-21.

The **instrument** is weaker than the claim says, though. Seven single-commit mutations keep
`t2_held` at 4/4 (exit 0) when the declared falsifiers or the docstring say the count should drop.
One of them hits a declared falsifier directly: "source row not opened this round". One more mutation
makes the whole measurement unevaluable. The L1 selftest (17/17) covers none of these. Not verified.

## Findings

Baseline (observed):
- `python3 -I -B count-c1.py --root <clone@69e82c48> --rev HEAD` exits 0 with `t2_held_count` 4.
  The blob sha256 is `f185960598b7…dcff00c`, matching the claims.json pin.
- `selftest.py --root <lane> --rev 69e82c48` exits 0 with 17/17 passed.
  - `selftest.py` is **untracked** at 69e82c48 (`git status`: `??`, sha256 `4d7cf12d…baf6f4`), so the
    "L1 selftest" is not a committed artifact of the measured revision.

Mutation battery (observed). Each case is one commit on a `--shared` clone of 69e82c48, run against
the pinned counter blob. The REA authentication column uses REA6.5.0's
`dist/domain/evidence.js` `parseEvidence`.

| Case | Mutation | Sound result | Observed | REA authentication |
|---|---|---|---|---|
| M1 | Set S064–S067 `opened` to `unknown`, `TBD`, or `n/a` | 0/4 | exit 0, **4/4** | n/a |
| M1 control | Set `opened` to `2025-10-21` | 0/4 | exit 1, 0/4 | n/a |
| M2 | dns/tls envelopes `packet_count` changed to 4000/1700, run `stdout` kept equal | pcap-capture dropped | exit 0, **4/4** | FAIL: "Evidence semantic identifier does not match its record" |
| M3 | pcap-client observation relabelled `meta.command=inspect-packet-fields`, `operation=inspect_packet_fields`, and placed at `l1-packet-fields-dns` (wrong verb) | packet-fields dropped | exit 0, **4/4** | FAIL |
| M4 | pcap-client run argv set to `['/bin/cat','envelope.json','rea-agents@6.5.0','inspect-pcap-client']` | pcap-client dropped | exit 0, **4/4** | n/a |
| M5 | Four genuine REA6.5.0 envelopes I produced with the lane's `run-rea.py --tshark` (see below), run times rewritten to 2019 | capture verbs dropped | exit 0, **4/4** | all OK (genuine) |
| M6a control | Every verb mention removed | 0/4 | exit 1, 0/4 | n/a |
| M6b | Verbs mentioned only in a final line "Not run and not claimed: …" | 0/4 if the mention must describe the run | exit 0, **4/4** | n/a |
| M7 | Injected into an ok:true envelope: `{status:'unavailable', code:'ENOENT', coverage:'partial'}` and `{exit_status:127, stderr:'tshark: command not found'}` | pcap-client dropped | exit 0, **4/4** | FAIL |
| M8 | Lone surrogate `\ud800` in one run record's `stdout` | that verb dropped, exit 1 with 3/4 | **exit 2, whole round unevaluable** | n/a |
| M9 control | Envelope replaced by a symlink to the round-22 refusal | 3/4 | exit 1, 3/4 | n/a |

The four M5 envelopes:
- `inspect-pcap-capture` on round-22 `empty.pcap`, copied out of tree: 0 packets.
- `inspect-packet-capture` on an out-of-tree copy of `http.pcap` with filter `dns`: 0 matching.
- `inspect-packet-fields --protocol nosuchproto`: 0 matching.
- All three are `ok:true`, and their subjects are paths under `/fast/scratch`.

Genuine REA failures are caught (observed). A garbage `.pcap` returns `ok:false unsupported_target`,
and a bogus field returns `ok:false execution_failure`, so the refusal path works for real REA
refusals. The real gap is in M2/M3/M7 (edited content) and M5 (genuine but vacuous or off-boundary
runs).

Root causes (code reading, `count-c1.py` at 69e82c48):
1. **Line 159**, `rows[sid][9] >= MIN_OPENED`, is a lexical string comparison. Any lowercase or
   uppercase token sorts above `'2'`, so a row that was never opened passes. The R22 counter used
   `== "2026-10-21"` (r22 count-c1.py:129). (M1)
2. **Lines 182–197** never recompute the content-derived `evidence_id`.
   - REA6.5.0 defines `computeEvidenceId = ev_${digestCanonicalValue(semanticProjection(evidence))}`
     (dist/domain/evidence.js:182), and `parseEvidence` rejects tampered ids.
   - Because `producer_ok` only checks run `stdout` equality, any consistent edit of both blobs counts.
     This covers altered content, relabelled verbs, and injected statuses. (M2, M3, M7)
3. **Lines 108–110** test only that `PACKAGE in argv` and `verb in argv`, as list membership anywhere
   in the list. They do not check that the record is an REA invocation of that verb. (M4)
4. **No subject or input binding.** Nothing ties `data.subject.digest.sha256` to
   `.ufo/waves/round-24/evidence/c1/captures/*` or to the pinned tshark digest, and nothing checks
   run time against the freeze. The claim's boundary ("saved captures from the pinned Wireshark
   source tree") is therefore unenforced. (M5)
   - Vacuous zero-result envelopes also count. Whether "held" requires a non-empty result is a
     tradeoff for the judge, not a code defect.
5. **Refusal vocabulary is closed.** r21 `REFUSALS` (round-21 verb-coverage.py:16–20) together with
   `refused()` (39–55) looks only at `error`/`errors`, `code`/`status`/`completion_status` against a
   fixed set, and `exit_code`. Statuses such as `unavailable` or `ENOENT`, or keys such as
   `exit_status` and `coverage: partial`, pass. (M7) Fix 2 makes this moot for edited envelopes.
6. **Mention test is context-free.** Line 176 searches the whole entry text for the verb, so a mention
   inside a disclaimer satisfies it. The `meta.command` and `operation` binding still prevents
   cross-verb inflation by mention alone. (M6b)
7. **Line 112**, `stdout.encode('utf-8')`, raises `UnicodeEncodeError` outside the per-record
   handling. `main` (line 223) then turns one bad run record into exit 2 for the entire round. This
   is robustness, not inflation. (M8)
8. **Line 148** (code reading only, not executed): `cited` does not strip a trailing `.` the way r20
   `cited_prefixes` does. A path at the end of a sentence fails `endswith('.envelope.json')`. This can
   only deflate the count.

Real items at 69e82c48 (observed):
- **Subjects:** the `pcap-capture` and `packet-capture` subject sha256 values equal the committed
  `captures/dns_port.pcap`, `tls12-dsb.pcapng` and `http.pcap`. The `packet-fields` subject is tshark
  `00ed7bde…6f770d`, which equals the run's `tool_sha256` and the installed binary. `pcap-client` has
  a null subject.
- **Producer argv:** all five run argv start with `['npx','-y','rea-agents@6.5.0',<verb>]`.
- **Run times:** `started_utc` is 16:45:41–16:45:46Z. That is after the freeze commit 5dc49bf
  (16:44:44Z) and before the evidence commit 74cd4e3 (16:45:57Z).
- **Source rows:** S064–S067 are tier A, `mined`, opened `'2026-10-21'`, and list the entry in
  `used-by`.

Selftest gaps (observed by reading `selftest.py`):
- `c1_refusal_not_counted` uses the round-22 refusal, which is `ok:false` with no `evidence_id`.
  It is rejected by the `ok` check before any refusal logic runs, so it is a weak red control.
- There are no cases for M1, M2, M3, M4, M5, M7 or M8.

## Cross-check with ResSources-2's `-T fields` finding

Observed:
- **What REA actually passes:**
  - The retained `l1-packet-capture-http.envelope.json` records `tool.arguments` as
    `['-n','-r','capture','-T','json','--no-duplicate-keys','--temp-dir=.','-2','-Y','http.request','-e',…]`.
  - REA6.5.0 `TsharkCaptureProvider.js:201-216` builds `-T json` as well.
- **Where the wrong flag appears:** the knowledge entry itself states
  "REA builds `-r … -T fields … -2 … -Y … -d … -e`" at line 73. So the defect sits in the C1 witness
  entry as well as the S065 and S066 rows.
- **Conditional flag:** `-2` is conditional on `input.two_pass`, but the entry presents it as
  unconditional.
- **Effect on the count:** none. `t2_held` does not change, and this is content accuracy only.

No tools were installed or updated. Throwaway clones and generated envelopes are under
`/fast/scratch/kaidoku-r24/seats/KagiR27-2.ResC1Instrument-2/`: `attack.py`, `verify-ev.mjs`,
`out/`, and `attack-results.json`. Nothing in the lane was written except this report.

## Recommended L1 action

Keep the 69e82c48 count as observed, but do not present the instrument as enforcing its falsifiers.
Make a disclosed `instrument_supersessions` revision with the smallest safe corrections. Every real
held item already satisfies each check below, as shown above, so 4/4 should be preserved. I have not
run a patched counter.

1. **Opened date:** require `re.fullmatch(r'\d{4}-\d{2}-\d{2}', opened)` before the comparison, or
   use `==` as R22 did. This closes M1.
2. **Evidence authentication:** authenticate each envelope's `data` with REA6.5.0
   `dist/domain/evidence.js` `parseEvidence`, digest-pinned in claims.json. The alternative is to
   reimplement `semanticProjection` and the canonical digest. This closes M2, M3 and M7. It is still
   not producer authentication.
3. **Producer argv:** require `argv[:4] == ['npx','-y',PACKAGE,verb]` and that the argv ends with
   `['--format','json','--full-output']`, matching `run-rea.py`. This closes M4.
4. **Input binding:**
   - For capture verbs, require `subject.digest.sha256` to equal a blob under
     `ROOT + 'captures/'` at REV.
   - For `inspect-packet-fields`, require it to equal the tshark digest in `tool-pins.json`.
   - Optionally require `started_utc` to be at or after the freeze commit.

   This closes M5's boundary escape. Whether vacuous (zero-result) envelopes should count stays a
   judge tradeoff.
5. **Per-record Unicode handling:** catch `UnicodeError` inside `producer_ok` and report
   `run_record_invalid`. This closes M8.
6. **Selftest:** commit `selftest.py` and add one red case each for M1, M2, M3, M4, M5, M7 and M8.
   Replace the refusal case with an `ok:true` envelope carrying a nested refusal plus a valid
   `evidence_id`.
