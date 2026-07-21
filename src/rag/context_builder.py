# Context Builder
#
# Combines retrieved chunks into a
# single context string.
#
# This context is later passed to
# an LLM during RAG.
#
# Flow:
# Chunks -> Context -> Prompt -> LLM
import logging
logger = logging.getLogger(__name__)

class ContextBuilder:

    def build(self,chunks):

        content=""

        logger.info("Building context from %d chunks", len(chunks))

        for chunk in chunks:

            content += chunk.content+"....\n"
        
        logger.info(
            "Context built successfully (%d characters)",
            len(content)
        )

        return content
