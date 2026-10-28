- **24. An exactness matrix states one exact arm per routed defect.** <!-- exactness-table v3 --> The round-46 spot-check routed four instrument defects; this table names each hole and the arm that closes it.

| trigger | v2 hole | v3 arm | exit |
|---|---|---|---|
| a loose cell | the check is a containment, so any word passes | arm one | 1 |
| a loose cell | the check is at-least-once, so a row may overclaim | arm two | 1 |
| a loose cell | the list is counted, never pinned | arm three | 2 |
| a loose cell | the flag order is a code detail no clause reads | arm four | 1 |
