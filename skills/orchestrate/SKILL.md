---
name: orchestrate
description: Coordinate independent work with subagents when delegation materially improves a substantial task.
---

# Orchestrate

Delegate work that has a clear question or output and can proceed independently. Handle short or tightly coupled work directly. The primary agent owns scope, user communication, integration, and the final result.

Keep the delegation tree flat. Give each worker the task, relevant file or evidence pointers, constraints, expected output, and a no-delegation instruction. Supply only the context it needs. Use the native client tools and its actual capabilities. Include the acceptance question and existing valid evidence so workers do not repeat the same verification. Share one reusable harness instead of having each worker invent a private loop.

Partition writers by file ownership or isolated worktrees. Respect the client's concurrency limit and increase parallelism only while useful. Check active work before spawning replacements. Continue unrelated work while a worker runs.

Use [model selection](references/models.md) for OpenAI defaults and client-specific syntax. Preserve explicit user choices. Report an unavailable model or feature instead of silently changing providers or starting a different agent system.

Two optional roles provide different kinds of evidence:

- [Investigator](references/investigator.md): answer a bounded technical question.
- [Reviewer](references/reviewer.md): inspect a proposed change independently.

Use an ordinary worker for implementation. Reuse a worker for follow-up work when its context remains useful; start fresh when independence or a new scope warrants it. Review worker evidence and changes before integrating them. A reviewer agreement is supporting evidence, not a substitute for checking the affected behavior.
