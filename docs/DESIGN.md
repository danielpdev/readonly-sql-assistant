# Design record

## Decision

An LLM may propose SQL, but a separate SQLite read-only URI, query-only connection and authorizer decide whether it can run. Table/function allowlists, operation limits and row caps constrain execution.

## Failure model

DELETE, DROP, ATTACH, PRAGMA, extension loading, metadata access and multiple statements are rejected. Expensive queries stop at an operation budget; results are capped.

## Tradeoffs

Only one synthetic orders table and a small function allowlist are supported. It is not a general SQL firewall for arbitrary databases. Real-model query correctness is demonstrated on one simple aggregate.

## Next change to defend in review

Add a reviewed semantic layer, tenant row filtering and more labeled question/SQL pairs.

## Reproducibility

`uv.lock` pins Python dependencies; the web lockfile pins the React build where present. Model-backed evaluations use a separately installed local service. Dataset examples are synthetic and intentionally small. Reported timing is a local observation, not a throughput SLA. Run `make test` after changing state transitions and `make eval` after changing decisions. Keep inference quality separate from deterministic invariant checks.
