# Generator
#
# Sends prompts to a language model
# and returns generated answers.
#
# Flow:
# Prompt -> LLM -> Answer
import logging
from src.exceptions.generator import GeneratorError

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

        
        except Exception as e:
            logger.exception("Answer generation failed")
            raise GeneratorError(
                "Unable to generate answer."
            ) from e

        content = response.get(
            "message", {}
        ).get("content")

        if not content:

            logger.error(
                "Generator returned an empty response"
            )

            raise GeneratorError(
                "Generator returned an empty response."
            )

        logger.info(
            "Answer generated successfully"
        )

        return content
        
    