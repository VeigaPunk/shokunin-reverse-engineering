- **An artifact that records its own byte-identity must re-derive that identity
  after every revision; a stale self-identity voids the verification block, not
  the work.** The arc3-loop1-round1 entry patch churned mid-wave: its recorded
  identity stopped describing the artifact it produced, and an independent
  re-apply read different bytes (8,598 B vs the claimed 8,316 B). Re-derive
  before citing; the integrator records the fresh identity at landing. The
  evidence-id family's analogue: an id held across a day and re-derived
  byte-exact (`corpus/knowledge/2026-10-14-r12-01-queue-b-ready.md:11`).
