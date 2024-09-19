import os
import openai
from openai import OpenAI
from pyicl import ContextManager, PromptBuilder

# Load API key from environment variable
api_key = os.environ.get("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

def create_openai_client(api_key: str) -> OpenAI:
    """
    Creates an OpenAI client instance with the given API key.
    
    Args:
        api_key (str): The API key for authenticating with OpenAI.

    Returns:
        OpenAI: An instance of the OpenAI client.
    """
    return openai.Client(api_key=api_key)

def create_context_manager() -> ContextManager:
    """
    Create a context manager instance.
    
    Returns:
        ContextManager: An instance of the context manager from PyICL.
    """
    # Assuming ContextManager is a custom class
    return ContextManager()

def create_prompt_builder(context_manager: ContextManager) -> PromptBuilder:
    """
    Create a prompt builder instance.

    Args:
        context_manager (ContextManager): The context manager instance to be used by the prompt builder.

    Returns:
        PromptBuilder: An instance of the prompt builder from PyICL.
    """
    # Assuming PromptBuilder is a custom class
    return PromptBuilder(context_manager)

def add_context(context_manager: ContextManager, context_type: str, examples: list[str]) -> None:
    """
    Add context examples to the context manager.

    Args:
        context_manager (ContextManager): The context manager to which context examples will be added.
        context_type (str): The type of context (e.g., 'medical').
        examples (list[str]): A list of context examples.
    """
    context_manager.add_context(context_type, examples)

def call_openai_api(model: str, prompt: str, max_tokens: int, temperature: float) -> str:
    """
    Call the OpenAI API to generate a response.

    Args:
        model (str): The model to use for generating responses (e.g., 'gpt-4').
        prompt (str): The prompt to send to the API.
        max_tokens (int): The maximum number of tokens to generate.
        temperature (float): Sampling temperature, controlling randomness in responses.

    Returns:
        str: The response text from the OpenAI API or None if an error occurs.
    """
    try:
        response = client.chat.completions.create(
            model=model,
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=max_tokens,
            temperature=temperature
        )
        return response.choices[0].message.content
    except Exception as e:
        print(f"Error: {e}")
        return None

def main() -> None:
    """
    Main function to execute the script.

    - Creates an OpenAI client.
    - Initializes a ContextManager and a PromptBuilder.
    - Adds context examples related to medical scenarios.
    - Constructs a prompt based on user input.
    - Calls the OpenAI API with the constructed prompt and prints the model's output.
    """
    # Create OpenAI client
    client = create_openai_client(api_key)  # Pass api_key as an argument

    # Create a ContextManager instance
    context_manager = create_context_manager()

    # Create a PromptBuilder instance with the ContextManager
    prompt_builder = create_prompt_builder(context_manager)

    # Add some examples for the "medical" context
    add_context(context_manager, "medical", [
        "A patient is experiencing symptoms of fever and headache.",
        "A patient has been diagnosed with diabetes and needs treatment."
    ])

    # Build a prompt for the "medical" context with a user input
    user_input = "A patient is experiencing symptoms of chest pain and shortness of breath."
    prompt = prompt_builder.build_prompt("medical", user_input)
    # Print the built prompt
    print(prompt)

    # Call OpenAI API
    model_output = call_openai_api("gpt-4", prompt, 150, 0.7)

    # Print response
    if model_output:
        print("Model Output:", model_output)

if __name__ == "__main__":
    main()
