from pathlib import Path
import logging
import time


class FixedWidthFormatter(logging.Formatter):
    def format(self, record):
        # Create fixed-width "[filename:lineno]" block (22 chars)
        caller = f"[{record.filename}:{record.lineno}]"
        record.caller = f"{caller:<22}"  # pad to 22 characters
        return super().format(record)


class STSLogger:
    def __init__(self, base_path: Path, log_level: int = logging.DEBUG):
        # intit logging
        self.base_path = base_path
        runsPath = self.base_path / "logs" / "runs"
        runNumber = str(len(list(runsPath.glob("*"))))
        runPath = runsPath / runNumber
        runPath.mkdir()

        self.log_level = log_level
        self.logs_path = runPath / "run.log"

        # formatter = logging.Formatter(
        #     "%(asctime)s,%(msecs)03d %(levelname)-8s [%(filename)s:%(lineno)d]-25s %(message)s"
        # )

        formatter = FixedWidthFormatter(
            "%(asctime)s,%(msecs)03d %(levelname)-8s %(caller)s %(message)s"
        )
        self.stream_logger = logging.getLogger("Stream")
        stream_handler = logging.StreamHandler()
        stream_handler.setFormatter(formatter)
        self.stream_logger.setLevel(self.log_level)
        self.stream_logger.handlers = []
        self.stream_logger.addHandler(stream_handler)

        self.file_logger = logging.getLogger("File")
        self.file_logger.setLevel(self.log_level)
        log_file_handler = logging.FileHandler(self.logs_path)
        self.file_logger.handlers = []
        self.file_logger.addHandler(log_file_handler)

    def debug(self, msg, *args, **kwargs):
        self.stream_logger.debug(msg, *args, **{**kwargs, "stacklevel": 2})
        self.file_logger.debug(msg, *args, **{**kwargs, "stacklevel": 2})

    def info(self, msg, *args, **kwargs):
        self.stream_logger.info(msg, *args, **{**kwargs, "stacklevel": 2})
        self.file_logger.info(msg, *args, **{**kwargs, "stacklevel": 2})

    def warning(self, msg, *args, **kwargs):
        self.stream_logger.warning(msg, *args, **{**kwargs, "stacklevel": 2})
        self.file_logger.warning(msg, *args, **{**kwargs, "stacklevel": 2})

    def error(self, msg, *args, **kwargs):
        self.stream_logger.error(msg, *args, **{**kwargs, "stacklevel": 2})
        self.file_logger.error(msg, *args, **{**kwargs, "stacklevel": 2})
