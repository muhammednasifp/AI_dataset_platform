"""
Exceptions related to Chunking.
"""
from src.exceptions.base import DatasetPlatformError

class ChunkingError(DatasetPlatformError):
    """
    Raised when a document cannot be collected
    from a source.
    """

    pass