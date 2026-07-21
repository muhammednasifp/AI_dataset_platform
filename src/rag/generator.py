# Generator
#
# Sends prompts to a language model
# and returns generated answers.
#
# Flow:
# Prompt -> LLM -> Answer
import logging

logger = logging.getLogger(__name__)

from ollama import chat

class Generator:
    
    def generate(self,prompt):
        logger.info("Generating response using LLM")
        try:
            response=chat(
                model="phi3",
                messages=[
                    {
                        "role":"user",
                        "content":prompt
                    }
                ]
            )
            logger.info("LLM response generated successfully")

            return (response["message"]["content"])
        
        except Exception:
            logger.exception("Failed to generate LLM response")
            return None
        
    