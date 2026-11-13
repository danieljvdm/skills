# Rust tooling

## Establish the build being checked

Use repository task entrypoints when available. Otherwise select the affected package with `-p`, target, and supported feature combination before running Cargo. Read `rust-toolchain.toml`, `rust-version`, workspace settings, and CI for the supported configuration. A newer local compiler passing is not evidence that the MSRV passes.

Cargo features are unified across dependency edges. Verify changed feature behavior in the supported configurations; `--all-features` can hide a missing feature gate or combine incompatible backends. Use `--no-default-features` only for configurations the crate supports. `cargo tree -e features -i <dependency>` explains who enabled a feature. See the [Cargo features reference](https://doc.rust-lang.org/cargo/reference/features.html).

## Keep the feedback loop focused

The commands below are options, not a checklist to run on every edit. Apply the repository's lockfile and feature policy to the selected command.

| Question | Useful check |
| --- | --- |
| Does the affected crate typecheck? | `cargo check -p <package>` with the relevant targets/features |
| Does the change follow formatting and lint policy? | Repository format/lint tasks; otherwise `cargo fmt --all -- --check` and scoped `cargo clippy` |
| Does the changed behavior work? | The existing focused test or real executable workflow |
| Do public examples still work? | `cargo test -p <library-package> --doc` with the supported features |
| Why did dependency features change? | `cargo tree -e features -i <dependency>` |

Interpret Clippy findings in context and preserve the configured lint policy. Use narrow, explained suppressions for intentional code; use `#[expect(...)]` when the supported compiler permits it and the lint is expected to fire. Fix the design when a warning reveals a real problem. `cargo check` does not execute tests or prove runtime behavior.

Reuse [nextest](https://nexte.st/docs/running/) when the repository uses it for test selection, isolation, and CI reporting. Keep documentation tests covered explicitly rather than inferring they ran from the unit/integration runner's success. Reuse valid results while the relevant code and configuration are unchanged.

When tests are warranted under the existing testing policy, assert the observable contract. Several assertions can describe one behavior. [Insta](https://insta.rs/) is useful for stable structured output with meaningful diffs; review changes against the intended result before accepting snapshots. [cargo-mutants](https://mutants.rs/) can investigate a concrete gap in test effectiveness. Neither tool is an automatic dependency or mandatory gate.

## Performance and unsafe code

When performance work is in scope, use the existing measurement workflow and representative optimized builds. Check the benchmark profile, features, workload, and whether setup or I/O dominates before changing an allocation, dispatch, or iterator choice. `cargo bench` uses the bench profile; inspect overrides rather than blindly adding flags. [The Rust Performance Book](https://nnethercote.github.io/perf-book/profiling.html) covers profiling and symbol information, including samply on macOS and flamegraph on supported platforms.

Profile the work that limits the outcome. Clones, intermediate collections, generic code size, and allocations are hypotheses to investigate, not proof of a bottleneck. Keep a loop when it makes control flow clearer; an iterator chain is not intrinsically faster. Report only the improvement the comparison establishes.

Unsafe code needs the relevant validity, aliasing, lifetime, and synchronization invariants stated at its safe boundary and justified at each unsafe operation. Checking pointer nullness or adding `repr(C)` alone does not establish those invariants. Consult the [Rust Reference on undefined behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html). When changed unsafe behavior can be exercised, [Miri](https://github.com/rust-lang/miri) can detect classes of undefined behavior on executed paths; a passing run does not prove soundness, and unsupported FFI may need other evidence. Preserve repository unsafe policy and keep the unsafe surface small.
