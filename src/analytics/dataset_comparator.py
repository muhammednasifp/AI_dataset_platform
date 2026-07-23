# Composition
#
# Build new features by combining
# existing components.
#
# Example:
# VersionManager + DatasetAnalyzer
# = DatasetComparator

from src.analytics.dataset_analyzer import DatasetAnalyzer

class Comparator:

    def __init__(self,version_1,version_2):
        self.version_1=version_1
        self.version_2=version_2

    def _document_count(self,version):
        # Python Access Conventions
        #
        # method()      -> Public
        #
        # _method()     -> Internal/Protected
        #
        # __method()    -> Name Mangling
        #
        # Python relies on conventions rather
        # than strict access modifiers.

        analytics_obj=DatasetAnalyzer(version)
        
        return analytics_obj.total_documents()
    def _word_count(self,version):

        analytics_obj=DatasetAnalyzer(version)
        
        return analytics_obj.total_words()

    def compare_documents(self):
        
        v1_document_count=self._document_count(self.version_1)
        v1_word_count=self._word_count(self.version_1)

        v2_document_count=self._document_count(self.version_2)
        v2_word_count=self._word_count(self.version_2)

        document_diff = (
            v2_document_count
            - v1_document_count
        )

        word_diff = (
            v2_word_count
            - v1_word_count
        )

        output=f"""

        Version 1
        ----------
        Documents: {v1_document_count}
        Words: {v1_word_count}

        Version 2
        ----------
        Documents: {v2_document_count}
        Words: {v2_word_count}

        Difference
        ----------
        {document_diff:+}
        {word_diff:+}
        
        """
        # f-string sign formatting
        #
        # {value:+}
        #
        # Always displays the sign.
        #
        # Examples:
        # +5
        # -3
        # +0
        return output



# v_obj=DataVersionManager("data/versions/")
# v1=v_obj.read_version(1)
# v2=v_obj.read_version(2)


# obj=Comparator(version_1=v1,version_2=v2)

# obj.compare_documents()
