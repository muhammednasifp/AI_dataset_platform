# -----------------------------------------------------------------------------
# DocumentCleaner
#
# Cleans and normalizes document fields before validation, storage, and
# downstream AI processing.
#
# Current cleaning operations:
# - Removes extra whitespace from the document title.
# - Removes extra whitespace from the document content.
#
# Design Notes:
# - Modifies the existing Document object in place.
# - Acts as a preprocessing step in the data ingestion pipeline.
# - Can be extended with additional cleaning tasks such as HTML removal,
#   Unicode normalization, special character filtering, and text normalization.
# -----------------------------------------------------------------------------

import logging
logger = logging.getLogger(__name__)

class DocumentCleaner:

    def clean(self,document):

        logger.info("Cleaning document (id=%s)", document.id)

        document.content=' '.join(document.content.split())
        document.title=' '.join(document.title.split())

        logger.info("Finished cleaning document (id=%s)", document.id)

        return document