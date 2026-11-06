# Kaidoku: search paths belong to dependency edges

The historical [ld.so manual](https://github.com/mkerrisk/man-pages/blob/master/man8/ld.so.8), dated2021-08-27, distinguishes DT_RPATH from DT_RUNPATH. The [current rendering](https://man7.org/linux/man-pages/man8/ld.so.8.html), inspected2026-11-06, retains the direct-dependency distinction. This is continuity.

For names without slashes, RUNPATH applies to direct DT_NEEDED dependencies; their children need their own RUNPATH. RPATH instead affects searches throughout the dependency tree and is considered only when RUNPATH is absent. A dependency containing a slash follows its pathname instead.

Record each object's tags and dependency edges, not the executable's directory list to every descendant. Environment, secure-execution mode, caches and defaults still affect resolution. A plausible dependency map is not proof of which library loaded.

Unlike IFUNC selection or TLS coordinates, this concerns dependency lookup. No binary or loader executed. Historical source declares public domain; current rendering rights were not independently established. Original commentary only, no source reproduction. Optional exercises omitted; originals retained.
