import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

from .context_manager import ContextManager

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