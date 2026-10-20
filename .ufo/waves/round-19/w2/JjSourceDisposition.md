# JjSourceDisposition — round 19 wave 2

## Findings (severity order)

### Low — “triple registration” is now an incomplete count, not a fleet-wide inventory

**[OBSERVATION]** The historical carry calls this the “jj 0.45.1 doc triple registration” (`.ufo/waves/round-19/claims.json:32`; `.ufo/waves/round-18/lessons/round-18.md:92`). The earlier crosswalk names Kaidoku S036, Tameshi S061, and Tabi S049 (`.ufo/waves/round-18/w2/SiblingOverlap2.md:102-112`; `.ufo/waves/round-19/w1/JjRowRouting.md:5-8`). In the current readable lane registries, Tabi still has S049 but S055 explicitly says “supersedes S049” (`tabi-shokunin/corpus/SOURCES.md:63,69`). Thus those three lane registries currently contain **four** `git-compatibility` rows, not three: Kaidoku S036, Tameshi S061, Tabi S049, and Tabi S055.

**[OBSERVATION]** A targeted count over all `*-shokunin/corpus/SOURCES.md` files finds **six** rows across five lanes: Kaidoku S036, Mori S044, Souji S051, Tameshi S061, and Tabi S049/S055. Exact anchors: `kaidoku-shokunin/corpus/SOURCES.md:42`; `mori-shokunin/corpus/SOURCES.md:50`; `souji-shokunin/corpus/SOURCES.md:67`; `tameshi-shokunin/corpus/SOURCES.md:70`; `tabi-shokunin/corpus/SOURCES.md:63,69`. These are not six independent confirmations: the anchors differ. S036 and Tabi S055 are versioned v0.45.1; Tameshi S061 says `latest`/v0.46.0; Mori S044 says `latest`; Souji S051 combines `latest` with a raw v0.45.1 URL. Tabi S055 marks S049 superseded, but S049 remains in the table as `queued`.

**[INFERENCE]** Keep “triple registration” only as the historical name for the original three-lane observation. Any current crosswalk should name S055 as Tabi’s superseding row, retain S049 as its historical predecessor, distinguish version anchors, and avoid treating repeated rows as independent evidence. The fleet count is an exact `git-compatibility` source-field count, not a count of every jj-related document (for example, adjacent CHANGELOG rows are outside it).

### No actionable scope/ownership finding — S036 remains tool-local in Kaidoku

**[OBSERVATION]** S036 is a v0.45.1 raw-tag citation with a fetched-document SHA-256 and anchors at upstream `docs/git-compatibility.md` lines 114–116 and 208 (`kaidoku-shokunin/corpus/SOURCES.md:42`). Its `used-by` list is only `corpus/lessons/round-18.md, SKILL.md` (same line). The sole SOURCES path is explicitly “Revision pins under jj — S036” and says lane tools pin the branch ref, with the lane sandbox receipt carrying the off-branch failure (`kaidoku-shokunin/corpus/SOURCES.md:53`). The local SKILL section is titled “Revision pins under jj,” describes branch-ref pinning and its limits, and identifies the local `revpin` probe (`kaidoku-shokunin/SKILL.md:567-579,588`). The helper’s own contract describes branch/HEAD/remote checks (`kaidoku-shokunin/.ufo/waves/round-18/tools/revpin.py:2-15,98-126`); its verifier calls `resolve_source` before running commands (`kaidoku-shokunin/.ufo/waves/round-18/verify.py:90-100`). The lesson itself says S036 is retained only for Kaidoku’s own pin tools and the broader item is “Reported, not absorbed” (`kaidoku-shokunin/corpus/lessons/round-18.md:92`).

**[INFERENCE]** This is a bounded source citation for a lane-local revision-pin tool, not evidence that Kaidoku owns jj generally. The row’s scope sentence states a general Git-HEAD fact, so its tool-local boundary comes from the explicit `used-by`/Paths mapping and local tool contract; do not expand it into a Kaidoku jj knowledge entry or tool manual.

