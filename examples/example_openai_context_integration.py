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
            {"role": "system", "content": "You are an expert assistant specialized in Retrieval-Augmented Generation (RAG), In-Context Learning (ICL), and Retrieval-Based Context. Your role is to provide clear, accurate, and detailed explanations of these concepts based on recent academic research. You should assist users by clarifying the differences, applications, and benefits of these methods in large language models (LLMs). When answering, ensure to refer to the latest findings on these techniques, offering examples and insights from research papers to support your explanations."},
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

    # Add some examples for the "AI-Research" context
    context_manager.add_context("AI-Research", [
        "Retrieval-Augmented Generation (RAG) enhances language models by integrating external information retrieval with generation capabilities.",
        "It retrieves relevant knowledge based on the user's query and then generates a response grounded in this context.",
        "The goal of RAG is to improve accuracy and relevance by incorporating external knowledge, making it ideal for tasks like question answering and knowledge grounding.",
        "Retrieval-Augmented Generation (RAG) verbessert Sprachmodelle, indem es externe Informationsabrufe mit Generierungsfunktionen kombiniert.",
        "Es ruft relevantes Wissen basierend auf der Benutzeranfrage ab und generiert dann eine Antwort, die in diesem Kontext verankert ist.",
        "Das Ziel von RAG ist es, die Genauigkeit und Relevanz zu verbessern, indem externes Wissen einbezogen wird, was es ideal für Aufgaben wie die Beantwortung von Fragen und das Fundieren von Wissen macht.",
        "A Geração Aumentada por Recuperação (RAG) melhora os modelos de linguagem ao integrar a recuperação de informações externas com capacidades de geração.",
        "Ela recupera conhecimento relevante com base na consulta do usuário e gera uma resposta fundamentada nesse contexto.",
        "O objetivo do RAG é melhorar a precisão e a relevância, incorporando conhecimento externo, tornando-o ideal para tarefas como respostas a perguntas e fundamentação de conhecimento.",
        "In-Context Learning (ICL) allows language models to adapt to new tasks using examples provided in the input context without retraining.",
        "ICL leverages patterns from the input examples to generate predictions or responses based on the context, making it suitable for a wide range of tasks.",
        "The objective of ICL is to enable flexible learning without explicit fine-tuning, allowing models to perform well even in zero-shot or few-shot scenarios.",
        "In-Context Learning (ICL) ermöglicht es Sprachmodellen, sich anhand von im Eingabekontext bereitgestellten Beispielen an neue Aufgaben anzupassen, ohne dass ein erneutes Training erforderlich ist.",
        "ICL nutzt Muster aus den Eingabebeispielen, um Vorhersagen oder Antworten auf Basis des Kontexts zu generieren, was es für eine Vielzahl von Aufgaben geeignet macht.",
        "Das Ziel von ICL ist es, flexibles Lernen ohne explizites Feintuning zu ermöglichen und Modelle auch in Zero-Shot- oder Few-Shot-Szenarien erfolgreich zu machen.",
        "O Aprendizado no Contexto (ICL) permite que modelos de linguagem se adaptem a novas tarefas usando exemplos fornecidos no contexto de entrada, sem necessidade de retreinamento.",
        "ICL aproveita padrões dos exemplos de entrada para gerar previsões ou respostas com base no contexto, tornando-o adequado para uma ampla gama de tarefas.",
        "O objetivo do ICL é possibilitar o aprendizado flexível sem ajuste fino explícito, permitindo que os modelos tenham bom desempenho mesmo em cenários de zero-shot ou few-shot.",
        "Retrieval-Based Context involves querying an external knowledge base to retrieve relevant information that informs the model's response.",
        "This method is highly effective in ensuring accuracy, especially in tasks that require real-time or up-to-date knowledge.",
        "The primary difference from ICL is that Retrieval-Based Context dynamically accesses external data, while ICL works purely from internal examples.",
        "Der Retrieval-Based Context umfasst das Abfragen einer externen Wissensdatenbank, um relevante Informationen abzurufen, die die Antwort des Modells beeinflussen.",
        "Diese Methode ist besonders effektiv, um Genauigkeit zu gewährleisten, insbesondere bei Aufgaben, die Echtzeit- oder aktuelle Kenntnisse erfordern.",
        "Der Hauptunterschied zu ICL besteht darin, dass der Retrieval-Based Context dynamisch auf externe Daten zugreift, während ICL rein auf internen Beispielen basiert.",
        "O Contexto Baseado em Recuperação envolve a consulta a uma base de conhecimento externa para recuperar informações relevantes que informam a resposta do modelo.",
        "Esse método é altamente eficaz em garantir precisão, especialmente em tarefas que exigem conhecimento em tempo real ou atualizado.",
        "A principal diferença do ICL é que o Contexto Baseado em Recuperação acessa dinamicamente dados externos, enquanto o ICL trabalha puramente com exemplos internos."

    ])

    # Get the context examples
    context_examples = context_manager.get_context("AI-Research")

    # Evaluate the relevance of each context example
    for example in context_examples:
        # For demonstration purposes, assume a performance metric of 0.5
        context_optimizer.evaluate_relevance(example, "AI-Research", 0.5)

    # Adjust the context examples based on their relevance
    context_optimizer.adjust_contexts()

    # Get the optimized context examples
    optimized_context = context_optimizer.get_optimized_context()

    # Build a prompt for the "AI-Research" context with a user input
    user_input = "Explain if In-Context Learning (ICL) with Retrieval-Augmented Generation (RAG) improves the accuracy of language models in providing relevant responses, particularly in real-time applications."
    prompt = prompt_builder.build_prompt("AI-Research", user_input)
    # Print the built prompt
    print(prompt)

    # Call OpenAI API
    model = "gpt-4o"
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