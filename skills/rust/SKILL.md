---
name: rust
description: Write, review, or refactor Rust code, including ownership, public APIs, errors, async lifecycles, unsafe boundaries, Cargo checks, and performance.
license: MIT
metadata:
  source: "https://github.com/apollographql/skills/tree/9dda1397730370aeb8df4ff8f2015c34c86b5003/skills/rust-best-practices"
  source_commit: "9dda1397730370aeb8df4ff8f2015c34c86b5003"
  source_skill: "rust-best-practices"
---

# Rust

Start with the affected crate's manifests, toolchain, features, nearby code, and repository commands. Preserve its minimum supported Rust version (MSRV), runtime, public contracts, and dependency policy. Resolve version-sensitive APIs against the locked dependency's source or versioned documentation; a compiler suggestion or latest documentation may exceed the supported toolchain.

Name the ownership and failure boundaries before changing types. Borrow when the caller retains the value; take ownership when the callee stores, consumes, or transfers it. A clone can be the right contract. Diagnose the lifetime or sharing requirement before adding clones, reference counting, locks, or broader lifetime bounds to satisfy the compiler.

Read only the reference needed for the decision:

- Ownership, domain types, dispatch, or public API compatibility: [API and ownership](references/api-and-ownership.md).
- Error contracts, panics, unsafe abstractions, or FFI: [errors and safety](references/errors-and-safety.md).
- Async tasks, shared state, cancellation, or shutdown: [async and resources](references/async-and-resources.md).
- Cargo features, diagnostics, test selection, or crate configuration: [tooling](references/tooling.md).
- Allocation, CPU, contention, future size, or an optimization claim: [performance](references/performance.md).

Repository policy and the active testing, debugging, and performance workflows govern those activities. This skill supplies Rust-specific guidance; it does not require new tests, benchmarks, dependencies, or a replacement project layout for ordinary changes. Run the repository's required checks and the focused checks that establish the changed behavior. State which feature/target configuration was verified when that limits the result.

The references distill Apollo's Rust practices, [Microsoft's Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/), and the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) into decisions for this stack. Use their linked chapters to resolve a deeper question, and the installed crate documentation for version-sensitive details. Upstream preferences about panic recovery, error representation, runtimes, allocators, or project layout are not blanket project requirements.
