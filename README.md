# synapsense Overview

**SynapSense** Python In-Context Learning for Large Language Models
SynapSense is a cutting-edge Python library designed to streamline the implementation of In-Context Learning (ICL) with Large Language Models (LLMs). By combining the concept of "synapse" (neural connections) with "sense," SynapSense empowers developers to build intelligent, sense-making models that leverage contextual information for more accurate and dynamic learning. Whether you’re working with natural language processing, AI-driven applications, or advanced machine learning projects, SynapSense provides an intuitive, scalable framework for enhancing LLM performance with in-context capabilities.

## Demo
![Alt text](ttyrecord.gif) 

In-Context Learning refers to the technique where a model is provided with examples within the context of its input, allowing the model to learn from these examples without the need for explicit fine-tuning. The idea is to leverage contextual examples to influence the model's output dynamically.

The synapsense library offers tools to manage and utilize these contextual examples efficiently, providing a structured way to build prompts and optimize the context provided to the LLM. synapsense is modular, allowing developers to pick and choose components based on their needs.

## Usage
This component is particularly useful in scenarios where the diversity of examples is critical, such as in adversarial settings or when working with limited data.

Here is a simple example of how to use synapsense:

```python
import os
import openai
from openai import OpenAI
from synapsense import ContextManager, PromptBuilder, ContextOptimizer
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
```

## Components of synapsense

### 1. ContextManager

**Purpose**: The `ContextManager` is responsible for storing and managing contextual examples. These examples are crucial for guiding the LLM in generating desired outputs.

**Key Features**:
- **Add Context**: Allows adding new examples to a specific context. For instance, if you have medical examples, you can group them under a "medical" context.
- **Remove Context**: Enables removal of a context when it’s no longer needed.
- **Retrieve Context**: Fetches all examples from a specific context, which can then be used to build prompts.
- **List Contexts**: Provides a list of all available contexts managed by the `ContextManager`.

**Usage**: This component is essential for organizing and categorizing examples. For instance, in a chatbot application, different contexts (like medical, legal, or general conversation) can be stored and retrieved as needed.

### 2. PromptBuilder

**Purpose**: The `PromptBuilder` uses the examples managed by the `ContextManager` to construct dynamic prompts that guide the LLM’s output.

**Key Features**:
- **Build Prompt**: This function constructs a prompt by combining examples from a specified context with the user’s input. The resulting prompt is then fed to the LLM to generate a context-aware response.

**Usage**: `PromptBuilder` is used when you need to create a structured input for the LLM. For example, in a Q&A system, you can use it to frame the user’s query in the context of relevant examples, ensuring the model produces a more accurate response.

### 3. ContextOptimizer (Planned)

**Purpose**: The `ContextOptimizer` is intended to optimize the selection and use of contextual examples. Over time, it would learn which examples are most effective for different types of queries and adjust the context accordingly.

**Key Features** (Planned):
- **Evaluate Relevance**: Assess the effectiveness of different examples in improving model performance.
- **Adjust Contexts**: Automatically refine the list of examples based on feedback and performance metrics.
- **Experimentation**: Allows users to experiment with different contexts and measure their impact.

**Usage**: This component would be valuable in situations where the effectiveness of context changes over time or where fine-tuning the context is necessary to achieve the best results.

### 4. ExperimentTracker (Planned)

**Purpose**: The `ExperimentTracker` would monitor and evaluate the performance of different context setups. It’s designed to help users understand the impact of context on the LLM’s output.

**Key Features** (Planned):
- **Track Metrics**: Record various performance metrics, such as accuracy or relevance, for different contexts.
- **Compare Configurations**: Compare the effectiveness of different context setups.
- **Generate Reports**: Provide insights and visualizations on how different contexts influence outcomes.

**Usage**: This component is especially useful for data scientists and developers who want to experiment with and refine their use of context in LLM applications. By tracking performance, they can make data-driven decisions on how to improve context management.

### 5. IntegrationAPI (Planned)

**Purpose**: The `IntegrationAPI` is meant to facilitate the integration of synapsense with other applications and frameworks, making it easier to use in production environments.

**Key Features** (Planned):
- **RESTful API**: Provide a REST API for accessing synapsense components remotely.
- **ML Pipeline Integration**: Seamlessly integrate with machine learning pipelines in frameworks like TensorFlow or PyTorch.
- **Deployment Support**: Tools for deploying synapsense in production environments.

**Usage**: This component would be crucial for teams looking to deploy synapsense in large-scale applications or integrate it with existing systems, enabling more widespread adoption.

### 6. UserInterface (Planned)

**Purpose**: The `UserInterface` would provide a graphical interface for interacting with synapsense, making it accessible to non-technical users.

**Key Features** (Planned):
- **Context Management UI**: A visual interface to manage contexts and examples.
- **Prompt Building Tools**: Interactive tools for building and testing prompts.
- **Real-Time Reporting**: Visualizations and reports on the performance of different contexts.

**Usage**: This component is ideal for end-users or teams who prefer a more visual approach to managing and experimenting with contexts, rather than working directly with code.

### 7. DataAugmentor (Optional, Planned)

**Purpose**: The `DataAugmentor` would automatically generate variations of context examples to enhance the robustness and diversity of prompts.

**Key Features** (Planned):
- **Textual Augmentation**: Generate variants of examples using techniques like synonym replacement, paraphrasing, or back-translation.
- **NLP Integration**: Leverage NLP techniques to create adversarial examples or synthetic data.
- **Diversity Enhancement**: Increase the variety of examples to make the LLM more adaptable to different inputs.


## Running Tests

To run tests, use:

```bash
python -m unittest discover tests
```


## Execution

Installation and execution are simple, using Python 3.11. Just clone the repository and run the tests to verify that everything is working correctly.

```bash
python3 example_openai_integration.py

Prompt for medical: A patient is experiencing symptoms of chest pain and shortness of breath.
Model Output: Subject: Urgent Medical Consultation Required: Chest Pain and Shortness of Breath

Dear [Doctor's Name],

I hope this message finds you well.

I am writing on behalf of a patient who has been experiencing some worrisome symptoms recently and we are seeking your immediate advice. The patient has reported persistent chest pain along with shortness of breath.

The chest pain is described as a pressure-like discomfort that is not localized to any one spot and seems to be constant. The patient also experiences shortness of breath even while at rest, which is a new development.

The patient does not have any known pre-existing heart conditions but these symptoms are causing significant concern.

Could you kindly advise on the urgency of this matter and the necessary
```

### Next Steps

- **Expand ContextManager**: Add support for persistence in a database.
- **Optimization**: Create the `ContextOptimizer` to automatically adjust examples.
- **API Integration**: Develop a RESTful API to access the components remotely.
- **Graphical Interface**: Implement an interface for interactive use.

With this initial structure, you can start building on top of it, integrating more features, and optimizing it for specific use cases.


## Summary

synapsense is designed to provide a structured and modular approach to managing context in applications that utilize Large Language Models. By offering tools to manage, build, optimize, and experiment with contextual examples, synapsense aims to make In-Context Learning more accessible and effective, allowing users to maximize the potential of LLMs in various use cases. The planned components, such as ContextOptimizer and ExperimentTracker, will further enhance the library’s capabilities, making it a comprehensive solution for context-aware LLM applications.
