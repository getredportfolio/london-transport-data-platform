import logging

from tfl_pipeline.api import fetch_tube_lines, fetch_tube_status
from tfl_pipeline.database import insert_tube_status_snapshots, upsert_tube_lines
from tfl_pipeline.validation import validate_tube_lines, validate_tube_statuses

logger = logging.getLogger(__name__)


def run_ingestion():


    logger.info("Starting TfL ingestion")

    tube_lines_data = fetch_tube_lines()
    logger.info("Fetched %s tube lines", len(tube_lines_data))

    validated_lines = validate_tube_lines(tube_lines_data)
    logger.info("Validated %s tube lines", len(validated_lines))

    upsert_tube_lines(validated_lines)
    logger.info("Upserted %s tube lines", len(validated_lines))

    tube_line_status = fetch_tube_status()
    logger.info("Fetched status data for %s tube lines", len(tube_line_status))

    validated_status = validate_tube_statuses(tube_line_status)
    logger.info("Validated %s tube status snapshots", len(validated_status))

    insert_tube_status_snapshots(validated_status)
    logger.info("Inserted %s tube status snapshots", len(validated_status))

    logger.info("TfL ingestion complete")
