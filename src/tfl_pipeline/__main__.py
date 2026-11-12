import logging

from tfl_pipeline.pipeline import run_ingestion

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
    force=True,
)

run_ingestion()