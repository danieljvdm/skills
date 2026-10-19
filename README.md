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
| [show-me](skills/show-me/SKILL.md) | Focused visual explanations, diagrams, and code-shape sketches |
| [design-ui](skills/design-ui/SKILL.md) | UI implementation and refinement |
| [animate](skills/animate/SKILL.md) | Motion and gestures |
| [orchestrate](skills/orchestrate/SKILL.md) | Independent delegation and model selection |
| [scrawl](skills/scrawl/SKILL.md) | Read screen captures, transcripts, clicks, and drawings from Scrawl |

## Use

Copy the selected skill directories into the client's skill location, commonly `~/.agents/skills` for personal use or `.agents/skills` for a repository. Include the supporting skills reached by relative links, including links inside references, so the copy works without a personal installation. Select relevant workflows instead of installing the entire personal stack. Engineering skills do not depend on `dan-mode`.

Client discovery paths and invocation syntax vary. A repository and personal installation can contain the same skill name; do not assume the client merges or consistently prefers one copy. Required repository workflows should link to the exact repository path. Keep intentionally different workflows under distinct names.

`dan-mode` and `simplify` are manual skills. Both their frontmatter and Codex sidecars preserve that policy. In Codex invoke `$dan-mode` or `$simplify`; in Claude Code, Cursor, or Grok use `/dan-mode` or `/simplify`; in OpenCode 2 use `@dan-mode` or `@simplify`. Other skills are available for selection when relevant.

Dev Kit distributes these skills through its approved Git catalog, pinned to a commit. Installed copies remain ordinary repository content. Make shared changes here, then update the consuming copies; preserve intentional local changes. Native agent registrations remain client configuration and can refer to the investigator and reviewer instructions in `orchestrate`.

## Updates

Dan's dotfiles provide `skills-update` for personal copies, independent of a Dev Kit release. Preview with `skills-update --dry-run`, then apply the printed commit with `skills-update --ref <commit>`. Supply skill names to update only those skills. Review and commit the resulting files and origin receipts with `cfg`; normal dotfiles sync carries them to other machines. The command preserves locally edited or untracked collisions and leaves unrelated skills alone.

Pushes to `main` that change skills run the [Dev Kit update workflow](.github/workflows/update-dev-kit.yml). It refreshes only `dan-skills`, validates the selected source revision, and opens or updates one catalog PR with a patch changeset. Merging and publishing follow Dev Kit's normal release process. A manual workflow run is also available.

The workflow requires Dev Kit's shared-source integration and `catalog refresh --source` support on its `main` branch. Configure `APP_CLIENT_ID` and `APP_PRIVATE_KEY` in this repository for the existing GitHub App installed on `danieljvdm/dev-kit`, with contents and pull-request write access. The key stays in GitHub Actions secrets; no personal access token or runtime service is required.

### Scrawl upstream

[Scrawl](https://github.com/kitlangton/scrawl/tree/main/skills/scrawl) is vendored from Kit Langton's repository with its MIT license. The [daily update workflow](.github/workflows/update-scrawl.yml) checks upstream `main` at 10:23 UTC, validates the skills, and commits changed Scrawl content directly to this repository's `main`. GitHub may delay scheduled runs. The same GitHub App must also be installed on this repository with contents write access; its commits trigger the existing Dev Kit update workflow. Run the Scrawl workflow manually to check immediately.

The skill's `.upstream.json` records the upstream commit and file hashes; unrelated upstream commits produce no update. Source attribution and the Codex sidecar are generated while preserving upstream instructions and invocation policy. Local changes to the imported skill block updates until reconciled. To refresh from a checkout, run `uv run --with pyyaml python scripts/update-scrawl.py`, then the validation command below. Personal installed copies still update through `skills-update`; this workflow updates the canonical repository.

## Maintain

Write normal Markdown paragraphs without manual line wrapping. Keep entrypoints concise, place conditional detail in references, and retain invocation policies and attribution. Validate the same files before publishing or refreshing a consumer:

```sh
uv run --with pyyaml python scripts/validate.py
```

To check selected installed copies and their relative links, use `uv run --with pyyaml python scripts/validate.py --skills-dir /path/to/repo/.agents/skills effect cloudflare`. This checks the named skills without imposing this repository's metadata policy on unrelated third-party skills.

The [principles record](docs/principles.md) explains selected ideas and adaptations from Poteto mode. Skill-specific notices retain upstream authors and licenses; original material uses the root MIT license.
