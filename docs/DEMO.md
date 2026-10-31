# Demo walkthrough

## Start

```bash
make setup
make demo
make test
make eval
```

## What to show

An LLM may propose SQL, but a separate SQLite read-only URI, query-only connection and authorizer decide whether it can run. Table/function allowlists, operation limits and row caps constrain execution.

## Failure case to discuss

DELETE, DROP, ATTACH, PRAGMA, extension loading, metadata access and multiple statements are rejected. Expensive queries stop at an operation budget; results are capped.

## Evidence

Open the JSON evaluation report alongside the implementation. Distinguish synthetic fixture outputs, synthetic trace timing, actual elapsed evaluation time, and local model inference. Do not present a tiny test set as a production benchmark.

## Closing tradeoff

Only one synthetic orders table and a small function allowlist are supported. It is not a general SQL firewall for arbitrary databases. Real-model query correctness is demonstrated on one simple aggregate.

The repository's `docs/demo.webm` or `docs/demo.mp4`, when present, records the demonstration. A terminal replay is also available for focused projects as `docs/demo.cast`.
