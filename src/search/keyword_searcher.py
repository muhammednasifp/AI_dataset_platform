# *-----------------------------------------------------------------------------*
#
# *Keyword Search / BM25*
#
# *Retrieves chunks based on keyword relevance*
# *rather than semantic similarity.*
#
# *KeywordSearcher implements BM25-based retrieval,*
# *ranking chunks according to the relevance of query terms.*
#
# *Core Concepts:*
# *- Term Frequency (TF)      : Number of times a word occurs within a chunk.*
# *- Document Frequency (DF)  : Number of chunks containing a word.*
# *- Inverse Document Frequency*
# *  (IDF)                    : Measures the importance of a word based on*
# *                             how rare it is across all chunks.*
# *- Document Length           : Number of words contained in a chunk.*
# *- Average Document Length   : Average number of words across all chunks.*
#
# *BM25 Parameters:*
# *- k1 : Controls the influence of term frequency on the final score.*
# *- b  : Controls the effect of document-length normalization.*
#
# *Design Notes:*
# *- Builds an in-memory keyword index when the searcher is initialized.*
# *- Calculates BM25 scores for query terms against every chunk.*
# *- Ranks chunks from highest to lowest relevance score.*
# *- Complements semantic search by providing exact keyword-based retrieval.*
# *-----------------------------------------------------------------------------*
import math
import logging
from src.models.search_result import SearchResult

logger = logging.getLogger(__name__)

class KeywordSearcher:

    def __init__(self, chunk_store, k1=1.5, b=0.75):

        # Store all chunks that will be searched.
        self.chunk_store = chunk_store
        self.chunks=self.chunk_store.read_all()
        # k1 controls how strongly term frequency affects the BM25 score.
        # Higher k1 gives more importance to repeated occurrences of a word.
        self.k1 = k1

        # b controls document-length normalization.
        # b=0 means no length normalization.
        # b=1 means full length normalization.
        self.b = b

        # Stores how frequently each word occurs inside each chunk.
        # Example:
        # {
        #     "chunk_1": {"python": 2, "django": 1}
        # }
        self.term_frequencies = {}

        # Stores how many different chunks contain each word.
        # This is used to calculate IDF (Inverse Document Frequency).
        self.document_frequency = {}

        # Stores the number of words in each chunk.
        self.document_lengths = {}

        # Average number of words across all chunks.
        # Used for BM25 document-length normalization.
        self.average_document_length = 0

        # Pre-process all chunks and build the BM25 statistics.
        self._build_index()


    def search(self, question):

        logger.info("Keyword search started")

        # Convert the question into lowercase words.
        # This makes keyword matching case-insensitive.
        query_words = question.lower().split()

        results = []

        # Calculate a BM25 score for every chunk.
        for chunk in self.chunks:

            score = 0

            # Calculate the BM25 contribution of every query word.
            for word in query_words:

                score += self._calculate_score(
                    word=word,
                    chunk_id=chunk.id
                )

            # Ignore chunks that contain none of the query terms.
            if score > 0:

                results.append(
                    SearchResult(
                        chunk=chunk,
                        score=score
                    )
                )
        # Highest BM25 score means the chunk is considered more relevant.
        results.sort(
            key=lambda result: result.score,
            reverse=True
        )

        return results


    def _count_words(self, words):

        # Dictionary used to calculate term frequency manually.
        frequency = {}

        for word in words:

            # If the word already exists, increase its count.
            if word in frequency:
                frequency[word] += 1

            # Otherwise, this is the first occurrence of the word.
            else:
                frequency[word] = 1

        return frequency


    def _build_index(self):

        # Used to calculate the total number of words
        # across all chunks.
        total_length = 0

        for chunk in self.chunks:

            # Convert chunk text into lowercase words.
            words = chunk.content.lower().split()

            # Count how many times each word occurs in this chunk.
            # This gives us Term Frequency (TF).
            term_frequency = self._count_words(words)

            # Store the term frequencies using the chunk ID.
            self.term_frequencies[chunk.id] = term_frequency

            # Number of words in this chunk.
            document_length = len(words)

            # Store the length for later BM25 normalization.
            self.document_lengths[chunk.id] = document_length

            # Add this chunk's length to the total.
            total_length += document_length

            # Calculate Document Frequency (DF).
            # Each word is counted only once per chunk,
            # regardless of how many times it appears in that chunk.
            for word in term_frequency:

                if word in self.document_frequency:
                    self.document_frequency[word] += 1

                else:
                    self.document_frequency[word] = 1

        # Calculate the average chunk length after all chunks
        # have been processed.
        if self.chunks:

            self.average_document_length = (
                total_length / len(self.chunks)
            )


    def _calculate_score(self, word, chunk_id):

        # Get the number of times the query word appears
        # in this particular chunk.
        term_frequency = (
            self.term_frequencies[chunk_id].get(word, 0)
        )

        # If the word does not occur in this chunk,
        # it contributes nothing to the BM25 score.
        if term_frequency == 0:
            return 0

        # Number of chunks containing this word.
        document_frequency = self.document_frequency[word]

        # Total number of chunks in the collection.
        total_documents = len(self.chunks)

        # IDF = Inverse Document Frequency.
        #
        # Rare words get a higher IDF score.
        # Common words get a lower IDF score.
        idf = math.log(
            1 + (
                (total_documents - document_frequency + 0.5)
                /
                (document_frequency + 0.5)
            )
        )

        # Length of the current chunk.
        document_length = self.document_lengths[chunk_id]

        # BM25 compares the current chunk length
        # with the average chunk length.
        denominator = (
            term_frequency
            +
            self.k1
            * (
                1
                - self.b
                + self.b
                * (
                    document_length
                    / self.average_document_length
                )
            )
        )

        # Calculate the final BM25 score for this word.
        #
        # The score combines:
        #   1. Term Frequency (TF)
        #   2. Inverse Document Frequency (IDF)
        #   3. Document-length normalization
        score = (
            idf
            *
            (
                term_frequency
                * (self.k1 + 1)
            )
            /
            denominator
        )

        return score
