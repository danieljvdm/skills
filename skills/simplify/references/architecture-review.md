# Review a large feature, branch, or architecture

Use this workflow when the user asks whether a substantial solution is overbuilt, what could be deleted, or how much simpler its architecture could be. The result is a decision aid: a reviewer should understand what can disappear, why, what replaces it, and what they would give up. Question every major mechanism within the requested scope; size alone is not evidence that it is unnecessary. Scale the investigation to the decision rather than filling every section mechanically.

## Establish the scope and requirements

Record the repository, reviewed head, comparison base, and relevant working-tree changes. For a branch or PR, use its actual base and merge base rather than assuming the default branch. Distinguish the feature diff from the current implementation being sized for deletion. Link evidence to the reviewed revision so later changes do not silently invalidate the report.

Extract required user outcomes and external contracts from the request, repository guidance, callers, persisted data, and relevant operational evidence. Separate those facts from assumptions inherited from the implementation. Missing evidence is an uncertainty to expose, not permission to discard a guarantee. A pre-production codebase does not automatically authorize removing all compatibility; the [no-legacy workflow](no-legacy.md) owns that narrower case.

Distinguish explicit requirements from observed behavior in the report. A test asserting an intermediate status or a detailed progress timeline proves that the behavior exists; it does not independently justify the machinery behind it. Trace retention to a real consumer, explicit requirement, or operational need. If removing an optional behavior could eliminate a subsystem, present that larger option with its consequence and estimated savings, even when it needs a reviewer decision. Do not silently promote every existing detail into a requirement or silently discard it.

## Start with a smaller design

Trace representative paths from user intent to useful completion. Include failure, retry, or restart paths when a claimed guarantee depends on them. Map the major responsibilities, their owners, state stores, dependency boundaries, and asynchronous handoffs. Follow consequential callers beyond the diff; a search limited to changed files cannot establish that an interface is unused.

For a whole-feature or branch review, enumerate its major subsystems before choosing candidates. Cover them substantively or clearly narrow the report; inspecting one local cluster does not establish that the rest of the architecture is necessary.

Sketch how you would satisfy the requirements if the current implementation did not exist. Compare that design with the current one before collecting local cleanup suggestions. Useful questions include:

- Which user requirement or observed failure justifies each job, queue, state machine, adapter, dependency, or service boundary? What would fail if it vanished?
- Can an existing owner perform the work directly? Is state copied, derived, journaled, or synchronized when one authoritative owner would suffice?
- Do competing paths, compatibility layers, configuration options, demos, or frameworks still have consumers? Does a general abstraction have a present use beyond wrapping one call?
- If a mechanism disappears, which downstream writers, readers, types, endpoints, dependencies, UI states, tests, and documentation become obsolete with it?
- What is the strongest reason to retain it? Can the smaller design still provide that behavior without rebuilding the same machinery under a new name?

Use the [durability and verification guidance](durability-and-verification.md) when those mechanisms dominate the architecture. Preserve real authorization, ownership, typed failure, lifetime, recovery, and external-contract requirements. A useful boundary may stay while most of its implementation disappears. Do not turn the review into a catalog of hypothetical future needs.

Give every major area inspected a disposition: remove, collapse into an existing owner, keep with a concrete reason, or unresolved. Note areas not inspected. This coverage record makes a broad review distinguishable from a handful of local cleanups without pretending it proves exhaustiveness.

## Build proposals a reviewer can challenge

Group deletions by the responsibility that disappears, including its now-obsolete dependents. Use stable proposal IDs. Put the largest reductions in conceptual and operational burden first; line count is supporting evidence, not the ranking function. For each material proposal, establish:

- **Mechanism and evidence:** what exists, the exact files or symbols involved, relevant callers and contracts, and the observed evidence that supports removing it. Distinguish code inspection, runtime observation, and assumptions.
- **Why remove it:** the requirement it was meant to serve, why it is unnecessary or duplicated now, and the maintenance, latency, or operational burden that disappears. Do not claim a measured speedup from a simpler-looking diagram.
- **Smaller replacement:** a concrete owner and control/data path, or explicitly no replacement. A short code sketch can show that the replacement does not recreate the same abstraction.
- **Case for keeping it:** the strongest counterargument, behavior preserved, behavior deliberately changed, and any migration or recovery consequence. Treat a consequential unresolved guarantee as conditional rather than quietly assuming it away.
- **Size and dependencies:** estimated removals and additions, their basis, overlaps, prerequisite proposals, and mutually exclusive alternatives. Bundle tightly coupled deletions when that makes the decision more honest.
- **Recommendation and confidence:** recommend, conditional, or keep; explain what evidence limits confidence and what would resolve it. Name the focused checks needed before implementation can be called complete.

A short review may combine these fields in prose. A large review benefits from a summary table and expandable detail. A plausible keep decision is useful output; do not manufacture deletions to meet an expected number.

## Estimate honestly

