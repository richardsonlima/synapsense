import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

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


class PromptBuilder:
    """
    A class used to build prompts based on user input and context examples.

    Attributes:
    ----------
    context_manager : ContextManager
        A context manager object used to retrieve context examples.
    STOP_WORDS : set
        A set of stop words to ignore when extracting keywords.

    Methods:
    -------
    build_prompt(context_name, user_input)
        Builds a prompt using examples from a specific context.
    extract_keywords(user_input)
        Extracts relevant keywords from user input.
    find_relevant_examples(examples, keywords)
        Finds the most relevant examples that match the keywords.
    calculate_similarity(example, keywords)
        Calculates the similarity between the example and the keywords.
    generate_prompt(relevant_examples, user_input)
        Generates a prompt using the relevant examples and user input.
    """

    def __init__(self, context_manager: ContextManager):
        """
        Initializes a prompt builder with a context manager.

        Args:
        ----
        context_manager (ContextManager): A context manager object.

        Returns:
        -------
        None
        """
        self.context_manager = context_manager
        self.STOP_WORDS = set(stopwords.words('english'))

    def build_prompt(self, context_name: str, user_input: str) -> str:
        """
        Builds a prompt using examples from a specific context.

        Args:
        ----
        context_name (str): The name of the context.
        user_input (str): The user's input.

        Returns:
        -------
        str: A prompt based on the context examples and user input.
        """
        examples = self.context_manager.get_context(context_name)
        prompt = ""

        # Step 1: Extract relevant keywords from user input
        keywords = self.extract_keywords(user_input)

        # Step 2: Find the most relevant examples that match the keywords
        relevant_examples = self.find_relevant_examples(examples, keywords)

        # Step 3: Generate a prompt using the relevant examples and user input
        if relevant_examples:
            prompt = self.generate_prompt(relevant_examples, user_input)
        else:
            prompt = f"No relevant examples found for {context_name}. Please try again."

        return prompt

    def extract_keywords(self, user_input: str) -> list:
        """
        Extracts relevant keywords from user input.

        Args:
        ----
        user_input (str): The user's input.

        Returns:
        -------
        list: A list of keywords extracted from the user input.
        """
        # Tokenize the user input
        tokens = user_input.split()

        # Remove stop words and punctuation
        keywords = [token for token in tokens if token.isalpha() and token.lower() not in self.STOP_WORDS]

        return keywords

    def find_relevant_examples(self, examples: list, keywords: list) -> list:
        """
        Finds the most relevant examples that match the keywords.

        Args:
        ----
        examples (list): A list of context examples.
        keywords (list): A list of keywords.

        Returns:
        -------
        list: A list of the most relevant examples that match the keywords.
        """
        relevant_examples = []
        for example in examples:
            # Calculate the similarity between the example and the keywords
            similarity = self.calculate_similarity(example, keywords)
            if similarity > 0.5:
                relevant_examples.append((example, similarity))

        # Sort the relevant examples by similarity
        relevant_examples.sort(key=lambda x: x[1], reverse=True)

        return [example[0] for example in relevant_examples[:3]]  # Return the top 3 most relevant examples

    def calculate_similarity(self, example: str, keywords: list) -> float:
        """
        Calculates the similarity between the example and the keywords.

        Args:
        ----
        example (str): A context example.
        keywords (list): A list of keywords.

        Returns:
        -------
        float: The similarity between the example and the keywords.
        """
        # Calculate the Jaccard similarity between the example and the keywords
        example_tokens = set(example.split())
        keyword_tokens = set(keywords)
        intersection = example_tokens & keyword_tokens
        union = example_tokens | keyword_tokens
        similarity = len(intersection) / len(union)

        return similarity

    def generate_prompt(self, relevant_examples: list, user_input: str) -> str:
        """
        Generates a prompt using the relevant examples and user input.

        Args:
        ----
        relevant_examples (list): A list of relevant examples.
        user_input (str): The user's input.

        Returns:
        -------
        str: A prompt based on the relevant examples and user input.
        """
        prompt = ""
        for example in relevant_examples:
            prompt += f"Example: {example}\n"
        prompt += f"User Input: {user_input}\n"
        prompt += "Please respond based on the above context"

        return prompt
    
class ContextOptimizer:
    """
    A class used to optimize the list of contextual examples based on their performance.

    Attributes:
    ----------
    example_performance : dict
        A dictionary storing the performance metrics for each example.
    contexts : list
        A list of contextual examples.

    Methods:
    -------
    evaluate_relevance(example, query, performance_metric)
        Evaluates the relevance of an example and updates its performance metrics.
    adjust_contexts()
        Refines the list of examples based on their performance metrics.
    experiment(new_context)
        Allows users to experiment with different contexts and measures their impact.
    get_optimized_context()
        Returns the optimized list of contextual examples.
    """

    def __init__(self):
        """
        Initializes an empty context optimizer.

        Returns:
        -------
        None
        """
        self.example_performance = {}  # store performance metrics for each example
        self.contexts = []  # store the list of contextual examples

    def evaluate_relevance(self, example: str, query: str, performance_metric: float):
        """
        Evaluates the relevance of an example and updates its performance metrics.

        Args:
        ----
        example (str): The example to evaluate.
        query (str): The query related to the example.
        performance_metric (float): The performance metric of the example.

        Returns:
        -------
        None
        """
        # assess the effectiveness of the example in improving model performance
        # update the performance metrics for the example
        self.example_performance[example] = performance_metric

    def adjust_contexts(self):
        """
        Refines the list of examples based on their performance metrics.

        Returns:
        -------
        None
        """
        # automatically refine the list of examples based on feedback and performance metrics
        sorted_examples = sorted(self.example_performance, key=self.example_performance.get, reverse=True)
        self.contexts = sorted_examples[:10]  # keep only the top 10 performing examples

    def experiment(self, new_context: list):
        """
        Allows users to experiment with different contexts and measures their impact.

        Args:
        ----
        new_context (list): The new context to experiment with.

        Returns:
        -------
        None
        """
        # allow users to experiment with different contexts and measure their impact
        # temporarily replace the current context with the new one
        original_context = self.contexts
        self.contexts = new_context
        # run the model with the new context and measure the performance
        # ...
        # restore the original context
        self.contexts = original_context

    def get_optimized_context(self) -> list:
        """
        Returns the optimized list of contextual examples.

        Returns:
        -------
        list: The optimized list of contextual examples.
        """
        # return the optimized list of contextual examples
        return self.contexts