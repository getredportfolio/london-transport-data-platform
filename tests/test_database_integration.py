from tfl_pipeline.database import (
    get_connection,
    insert_tube_status_snapshots,
    upsert_tube_lines,
)
from tfl_pipeline.validation import TubeLine, TubeStatusSnapshot


def test_upsert_tube_line_to_postgres():
    line = TubeLine(
        id="integration-test",
        name="Integration Test Line"
    )
    connection = get_connection()
    cursor = connection.cursor()

    try:
        upsert_tube_lines([line])
        cursor.execute(
            """
            SELECT line_id, line_name FROM tube_lines
            WHERE line_id = %s;
            """,
            ("integration-test",),
        )
        result = cursor.fetchone()
        assert result == ("integration-test", "Integration Test Line")

    finally:
        cursor.execute(
            "DELETE FROM tube_lines WHERE line_id = %s",
            ("integration-test",),
        )
        connection.commit()
        cursor.close()
        connection.close()

def test_insert_tube_status_snapshots_appends_history():
    line = TubeLine(
        id="integration-status-line",
        name="Integration Status Line",
    )

    snapshot = TubeStatusSnapshot(
        line_id="integration-status-line",
        status_severity=8,
        status_description="Integration Test Status",
    )

    connection = get_connection()
    cursor = connection.cursor()

    try:
        upsert_tube_lines([line])

        insert_tube_status_snapshots([snapshot])
        insert_tube_status_snapshots([snapshot])

        cursor.execute(
            """
            SELECT COUNT(*)
            FROM tube_status_snapshots
            WHERE line_id = %s
              AND status_description = %s;
            """,
            ("integration-status-line", "Integration Test Status"),
        )

        result = cursor.fetchone()

        assert result[0] == 2

    finally:
        cursor.execute(
            """
            DELETE FROM tube_status_snapshots
            WHERE line_id = %s;
            """,
            ("integration-status-line",),
        )

        cursor.execute(
            """
            DELETE FROM tube_lines
            WHERE line_id = %s;
            """,
            ("integration-status-line",),
        )

        connection.commit()
        cursor.close()
        connection.close()