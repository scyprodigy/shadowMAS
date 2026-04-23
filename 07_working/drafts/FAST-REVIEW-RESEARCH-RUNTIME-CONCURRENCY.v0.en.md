# FAST-REVIEW-RESEARCH-RUNTIME-CONCURRENCY.v0.en.md

> Status: working draft / external research memo
> Nature: human-readable external research reference, not shadowMAS canonical truth, not packet law, not runtime policy.
> Scope: preserved as draft input for possible future runtime-concurrency formalization work.

Scope: concurrency and race-condition patterns relevant to a file-first,
local-first, multi-agent system. External research only. No product assumptions.
Evidence first; recommendation separated at the end.

---

## 0. Terms (short)

- Race condition: outcome depends on interleaving of concurrent actors.
- Lost update: two reads + two writes, second write overwrites first silently.
- TOCTOU: time-of-check to time-of-use gap between inspecting state and acting on it.
- Optimistic concurrency: allow concurrent work, detect conflict at commit, reject losers.
- Pessimistic concurrency: prevent conflict by acquiring lock before work.
- Idempotent operation: repeating it has the same net effect as running it once.
- Fencing token: monotonic sequence number presented to the resource on each write; resource rejects stale tokens.
- WAL (write-ahead log): append changes to a durable log before mutating main state; replay on recovery.

---

## 1. Evidence — concurrency strategies

### 1.1 Optimistic locking

Fowler's *Optimistic Offline Lock* pattern: attach a version (or ETag/row-checksum)
to each record. On commit, verify the version is unchanged; if so, write and
increment the version. If changed, reject the write — the loser retries or merges.
Assumes conflict is rare and re-work cost is bounded. Uses version counters
rather than wall-clock timestamps (clock skew is unreliable).
<https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html>
<http://thierryroussel.free.fr/java/books/martinfowler/www.martinfowler.com/isa/optimistic.html>

HTTP realization: ETag + `If-Match` header; server returns 412 Precondition Failed
on mismatch. Standard pattern for RESTful systems; stateless and cheap.
<https://fideloper.com/etags-and-optimistic-concurrency-control>

Hardware/algorithmic realization: compare-and-swap (CAS). Atomic read-verify-write;
loser retries. CAS has a known weakness (ABA) solved by adding a version counter
to the compared value.
<https://en.wikipedia.org/wiki/Compare-and-swap>
<https://www.baeldung.com/cs/aba-concurrency>

Cloud object-store realization: S3 conditional writes (`If-Match`, `If-None-Match`)
serialize commits to a manifest pointer via CAS; parallel writers race, losers
retry against the new version.
<https://aws.amazon.com/blogs/storage/building-multi-writer-applications-on-amazon-s3-using-native-controls/>
<https://www.shayon.dev/post/2025/277/an-mvcc-like-columnar-table-on-s3-with-constant-time-deletes/>

Fails well when:

- conflicts are rare,
- rework is cheap,
- the unit of contention is small and versioned.

Fails badly when:

