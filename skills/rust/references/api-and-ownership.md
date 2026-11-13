# API and ownership

## Ownership is part of the contract

Choose parameters by what the function does with the value. Use `&str`, `&[T]`, and `&Path` for read-only access; `&mut T` for exclusive mutation; and owned values for storage, consumption, or transfer. If the function always clones an argument, consider accepting ownership and letting the caller choose whether to clone. Borrowed outputs should express a real relationship to an input, not force unrelated data to share one lifetime.

Distinguish copying data from sharing ownership. `Arc::clone` shares an allocation and updates a reference count; cloning a `Vec` or `String` copies its contents. `Arc<T>` does not make arbitrary `T` safe for concurrent use. Prefer simple ownership first; use shared ownership and interior mutability when the lifetime and access requirements justify them. Keep lock and runtime borrow scopes visible.

Small, cheap `Copy` values often belong by value. There is no universal byte threshold: layout, calling convention, and workload matter. Use `Cow` when the boundary can actually preserve a borrow or avoid a copy, rather than as a default parameter wrapper. An owned representation may simplify an API more than a web of lifetimes saves.

For the caller-control rule and examples, see [Rust API Guidelines: flexibility](https://rust-lang.github.io/api-guidelines/flexibility.html).

## Model the current domain

Use an enum when alternatives have different payloads or transitions; a tag plus several optional fields can admit impossible states. Use a newtype when it prevents a plausible mix-up or preserves a checked invariant. Keep invariant-bearing fields private and construct the valid value at the boundary. Plain values and public fields remain appropriate where every representable value is valid and direct access is the intended contract.

Use exhaustive matches on owned domain enums where a new variant should force callers to reconsider behavior. Public enum extensibility is a compatibility decision. Typestate is useful when callers benefit from compile-time sequencing; keep runtime state when it expresses the actual lifecycle more clearly. Neither newtypes nor typestate are quotas.

## Choose abstraction by its consumer

Concrete types and enums often suffice for known alternatives. Generics support caller-selected implementations and specialization; `dyn Trait` supports runtime polymorphism and can also reduce monomorphization, code size, or compile time. Choose the tradeoff at the relevant boundary. Dynamic dispatch is not limited to heterogeneous collections, and a trait object can be borrowed without a `Box`.

Keep the public surface deliberate. Adding a trait bound, changing an error type, removing a trait implementation, or exposing a dependency type can affect downstream callers even when local code compiles. Consult the [Rust API checklist](https://rust-lang.github.io/api-guidelines/checklist.html) for the public boundary being changed. Preserve existing contracts unless their migration is in scope.

## Errors preserve useful distinctions

Use `Result` for failures the caller is expected to handle and `Option` for absence. Preserve causes and distinguish failures when consumers need different recovery or reporting. Follow the crate's existing error conventions: a typed library error and an application-level contextual report are useful defaults, not a reason to add `thiserror` or `anyhow` to every crate.

A panic is a contract decision. Check `unwrap` and `expect` against reachable inputs and established invariants; replace them on recoverable failure paths. A locally proven invariant can justify `expect`, and tests may use it for clear failures. Do not replace every invariant check with a speculative error branch. Document public panic conditions when they are part of the API.

Keep documentation about behavior, ownership, failure, and safety. Executable examples should demonstrate normal use. Explain a non-obvious invariant where it matters instead of narrating the design process. See [Microsoft's AI guidance](https://microsoft.github.io/rust-guidelines/guidelines/ai/) for common agent-generated API and documentation problems.
