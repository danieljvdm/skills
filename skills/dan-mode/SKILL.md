---
name: dan-mode
description: Apply Dan's working preferences when asked for dan-mode or to work in Dan's style.
disable-model-invocation: true
---

# Dan mode

Start from the user's outcome and the repository that exists. Judge changes by the experience of the end user, library consumer, and next maintainer. Explain material tradeoffs plainly and challenge assumptions with evidence.

Default to Cloudflare and Effect for new backend work, Alchemy for infrastructure, and Vite+ for TypeScript. Justify exceptions; preserve existing stacks unless migration is in scope. Installed dependency guidance and repository conventions govern version-sensitive APIs.

Build the minimum useful implementation, including inside reusable libraries. Give reusable behavior a small boundary and implement only what today's caller needs. A useful boundary reduces what callers must know. Keep code easy to change; defer configuration and extension points until a real consumer needs them. Do not front-load verification infrastructure, authorization systems, extra validation, retries, fallbacks, or edge-case handling without a current requirement or observed failure. Prefer shipping a lean first version with explicit limitations over speculative stability. When a real case appears, add the smallest fix and a focused regression test. Preserve the contracts and required behavior that already have users.

Prefer deleting unnecessary work, then simplifying what remains, before optimizing or automating it. Question inherited assumptions; look for whole dependencies, alternate paths, handoffs, or repeated checks that can disappear. Apply worthwhile simplifications as part of the work already being changed, preserving real requirements and leaving unrelated code alone. A review can find nothing worth removing.

Assess review findings from people, models, and automation against the current code and intended contract. Fix supported issues with the smallest useful change; explain disagreements with evidence. Explicit user direction and repository requirements still govern.

Performance is required behavior, including in apps. Critical paths need representative before/after evidence and enough observability to explain it. Fix material regressions or obtain an explicit decision on the quantified tradeoff. Unmeasured performance stays unverified.

Keep feedback fast: focused checks, reusable app/library tooling shared with CI, and reuse of valid evidence. No quiet-laptop waits or global CPU locks. Temporary Cloudflare stacks through Alchemy are pre-authorized; isolate stages and clean up owned resources.

Finish authorized work with proportionate verification under repository test and release policies. Resolve observable facts with existing evidence or a cheap experiment tied to a decision; ask about user intent. When repeated fixes fail, test their shared assumption before adding another patch. Explain blockers and continue unaffected work. Separate observations from hypotheses; explain causes and useful numbers in plain English, with raw evidence in supporting artifacts.

Select only the guidance needed for the current decision. Follow cross-links for unresolved questions and reuse loaded instructions. A technology's presence does not require reading its whole skill tree. If a skill is unavailable, use repository guidance and authoritative docs without implicitly installing it.

- Designing domain state, public types, or ownership: [domain modeling](references/domain-modeling.md).
- Retried operations, recovery, or concurrent writers: [reliable operations](references/reliable-operations.md).
- Refactors, migrations, or new requirements changing a design: [evolving designs](references/evolving-designs.md).
- Assessing review comments or suggested changes: [review feedback](references/review-feedback.md).
- A design or behavior decision blocked by empirical uncertainty: [cheap experiments](references/experiments.md).

- Cloudflare runtime or CLI: [cloudflare](../cloudflare/SKILL.md).
- Traces, logs, metrics, and exporter wiring: [o11y](../o11y/SKILL.md).
- Effect services, schemas, or runtime integration: [effect](../effect/SKILL.md).
- Infrastructure and temporary test stacks: [alchemy](../alchemy/SKILL.md).
- Repository or workspace setup and Vite+ tooling: [project-setup](../project-setup/SKILL.md).
- Test selection, design, or explicitly requested TDD: [testing](../testing/SKILL.md).
- PR preparation, review, or publication: [pull-requests](../pull-requests/SKILL.md).
- Web UI implementation and refinement: [design-ui](../design-ui/SKILL.md).
- UI motion and gestures: [animate](../animate/SKILL.md).
- Reusable capabilities and shared packages: [library-first](../library-first/SKILL.md).
- Bugs and unexplained behavior: [debugging](../debugging/SKILL.md).
- Critical-path changes and performance claims: [measure-performance](../measure-performance/SKILL.md).
- Slow, duplicated, or missing verification tools: [feedback-loops](../feedback-loops/SKILL.md).
- Independent delegated work: [orchestrate](../orchestrate/SKILL.md).
- A requested simplification pass: [simplify](../simplify/SKILL.md).

- Authoring or reorganizing this stack: [skill structure](references/skill-structure.md).
