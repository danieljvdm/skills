---
name: orchestrate
description: Coordinate independent work, parallel coverage, and competing approaches with subagents when delegation materially improves a substantial task.
---

# Orchestrate

Delegate work that has a clear question or output and can proceed independently. Handle short or tightly coupled work directly. The primary agent owns scope, user communication, integration, and the final result.

For parallel coverage, races, or exploration of competing approaches, read [swarm patterns](references/swarms.md). Define the completion condition and required slices or selection rule before spawning. A swarm is a bounded delegation pattern; it does not require a separate agent runtime or project-management system.

Keep the delegation tree flat. Give each worker the task, relevant file or evidence pointers, constraints, allowed write paths, acceptance criteria, expected evidence and output, and a no-delegation instruction. Supply only the context it needs. Include existing valid evidence so workers do not repeat the same verification. Share one reusable harness instead of having each worker invent a private loop.

Partition writers by file ownership or isolated worktrees. Tell workers they share the codebase, must preserve others' edits, and must report changes outside their assigned scope instead of making them. A native agent does not imply an isolated checkout. Respect the client's concurrency limit and increase parallelism only while useful. Continue unrelated work while a worker runs.

In Codex, use the available native collaboration tools and registered roles. Use a focused brief with `fork_turns: "none"` when full conversation history is unnecessary; include relevant user constraints and repository instructions. Inherit context when the task genuinely depends on it. Use status and messages to inspect running work; a follow-up can start an idle agent, so do not use it merely to poll. Wait for notifications when there is no useful independent work. Before replacing a missing worker or reassigning its files, establish whether it is still running and stop it or isolate the replacement's writes. Confirm its state before reusing shared paths. Do not launch a nested Codex CLI or another provider as an implicit fallback. Session instructions govern whether delegation is allowed.

Use [model selection](references/models.md) for OpenAI defaults and client-specific syntax. Preserve explicit user choices. Report an unavailable model or feature instead of silently changing providers or starting a different agent system.

Two optional roles provide different kinds of evidence:

- [Investigator](references/investigator.md): answer a bounded technical question.
- [Reviewer](references/reviewer.md): inspect a proposed change independently.

Use an ordinary worker for implementation. Reuse a worker for follow-up work when its context remains useful; start fresh when independence or a new scope warrants it. Review worker evidence and changes before integrating them. A reviewer agreement is supporting evidence, not a substitute for checking the affected behavior.
