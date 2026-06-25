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
class DocumentCleaner:

    def clean(self,document):
        
        document.content=' '.join(document.content.split())
        document.title=' '.join(document.title.split())

        return document