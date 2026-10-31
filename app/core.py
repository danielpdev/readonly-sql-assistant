"""The read-only connection and authorizer enforce permissions independently of prompts."""

import sqlite3
import tempfile
import time
from pathlib import Path
from pydantic import BaseModel


class SQLPlan(BaseModel):
    sql: str


def seed(path):
    with sqlite3.connect(path) as c:
        c.execute(
            "CREATE TABLE IF NOT EXISTS orders (id INTEGER PRIMARY KEY, region TEXT, amount_cents INTEGER)"
        )
        if not c.execute("SELECT count(*) FROM orders").fetchone()[0]:
            c.executemany(
                "INSERT INTO orders VALUES (?,?,?)",
                [(1, "Spain", 12000), (2, "Romania", 8500), (3, "Spain", 7000), (4, "Romania", 15000)],
            )


def run_sql(path, sql, row_limit=20, timeout_seconds=0.2, max_operations=100000):
    if not 1 <= row_limit <= 1000:
        raise ValueError("row limit must be 1..1000")
    c = sqlite3.connect(Path(path).resolve().as_uri() + "?mode=ro", uri=True)
    c.execute("PRAGMA query_only=ON")
    allowed_functions = {"sum", "count", "avg", "min", "max", "round", "coalesce", "lower", "upper", "abs"}

    def authorize(action, arg1, arg2, db, source):
        if action == sqlite3.SQLITE_SELECT:
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_READ and db == "main" and arg1 == "orders":
            return sqlite3.SQLITE_OK
        if action == sqlite3.SQLITE_FUNCTION and arg2 in allowed_functions:
            return sqlite3.SQLITE_OK
        return sqlite3.SQLITE_DENY

    deadline = time.monotonic() + timeout_seconds
    operations = 0

    def progress():
        nonlocal operations
        operations += 100
        return int(time.monotonic() > deadline or operations > max_operations)

    c.set_authorizer(authorize)
    c.set_progress_handler(progress, 100)
    try:
        cursor = c.execute(sql)
        if cursor.description is None:
            raise ValueError("read query required")
        rows = cursor.fetchmany(row_limit + 1)
        return dict(
            columns=[d[0] for d in cursor.description],
            rows=[list(r) for r in rows[:row_limit]],
            truncated=len(rows) > row_limit,
        )
    except sqlite3.Error as exc:
        raise ValueError("Query blocked or invalid: " + str(exc)) from exc
    finally:
        c.close()


def answer(path, question, mode="fixture"):
    if mode == "fixture":
        mapping = {
            "total by region": "SELECT region, SUM(amount_cents) AS revenue_cents FROM orders GROUP BY region ORDER BY region",
            "order count": "SELECT COUNT(*) AS order_count FROM orders",
        }
        if question not in mapping:
            raise ValueError("Fixture questions: total by region; order count. Use local mode for a model.")
        sql = mapping[question]
    else:
        from app.local_model import generate

        prompt = (
            "Return a read-only SQLite SELECT for this synthetic schema: orders(id INTEGER, region TEXT, amount_cents INTEGER). Only this table is available. Question: "
            + question
        )
        sql = SQLPlan.model_validate_json(generate(prompt, schema=SQLPlan.model_json_schema())["text"]).sql
    return dict(sql=sql, result=run_sql(path, sql), mode=mode)


def demo(mode="fixture"):
    with tempfile.TemporaryDirectory() as d:
        path = Path(d) / "analytics.sqlite"
        seed(path)
        r = answer(path, "total by region", mode)
        try:
            run_sql(path, "DELETE FROM orders")
        except ValueError as exc:
            r["write_blocked"] = str(exc)
        return r


def evaluate(mode="fixture"):
    r = demo(mode)
    return dict(passed=bool(r["write_blocked"]), scenario=r)
