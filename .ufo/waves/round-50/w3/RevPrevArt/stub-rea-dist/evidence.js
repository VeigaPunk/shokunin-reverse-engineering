// Offline selftest stub of the rea-agents 6.5.0 evidence entry point.
// The real semanticProjection excludes the run-derived evidence_id field (the id
// is a digest OF the projection, so it cannot be part of it); replicate that so
// mint-vs-recompute is consistent and the stale-evidence-id case still fails.
export function parseEvidence(record) { return record; }
const semanticProjection = (evidence) => {
  const { evidence_id, ...rest } = evidence;
  return rest;
};
export { semanticProjection };
