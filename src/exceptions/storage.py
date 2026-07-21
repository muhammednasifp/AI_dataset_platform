"""
Exceptions related to document collection.
"""
from src.exceptions.base import DatasetPlatformError

class StorageError(DatasetPlatformError):
    """
    Raised when a document cannot be collected
    from a source.
    """

    pass