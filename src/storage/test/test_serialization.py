from src.models.document import Document

from dataclasses import asdict
doc=Document(
    id="1",
    title="Python Basics",
    url="https://example.com",
    content="Python intro",
    source="python_docs"
    )

print(doc)
print(asdict(doc))