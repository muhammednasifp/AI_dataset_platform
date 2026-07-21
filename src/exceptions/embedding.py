"""
Exceptions related to document collection.
"""
from src.exceptions.base import DatasetPlatformError

class EmbeddingError(DatasetPlatformError):
    """
    Raised when a document cannot be collected
    from a source.
    """

    pass