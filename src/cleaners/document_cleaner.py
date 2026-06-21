class DocumentCleaner:

    def clean(self,document):
        
        document.content=' '.join(document.content.split())
        document.title=' '.join(document.title.split())

        return document