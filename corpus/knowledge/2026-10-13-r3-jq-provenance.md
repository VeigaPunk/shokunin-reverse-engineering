<!-- corpus entry — kaidoku-shokunin round 3 (2026-10-13). Staging evidence: fleet .ufo/waves/kaidoku-r3/09-jq-provenance.md. -->

# 09 — `~/.local/bin/jq` install provenance (round 3)

Round 2 proved `~/.local/bin/jq` byte-identical to the upstream `jqlang/jq`
`jq-1.8.2` release (`jq-linux-amd64`). This round resolves *how it landed on
this host*. Verdict: **resolved — a kimi-code agent swarm installed it.**

## Candidates

### Candidate 1 — kimi-code swarm, agent-2 "CLI DEPS" (confirmed)

- **claim:** On 2026-10-03 at 18:34:03 -0300, a kimi-code subagent
  (`agent-2`, titled "CLI DEPS into ~/.local/bin") downloaded the official
  `jqlang/jq` GitHub release asset `jq-linux-amd64` (tag `jq-1.8.2`, resolved
  via `api.github.com/repos/jqlang/jq/releases/latest`) and installed it to
  `~/.local/bin/jq`, as one step of a user-initiated, no-sudo dev-environment
  bootstrap.
- **source:** Session transcript
  `~/.kimi-code/sessions/wd_vgpnk_403b91ce3657/session_cf944588-5aa0-418b-bd06-2891c6833202/agents/main/wire.jsonl`
  (line ~153, `agent_swarm_result`) and
  `agents/agent-2/wire.jsonl`. Session dir mtimes: notify 18:30:16, agents
  18:33:40, main agent dir 18:34:21 — bracketing the file's birth exactly.
- **verify:**
  - User's actual prompt recovered verbatim from `main/wire.jsonl`:
    `/write-goal ok i want you to optimize agentic usage by updating and
    installing any deps, libs and config knobs … setup jujutsu as the git
    manager; i prefer fnm as the node manager … pin node version to node 24
    LTS; /skill:godspeed` — a goal-mode swarm dispatch on a fresh omarchy box.
  - agent-2's task text (recorded in the swarm result): install latest
    prebuilt `jq, ripgrep, fd, bat, gh, delta` into `~/.local/bin`, resolving
    each repo via `/releases/latest`. Its report-back lists `jq 1.8.2`,
    asset `jq-linux-amd64`, all six `--version` proofs passing.
  - agent-2 wire.jsonl shows it enumerated the `jq-1.8.2` release assets —
    including `jq-attestation.json` and every `jq-linux-*` platform binary —
    before fetching the amd64 one.
  - Filesystem corroboration of the same event:
    - `stat ~/.local/bin/jq`: Birth == Modify ==
      `2026-10-03 18:34:03.581916043` — written in place, never modified.
    - The whole agent-2 cohort landed in a 13 ms burst: `jq` .5819, `rg`
      .5829, `fd` .5840, `bat` .5859, `gh` .5939, `delta` .5949 — sequential
      loop installing already-downloaded assets.
    - `jj` born 18:33:58.917 (agent-1 "JUJUTSU" lane; `~/.config/jj/config.toml`
      carries the git identity "Joao Pedro Veiga" / `jpveigao10@gmail.com`
      exactly as that lane's brief specified).
    - `~/.local/state/gh/device-id` born 18:34:08 — agent-2's `gh --version`
      proof run creating gh's first-run device id.
    - `~/.local/share/fnm/node-versions/v24.21.0` created 18:34:17 —
      agent-0 "FNM + NODE 24" lane (`fnm install 24`), and `~/.bashrc` edits
      it described are still present.
    - Local `fd` is 10.5.0 and `gh` 2.102.0 vs pacman's 10.4.2-2 / 2.96.0-1:
      different versions → upstream release binaries, not copies of
      `/usr/bin`.
  - Correlating system evidence: journalctl records a failed
    `sudo /usr/bin/true` at 18:31:55 (`a password is required`) — consistent
    with the swarm brief's "NO sudo (password-protected — do not attempt)".
  - Version check still holds: `~/.local/bin/jq --version` → `jq-1.8.2`.
- **verified-at:** 2026-10-13T15:58Z
- **suggested:** mark `~/.local/bin/jq` provenance **resolved**. It is a
  benign, intentional install: an agent-executed copy of the official
  `jqlang/jq` `jq-1.8.2` `jq-linux-amd64` release artifact, placed alongside
  five sibling CLI tools during the Oct-3 post-omarchy "optimize agentic
  usage" bootstrap. The residual Unknown from round 2 is closed. If the lane
  wants belt-and-suspenders, GitHub's `jq-attestation.json` artifact (seen in
  the same release listing) can be used for a `gh attestation verify` pass —
  unnecessary given the round-2 byte-identity result.

### Candidate 2 — pacman / omarchy package install (ruled out)

- **claim:** jq came from the system package manager.
- **source:** `/var/log/pacman.log`.
- **verify:** `pacman -Qqo ~/.local/bin/jq` → `error: No package owns
  /home/vgpnk/.local/bin/jq`. Pacman *did* install `jq 1.8.2-1` at
  `2026-10-03T17:44:22` during the omarchy bootstrap (`pacman -S` line at
  17:42:38), but to `/usr/bin/jq` — a separate system copy that still exists.
  The `~/.local/bin` file is a second, user-local upstream binary written 50
  minutes later.
