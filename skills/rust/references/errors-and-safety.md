# Errors and safety

## Design errors around caller decisions

Use `Result` for expected failure and `Option` for absence. Preserve the cause when translating an error, and add context at the boundary that knows what operation failed. Replacing an error with its formatted string loses structured information; discarding it with `.ok()` or a default is appropriate only when that is the intended contract.

Choose error granularity by the unit of fallibility. A parser and a downloader need not return a crate-wide enum containing every possible failure. A few related operations can share an error without requiring one type per function. Expose the distinctions callers can act on, such as missing data, invalid input, or a temporary failure; leave incidental backend details behind the boundary.

An enum is useful when matching its variants is part of the API. A struct with private representation and public queries can preserve flexibility when implementation failures change. Decide whether public enum variants should be exhaustive or extensible. Apollo favors typed library errors; Microsoft's [error design](https://github.com/microsoft/rust-guidelines/blob/9585e288d21d2da994a0550c926a09b62d79f8bd/src/guidelines/libs/ux/M-ERRORS-CANONICAL-STRUCTS.md) emphasizes stable structs. Use the existing contract and caller needs to choose, rather than imposing either shape or adding a backtrace to every error.

Follow the crate's reporting conventions. `thiserror` can implement typed errors and their source chains; `anyhow` or an equivalent report suits application boundaries that primarily present failures. Keep typed decisions where callers must recover. Return errors from libraries and emit telemetry where it is useful to the application; logging and propagating at every layer duplicates the same failure.

Use `?` for propagation, `map_err` for translation, and an explicit branch when recovery changes control flow. Use lazy fallbacks such as `ok_or_else` when constructing the error is expensive. Preserve simple eager values when they are already cheap.

## Panic is not a recoverable failure channel

Invalid external input normally belongs in a fallible parse or operation. A violated internal invariant can justify an assertion or `expect` whose message states the invariant. Make invalid states impossible when the type model can do so simply; avoid inventing an error that callers cannot meaningfully handle just to eliminate a panic.

Do not depend on catching a panic for ordinary control flow: the application may use `panic = "abort"`. If a host deliberately isolates panicking work, identify which state may be partially changed and how it is discarded or restored before reuse. `catch_unwind` does not roll back mutations. Follow the host's failure policy instead of imposing Microsoft's application-restart preference on every panic. See its [panic-continuation rationale](https://github.com/microsoft/rust-guidelines/blob/9585e288d21d2da994a0550c926a09b62d79f8bd/src/guidelines/correctness/M-PANIC-CONTINUATION.md).

Make resource release and failure reporting separate when needed: an explicit `finish`, `flush`, or `close` can report failure; `Drop` cannot return a `Result`. Keep destructors safe during unwinding and avoid a second panic while unwinding. A debug-only assertion cannot be the only enforcement of an unsafe precondition.

## Unsafe preserves a safe caller's guarantees

Use safe operations or an established abstraction where they express the requirement. Introducing unsafe for speed needs a measured reason. An unsafe cast or `Send` implementation is not a shortcut around an unresolved ownership problem.

Document caller obligations on an unsafe API and the proof at each unsafe operation. Account for allocation validity, bounds, alignment, initialization, aliasing, lifetimes, and synchronization as applicable. Checking nullness or adding `repr(C)` does not establish the remaining conditions. A safe wrapper must remain sound for every permitted safe caller, including callbacks that panic and safe trait implementations that behave unexpectedly.

For FFI, specify pointer ownership, who frees each allocation, callback lifetimes, thread affinity, and the permitted unwind behavior. Keep conversion and ABI details at the boundary; express core behavior in normal Rust types. A focused module can provide that separation without a compulsory new crate.

Use the [Rust Reference on undefined behavior](https://doc.rust-lang.org/reference/behavior-considered-undefined.html) for the affected invariant. When the changed behavior can be exercised, [Miri](https://github.com/rust-lang/miri) can detect classes of undefined behavior on executed paths; passing it does not prove soundness, and unsupported FFI may need other evidence. Preserve the repository's unsafe and verification policies.
