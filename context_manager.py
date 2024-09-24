class ContextManager:
    """
    A class used to manage contexts and their corresponding examples.

    Attributes:
    ----------
    contexts : dict
        A dictionary where the keys are context names and the values are lists of examples.

    Methods:
    -------
    add_context(context_name, examples)
        Adds a new list of examples for a specific context.
    remove_context(context_name)
        Removes a context by name.
    get_context(context_name)
        Retrieves the examples of a specific context.
    list_contexts()
        Lists all available contexts.
    search_context(query)
        Searches for contexts that match a query.
    filter_contexts(filter_func)
        Filters contexts using a custom function.
    merge_contexts(other)
        Merges two context managers into one.
    """

    def __init__(self):
        """
        Initializes an empty context manager.

        Returns:
        -------
        None
        """
        self.contexts = {}

    def add_context(self, context_name: str, examples: list):
        """
        Adds a new list of examples for a specific context.

        Args:
        ----
        context_name (str): The name of the context.
        examples (list): A list of examples for the context.

        Returns:
        -------
        None
        """
        if context_name in self.contexts:
            self.contexts[context_name].extend(examples)
        else:
            self.contexts[context_name] = examples

    def remove_context(self, context_name: str):
        """
        Removes a context by name.

        Args:
        ----
        context_name (str): The name of the context to remove.

        Returns:
        -------
        None
        """
        self.contexts.pop(context_name, None)

    def get_context(self, context_name: str) -> list:
        """
        Retrieves the examples of a specific context.

        Args:
        ----
        context_name (str): The name of the context.

        Returns:
        -------
        list: A list of examples for the context.
        """
        return self.contexts.get(context_name, [])

    def list_contexts(self) -> list:
        """
        Lists all available contexts.

        Returns:
        -------
        list: A list of context names.
        """
        return list(self.contexts.keys())

    def search_context(self, query: str) -> list:
        """
        Searches for contexts that match a query.

        Args:
        ----
        query (str): The query to search for.

        Returns:
        -------
        list: A list of tuples containing the context name and example.
        """
        results = []
        for context_name, examples in self.contexts.items():
            for example in examples:
                if query in example:
                    results.append((context_name, example))
        return results

    def filter_contexts(self, filter_func: callable) -> dict:
        """
        Filters contexts using a custom function.

        Args:
        ----
        filter_func (callable): A function that takes an example and returns a boolean.

        Returns:
        -------
        dict: A dictionary of filtered contexts.
        """
        filtered_contexts = {}
        for context_name, examples in self.contexts.items():
            filtered_examples = [example for example in examples if filter_func(example)]
            if filtered_examples:
                filtered_contexts[context_name] = filtered_examples
        return filtered_contexts

    def merge_contexts(self, other: 'ContextManager') -> 'ContextManager':
        """
        Merges two context managers into one.

        Args:
        ----
        other (ContextManager): The context manager to merge with.

        Returns:
        -------
        ContextManager: A new context manager containing the merged contexts.
        """
        merged_contexts = {}
        for context_name, examples in self.contexts.items():
            merged_contexts[context_name] = examples
        for context_name, examples in other.contexts.items():
            if context_name in merged_contexts:
                merged_contexts[context_name].extend(examples)
            else:
                merged_contexts[context_name] = examples
        return ContextManager(**merged_contexts)

    def __str__(self) -> str:
        """
        Returns a string representation of the context manager.

        Returns:
        -------
        str: A string representation of the context manager.
        """
        return f"ContextManager with {len(self.contexts)} contexts"