Size proposals against the recorded current head. Count identified files or line ranges and inspect partial-file removals; do not convert the whole feature diff into a deletion estimate. State the counting convention, normally physical lines matching Git diff statistics. Distinguish measured existing lines from guessed removable portions and replacement size. Use ranges when the replacement has not been implemented, and state the basis, such as whole files plus identified branches, less retained public contracts.

Report gross deletions, expected additions, and net reduction separately. For deletion range `Dlow–Dhigh` and addition range `Alow–Ahigh`, conservative net reduction is `Dlow − Ahigh` through `Dhigh − Alow`. Negative reduction means growth. Use sensible precision; an exact file count does not make a replacement estimate exact.

Separate production code from tests, documentation, examples, and generated files. Identify vendored or lockfile churn separately too. Moving code to another file or package does not remove its maintenance burden. Do not let deleted examples or regenerated files stand in for architectural simplification.

Count the union of removed ranges, not the sum of overlapping ideas. Combine proposals that delete the same code, or present them as alternatives and exclude them from the aggregate. Explain prerequisite chains and count shared cleanup once. Show a total only for a compatible bundle with disjoint estimates. Label a partial total and list excluded or unsized proposals; unknown is not zero. If a deletion needs a major product decision, show its estimate separately from the recommended bundle.

## Produce the decision aid

Lead with the recommended smaller design, the main responsibilities removed, and the estimated net production reduction. Include enough contrary evidence for the reviewer to reject the recommendation. A useful large review has:

1. Scope, revision, requirements, and a brief recommendation.
2. Current and proposed architecture diagrams at the same level of detail, naming actual owners and the proposal IDs that remove or collapse them. Mark proposed behavior as proposed. Show important branches or failure paths separately when a linear path would be misleading.
3. A proposal table with recommendations, confidence, and estimate ranges; a breakdown of gross deletions, additions, and net reduction by code category.
4. The proposal evidence and tradeoffs, plus coverage and reasons for retaining major machinery.
5. Concrete decisions or unanswered questions, such as whether a later-arriving derived field is acceptable, and the checks that would validate the proposed replacement.

Keep the decision overview compact. Show a larger conditional alternative alongside the conservative bundle when it could materially change the architecture; make its premise and savings easy to compare. Group incidental cleanups and avoid repeating the same retained guarantees in every finding. Put detailed source evidence behind disclosures in HTML rather than letting it bury the decisions.

For a shareable visual report, copy the [standalone HTML template](../assets/architecture-review.html). It provides before/after path diagrams, deletion/addition range charts, category totals, source links, and expandable proposals. Replace its illustrative data; the example is not evidence about the reviewed repository. For a compact in-chat review, Markdown tables and Mermaid may be enough. Use [show-me](../../show-me/SKILL.md) for visual choices. The HTML is a presentation option for this workflow, not a prerequisite for ordinary simplification.

The template has one `review-data` JSON block and no build or network dependencies. Its example demonstrates the fields. Keep `requirements` separate from `assumptions`. Each side of `architecture` (`current` and `proposed`) has an `entry`, named `lanes` containing `nodes`, and a closing `note`; use lane labels and notes to make parallel work, joins, and recovery explicit. Put only compatible, disjoint recommended proposals in the total with `includeInTotal: true`; explain exclusions in `countNote`, including unknown estimates and alternatives. Optional `overlapsWith` and `requires` arrays name conflicting or prerequisite proposal IDs; the template rejects a bundle that violates those declared constraints. Establish actual overlaps from source inspection, not from the renderer. All proposals remain visible. Estimates are arrays of `{category, removed: [low, high], added: [low, high]}`; categories are `production`, `tests`, `docs`, `examples`, `generated`, `vendored`, or `lockfiles`. `coverage` describes what was actually inspected, including retained and unresolved areas. Source entries accept a label, evidence, and an optional URL. Use revision-pinned source links where available.

Generate the artifact in the task's temporary/output directory unless the user wants it committed. Replace the JSON block programmatically so quotes and code snippets remain data:

```python
import json
from pathlib import Path

template = Path("/path/to/simplify/assets/architecture-review.html").read_text()
data = json.loads(Path("/path/to/review.json").read_text())
data["example"] = False
payload = json.dumps(data, ensure_ascii=False, indent=2).replace("<", "\\u003c")
start = '<script id="review-data" type="application/json">'
before, rest = template.split(start, 1)
_, after = rest.split("</script>", 1)
Path("/path/to/review.html").write_text(before + start + "\n" + payload + "\n</script>" + after)
```

Open the result in an available browser, check its diagrams, totals, source links, and a narrow viewport, and inspect any reported data issues. Keep the labels and numbers accessible as text; color alone cannot explain a deletion or a range. The built-in lanes show named paths, not arbitrary graph edges; add a small SVG when ownership or branching would otherwise be obscured. Link the artifact from the response and include the recommendation and major uncertainty in chat too.

For a review request, stop at the decision aid. Do not interpret its recommendations as authorization to implement them. If implementation is already authorized, proceed within that scope without a new approval ceremony; use the proposals to guide the work, run appropriate checks, and replace estimates with actual gross and net changes. Revisit the design if the implementation merely relocates machinery or grows without removing meaningful responsibilities.
