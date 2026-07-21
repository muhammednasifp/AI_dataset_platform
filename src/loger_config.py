# Logger:
# Creates log messages.
# Example: logger.info("Dataset created")

# Handler:
# Decides where logs are written
# (console, file, cloud, etc.). 

# Formatter:
# Controls how log messages are displayed,
# including timestamps, levels, and module names.

# Logging Architecture:
# Logger → Handler → Formatter → Output

# Separating these responsibilities makes the
# logging system flexible and extensible.

import logging
import os
def setup_logging():
    # Root Logger
    #
    # The root logger is the top-level logger in Python's logging hierarchy.
    #
    # It stores the application's global logging configuration
    # (handlers, formatters, and log level).
    #
    # Every module logger created using:
    #
    #     logging.getLogger(__name__)
    #
    # automatically inherits this configuration.
    #
    # Configure the root logger once when the application starts.
    # Modules should only obtain their own logger, not configure logging.
    logger=logging.getLogger()

    # Set the minimum severity level for the application.
    # Messages below INFO (e.g., DEBUG) will be ignored.
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )
    # Formatter
    #
    # A formatter controls how log messages are displayed.
    #
    # Common fields:
    # %(asctime)s   -> Timestamp
    # %(levelname)s -> Log severity (INFO, ERROR, etc.)
    # %(name)s      -> Logger (module) name
    # %(message)s   -> User-defined log message
    #
    # A formatter is attached to handlers, allowing different
    # outputs (console, file) to have different formats.

    console_handler=logging.StreamHandler()
    # StreamHandler
    #
    # A StreamHandler writes log messages to a stream.
    #
    # By default, the stream is the console (stdout),
    # allowing developers to see logs while the application runs.

    console_handler.setFormatter(formatter)
    #Set Format
    os.makedirs("src/logs", exist_ok=True)
    file_handler=logging.FileHandler("src/logs/app.log")
    # FileHandler writes log messages to a file.
    #
    # The log file can be created automatically,
    # but its parent directory must already exist.
    #
    # Ensure the log directory exists before creating
    # the FileHandler.
    file_handler.setFormatter(formatter)

    logger.addHandler(console_handler)
    logger.addHandler(file_handler)
    # Logger owns one or more handlers.
    #
    # Handlers are attached using:
    #
    #logger.addHandler(handler)
    #
    # A logger decides which messages should be processed,
    # while handlers decide where those messages are written..
    # Logging Rule:
    #
    # Log meaningful application events,
    # not every function call or computation.
    #
    # Good:
    #   "Generated 245 embeddings."
    #
    # Bad:
    #   "Current vector = [0.23, ...]"



