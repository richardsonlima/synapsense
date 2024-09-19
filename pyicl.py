class ContextManager:
    def __init__(self):
        """Initialize an empty context manager."""
        self.contexts = {}

    def add_context(self, context_name: str, examples: list):
        """Add a new list of examples for a specific context."""
        if context_name in self.contexts:
            self.contexts[context_name].extend(examples)
        else:
            self.contexts[context_name] = examples

    def remove_context(self, context_name: str):
        """Remove a context by name."""
        self.contexts.pop(context_name, None)

    def get_context(self, context_name: str) -> list:
        """Retrieve the examples of a specific context."""
        return self.contexts.get(context_name, [])

    def list_contexts(self) -> list:
        """List all available contexts."""
        return list(self.contexts.keys())


class PromptBuilder:
    def __init__(self, context_manager: ContextManager):
        """Initialize a prompt builder with a context manager."""
        self.context_manager = context_manager

    def build_prompt(self, context_name: str, user_input: str) -> str:
        """Build a prompt using examples from a specific context."""
        examples = self.context_manager.get_context(context_name)
        # TO DO: implement the logic to build the prompt using examples and user_input
        # For now, return a simple prompt
        return f"Prompt for {context_name}: {user_input}"