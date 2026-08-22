from dataclasses import dataclass

from src.models.chunk import Chunk

@dataclass
class SearchResult:

    chunk: Chunk
    score: float