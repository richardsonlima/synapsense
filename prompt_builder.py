class PromptBuilder:
    def __init__(self, context_manager):
        self.context_manager = context_manager

    def build_prompt(self, context_name, user_input):
        """Builds a prompt using examples from a specific context."""
        examples = self.context_manager.get_context(context_name)
        prompt = ""

        for example in examples:
            prompt += f"Example: {example}\n"

        prompt += f"User Input: {user_input}\n"
        prompt += "Model Output:"

        return prompt
