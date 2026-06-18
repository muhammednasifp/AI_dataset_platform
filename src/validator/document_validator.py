

class DocumentValidator:

    def validate(self, document):

        if not document.title: #here 'not' catches both None and empty tring("")
            return False

        if not document.content:
            return False

        if len(document.content) < 100:
            return False

        return True