- conflict rate is high — throughput collapses into retry storms,
- the transaction is long and rework cost is large (Fowler's explicit caution in *Pessimistic Offline Lock*),
- there is no clean merge strategy for conflicting edits.

### 1.2 Pessimistic locking

Fowler's *Pessimistic Offline Lock*: acquire the lock before touching the data.
Justified when conflict is likely or when re-doing the work is expensive enough
that forcing a queue is cheaper than forcing retries.
<https://martinfowler.com/eaaCatalog/pessimisticOfflineLock.html>

Known operational costs:

- reduced concurrency,
- lock-table management,
- stale-lock recovery (holder crashed, who releases?),
- deadlock potential across multiple locks.

Fails well when: contention is genuinely high and rework is expensive.
Fails badly when: hold times are unbounded (crashed holder blocks everyone).

### 1.3 Coarse-grained locking

Fowler's *Coarse-Grained Lock*: one lock covers an aggregate (parent + children)
rather than one lock per entity. Trades concurrency for simplicity and correctness.
Especially relevant when the members of a group are semantically tied and partial
locking of the group is meaningless.
<https://martinfowler.com/eaaCatalog/coarseGrainedLock.html>

Evidence for preferring coarse over fine:

- fewer locks → less deadlock surface,
- simpler recovery semantics,
- simpler reasoning for reviewers.

Cost: reduced parallelism on unrelated members of the same aggregate.

### 1.4 Single-writer queue

LMAX/Disruptor line of work: if you serialize writes to a given data structure
through one writer thread, contention disappears and a very large class of
concurrency bugs is ruled out by construction. Multiple readers are fine;
only writes are serialized.
<https://martinfowler.com/articles/lmax.html>
<https://mechanical-sympathy.blogspot.com/2011/09/single-writer-principle.html>
<https://lmax-exchange.github.io/disruptor/disruptor.html>
<https://martinfowler.com/articles/mechanical-sympathy-principles.html>

Adjacent realization: SQLite WAL mode — many readers, exactly one writer at a time.
The simplicity of the single-writer invariant is a large part of why SQLite is
reliable across millions of deployments.
<https://sqlite.org/wal.html>

Single-writer is not distributed consensus; it is a discipline. It works because
the queue, not the locks, is the coordination primitive.

Fails well when:

- throughput on one writer is sufficient for the workload,
- the writer is cheap to restart,
- work items can be serialized and ordered.

Fails badly when:

- throughput must exceed what one writer can handle,
- the writer becomes a liveness single-point-of-failure without a restart story.

### 1.5 Comparison (compressed)

| Strategy | Correct-by-construction? | Concurrency | Complexity | Best fit |
|---|---|---|---|---|
| Optimistic + version | No, detects at commit | High | Low | Rare-conflict, small items, cheap retry |
| Pessimistic | Yes, if lock is sound | Low | Medium | Frequent-conflict, expensive rework |
| Coarse-grained | Yes, within aggregate | Low-Mid | Low | Aggregates that must move together |
| Single-writer queue | Yes, by serialization | Mid (one writer) | Lowest for correctness | Low-to-moderate throughput, strong ordering needs |

---

## 2. Evidence — file-based coordination primitives

### 2.1 Lockfiles

Two reliable POSIX idioms:

- `open(..., O_CREAT | O_EXCL)` — atomic create-or-fail; the creator owns the lock.
  Broken historically on some NFS versions; local filesystems are fine.
- `mkdir(path)` — also atomic create-or-fail at the kernel level; widely recommended
  for shell-level mutual exclusion.
- `flock(fd, LOCK_EX)` — advisory lock on an open file descriptor; released on close.
  Advisory means cooperating processes only; the OS will not enforce it on non-cooperators.

Sources:
<https://mywiki.wooledge.org/BashFAQ/045>
<https://man7.org/linux/man-pages/man2/flock.2.html>

Known failure modes:

- stale lockfile after a crash — no one to clean it up; needs PID probe or TTL,
- advisory-lock bypass — any uncooperative process can ignore it,
- NFS semantics differ from local FS; cross-host locking via plain lockfiles is unsafe,
- delete-then-recreate race between check-name and check-inode (TOCTOU on lockfile replacement).

### 2.2 Leases

A lease is a lock with a TTL. The holder must renew; if it fails to renew, the
lease expires and another actor may acquire it. Solves the crashed-holder problem
that plagues plain locks.
<https://medium.com/nerd-for-tech/leases-fences-distributed-design-patterns-c1983eccc9b1>
<https://etcd.io/docs/v3.5/learning/why/>

Critical caveat (Kleppmann): a lease alone is not safe if the previous holder
is only paused (GC, swap, scheduler delay) rather than dead. The paused process
may wake up and write after the lease expired. Fix: fencing tokens.
<https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html>

### 2.3 Fencing tokens

The lock service issues a strictly increasing integer on each acquisition.
The protected resource persists the largest token it has seen and rejects
any write carrying a smaller token. This pushes the correctness check to the
resource, which is the only actor that can actually enforce it.
<https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html>
<https://hazelcast.com/blog/long-live-distributed-locks/>

Chubby calls this the "sequencer"; etcd uses the lease ID + revision number;
DynamoDB's lock client generates monotonic tokens. All three converge on the
same idea.

### 2.4 Atomic rename / replace

POSIX `rename(old, new)` replaces `new` atomically with respect to concurrent
readers within the same filesystem — readers see either the old file or the
new file, never a missing or half-written file.
<https://man7.org/linux/man-pages/man2/rename.2.html>

Canonical atomic-write recipe (widely used, e.g. Python `atomicwrites`, npm `write-file-atomic`):

1. Write content to a temp file in the *same* directory as the target.
2. `fsync` the temp file.
3. `rename` temp onto the target.
4. `fsync` the containing directory (so the rename is durable, not just visible).

Sources:
<https://python-atomicwrites.readthedocs.io/>
<https://github.com/untitaker/python-atomicwrites>
<https://github.com/npm/write-file-atomic/issues/64>
<https://zetcode.com/python/os-fsync/>

Caveats worth naming:

- "Atomic on crash" is weaker than "atomic with respect to concurrent readers".
  Several mainstream Linux filesystems can leave a rename in an unexpected state
  across a crash, depending on mount options and fs.
  <https://github.com/remzi-arpacidusseau/ostep-code/issues/10>
- Cross-filesystem rename is not atomic (it falls back to copy+unlink).
- `fsync` on a file does not durably commit the rename itself — you must also
  `fsync` the directory.
- `O_EXCL` on NFS has historical holes; a link/unlink idiom is the NFS-safe fallback.
  <https://www.php.net/manual/en/function.flock.php> (NFS-lock discussion is also applicable.)
- Hardware write-caches can still reorder; `fsync` guarantees are filesystem-dependent.
  <https://lwn.net/Articles/789600/>

### 2.5 Staged commit + commit marker

Write the full new state to a staging location first. Only once all staged
artifacts exist and are `fsync`ed, flip a single commit marker (one small file
or a rename of a pointer) to publish them. Readers only look at what the marker
points to. This is the same idea as SQLite rollback-journal commits, Parquet
manifest pointers, and the "temp-then-rename" atomic-write pattern generalized
to multiple files: one small atomic operation gates the visibility of many larger
ones.

Evidence for the generalization: Parquet/S3 manifest CAS flip used by columnar
table formats (Iceberg-style) — the manifest pointer is the commit marker; all
data files are staged first.
<https://www.shayon.dev/post/2025/277/an-mvcc-like-columnar-table-on-s3-with-constant-time-deletes/>

### 2.6 Append-only operation log

A single append-only log is, in effect, a single-writer primitive with built-in
history. Each operation is written to the tail of the log before any derived
state changes; derived state can always be rebuilt by replaying the log.
This is the SQLite / PostgreSQL / Kafka / Raft-log family.
<https://sqlite.org/wal.html>
<https://www.architecture-weekly.com/p/the-write-ahead-log-a-foundation>

Properties worth noting:

- sequential append on the same file is the single cheapest durable write on
  modern storage,
- replay + checkpoint gives crash consistency without a custom rollback protocol,
- ordering falls out for free: the log position is a natural sequence number
  (effectively a fencing token),
- a second process can consume the log as input instead of polling mutable state.

---

## 3. Evidence — cross-file consistency

POSIX filesystems do not provide atomic commits across multiple files. The only
atomic operations are single-file rename/replace and single-file writes within
a block. Anything that must update N files together requires a strategy.

Real-world strategies:

- **Collapse to one file.** If the unit of truth fits in one file, the atomic-rename
  recipe is sufficient and there is no cross-file problem. This is the SQLite
  philosophy.
- **Commit marker.** Stage N files, then atomically flip one marker (§2.5).
  Readers are gated on the marker. Partial staging is invisible.
- **Append-only log as truth.** Files on disk are a materialized view; the log
  is the source of truth. Partial materialization is recoverable by replay.
- **Saga with compensations.** When each step must commit independently and no
  global commit exists, each step has a matching compensating action that
  semantically undoes it. The saga is the coordinator; failures run the
  compensations in reverse. Originates in Garcia-Molina & Salem, 1987; still
  the industry-standard answer for long-lived multi-step workflows where a
  single transaction is not available.
  <https://dl.acm.org/doi/10.1145/38713.38742>
  <https://dev.to/temporalio/paper-summary-sagas-4bb6>

Rollback vs compensation:

- Rollback = database-level undo; requires a transactional container. Unavailable
  across arbitrary files.
- Compensation = application-level semantic undo; each step defines its own
  inverse. Weaker than rollback (the world may have observed the intermediate
  state), but always available.

Partial-success handling requires that every step be either retriable (idempotent)
or compensatable. If neither holds, the system has no recovery story for that step.

---

## 4. Evidence — idempotency and replay safety

### 4.1 Idempotency keys

Stripe's formulation: the client generates a unique key (V4 UUID recommended),
sends it with a mutating request (e.g. `Idempotency-Key` header). The server
stores the response associated with the key. A retry with the same key returns
the stored response instead of re-executing. Keys expire after a bounded window
(Stripe uses 24h).
<https://stripe.com/blog/idempotency>
<https://docs.stripe.com/api/idempotent_requests>
<https://docs.stripe.com/error-low-level>

Brandur's deeper write-up: break the operation into restartable atomic phases,
each of which is either idempotent or guarded by a check. The idempotency key
is the anchor across retries; the phases are the units of progress.
<https://brandur.org/idempotency-keys>

There is now a draft IETF RFC formalizing the `Idempotency-Key` HTTP header.
<https://httptoolkit.com/blog/idempotency-keys/>

### 4.2 Semantic equivalence and duplicate suppression

Idempotency requires a notion of "same operation". Two implementations:

- **Key-based:** same key → treated as the same request; response is replayed.
  Simple, but requires key generation and storage.
- **Content-based:** natural keys in the operation itself (e.g. `POST /orders`
  with a client-supplied `order_id`; upserts by primary key). No side-channel
  needed, but requires the domain to provide a natural key.

Key scoping matters — Stripe scopes keys to endpoint + API credential, so the
same key on a different endpoint is a new request. Without scoping, key reuse
causes wrong-response replay.

### 4.3 At-least-once + idempotent ≠ exactly-once

A widely repeated correction: there is no practical "exactly once" in a
distributed setting; what real systems build is at-least-once delivery plus
idempotent processing. The effect is the same as exactly-once, but the
implementation is honest about retries.
<https://jolynch.github.io/posts/distsys_shibboleths/>

### 4.4 Retry safety

Practical rules from Stripe's retry logic:

- Retry on network errors and 5xx.
- Do not retry on 4xx (except with a new key) — the client is wrong.
- Use exponential backoff with jitter — synchronized retries cause thundering herds.
- Honor server-provided retry signals (`Retry-After`, `stripe-should-retry`).
  <https://deepwiki.com/stripe/stripe-node/3.5-idempotency-and-retry-logic>

---

## 5. Recommendation (separated from evidence)

Scoped to a file-first, local-first, v0 multi-agent system.

### 5.1 Strong fits for a local file-first v0

- **Single-writer queue as the default coordination primitive** for any
  mutable shared state. One process, one actor, one thread owns the write
  path; everyone else produces jobs. Correctness by construction; debuggable;
  matches SQLite-WAL philosophy at system level.
- **Atomic-write-by-rename** (write-temp → fsync → rename → fsync-dir) for every
  single-file update of consequence. The most common file-system invariant
  you can rely on.
- **Append-only operation log** as the source of truth for agent actions;
  derived files are projections. Gives you replay, ordering, and a natural
  fencing token (log position) for free.
- **Optimistic concurrency with version numbers (CAS-style)** for low-contention
  metadata and registry-style records. Cheap, local, no lock service needed.
- **Coarse-grained locking on the aggregate** when multiple files must move
  together but a commit-marker is heavier than warranted — e.g. a per-task
  directory lock instead of per-file locks.
- **Idempotency keys on every mutating agent operation.** In an agent system
  with retries, tool crashes, and replayed runs, non-idempotent writes are
  a source of silent duplication. The cost is one extra field on the op record.

### 5.2 Justified only under evidence of contention or correctness need

- **Pessimistic file-locking with leases and fencing tokens**, if and only if
  (a) contention is measured, not assumed, and (b) the underlying store is
  single-host or a trusted local FS. The moment leases cross hosts or NFS,
  the correctness argument gets much harder and needs fencing enforced at the
  resource.
- **Staged commit + commit marker** across multiple files, when the unit of
  truth genuinely cannot collapse into one file.
- **Saga-style compensations**, only for multi-step workflows where a step
  has an observable external effect that cannot be rolled back.

### 5.3 Overkill for a local v0

- Distributed consensus (Raft, Paxos, etcd-style lease servers) — adds a
  component that must itself be operated and reasoned about; unnecessary
  when one host is enough.
- Redlock-style multi-node Redis locks — Kleppmann's critique stands;
  no fencing tokens means no safety under process pauses.
- Two-phase commit across files — operational nightmare, no fs supports it
  natively.
- CRDTs / vector clocks — designed for multi-writer geo-replication; a
  single-writer queue is a cheaper, stronger answer for this problem shape.
- Heavyweight workflow engines for compensations (Temporal, etc.) — the
  saga pattern is useful; a framework is not required to implement it.
- LMAX Disruptor itself — the *principle* transfers, the library is aimed
  at microsecond-latency trading and is not a fit for an agent system.

### 5.4 Failure modes to design against explicitly

- stale lockfiles after a crash (hence leases over plain lockfiles if locks are used),
- lost updates when two agents race on the same file without a version check,
- torn writes when a file is read mid-write (hence atomic-rename, not in-place rewrite),
- partial multi-file updates (hence commit marker or append-only log),
- duplicate work on retry (hence idempotency keys),
- silent clock drift (hence version counters, not timestamps, as lock/ETag values).

---

## 6. Explicit out-of-scope for v0

The following are real problems but should not be solved in a v0 local system:

- cross-host coordination (single-host assumption simplifies everything),
- multi-datacenter replication,
- exactly-once delivery guarantees (aim for at-least-once + idempotent),
- strict linearizability across independent files,
- distributed deadlock detection,
- Byzantine-fault tolerance,
- automatic schema migration of the operation log,
- compaction/GC of append-only logs at scale (bounded local size is fine for v0).

Deferring these is not a hack; it is the explicit choice that makes the v0
tractable. They re-enter scope only if and when the system is shown to need them.

---

## 7. Sources

Primary and canonical:

- Fowler, *Optimistic Offline Lock*, PoEAA. <https://martinfowler.com/eaaCatalog/optimisticOfflineLock.html>
- Fowler, *Pessimistic Offline Lock*, PoEAA. <https://martinfowler.com/eaaCatalog/pessimisticOfflineLock.html>
- Fowler, *Coarse-Grained Lock*, PoEAA. <https://martinfowler.com/eaaCatalog/coarseGrainedLock.html>
- Fowler & Rice, extended Optimistic Offline Lock article. <http://thierryroussel.free.fr/java/books/martinfowler/www.martinfowler.com/isa/optimistic.html>
- Fowler, *The LMAX Architecture*. <https://martinfowler.com/articles/lmax.html>
- Fowler, *Principles of Mechanical Sympathy*. <https://martinfowler.com/articles/mechanical-sympathy-principles.html>
- Thompson, *Single Writer Principle*. <https://mechanical-sympathy.blogspot.com/2011/09/single-writer-principle.html>
- LMAX Disruptor technical paper. <https://lmax-exchange.github.io/disruptor/disruptor.html>
- Kleppmann, *How to do distributed locking*. <https://martin.kleppmann.com/2016/02/08/how-to-do-distributed-locking.html>
- Garcia-Molina & Salem, *Sagas*, SIGMOD 1987. <https://dl.acm.org/doi/10.1145/38713.38742>
- SQLite, *Write-Ahead Logging*. <https://sqlite.org/wal.html>
- Stripe Engineering, *Designing robust and predictable APIs with idempotency*. <https://stripe.com/blog/idempotency>
- Stripe API reference, *Idempotent requests*. <https://docs.stripe.com/api/idempotent_requests>
- Stripe, *Advanced error handling* (retry + idempotency). <https://docs.stripe.com/error-low-level>
- Brandur, *Implementing Stripe-like Idempotency Keys*. <https://brandur.org/idempotency-keys>
- Lynch, *Distributed Systems Shibboleths* (idempotency & fencing). <https://jolynch.github.io/posts/distsys_shibboleths/>

File-system and primitives:

- `rename(2)` Linux man page. <https://man7.org/linux/man-pages/man2/rename.2.html>
- `flock(2)` Linux man page. <https://man7.org/linux/man-pages/man2/flock.2.html>
- BashFAQ 045, *How can I ensure that only one instance of a script is running*. <https://mywiki.wooledge.org/BashFAQ/045>
- python-atomicwrites docs. <https://python-atomicwrites.readthedocs.io/>
- npm `write-file-atomic` issue on rename durability. <https://github.com/npm/write-file-atomic/issues/64>
- LWN, *A way to do atomic writes*. <https://lwn.net/Articles/789600/>
- OSTEP errata, *rename atomicity and crashes*. <https://github.com/remzi-arpacidusseau/ostep-code/issues/10>

Leases, fencing, CAS:

- Hazelcast, *Distributed Locks are Dead; Long Live Distributed Locks*. <https://hazelcast.com/blog/long-live-distributed-locks/>
- etcd, *etcd versus other key-value stores* (lease + sequencer). <https://etcd.io/docs/v3.5/learning/why/>
- Wikipedia, *Compare-and-swap*. <https://en.wikipedia.org/wiki/Compare-and-swap>
- Baeldung, *ABA Problem in Concurrency*. <https://www.baeldung.com/cs/aba-concurrency>
- HTTP `If-Match` / ETag optimistic concurrency example. <https://fideloper.com/etags-and-optimistic-concurrency-control>
- AWS, *Multi-writer applications on S3 using conditional writes*. <https://aws.amazon.com/blogs/storage/building-multi-writer-applications-on-amazon-s3-using-native-controls/>
- Parquet-on-S3 manifest CAS pattern. <https://www.shayon.dev/post/2025/277/an-mvcc-like-columnar-table-on-s3-with-constant-time-deletes/>

Saga reference reading:

- Temporal.io summary of the 1987 Sagas paper. <https://dev.to/temporalio/paper-summary-sagas-4bb6>
