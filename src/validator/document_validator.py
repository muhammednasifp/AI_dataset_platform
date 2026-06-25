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

class DocumentValidator:

    def validate(self, document):

        if not document.title: #here 'not' catches both None and empty tring("")
            return False

        if not document.content:
            return False

        if len(document.content) < 100:
            return False

        return True