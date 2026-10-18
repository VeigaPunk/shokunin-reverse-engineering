# Mechanism-matched wall engagements (and when to stop)

Case: the 91.6MB Godot ARM64 PE scale wall, arc2 rounds 3-8.

## The pattern

Each engagement changed exactly the mechanism the prior failure named, and
nothing else: round 3's outer-cap kill named time → the deadline was raised;
round 4's memcg kill named memory (10 decompile workers at 7G) → the analyzers
driving the workers were disabled; round 6's refusal named validation → the
analyzer names were validated against Ghidra's registry; round 7 held. Round 8
sealed the attribution with a natural control — same target, same caps, same
deadline, only the disable absent — and the run died in 4m42.945s with the
original kill profile. The kill is what makes the hold's attribution a fact
rather than a story.

## Standing rules

1. A wall engagement changes one mechanism per attempt, pre-commits all
   outcome branches (held / refusal / kill / in-flight), and carries the
   prior failure's evidence into the next design.
2. A natural control — same everything, treatment absent — is the cheapest
   way to convert a mitigated success into attributed knowledge. Budget it
   when the mitigation will be reused or cited.
3. Containment and outcome are separate claims: a contained kill is a
   successful containment and a failed run; record both.
4. Stop rule: when the mechanism list is near-exhausted, a further engagement
   without a NEW mechanism is sunk cost — retire the thread and hold the
   taxonomy (arc2's wall thread is retired at round 8; a ninth engagement
   would need a genuinely new hypothesis).

(arc2-loop1-round8; convergent with CR1's stop rule and R1's fairness matrix.)
