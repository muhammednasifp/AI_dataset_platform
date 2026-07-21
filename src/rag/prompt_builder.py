# Prompt Builder
#
# Combines context and question into
# a prompt for an LLM.
#
# Flow:
# Context + Question -> Prompt

import logging

logger = logging.getLogger(__name__)

class PromptBuilder:

    def build(self,question,context):

        logger.info("Building prompt")

        prompt=f"""

        Answer the question using the
        provided context.

        Context:
        ---------
        {context}
        
        Question:
        ---------
        {question}

        Answer:
        
        """

        logger.info(
            "Prompt built successfully (%d characters)",
            len(prompt)
        )
    
        return prompt