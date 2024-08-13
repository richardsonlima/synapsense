class ContextManager:
    def __init__(self):
        self.contexts = {}

    def add_context(self, context_name, examples):
        """Adds a new list of examples for a specific context."""
        if context_name in self.contexts:
            self.contexts[context_name].extend(examples)
        else:
            self.contexts[context_name] = examples

    def remove_context(self, context_name):
        """Removes a context by name."""
        if context_name in self.contexts:
            del self.contexts[context_name]

    def get_context(self, context_name):
        """Retrieves the examples of a specific context."""
        return self.contexts.get(context_name, [])

    def list_contexts(self):
        """Lists all available contexts."""
        return list(self.contexts.keys())
