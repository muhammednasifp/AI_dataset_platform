# -----------------------------------------------------------------------------
# Testing Notes
#
# Testing verifies that individual components of the AI Dataset Platform
# behave according to their expected behavior.
#
# Pytest is used as the automated testing framework.
#
# Test files:
# - pytest discovers files such as test_*.py or *_test.py.
# - Test functions are identified by names beginning with test_.
# - Each test checks expected behavior using assert statements.
#
# Example:
#
#     assert result == expected
#
# If the condition is True:
#     Test PASSED
#
# If the condition is False:
#     Test FAILED
#
# pytest can run all tests using:
#
#     python -m pytest
#
# Temporary test files are created using pytest's tmp_path fixture so that
# tests do not modify the actual project dataset.
#
# Example:
#
#     def test_save_and_read_one(tmp_path):
#         path = tmp_path / "documents.jsonl"
#
# This creates an isolated temporary location for the test.
#
# Testing approach:
# - Test individual components independently.
# - Test normal/expected behavior.
# - Test important edge cases.
# - Test exception handling where required.
# - Keep test data separate from production data.
#
# The project components were also manually tested during development before
# integrating them into the complete pipeline.
#
# Current automated testing focuses on verifying the core storage behavior
# of JSONLStore, while component-level testing was performed during
# development.
#
# Testing flow:
#
#     Test Input
#         ↓
#     Component
#         ↓
#     Result
#         ↓
#     assert expected behavior
#         ↓
#     PASS / FAIL
#
# -----------------------------------------------------------------------------
from src.models.document import Document
from src.storage.jsonl_store import JSONLStore

def test_save_and_read_one(tmp_path):

    path = tmp_path / "documents.jsonl"

    store = JSONLStore(
        path=str(path),
        model_class=Document,
    )

    document = Document(
        id="1",
        title="Python",
        url="https://example.com",
        content="Python is a programming language.",
        source="test"
    )

    store.save_one(document)

    documents = store.read_all()

    assert len(documents) == 1
    assert documents[0].id == "1"
    assert documents[0].title == "Python"
    assert documents[0].content == "Python is a programming language."

def test_save_many(tmp_path):

    path = tmp_path / "documents.jsonl"
    
    store = JSONLStore(
        path=str(path),
        model_class=Document,
    )

    documents = [
        Document(
            id="1",
            title="Python",
            url="https://example.com/1",
            content="Python content",
            source="test"
        ),
        Document(
            id="2",
            title="Django",
            url="https://example.com/2",
            content="Django content",
            source="test"
        ),
    ]

    store.save_many(documents=documents)

    result = store.read_all()

    assert len(result)==2

    assert result[0].id=="1"

    assert result[1].id=="2"

def test_count(tmp_path):

    path = tmp_path / "documents.jsonl"
        
    store = JSONLStore(
        path=str(path),
        model_class=Document,
    )

    documents = [
        Document(
            id="1",
            title="Python",
            url="https://example.com/1",
            content="Python content",
            source="test"
        ),
        Document(
            id="2",
            title="Django",
            url="https://example.com/2",
            content="Django content",
            source="test"
        ),
    ]

    store.save_many(documents=documents)

    count=store.count()

    assert count==2

def test_replace(tmp_path):

    path = tmp_path / "documents.jsonl"
        
    store = JSONLStore(
        path=str(path),
        model_class=Document,
    )

    documents = [
        Document(
            id="1",
            title="Python",
            url="https://example.com/1",
            content="Python content",
            source="test"
        ),
        Document(
            id="2",
            title="Django",
            url="https://example.com/2",
            content="Django content",
            source="test"
        ),
    ]

    store.save_many(documents=documents)

    replace_documents = [
    Document(
        id="3",
        title="Python",
        url="https://example.com/1",
        content="Python content",
        source="test"
    ),
    Document(
        id="4",
        title="Django",
        url="https://example.com/2",
        content="Django content",
        source="test"
    ),
]
    store.replace_all(documents=replace_documents)

    result=store.read_all()

    assert result[0].id=="3"
    assert result[1].id=="4"

def test_clear(tmp_path):

    path = tmp_path / "documents.jsonl"
        
    store = JSONLStore(
        path=str(path),
        model_class=Document,
    )

    documents = [
        Document(
            id="1",
            title="Python",
            url="https://example.com/1",
            content="Python content",
            source="test"
        ),
        Document(
            id="2",
            title="Django",
            url="https://example.com/2",
            content="Django content",
            source="test"
        ),
    ]

    store.save_many(documents=documents)
