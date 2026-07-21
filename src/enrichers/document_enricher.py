# -----------------------------------------------------------------------------
# DocumentEnricher
#
# Enriches Document objects by computing and attaching derived metadata.
#
# Responsibilities:
# - Compute document statistics such as word and character counts.
# - Generate quality metrics using the QualityScorer.
# - Store computed metadata inside the Document object for reuse by
#   downstream components.
#
# Design Notes:
# - Acts as a metadata enrichment stage in the data processing pipeline.
# - Modifies the Document object in place by adding derived information.
# - Keeps metadata generation separate from document collection, cleaning,
#   validation, and storage.
# - Centralizes metadata computation so downstream components can reuse
#   precomputed values instead of recalculating them.
# -----------------------------------------------------------------------------

import logging
logger = logging.getLogger(__name__)


from src.analytics.quality_scorer import QualityScorer
class DocumentEnricher:
    
    def enricher(self,document):

        logger.info("Enriching document (id=%s)", document.id)
        
        word_count=len(document.content.split())
        char_count=len(document.content) # len(string) returns the number of characters in the text.

        document.metadata["word_count"]=word_count
        document.metadata["char_count"]=char_count

        if word_count == 0:
            logger.warning(
                "Document (id=%s) has no words after enrichment",
                document.id
            )
        scorer=QualityScorer(document=document)

        scoring_info=scorer.score_document()

        document.metadata["quality_score"]=scoring_info["score"]
        document.metadata["reasons"]=scoring_info["reasons"]

        logger.info(
                "Enrichment completed (id=%s, words=%d, chars=%d, quality=%.2f)",
                document.id,
                word_count,
                char_count,
                scoring_info["score"]
        )

        return document

        