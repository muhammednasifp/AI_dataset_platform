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

class ContextBuilder:

    def build(self,chunks):

        content=''

        for chunk in chunks:

            content += chunk.content+"....\n"

        return content
