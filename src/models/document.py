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