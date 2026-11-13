# Rust tooling

## Establish the build being checked

Use repository task entrypoints when available. Otherwise select the affected package with `-p`, target, and supported feature combination before running Cargo. Read `rust-toolchain.toml`, `rust-version`, workspace settings, and CI for the supported configuration. A newer local compiler passing is not evidence that the MSRV passes.

Cargo features are unified across dependency edges. Verify changed feature behavior in the supported configurations; `--all-features` can hide a missing feature gate or combine incompatible backends. Use `--no-default-features` only for configurations the crate supports. `cargo tree -e features -i <dependency>` explains who enabled a feature. See the [Cargo features reference](https://doc.rust-lang.org/cargo/reference/features.html).

Design optional features to add capability without disabling existing behavior. Feature unification means another dependent can enable a feature even when one edge disables defaults. Keep platform, runtime, and `no_std` support explicit. Resolve versions and syntax against the project's toolchain rather than upgrading the edition, MSRV, or dependency graph as a side effect of a code change.

For setup work, start with the smallest useful crate structure. Use workspace inheritance where members genuinely share policy, and keep Cargo's resolver and feature behavior explicit. Split crates for a real dependency, compilation, reuse, or ownership boundary; a prescribed folder tree or one crate per module is not the objective.

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

For a public API change, verify from a consumer's perspective when that exposes a real uncertainty: imports, trait bounds, feature gates, or an executable example. A library's own tests can accidentally rely on private visibility or dev-dependency features. Choose an existing integration test, doctest, or small temporary consumer as appropriate; this is not a requirement to add a new permanent harness.
