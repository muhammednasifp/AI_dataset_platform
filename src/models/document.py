# -----------------------------------------------------------------------------
# Document
#
# Represents a single document within the AI dataset pipeline.
#
# A Document serves as the primary data model throughout the application,
# storing both the original content and any derived metadata generated during
# processing.
#
# Fields:
# - id       : Unique identifier for the document.
# - title    : Human-readable document title.
# - url      : Original source location of the document.
# - content  : Main textual content extracted from the source.
# - source   : Identifier of the data source (e.g., website, documentation).
# - metadata : Dictionary containing computed information such as word count,
#              quality score, and other enrichment results.
#
# Design Notes:
# - Acts as the central domain model shared across all pipeline stages.
# - Separates raw document data from computed metadata.
# - Uses a default empty dictionary for metadata to safely support
#   per-document enrichment.
# -----------------------------------------------------------------------------
from dataclasses import dataclass,field

@dataclass
class Document:
    id: str
    title: str
    url:str
    content:str
    source:str
    metadata:dict=field(default_factory=dict)
    #
    # field(default_factory=dict)
    # Creates a new dictionary for every Document object.
    # Prevents multiple objects from accidentally sharing the same dictionary.
    # Commonly used in dataclasses for mutable defaults like dict and list.
    #

    # Metadata stores additional information about a document.
    # Examples:
    # - word_count
    # - char_count
    # - source information
    # - future embedding statistics