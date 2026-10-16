---
name: debugging
description: Diagnose bugs, regressions, and unexplained behavior, then implement and verify an authorized fix.
---

# Debugging

Establish the expected and observed behavior, the affected environment, and the revision or configuration involved. Reuse a reliable existing reproduction or trace. Create the smallest useful reproduction when the failure remains unclear.

Follow the failing path to the first point where behavior diverges. State the leading explanation and the observation that would distinguish it from a plausible alternative. Run the cheapest useful probe, then update the explanation. A tool or access failure is evidence about that boundary, not proof that the application is broken.

Search code, history, logs, or runtime traces according to the question each can answer. Delegate independent hypotheses only when doing so helps the investigation. When repeated fixes fail in the same way, name the assumption they share and choose an observation that could disprove it before adding another patch. Reuse the application's diagnostic and verification paths. If the same question needs repeated custom probes, improve a shared harness through `feedback-loops`.

Fix the cause within the requested scope. If the practical answer is a mitigation, explain what it relieves and what remains. Avoid hiding a defect behind broader retries, fallbacks, or exception handling.

Verify the changed behavior at the affected boundary and run the applicable repository checks. Follow repository policy for regression tests. When changing a critical user path or making a performance claim, also use the installed `measure-performance` workflow.

Report the cause, supporting evidence, change, and result in plain language. State uncertainty and the next discriminating check when the cause is unresolved. Keep detailed traces and commands in a small supporting artifact when useful.
