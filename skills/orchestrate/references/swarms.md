# Swarm patterns

Use a swarm when distinct coverage or independent alternatives justify the added work. Choose the smallest useful group. More agents do not compensate for unclear acceptance criteria, shared write conflicts, or a serial dependency.

## Choose the shape

Before spawning, state what completes the task, what artifact or answer is required, and which shape serves it:

- **Coverage:** partition by component, hypothesis, platform, or review concern. Record the required slices and give each an owner. Completion requires evidence for every required slice, including slices the primary agent handles.
- **Race:** give independent workers the same question and acceptance criteria. Declare the selection rule first: first acceptable result, rank all results, or choose the best against named criteria. Speed alone does not make a result acceptable.
- **Exploration:** assign distinct approaches to an unresolved design or implementation decision. Compare them against the same consumer requirements and constraints. Keep prototypes isolated. Combine useful parts only after checking that their assumptions and interfaces agree.

Mix shapes only when each arm has a clear purpose. For example, race two hypotheses within one coverage slice while other workers inspect separate components. Keep unfilled required coverage visible even if another arm succeeds.

## Brief and evidence

Each brief names its slice or alternative, allowed writes, acceptance criteria, verification method, and report format. For a race, withhold sibling conclusions until independent results arrive. For dependent work, relay the actual upstream contract and evidence before the next worker starts.

For verification, identify the exact artifact under review: commit SHA, diff plus base, build, or captured output. Shared uncommitted files can change while a worker reads them; hold the relevant writes or provide an isolated snapshot when stable evidence matters. Measurement briefs also name the method and conditions, using the existing performance guidance when needed. Evidence for a previous revision does not validate changed behavior.

Ask workers to return `PASS`, `ISSUES`, or `BLOCKED`, with their scope, artifact identity, checks actually run, supported findings, and gaps. `PASS` covers only that worker's assigned acceptance criteria. An unsupported conclusion or missing required check remains a gap. Request the missing evidence or rerun the bounded slice; do not silently count it as a pass.

## Collect and decide

Keep a compact record of slices, owners, states, and evidence pointers in the existing plan or task notes. Add durable records only when the work must survive handoff or session loss. Refill available slots as independent work becomes ready instead of waiting for the slowest member of an arbitrary batch.

For a first-acceptable race, verify the candidate against the declared criteria before selecting it. Stop remaining arms when their work no longer helps, and account for any writes before integration. For ranking or best-result selection, collect the required arms or explicitly qualify the result if an arm drops out.

Review the evidence, resolve contradictions with a focused check, and integrate the chosen changes. Agreement between agents is not proof. Verify the combined behavior where independently correct changes interact.

Return one consolidated answer: the result or selected approach and why, required coverage completed, material findings, and any missing slices, blocked checks, or stopped arms. A dropout may leave useful partial results; it cannot satisfy the original completion condition without replacement evidence or an explicit scope change.
