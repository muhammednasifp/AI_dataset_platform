
class DocumentEnricher:
    
    def enricher(self,document):
        
        word_count=len(document.content.split())
        char_count=len(document.content) # len(string) returns the number of characters in the text.

        document.metadata["word_count"]=word_count
        document.metadata["char_count"]=char_count

        return document

        