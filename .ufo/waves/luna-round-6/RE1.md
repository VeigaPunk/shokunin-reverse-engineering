## CLAIM
Protocol compliance is only partially evidenced at the review cut; the preregistration is attested in the dispatch, not independently timestamped.

## METHOD
Compared the parent dispatch’s freeze statement and ten predictions with `PS4.md:5-8`; reviewed existing `receipts/leg-*.md` fields, `/tmp` working-directory evidence, stdout hashes, and server exit records. Ran `date; ps -C node -o pid,ppid,etime,args` at 2026-10-16 18:27:17 -0300.

## FINDINGS
- The dispatch says predictions were frozen before dispatch and lists all ten outcomes. No separate signed/timestamped preregistration artifact was available (`PS4.md:8`); timing is therefore dispatch-attested only.
- Eight receipts existed: L1, L2, L3, L4, L5, L6, L8, L9. All record `/tmp` via a working-directory field or `cd /tmp`; L7 and L10 were absent at review. L2, L3, L4, and L8 do not document a 240-second bound. L8 records provider stdout/hash, not the full MCP stdout (`leg-8.md:12-18,24-28`).
- L6’s recorded stdout SHA-256 (`leg-6.md:12`) did not match the displayed `FULL STDOUT` block (`:15-19`) with or without a final LF, or with CRLF. L3 and L4 hashes matched their blocks after accounting for their respective newline conventions; L1, L2, L5, L8 provider output, and L9 hashes also matched.
- Completed MCP receipts record normal exit/closure (L2 `:19`; L3 `:219-221`; L4 `:37-41`; L6 `:13`; L8 `:24-28`; L9 `:47`). The final `ps -C node` snapshot had headers only, no Node processes. It cannot certify post-battery cleanup while L7/L10 remain absent.

## THREATS
The dispatch cannot independently prove when the parent froze predictions. Receipt status is a time-bounded snapshot; no host-wide mutation/config audit was performed by this seat.

## VERDICT
FINDING: only 8/10 receipts are present; four omit timeout evidence, L6’s stdout hash is unreconciled, and end-of-battery cleanup remains unverified.