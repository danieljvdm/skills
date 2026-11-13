---
name: rust
description: Write, review, or refactor Rust code; resolve ownership and API design decisions; and select Cargo checks for the affected crate.
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

- Ownership, domain types, dispatch, public APIs, or error boundaries: [API and ownership](references/api-and-ownership.md).
- Cargo features, diagnostics, tests, profiling, or unsafe verification: [tooling](references/tooling.md).

Repository policy and the active testing, debugging, and performance workflows govern those activities. This skill supplies Rust-specific guidance; it does not require new tests, benchmarks, dependencies, or a replacement project layout for ordinary changes. Run the repository's required checks and the focused checks that establish the changed behavior. State which feature/target configuration was verified when that limits the result.

Use the [Rust API Guidelines](https://rust-lang.github.io/api-guidelines/) for idiomatic public contracts and [Microsoft's Pragmatic Rust Guidelines](https://microsoft.github.io/rust-guidelines/) for deeper design questions. Consult the relevant chapter rather than loading the complete books. Runtime-specific behavior, including Tokio cancellation and shutdown, follows the installed runtime's documentation.

Adaptation history and upstream terms are in [NOTICE](NOTICE) and [LICENSE](LICENSE).
