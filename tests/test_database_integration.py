from tfl_pipeline.database import get_connection, upsert_tube_lines
from tfl_pipeline.validation import TubeLine


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