"""QA bug tracker with severity, status, and release coverage."""
from datetime import datetime, timezone

STATUSES = ["Open", "In progress", "Fixed", "Verified"]
SEVERITIES = ["Low", "Medium", "High", "Critical"]


def init(db):
    db.executescript(
        """CREATE TABLE IF NOT EXISTS bugs(
            id INTEGER PRIMARY KEY,
            title TEXT NOT NULL,
            area TEXT NOT NULL,
            severity TEXT NOT NULL,
            status TEXT NOT NULL DEFAULT 'Open',
            steps TEXT NOT NULL,
            created_at TEXT NOT NULL
        )"""
    )
    if not db.execute("SELECT COUNT(*) FROM bugs").fetchone()[0]:
        now = datetime.now(timezone.utc).isoformat()
        db.executemany(
            "INSERT INTO bugs(title,area,severity,status,steps,created_at) VALUES(?,?,?,?,?,?)",
            [
                ("Checkout accepts empty name", "Checkout", "High", "Open", "Submit checkout with blank name.", now),
                ("Mobile menu overlaps logo", "Responsive UI", "Medium", "Open", "Open homepage at 390px width.", now),
                ("CSV import success message unclear", "CRM", "Low", "Verified", "Import duplicate row and read toast.", now),
            ],
        )


def bugs(db):
    return [dict(row) for row in db.execute("SELECT * FROM bugs ORDER BY id DESC")]


def handle(method, path, data, db):
    if method == "GET" and path == "/api/state":
        rows = bugs(db)
        return {"bugs": rows, "statuses": STATUSES, "severities": SEVERITIES}

    if method == "POST" and path == "/api/bugs":
        title = str(data.get("title", "")).strip()
        severity = str(data.get("severity", "Medium")).strip()
        if severity not in SEVERITIES:
            raise ValueError("Choose a listed severity.")
        if not 3 <= len(title) <= 160:
            raise ValueError("Enter a bug title.")
        db.execute(
            "INSERT INTO bugs(title,area,severity,status,steps,created_at) VALUES(?,?,?,?,?,?)",
            (title, str(data.get("area", "General")).strip()[:80] or "General", severity, "Open", str(data.get("steps", "")).strip()[:1000], datetime.now(timezone.utc).isoformat()),
        )
        return {"ok": True}

    if method == "POST" and path == "/api/status":
        status = str(data.get("status", "")).strip()
        if status not in STATUSES:
            raise ValueError("Choose a listed status.")
        row = db.execute("UPDATE bugs SET status=? WHERE id=?", (status, data.get("id")))
        if not row.rowcount:
            raise LookupError()
        return {"ok": True}

    raise LookupError()
