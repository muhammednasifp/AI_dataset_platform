# Generator
#
# Sends prompts to a language model
# and returns generated answers.
#
# Flow:
# Prompt -> LLM -> Answer

from ollama import chat

class Generator:
    
    def generate(self,prompt):

        response=chat(
            model="phi3",
            messages=[
                {
                    "role":"user",
                    "content":prompt
                }
            ]
        )

        return (response["message"]["content"])
    