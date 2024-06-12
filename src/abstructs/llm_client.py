import instructor
from groq import Groq
from openai import OpenAI
from abstructs.config import settings
from abstructs.database import StructuredResponse
from abstructs.logging_config import setup_logging

logger = setup_logging()

groq_models = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
]

openai_models = [
    "gpt-4o",
    "gpt-4",
    "gpt-4-turbo",
    "gpt-3.5-turbo",
]

selected_model = "gpt-4o"


async def get_llm_response(abstract: str) -> StructuredResponse:
    if selected_model in groq_models:
        client = instructor.from_groq(
            Groq(api_key=settings.GROQ_API_KEY), mode=instructor.Mode.TOOLS
        )
    elif selected_model in openai_models:
        client = instructor.from_openai(OpenAI(api_key=settings.OPENAI_API_KEY))
    else:
        raise ValueError(f"Unsupported model: {selected_model}")

    messages = [{"role": "user", "content": abstract}]
    llm_response = client.chat.completions.create(
        model=selected_model,
        response_model=StructuredResponse,
        messages=messages,
    )
    logger.info(f"Sent to LLM: {messages}")
    logger.info(f"Received from LLM: {llm_response}")
    return llm_response
