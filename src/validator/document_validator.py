# -----------------------------------------------------------------------------
# DocumentValidator
#
# Validates Document objects to ensure they satisfy the minimum quality
# requirements before entering the dataset pipeline.
#
# Current validation rules:
# - Document must have a non-empty title.
# - Document must have non-empty content.
# - Document content must meet the minimum length requirement.
#
# Design Notes:
# - Acts as the quality gate for the data ingestion pipeline.
# - Performs lightweight validation without modifying the document.
# - Returns True for valid documents and False otherwise.
# - Can be extended with additional validation rules such as URL validation,
#   duplicate detection, language checks, and content quality constraints.
# -----------------------------------------------------------------------------

import logging
logger = logging.getLogger(__name__)

class DocumentValidator:

    def validate(self, document,threshold):

        logger.info("Validating document (id=%s)", document.id)

        if not document.title: #here 'not' catches both None and empty tring("")
            logger.warning("Validation failed: document (id=%s) has no title", document.id)
            return False

        if not document.content:
            logger.warning("Validation failed: document (id=%s) has no content", document.id)
            return False

        if len(document.content) < threshold :
            logger.warning("Validation failed: document (id=%s) short length", document.id)
            return False

        return True