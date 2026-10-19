# SC-1 — C3 pin-line drift characterization

Scope: frozen claim C3 in `.ufo/waves/arc3-loop1-round9/claims-frozen.md:44-56`. All live-file reads below were filtered to pin lines or derived through the gate; the Kimi config and other custody paths were not modified. The synthetic edit probe used an auto-removed fixture under `/var/tmp`, never `/tmp`.

## Findings and per-item verdicts

- **VERIFIED — live pin and uniqueness in the current file.** A first-hand filtered read of `~/.kimi-code/config.toml` returned:

  ```text
  file_lines=4150
  rea-agents_match_count=1
  4126:args = [ "-y", "rea-agents@6.7.0", "mcp" ]
  matched_line_sha256_no_lf=eb23737749a7dbd615db449daee491d821580fdb86df2660a92334df733b6cb1
  ```

  The same fresh line hash equals the receipt's `line-sha256-excluding-LF` at `.ufo/receipts/arc3-loop1-round8-kimi-rea-line.txt:6` (`receipt_matches_live=True`). This comparison re-derives the live bytes; it does not treat the receipt as a live anchor.

- **REPRODUCED — gate's targeted disposition is `current-ok`; DISCREPANCY — overall gate run is not PASS.** Ran `python3 .ufo/gates/c1-census-v10.py --root .`. Relevant exact output:

  ```text
  live anchors (re-derived): {'devin': '6.5.0', 'omp': '6.5.0', 'kimi': '6.7.0'}
  PROVINCE.md block 15-26 [scope CURRENT]
      :18 [ptr] __ptr__=~/.kimi-code/config.toml:4126 -> current-ok (pins 6.7.0)
  -- UNDECLARED (1) --
    SCORECARD.md block 1833-1839 [scope None]
        :1834 [pin] None=6.7.0 -> AMBIGUOUS (no client token in clause)
  VERDICT: FAIL  (stale=0 ambiguous=0 undeclared=1 unresolved=0)
  ```

  The pin pointer is explicitly graded `current-ok`, but this command exits 1 because of the separate undeclared SCORECARD locus at `:1834`; the gate's SCORECARD scope ends at line 1813 (`.ufo/gates/c1-census-v10.py:274-276`). I do not report an overall gate PASS. A separate first-hand direct call to the gate's `ptr_check()` (reporting state only) returned:

  ```text
  live_pin_matches=[4126]
  live_line=4126 state=ok
  old_candidate_line=3546 state=stale
  ```

- **REPRODUCED — the line number is perishable under edits.** A read-only census of all seven `config.toml.*` backup files in `~/.kimi-code` found these matching pin locations (the current file is reported separately above):

  ```text
  backup_files=7
  config.toml.20261018-085645.bak lines=2939 hits=[(2915, '6.7.0')]
  config.toml.20261018-114557.bak lines=2956 hits=[(2932, '6.7.0')]
  config.toml.20261018-143236.bak lines=2964 hits=[(2940, '6.7.0')]
  config.toml.20261018-145016.bak lines=3251 hits=[(3227, '6.7.0')]
  config.toml.20261018-150133.bak lines=3322 hits=[(3298, '6.7.0')]
  config.toml.20261018-161746.bak lines=3322 hits=[(3298, '6.7.0')]
  config.toml.20261018-201656.bak lines=3181 hits=[(3157, '6.7.0')]
  ```

  Thus independently inspected snapshots show the pin moving as file contents/length change, including a later backup at line 3157 after snapshots at 3298. The available seven backups do not contain a pin match at line 3546, so that historical intermediate's occurrence is **UNVERIFIABLE from this snapshot set**; only its present-day stale state above was tested. No prior seat or round value is used as evidence here.

  To isolate the instrument's behavior, I imported the current gate and ran its `ptr_check()` against a minimal synthetic `config.toml` under `/var/tmp`. Exact output:

  ```text
  synthetic baseline: line2=('ok', 'pins 6.7.0')
  after one-line insertion: old line2=('stale', "line holds no rea-agents pin: '[mcp_servers.rea]'")
  after one-line insertion: moved pin line3=('ok', 'pins 6.7.0')
  two identical pin lines: match_count=2
  two identical pin lines: line2=('ok', 'pins 6.7.0')
  two identical pin lines: line3=('ok', 'pins 6.7.0')
  ```

## Characterization

The current live file has exactly one `rea-agents@` match, but the gate does **not** enforce uniqueness or identify the `[mcp_servers.rea]` stanza. `live_pins()` takes the first version regex match in each client file (`.ufo/gates/c1-census-v10.py:324-334`). `ptr_check()` then reads the caller-specified physical line, looks for a version there, and compares it to the live anchor for the client inferred from the path (`:466-482`); `classify()` routes pointer detections through this function (`:538-544`). The synthetic insertion makes an unchanged pin stale at its former line and current at its new line. The duplicate probe also shows that a second same-version match at a numbered line is accepted, so the pin being unique today is an observed property of the live file, not an instrument invariant.

The receipt's content hash matches the live line now, but the pointer checker does not validate that hash or consult the receipt. Receipt-language checking is a separate text heuristic (`:316`, `:589-595`). Therefore the characterization is: **line-addressed, version-checked, and sensitive to insertions/deletions before the pin; not stanza-identity-, uniqueness-, or content-hash-bound.** The C3 measurement is delivered here as the seat's durable note; no receipt, gate, province, corpus, or other custody/source file was edited.
