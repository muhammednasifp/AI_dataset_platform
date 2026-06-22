from dataclasses import dataclass

@dataclass
class Embedding:
    chunk_id:str
    vector:list[float]