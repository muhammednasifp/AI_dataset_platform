# Prompt Builder
#
# Combines context and question into
# a prompt for an LLM.
#
# Flow:
# Context + Question -> Prompt

class PromptBuilder:

    def build(self,question,context):

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
    
        return prompt