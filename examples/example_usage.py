from pyicl import ContextManager, PromptBuilder

# Initializing the context manager and the prompt builder
context_manager = ContextManager()
prompt_builder = PromptBuilder(context_manager)

# Adding some context examples
context_manager.add_context("medical", [
    "Patient has a headache and dizziness.",
    "Patient reports chest pain during exercise.",
])

context_manager.add_context("legal", [
    "Client is seeking advice on intellectual property rights.",
    "Client has a dispute over a contract breach.",
])

# Building a prompt for the medical context
user_input = "Patient has a sore throat and fever."
prompt = prompt_builder.build_prompt("medical", user_input)

print(prompt)
