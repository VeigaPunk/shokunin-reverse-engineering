## CLAIM
The only live round-8 probe observed so far resolved the exact 6.4.0 version, but does not prove a live npm-registry fetch. Registry, quota, and server-cleanup risks remain bounded only by the prescribed per-leg timeout, evidence capture, and honest-stop rules.

## METHOD
Read-only review: `.ufo/waves/luna-round-8/receipts/leg-1.md:3-11`; prior npx cache inventory `.ufo/waves/luna-round-2/receipts/L4-npx-cache.txt:1-21`; MCP runner `.ufo/waves/luna-round-2/receipts/L15-tools-6.5.0.txt:1-9`; historic adversarial tests `.ufo/waves/luna-round-6/CB4.md:7-17`. Ran `df -Pk /tmp "$HOME"; du -sk "$HOME/.npm/_npx"`: `/tmp` had 14,030,024 KiB available (12% used), `$HOME` filesystem 825,852,632 KiB available (14% used), npx cache 329,304 KiB. No live registry/cache/quota test, configuration audit, or current-server cleanup check was performed.

## FINDINGS
- L1 returned stdout `6.4.0`, empty stderr, exit 0 (receipt lines 3-11); it may have reused cache. Prior inventory puts npx packages under `/home/vgpnk/.npm/_npx`, not `/tmp` (L4:3-21). Thus `/tmp` as cwd does not isolate cache writes; this is not evidence of config drift.
- Current filesystem free space is ample, but `df` does not establish user/project quotas. Round-6 6.5.0 stress evidence recorded 173 tarball GETs / 336 MB on cold install and ~70 s warm stale-cache fallback; its preserved logs had zero 429/5xx/timeouts (CB4:10-17). Historic 6.5.0 behavior is not a 6.4.0 guarantee.
- Treat any registry/ENOSPC failure or 240s timeout as `ERROR-UNEXPECTED`, not `TYPED-REFUSAL`; retain the leg receipt and do not substitute another version. A completed response followed by an idle stdio server is not a hang: close stdin and await exit. On timeout terminate the process group, escalate after 5 s, and verify reaping (L15:2).
- Honest stop the remaining battery only if exact 6.4.0 identity cannot be established, a server cannot be confirmed terminated, observed config drift appears, or full stdout/stderr/exit/hash receipts cannot be durably recorded. An isolated leg error with confirmed cleanup is a mismatch; continue other pinned legs safely, without retrying to replace the result.

## THREATS
The prior rate-limit result is historical, the `df` snapshot cannot rule out quotas, and current 6.4.0 registry access/cache provenance and config drift are unverified. This seat did not launch MCP servers or edit config.

## VERDICT
FINDING: L1 matches, but registry provenance and config stability are unproven; cache storage is outside `/tmp`, so preserve explicit evidence and stop only on the stated containment or persistence failures.
