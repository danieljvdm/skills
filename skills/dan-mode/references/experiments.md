# Cheap experiments for a decision

Use an experiment when an unresolved empirical question changes what to build. State the decision and the observation that would favor one approach. Read existing evidence first; if it settles the question, proceed.

Use the lightest probe that exercises the relevant behavior. Prefer an existing app, test, or benchmark harness. A scratch script or small interactive prototype can help when no suitable path exists. Compare alternatives only when the choice needs a comparison, and stop once the evidence supports the decision. Keep scratch work separate from shipped code; avoid building configuration, abstractions, or a test framework for the experiment itself.

Report what happened, what it supports, and its limits. Integrate the chosen behavior through the repository's normal architecture and required checks. Performance acceptance still follows [measure-performance](../../measure-performance/SKILL.md).

When the same question recurs, improve the shared app or library harness through [feedback-loops](../../feedback-loops/SKILL.md), so agents and CI can reuse the operation.
