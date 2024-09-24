import os
import openai
from synapsense import ContextManager, PromptBuilder, ContextOptimizer
import nltk
nltk.download('stopwords')
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def main():
    # Load API key from environment variable
    api_key = os.environ.get("OPENAI_API_KEY")
    client = openai.Client(api_key=api_key)

    # Create a ContextManager instance
    context_manager = ContextManager()

    # Create a PromptBuilder instance with the ContextManager
    prompt_builder = PromptBuilder(context_manager)

    # Create a ContextOptimizer instance
    context_optimizer = ContextOptimizer()

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