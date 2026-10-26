def scrub:
  walk(
    if type == "string" then
      (gsub("/fast/scratch/hyaku/[^ \"]*"; "<SCRATCH>") | gsub("/home/vgpnk/Projects/shokunin/kaidoku-shokunin"; "<LANE>"))
    else . end
  );

{
  engine: (.normalized_result.engine | del(.worker_count)),
  coverage: .normalized_result.coverage,
  selection: .normalized_result.selection,
  published_bytes: .normalized_result.published_bytes,
  chunks: ([.normalized_result.chunks[] | del(.provider_id)] | sort_by(.range.offset, .handler)),
  files: ([.normalized_result.files[]
           | {relative_path, size, sha256, reported_sha256, mime_type, analysis_depth,
              runtime_address, original_file_range}]
          | sort_by(.relative_path)),
  gaps: ([.normalized_result.extraction_gaps[] | del(.provider_id)]
         | sort_by(.kind, (.relative_path // ""), .handler)),
  depth_limited: .normalized_result.depth_limited_paths,
  unpublished: .normalized_result.unpublished_entries,
  continuations: .normalized_result.extraction_continuations,
  derivations: .normalized_result.derivations,
  diagnostics: (.normalized_result.diagnostics | scrub),
  report: ([.raw_result.report[]
            | {subtasks: [.subtasks[]? | scrub],
               reports: [.reports[]? | scrub]}]
           | scrub),
  execution: (.raw_result.execution
              | {exit_code, signal, command, args, stdout: .stdout.text, stderr: .stderr.text}
              | scrub),
  version_execution: (.raw_result.version_execution
                      | {exit_code, signal, stdout: .stdout.text, stderr: .stderr.text}
                      | scrub),
  operation: .operation,
  predicate_type: .predicate_type,
  provider: .provider,
  subject: .subject,
  analysis_profile: .analysis_profile,
  confidence: .confidence,
  authority: .authority,
  locations: (.locations | scrub),
  limitations: (.limitations | scrub),
  relationship_coverage: .relationship_coverage,
  evidence_links: .evidence_links
}
