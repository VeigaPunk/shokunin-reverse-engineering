# R5 dispatch plan

64 seats, model `openai-codex/gpt-6-luna-max`, one AgentSwarm call.
Each seat gets: seat-id + chain + the round contract (read claims-frozen.md,
produce its artifact under claims/<chain>/<SEAT>/, never write repo files).
Prompt template carries the seat name as {{item}}.
