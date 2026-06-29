import logging
import sys

def setup_logging():
    """Configure standard logging for the application."""
    log_format = (
        "%(asctime)s.%(msecs)03d - [%(levelname)s] - %(name)s - "
        "(%(filename)s:%(lineno)d) - %(message)s"
    )
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S",
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )

    # Disable overly verbose third-party loggers
    logging.getLogger("uvicorn.access").setLevel(logging.WARNING)
    logging.getLogger("sqlalchemy.engine").setLevel(logging.WARNING)

    return logging.getLogger("sentrix")
