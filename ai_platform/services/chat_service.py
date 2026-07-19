from src.config import Config
from src.factories.rag_factory import RAGFactory
class ChatService:

    @staticmethod
    def validate_question(question):

        if question is None:
            return False, "Please enter a question."

        question = question.strip()

        if not question:
            return False, "Question cannot be empty."

        if len(question) < 3:
            return False, "Question is too short."

        if len(question) > 1000:
            return False, "Question is too long."

        return True, question
    @staticmethod
    def ask(question):

        valid,result=ChatService.validate_question(question)

        if not valid:
            return{
                "success":False,
                "message":result
            }


        factory_obj=RAGFactory(config=Config)
        rag_obj=factory_obj.factory()

        try:
            answer=rag_obj.ask(question=question)
            return{
                "success":True,
                "answer":answer
            }
        
        except Exception as e:

            return{
                "success":False,
                "Answer":answer,
                "error":str(e)
            }

    