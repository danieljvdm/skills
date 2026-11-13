# Async and resources

Read this for tasks, shared state, cancellation, or shutdown. Use the repository's runtime; the examples of behavior below are Tokio-specific where named. Confirm version-sensitive contracts in the locked runtime's documentation.

## Choose the execution and ownership boundary

Async I/O lets a task wait without occupying a worker thread. It does not make synchronous I/O or expensive computation nonblocking. Use the runtime's async APIs or an appropriate blocking/CPU executor. Tokio's `spawn_blocking` suits bounded blocking work; sustained CPU parallelism may need a bounded pool, and persistent blocking loops may need dedicated threads. Its large default blocking pool is not a CPU concurrency budget. See [spawn_blocking](https://docs.rs/tokio/latest/tokio/task/fn.spawn_blocking.html).

A loop containing `.await` can still starve other tasks if every awaited operation is immediately ready. For a demonstrated fairness problem, chunk the work, use the runtime's cooperative mechanisms, or move CPU work off the executor. Choose chunk size against latency and throughput; a fixed yield interval is not a universal rule. See [Tokio cooperative scheduling](https://docs.rs/tokio/latest/tokio/task/coop/index.html).

Prefer `async fn` for ordinary async APIs. Use an explicit future-returning signature when callers need an expressible future bound, eager setup is intentional, or measurement justifies controlling future capture. Preserve promised `Send` behavior when changing values held across suspension. For `tokio::spawn`, `Send + 'static` means the task can move between threads and cannot borrow short-lived external data; it does not mean the task must live forever. Local runtimes can legitimately support non-`Send` tasks.

## Shared state has a synchronization contract

A short synchronous critical section may use `std::sync::Mutex` inside async code when contention is acceptable and the guard ends before suspension. Use a lexical scope or non-async method to make that boundary clear. An async mutex is appropriate when a lock genuinely must span an await; an owner task with messages may fit an I/O resource better. Choose from the access pattern, not simply because the surrounding function is async. See [Tokio shared state](https://tokio.rs/tokio/tutorial/shared-state).

Moving work outside a lock changes atomicity. A read, remote await, and later write may race with another writer. Recheck the relevant version, use an atomic transition, or give the operation one owner when the contract requires it. Releasing the guard fixes blocking but does not by itself make the update correct.

When producers can outpace consumers, account for both queued work and tasks in flight. A bounded channel helps only if another unbounded queue or spawn loop does not bypass it. Decide whether overload waits, rejects, or intentionally drops work; the choice belongs to the behavior being implemented.

## Cancellation can interrupt a protocol

Review each suspension where cancellation is possible: what has already happened, what state survives, and whether retrying repeats an effect. Dropping a future runs destructors for its owned state but does not undo I/O or complete an application protocol. A timeout on the waiter does not establish that a remote operation failed.

Tokio `select!` drops losing branch futures. `read` and `recv` can be cancellation-safe while `read_exact` and `write_all` can lose partial progress when restarted. Preserve progress outside a repeatedly recreated future, or drive the operation to a deliberate completion/abort boundary. Cancellation-safe primitives do not make a sequence of effects transactional. Check the actual operation against [Tokio's cancellation-safety reference](https://docs.rs/tokio/latest/tokio/macro.select.html#cancellation-safety).

Give spawned work an owner that observes completion and failure. Dropping a Tokio `JoinHandle` detaches the task; it does not cancel it. Distinguish the task's `JoinError` from the operation's own `Result`. Started `spawn_blocking` work cannot be stopped by aborting its handle, so cancellation may need cooperation from the work itself. See [JoinHandle](https://docs.rs/tokio/latest/tokio/task/struct.JoinHandle.html) and the blocking-task documentation above.

When graceful shutdown is required, stop accepting new work, signal the owned tasks, and wait for the chosen drain or stop policy to complete. Reuse existing task tracking and cancellation facilities. Put asynchronous cleanup on an explicit shutdown path rather than assuming a destructor can perform it. [Tokio's shutdown guide](https://tokio.rs/tokio/topics/shutdown) describes the lifecycle.
