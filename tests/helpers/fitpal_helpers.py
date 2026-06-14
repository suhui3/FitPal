import logging

logger = logging.getLogger(__name__)


def log_result(test_id, status, detail=""):
    msg = f"[{test_id}] {status}"
    if detail:
        msg += f" | {detail}"
    if status == "PASS":
        logger.info(msg)
    else:
        logger.error(msg)
