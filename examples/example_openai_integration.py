import openai
from pyicl import ContextManager, PromptBuilder

# Set up your OpenAI API key
openai.api_key = 'your-api-key'

# Initialize PyICL components
context_manager = ContextManager()
prompt_builder = PromptBuilder(context_manager)

# Add some context examples
context_manager.add_context("medical", [
    "Patient has a headache and dizziness.",
    "Patient reports chest pain during exercise.",
])

# User input
user_input = "Patient has a sore throat and fever."

# Build the prompt using PyICL
prompt = prompt_builder.build_prompt("medical", user_input)

# Call the OpenAI API with the generated prompt
response = openai.ChatCompletion.create(
    model="gpt-4",  # or "gpt-4-turbo", etc.
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": prompt}
    ]
)

# Extract and print the model's response
model_output = response['choices'][0]['message']['content']
print("Model Output:", model_output)
