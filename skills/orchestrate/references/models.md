# Model selection

These preserve the existing personal orchestration defaults. Select only models and effort levels actually offered by the current client.

| Work | OpenAI model | Effort |
| --- | --- | --- |
| Bounded search or mechanical inspection | `gpt-6.1-sol` | `low` |
| Implementation, diagnosis, or review | `gpt-6.1-sol` | `high` |
| Difficult reasoning or interacting constraints | `gpt-6-astra` | `xhigh` |
| Hardest problems requiring deeper reasoning | `gpt-6-astra` | `max` |

Choose by the problem, not the role's name. Honor the user's task-specific model choice. If the client cannot express the choice, explain the limitation and use an explicitly accepted option.

Codex native custom-agent files deliberately omit model fields. A model pinned there overrides spawn choices. Set the model and effort at spawn time when the tool supports them. If its schema exposes `fork_turns`, use `none` for an explicit override and provide a focused task brief. When overrides are unavailable, inherit the parent model unless this conflicts with an explicit task choice; resolve that conflict before spawning. Codex's service tier follows the root session.

In Grok, use the available `model` and `reasoning_effort` spawn fields. Local model IDs currently include `gpt-6.1-sol` and `gpt-6-astra`. In OpenCode 2, model selectors use `provider/model#variant`, such as `openai/gpt-6.1-sol#high`, when that variant is available. The roles inherit the session model rather than changing the client's global default. Select an OpenAI parent session when using these roles with OpenAI models in another client.

Sources: [Codex custom agents](https://learn.chatgpt.com/docs/agent-configuration/subagents), [OpenCode 2 agents](https://opencode.ai/v2/docs/agents/), and the installed `~/.grok/docs/user-guide/16-subagents.md`. Checked 2026-10-15.
