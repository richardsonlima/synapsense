class ContextManager:
    """
    A class to manage a collection of contexts.

    Attributes:
        contexts (dict): A dictionary where the keys are context names and the values are the corresponding context objects or data.

    Methods:
        list_contexts: Returns a list of all available context names.
        get_context: Retrieves the examples associated with a specific context name.
    """

    def list_contexts(self) -> list:
        """
        List all available contexts.

        Returns:
            list: A list of all available context names.
        """
        return list(self.contexts.keys())

    def get_context(self, context_name: str) -> dict:
        """
        Retrieves the examples associated with a specific context name.

        Args:
            context_name (str): The name of the context.

        Returns:
            dict: The examples associated with the specified context name.
        """
        # Implementation of get_context method is not shown in the original code snippet


class PromptBuilder:
    """
    A class to build prompts using examples from a specific context.

    Attributes:
        context_manager (ContextManager): An instance of the ContextManager class.

    Methods:
        build_prompt: Builds a prompt using examples from a specific context and user input.
    """

    def __init__(self, context_manager: ContextManager):
        """
        Initialize a prompt builder with a context manager.

        Args:
            context_manager (ContextManager): An instance of the ContextManager class.
        """
        self.context_manager = context_manager

    def build_prompt(self, context_name: str, user_input: str) -> str:
        """
        Builds a prompt using examples from a specific context and user input.

        Args:
            context_name (str): The name of the context.
            user_input (str): The user's input.

        Returns:
            str: A prompt string that includes the context name and user input.

        Note:
            The implementation of the logic to build a more sophisticated prompt using examples and user input is still pending.
        """
        examples = self.context_manager.get_context(context_name)
        # TO DO: implement the logic to build the prompt using examples and user_input
        # For now, return a simple prompt
        return f"Prompt for {context_name}: {user_input}"
