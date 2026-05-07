import logging

def setup_logger(verbose=False):

    level = logging.DEBUG if verbose else logging.INFO

    logging.basicConfig(
        level=level,
        format="%(asctime)s [%(levelname)s] %(message)s"
    )

    return logging.getLogger("log_bundle_tool")