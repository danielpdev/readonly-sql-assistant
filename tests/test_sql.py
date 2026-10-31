import sqlite3
import pytest
from app.core import seed, run_sql


@pytest.fixture
def db(tmp_path):
    p = tmp_path / "a.sqlite"
    seed(p)
    return p


@pytest.mark.parametrize(
    "sql",
    [
        "DELETE FROM orders",
        "DROP TABLE orders",
        "ATTACH DATABASE ':memory:' AS other",
        "PRAGMA table_info(orders)",
        "SELECT load_extension('bad')",
        "SELECT * FROM sqlite_master",
        "SELECT 1; DELETE FROM orders",
    ],
)
def test_write_metadata_and_escape_blocked(db, sql):
    with pytest.raises(ValueError):
        run_sql(db, sql)
    with sqlite3.connect(db) as c:
        assert c.execute("SELECT count(*) FROM orders").fetchone()[0] == 4


def test_rows_and_budget(db):
    r = run_sql(db, "SELECT * FROM orders ORDER BY id", row_limit=2)
    assert len(r["rows"]) == 2 and r["truncated"]
    with pytest.raises(ValueError):
        run_sql(
            db,
            "SELECT SUM(a.amount_cents*b.amount_cents*c.amount_cents) FROM orders a, orders b, orders c",
            max_operations=1,
        )
