import nltk
nltk.download('stopwords')
from nltk.corpus import stopwords

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

    def search_context(self, query: str) -> list:
        """Search for contexts that match a query."""
        results = []
        for context_name, examples in self.contexts.items():
            for example in examples:
                if query in example:
                    results.append((context_name, example))
        return results

    def filter_contexts(self, filter_func: callable) -> dict:
        """Filter contexts using a custom function."""
        filtered_contexts = {}
        for context_name, examples in self.contexts.items():
            filtered_examples = [example for example in examples if filter_func(example)]
            if filtered_examples:
                filtered_contexts[context_name] = filtered_examples
        return filtered_contexts

    def merge_contexts(self, other: 'ContextManager') -> 'ContextManager':
        """Merge two context managers into one."""
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
        """Return a string representation of the context manager."""
        return f"ContextManager with {len(self.contexts)} contexts"


class PromptBuilder:
    def __init__(self, context_manager: ContextManager):
        """Initialize a prompt builder with a context manager."""
        self.context_manager = context_manager
        self.STOP_WORDS = set(stopwords.words('english'))

    def build_prompt(self, context_name: str, user_input: str) -> str:
        """Build a prompt using examples from a specific context."""
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
        """Extract relevant keywords from user input."""
        # Tokenize the user input
        tokens = user_input.split()

        # Remove stop words and punctuation
        keywords = [token for token in tokens if token.isalpha() and token.lower() not in self.STOP_WORDS]

        return keywords

    def find_relevant_examples(self, examples: list, keywords: list) -> list:
        """Find the most relevant examples that match the keywords."""
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
        """Calculate the similarity between the example and the keywords."""
        # Calculate the Jaccard similarity between the example and the keywords
        example_tokens = set(example.split())
        keyword_tokens = set(keywords)
        intersection = example_tokens & keyword_tokens
        union = example_tokens | keyword_tokens
        similarity = len(intersection) / len(union)

        return similarity

    def generate_prompt(self, relevant_examples: list, user_input: str) -> str:
        """Generate a prompt using the relevant examples and user input."""
        prompt = ""
        for example in relevant_examples:
            prompt += f"Example: {example}\n"
        prompt += f"User Input: {user_input}\n"
        prompt += "Please respond based on the above context."

        return prompt
    
class ContextOptimizer:
    def __init__(self):
        self.example_performance = {}  # store performance metrics for each example
        self.contexts = []  # store the list of contextual examples

    def evaluate_relevance(self, example, query, performance_metric):
        # assess the effectiveness of the example in improving model performance
        # update the performance metrics for the example
        self.example_performance[example] = performance_metric

    def adjust_contexts(self):
        # automatically refine the list of examples based on feedback and performance metrics
        sorted_examples = sorted(self.example_performance, key=self.example_performance.get, reverse=True)
        self.contexts = sorted_examples[:10]  # keep only the top 10 performing examples

    def experiment(self, new_context):
        # allow users to experiment with different contexts and measure their impact
        # temporarily replace the current context with the new one
        original_context = self.contexts
        self.contexts = new_context
        # run the model with the new context and measure the performance
        # ...
        # restore the original context
        self.contexts = original_context

    def get_optimized_context(self):
        # return the optimized list of contextual examples
        return self.contexts