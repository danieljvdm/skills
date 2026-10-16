# Skills

Dan's shared engineering skills for Codex, Claude Code, Cursor, Grok, OpenCode, and other clients that support Agent Skills. This repository is the source of truth; dotfiles and Dev Kit distribute pinned copies.

Start with [dan-mode](skills/dan-mode/SKILL.md) for the personal working style: minimum useful implementations, reusable capabilities, fast feedback, and performance as required behavior. Cloudflare, Effect, Alchemy, and Vite+ are defaults with justified exceptions. These are personal preferences to review before adopting elsewhere.

## Skills

| Skill | Purpose |
| --- | --- |
| [dan-mode](skills/dan-mode/SKILL.md) | Working preferences and progressive disclosure |
| [library-first](skills/library-first/SKILL.md) | Reusable capabilities inside apps or standalone libraries |
| [simplify](skills/simplify/SKILL.md) | Remove unnecessary machinery |
| [debugging](skills/debugging/SKILL.md) | Diagnose causes with focused evidence |
| [measure-performance](skills/measure-performance/SKILL.md) | Protect critical paths and compare performance |
| [feedback-loops](skills/feedback-loops/SKILL.md) | Reusable, fast development feedback |
| [o11y](skills/o11y/SKILL.md) | Tracing, Maple, Cloudflare signals, and Effect OTLP |
| [cloudflare](skills/cloudflare/SKILL.md) | Workers, Durable Objects, and CLI use |
| [effect](skills/effect/SKILL.md) | Effect architecture, APIs, and runtime integration |
| [alchemy](skills/alchemy/SKILL.md) | Infrastructure and temporary test resources |
| [project-setup](skills/project-setup/SKILL.md) | Repository setup and Vite+ tooling |
| [testing](skills/testing/SKILL.md) | Test selection and design |
| [pull-requests](skills/pull-requests/SKILL.md) | PR preparation, evidence, review, and publication |
| [design-ui](skills/design-ui/SKILL.md) | UI implementation and refinement |
| [animate](skills/animate/SKILL.md) | Motion and gestures |
| [orchestrate](skills/orchestrate/SKILL.md) | Independent delegation and model selection |

## Use

Copy the selected skill directories into the client's skill location, commonly `~/.agents/skills` for personal use or `.agents/skills` for a repository. Keep sibling skills together when following their cross-links. Client discovery paths and invocation syntax vary.

`dan-mode` and `simplify` are manual skills. Both their frontmatter and Codex sidecars preserve that policy. In Codex invoke `$dan-mode` or `$simplify`; in Claude Code, Cursor, or Grok use `/dan-mode` or `/simplify`; in OpenCode 2 use `@dan-mode` or `@simplify`. Other skills are available for selection when relevant.

Dev Kit can distribute these skills through its approved Git catalog, pinned to a commit. Installed copies remain ordinary repository content. Make shared changes here, then advance the consuming catalog and update its copies; preserve intentional local changes during updates. Native agent registrations remain client configuration and can refer to the investigator and reviewer instructions in `orchestrate`.

## Maintain

Write normal Markdown paragraphs without manual line wrapping. Keep entrypoints concise, place conditional detail in references, and retain invocation policies and attribution. Validate the same files before publishing or refreshing a consumer:

```sh
uv run --with pyyaml python scripts/validate.py
```

The [principles record](docs/principles.md) explains selected ideas and adaptations from Poteto mode. Skill-specific notices retain upstream authors and licenses; original material uses the root MIT license.
