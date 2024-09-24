import os
import openai
from openai import OpenAI
from pyicl import ContextManager, PromptBuilder, ContextOptimizer
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Download NLTK stopwords corpus if not already downloaded
try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords')

# Load API key from environment variable
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def create_openai_client(api_key):
    """Creates an OpenAI client instance with the given API key."""
    return openai.Client(api_key=api_key)

def create_context_manager() -> ContextManager:
    """Create a context manager instance."""
    # Assuming ContextManager is a custom class
    return ContextManager()

def create_prompt_builder(context_manager: ContextManager) -> PromptBuilder:
    """Create a prompt builder instance."""
    # Assuming PromptBuilder is a custom class
    return PromptBuilder(context_manager)

def create_context_optimizer() -> ContextOptimizer:
    """Create a context optimizer instance."""
    # Assuming ContextOptimizer is a custom class
    return ContextOptimizer()

def add_context(context_manager: ContextManager, context_type: str, examples: list[str]) -> None:
    """Add context examples to the context manager."""
    context_manager.add_context(context_type, examples)

def call_openai_api(model: str, prompt: str, max_tokens: int, temperature: float) -> str:
    """Call the OpenAI API to generate a response."""
    try:
        response = client.chat.completions.create(model=model,
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt}
        ],
        max_tokens=max_tokens,
        temperature=temperature)
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def main() -> None:
    # Create OpenAI client
    client = create_openai_client(api_key)  # Pass api_key as an argument

    # Create a ContextManager instance
    context_manager = create_context_manager()

    # Create a PromptBuilder instance with the ContextManager
    prompt_builder = create_prompt_builder(context_manager)

    # Create a ContextOptimizer instance
    context_optimizer = create_context_optimizer()

    # Add some examples for the "medical" context
    context_manager.add_context("medical", [
        "A patient is experiencing symptoms of fever and headache.",
        "A patient has been diagnosed with diabetes and needs treatment.",
        "A patient is experiencing symptoms of chest pain and shortness of breath.",
        "A patient has been diagnosed with hypertension and needs medication.",
        "A patient is experiencing symptoms of dizziness and nausea."
    ])

    # Get the context examples
    context_examples = context_manager.get_context("medical")

    # Evaluate the relevance of each context example
    for example in context_examples:
        # For demonstration purposes, assume a performance metric of 0.5
        context_optimizer.evaluate_relevance(example, "medical", 0.5)

    # Adjust the context examples based on their relevance
    context_optimizer.adjust_contexts()

    # Get the optimized context examples
    optimized_context = context_optimizer.get_optimized_context()

    # Build a prompt for the "medical" context with a user input
    user_input = "A patient is experiencing symptoms of chest pain and shortness of breath."
    prompt = prompt_builder.build_prompt("medical", user_input)
    # Print the built prompt
    print(prompt)

    # Call OpenAI API
    model = "gpt-3.5-turbo"
    max_tokens = 2048
    temperature = 0.7
    response = call_openai_api(model, prompt, max_tokens, temperature)

    # Print the model's response
    if response is not None:
        print("Model Output:")
        print(response)
    else:
        print("Failed to retrieve model response.")

if __name__ == "__main__":
    main()