**[OBSERVATION]** The routing map assigns the general “Colocation hazards + helper contract” candidate to **kumitate** (R1), explicitly says it does not own helper code, receipts, or contract text, and lists Kaidoku among “No route” lanes that must not seed jj entries in product domains (R9) (`/home/vgpnk/Projects/shokunin/.ufo/waves/hyaku/jj-w1/reports/JjConnectorProvinces.md:181,189`). The report calls its recommendations routed candidates, not corpus writes, and says the owner’s lane must admit them (`:191-196`). The protocol requires an integrator routing line, an aggregator mirror/open row, and owner-side admission (`/home/vgpnk/Projects/shokunin/PROTOCOL.md:241-248`). In the bounded searches, Kumitate `corpus/SOURCES.md` returned no `jj-vcs.dev`, `git-compatibility`, or `jj-lane-vcs-substrate` match; `corpus/lessons/` returned no `jj-lane-vcs-substrate`, `JjConnectorProvinces`, `jj 0.45.1`, or `S036` match; `corpus/knowledge/` returned no `jj-vcs`, `jujutsu`, `colocated jj`, `git-compatibility`, or `jj 0.45` match. The listed knowledge files contain no `jj-lane-vcs-substrate.md`. These are bounded text/name searches, not proof that semantically related material is absent.

**[INFERENCE]** Kumitate ownership of the general candidate is supported; owner admission is not observed. Do not report S036 as transferred, admitted, or closed. The separate Mori/Souji records fit their routing scopes (R6/R2) and do not transfer Kaidoku’s scope (`JjConnectorProvinces.md:182,186`).

## Axis impact

- **Calibration — [INFERENCE] likely helped by this disposition:** it distinguishes repeated registrations from independent evidence and makes the count’s scope explicit; no score change was measured.
- **Freshness — [OBSERVATION] correction needed in the count:** Tabi S055 supersedes S049, and current `latest` rows do not all identify the v0.45.1 artifact. No live document re-fetch was performed.
- **Depth — [INFERENCE] unchanged:** this is source-scope/routing review only; no runtime or tool logic changed.

## Residual risk

- R9’s “no route” is broader than the local pin-tool citation if read literally. The accepted narrow boundary is recorded in the round-18 carry and the explicit local Paths/`used-by` mapping; do not present that interpretation as a new authoritative exception to R9.
- The observed R1 route is a candidate. This review found no Kumitate corpus admission, and did not verify an aggregator ledger row or owner decision. Per the protocol, only Kumitate may admit the general knowledge.
- The six-row count is limited to the exact `git-compatibility` string in the source column of lane `SOURCES.md` files. It does not establish that every row has identical scope or that no other jj-related sources exist.

## Verification and gaps

Commands were read-only; no source/tool edits, jj invocation, tests, runtime, build, or external document fetch was performed.

```text
git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin rev-parse refs/heads/main
=> 279e8b19c51658bfd05b9e31a1c0894ab2e70537 ; exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --stat refs/heads/main
=> .ufo/waves/round-19/wave2-registry.json | 150 ++++++++++++++++----------------
   corpus/SOURCES.md                       |  14 +--
   2 files changed, 84 insertions(+), 80 deletions(-) ; exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=0 refs/heads/main -- corpus/SOURCES.md
=> no S036 hunk; displayed hunks are unrelated S003/S023/S024/S026/S031/S035 changes, S039 addition, and path addition ; exit 0

git -C /home/vgpnk/Projects/shokunin/kaidoku-shokunin diff --no-ext-diff --unified=0 refs/heads/main -- SKILL.md .ufo/waves/round-18/tools/revpin.py
=> empty ; exit 0

awk -F '|' 'index($3,"git-compatibility") { printf "%s:%d:%s\n", FILENAME, FNR, $2; n++ } END { printf "git-compatibility source rows=%d\n", n }' /home/vgpnk/Projects/shokunin/kaidoku-shokunin/corpus/SOURCES.md /home/vgpnk/Projects/shokunin/tameshi-shokunin/corpus/SOURCES.md /home/vgpnk/Projects/shokunin/tabi-shokunin/corpus/SOURCES.md
=> S036, S061, S049, S055; git-compatibility source rows=4 ; exit 0

awk -F '|' 'index($3,"git-compatibility") { printf "%s:%d:%s\n", FILENAME, FNR, $2; n++ } END { printf "git-compatibility source rows=%d\n", n }' /home/vgpnk/Projects/shokunin/*-shokunin/corpus/SOURCES.md
=> kaidoku S036; mori S044; souji S051; tabi S049; tabi S055; tameshi S061; git-compatibility source rows=6 ; exit 0
```

**LSP limitation:** no `lsp` device/status endpoint was exposed in this session, so LSP references/definition/diagnostics were unavailable. The caller relation above is supported by the cited SKILL and verifier source text; text-search results were used only to locate registry entries, not as semantic proof. No live jj behavior or owner-side admission was tested.