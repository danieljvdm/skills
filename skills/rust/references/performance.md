# Rust performance decisions

Use the existing measurement workflow when performance work is in scope. Identify the actual limiting resource before changing a representation. Compare the same optimized profile, features, target, and representative workload; include enough symbol information to attribute the work. `cargo bench` uses the bench profile, which may have repository overrides. [The Rust Performance Book](https://nnethercote.github.io/perf-book/profiling.html) covers profiling setup, samply on macOS, flamegraph, and allocation profilers.

## Remove repeated work before changing machinery

Trace ownership and allocation through the hot operation. Look for repeated formatting, cloning large buffers, temporary collections, rehashing the same data, and building state that could have been reused. Count or profile these costs before treating their presence as a bottleneck. Iterator syntax and a smaller diff alone do not establish a speedup.

| Observed cost | Candidate change and tradeoff |
| --- | --- |
| An expensive fallback is built on the success path | Use the lazy `_else` combinator; keep simple constants eager. |
| A collection is allocated only to inspect or iterate it once | Consume the iterator directly when that preserves ownership and readability. |
| Each operation allocates a fresh output buffer | Reuse capacity through an existing buffer/`clear` path or an additional caller-controlled operation when needed. Retained peak capacity is a memory tradeoff. |
| A large enum variant inflates every stored value | Inspect layout and frequency; boxing the uncommon payload reduces inline size but adds allocation and indirection. |
| A large generic implementation is emitted for many types | Keep a small generic adapter and a shared concrete or erased implementation when specialization is not buying enough. |
| A shared lock or counter dominates | Partition ownership or batch work before trying a different primitive. Account for fairness and latency. |

Reserve capacity from a credible bound or observed workload, not an arbitrary large default. Avoid grow/shrink churn in a reusable buffer. `Box::new(large_value)` may still construct or move a large temporary through the stack; when stack pressure is the problem, use an appropriate heap-first construction path and verify it. Change a hasher only after considering attacker-controlled inputs and the required collision resistance.

Microsoft's [allocation reuse](https://github.com/microsoft/rust-guidelines/blob/9585e288d21d2da994a0550c926a09b62d79f8bd/src/guidelines/performance/M-MEM-REUSE.md) motivates caller control. Keep a convenient return-value API when it meets the requirement; adding output parameters or arenas to every API would impose costs on callers without evidence.

## Account for async state and scheduling

Arguments and values retained across `.await` contribute to a future's state. A large future can increase per-task memory and movement costs before it performs useful work. If this is material, inspect `size_of_val(&future)`, shorten the lifetime of large temporaries, or move appropriate setup outside the async body. Boxing trades inline size for allocation and indirection. Moving setup outside the future changes when it executes, so preserve observable timing and cancellation behavior. See [future size](https://github.com/microsoft/rust-guidelines/blob/9585e288d21d2da994a0550c926a09b62d79f8bd/src/guidelines/performance/M-ASYNC-STACK-SIZE.md).

For throughput, look at useful completed work per unit of CPU as well as wall time. Batching and independent partitions can amortize task scheduling, synchronization, and I/O costs, but larger batches can worsen tail latency. Avoid spinning or extra tasks merely to make an isolated microbenchmark look faster. Apply this only to the measured workload, rather than making all APIs batch-oriented. See [throughput tradeoffs](https://github.com/microsoft/rust-guidelines/blob/9585e288d21d2da994a0550c926a09b62d79f8bd/src/guidelines/performance/M-THROUGHPUT.md).

Treat telemetry as part of the workload. Prefer useful structured events and appropriate aggregation over per-item formatting in a hot loop. Check enabled telemetry as well as disabled instrumentation when that matches production use. Preserve the signals needed to explain failures and performance; removing observability is not automatically an improvement.

Keep the change only when the observed benefit or another explicit requirement justifies its complexity. Report the supported result and its measurement limits.