- **verified-at:** 2026-10-13T15:45Z
- **suggested:** none — the dual-jq state (system `/usr/bin/jq` 1.8.2-1 +
  user-local 1.8.2) is explained, not anomalous.

### Candidate 3 — version managers / package shims (ruled out)

- **claim:** mise / fnm / asdf / aqua / `bin` / `eget` / `ubi` placed it.
- **source:** `~/.config/mise/config.toml`, `~/.local/share/mise/`,
  `~/.local/share/fnm/`, `~/.local/bin` metadata sweep, PATH tool probe.
- **verify:** mise config states it "manages nothing" (fnm owns node;
  `mise ls` empty; installs dir holds node only). fnm manages
  `~/.local/share/fnm/node-versions` only. No `eget`/`ubi`/`bin`/`brew`/`nix`/
  `devbox`/`pkgx` on PATH; `~/.local/bin` contains no manager manifest,
  config, or state files; jq is a regular file, not a symlink (rules out
  aqua/nix/home-manager styles).
- **verified-at:** 2026-10-13T15:46Z
- **suggested:** none.

### Candidate 4 — omarchy installer / AI-CLI install scripts (ruled out)

- **claim:** an omarchy script, the kimi-code installer itself, or the omp
  installer dropped the cohort.
- **source:** `~/.local/share/omarchy/{bin,install}`, fetched
  `https://omp.sh/install` and `code.kimi.ai/kimi-code/install.sh`, dir birth
  times.
- **verify:** Omarchy ships no release-binary downloader for these tools
  (its `install/` tree uses pacman/AUR; `omarchy-npx-install` only writes the
  ~1.4 KB npx stubs seen at 17:44:35 — `codex gemini copilot opencode
  playwright-cli pi ghui`, matching `omarchy-remove-preinstalls`' list). The
  kimi install.sh merely *prefers* jq for JSON parsing when present
  (line ~173-177). `~/.omp` was born 19:10:34 — after the cohort. Timeline:
  omarchy bootstrap 17:42-17:44 → kimi install ~17:52 (`~/.kimi-code` birth
  17:52:50) → swarm session 18:30-18:40 → omp install ~19:10.
- **verified-at:** 2026-10-13T15:50Z
- **suggested:** none.

## Run log

- `stat` + neighbor sweep → cohort `{jj 18:33:58; jq rg fd bat gh delta 18:34:03}` same-second births; stubs at 17:44:35; nothing else that evening until 21:12.
- `grep jq` across all shell histories → `.bash_history` is a 109-line post-Oct-3 tail; no install command (swarm ran inside kimi-code, not bash).
- `~/Downloads` → no jq archives; no `*jq*`/tool tarballs left in `/tmp`/`~/.cache` (agent cleaned staging dirs).
- `pacman -Qqo` fails on the file; `pacman.log` shows system `jq 1.8.2-1` installed 17:44:22 as part of the omarchy `pacman -S` mega-line.
- journalctl 18:31:55 → failed `sudo /usr/bin/true` (non-interactive sudo probe; matches swarm's NO-sudo brief).
- `~/.local/state/gh/device-id` @18:34:08, `~/.config/jj/config.toml` @~18:34, `fnm` node v24.21.0 @18:34:17 — three other swarm lanes' footprints, same minute.
- `find ~/.kimi-code/sessions -newermt …` → session `cf944588` active 18:30-18:49; `main/wire.jsonl` line ~153 holds the full `agent_swarm_result` with per-agent briefs and completion reports, including agent-2's jq 1.8.2 / `jq-linux-amd64` install + proof table.

## Summary

**Provenance resolved — not unknown.** `~/.local/bin/jq` is the official
upstream `jq-1.8.2` `jq-linux-amd64` release binary, downloaded from
`github.com/jqlang/jq/releases` (via `api.github.com` latest-release
resolution) and written to `~/.local/bin` at `2026-10-03 18:34:03.58 -0300`
by **agent-2 of a 4-lane kimi-code agent swarm**. The swarm was executing the
user's `/write-goal` + `/skill:godspeed` request to bootstrap agentic tooling
(jj + fnm/node-24 + CLI deps + config knobs) rootlessly on a fresh omarchy
install — the same event that installed the bat/delta/fd/gh/rg/jj cohort, ran
the `gh --version` proof (18:34:08 device-id), and provisioned fnm node
v24.21.0 (18:34:17). Consistent with round 2's byte-identical-to-upstream
finding; no malicious or accidental pathway indicated. Residual Unknown
closed.

## Errata (arc2-loop1-round1 freshness, 2026-10-18, append-only)

- **Safety-verdict scope (arc2-loop1-round1):** The phrases "benign, intentional install" (`:60`) and "no malicious or accidental pathway indicated" (`:136`) are historical wording, not a present endorsement or a safety/trust verdict. Folded back to the recorded evidence, they assert only that no byte difference from the cited upstream artifact was recorded — the round-2 SHA-256 byte-identity match to the upstream jq-1.8.2 `jq-linux-amd64` release artifact (`:5-6`; `2026-10-13-r2-jq-shadow-verdict.md:10-13,204-219`) — and that the sources examined in the round surfaced one pathway, the recorded agent-2 fetch-and-install event of 2026-10-03 18:34:03 -0300 (`:11-66`; run-log source set `:116-122`); they are not an absence-of-malice finding about the artifact. The lane never answers whether an artifact is "safe, trustworthy, or licensed for reuse" (`PROVINCE.md:114-116`); nothing here asserts that the artifact or its upstream is uncompromised, safe, trustworthy, or reusable. This note qualifies, and does not rewrite, the historical text.
