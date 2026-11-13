# API and ownership

## Ownership is part of the contract

Choose parameters by what the function does with the value. Use `&str`, `&[T]`, and `&Path` for read-only access; `&mut T` for exclusive mutation; and owned values for storage, consumption, or transfer. If the function always clones an argument, consider accepting ownership and letting the caller choose whether to clone. Borrowed outputs should express a real relationship to an input, not force unrelated data to share one lifetime.

Distinguish copying data from sharing ownership. `Arc::clone` shares an allocation and updates a reference count; cloning a `Vec` or `String` copies its contents. `Arc<T>` does not make arbitrary `T` safe for concurrent use. Prefer simple ownership first; use shared ownership and interior mutability when the lifetime and access requirements justify them. Keep lock and runtime borrow scopes visible.

When a borrow conflict appears, locate the last use and the intended owner before changing the representation. A shorter borrow scope, disjoint field borrow, or separate read and write phase may express the algorithm directly. An arena or index can suit a graph whose references otherwise force pervasive shared ownership. Use `mem::take` or `replace` only when the temporary replacement is a valid state, including on early return or panic.

Small, cheap `Copy` values often belong by value. There is no universal byte threshold: layout, calling convention, and workload matter. Use `Cow` when the boundary can actually preserve a borrow or avoid a copy, rather than as a default parameter wrapper. An owned representation may simplify an API more than a web of lifetimes saves.

For the caller-control rule and examples, see [Rust API Guidelines: flexibility](https://rust-lang.github.io/api-guidelines/flexibility.html).

## Model the current domain

Use an enum when alternatives have different payloads or transitions; a tag plus several optional fields can admit impossible states. Use a newtype when it prevents a plausible mix-up or preserves a checked invariant. Keep invariant-bearing fields private and construct the valid value at the boundary. Plain values and public fields remain appropriate where every representable value is valid and direct access is the intended contract.

Check every construction and mutation path for a validated type. A fallible constructor is ineffective if `From<String>`, derived deserialization, or mutable access to the inner value bypasses it. Use `TryFrom` or `FromStr` for fallible conversions; `From` represents an infallible conversion. Serialization adapters should call the same validation boundary when the wire representation is weaker than the domain type.

Use exhaustive matches on owned domain enums where a new variant should force callers to reconsider behavior. Public enum extensibility is a compatibility decision. Typestate is useful when callers benefit from compile-time sequencing; keep runtime state when it expresses the actual lifecycle more clearly. Neither newtypes nor typestate are quotas.

## Choose abstraction by its consumer

Concrete types and enums often suffice for known alternatives. Generics support caller-selected implementations and monomorphization; `dyn Trait` supports runtime polymorphism and can also reduce code size or compile time. Choose the tradeoff at the relevant boundary. Dynamic dispatch is not limited to heterogeneous collections, and a trait object can be borrowed without a `Box`.

Consider the type a caller must store, not just how convenient construction looks. A service returning `Client<Transport<Pool<Backend>>>` can force implementation choices and bounds throughout consumer code. Keep generic parameters that give callers useful control; hide implementation-only nesting behind a concrete handle or a deliberate erased boundary. Generic containers and inferred iterator chains have different needs from long-lived service types. Microsoft explains this distinction in [public abstractions](https://github.com/microsoft/rust-guidelines/blob/9585e288d21d2da994a0550c926a09b62d79f8bd/src/guidelines/libs/ux/M-SIMPLE-ABSTRACTIONS.md).

Expose operations rather than forcing callers to coordinate an internal `Arc<Mutex<State>>`. Use an ownership wrapper in a public signature when sharing itself is the contract. Make a service's clone semantics clear: cloning a handle normally shares the service, while making an independent copy is a different operation.

Make essential operations discoverable on the concrete type; use traits for interoperability and real abstraction requirements. Prefer existing traits such as `Read`, `Write`, `AsRef`, `From`, and `TryFrom` when their semantics fit. A free function or module is sufficient for computation with no meaningful receiver. Prefer functions, generics, and ordinary types before introducing a macro; a macro should remove meaningful repetition while leaving its generated API understandable.

Keep the public surface deliberate. Adding a trait bound, changing an error type, removing a trait implementation, or exposing a dependency type can affect downstream callers even when local code compiles. Consult the [Rust API checklist](https://rust-lang.github.io/api-guidelines/checklist.html) for the public boundary being changed. Preserve existing contracts unless their migration is in scope.

Public dependency types couple consumers to compatible versions of that dependency. Prefer standard types when they express the contract equally well, but preserve useful ecosystem interoperability rather than wrapping everything. Choose re-exports and feature-gated adapters deliberately. Likewise, a private field change can alter public auto traits such as `Send` or `Sync`; inspect downstream usage before treating it as internal-only.

Keep one intentional public route to an item; keep implementation modules private when a facade re-exports their contents. Preserve existing paths when compatibility requires them. Implement useful standard traits, including `Debug`, according to the type's semantics, and redact secrets from diagnostic representations.

## State and documentation belong at the right boundary

Give correctness-critical shared state an explicit owner. A library `static` is not necessarily a process-wide singleton: multiple versions of a crate can coexist with separate statics. This matters for registries, counters, and initialization whose consistency is part of the contract. Immutable tables or independent performance caches are different cases. See [Microsoft's static-state guidance](https://github.com/microsoft/rust-guidelines/blob/9585e288d21d2da994a0550c926a09b62d79f8bd/src/guidelines/libs/resilience/M-AVOID-STATICS.md).

Keep documentation about behavior, ownership, failure, and safety. Executable examples should demonstrate normal use. Explain a non-obvious invariant where it matters instead of narrating the design process. See [Microsoft's AI guidance](https://microsoft.github.io/rust-guidelines/guidelines/ai/) for common agent-generated API and documentation problems.
