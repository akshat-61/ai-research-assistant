from openai import AsyncOpenAI
from core.config import settings

client = AsyncOpenAI(
    base_url=settings.LLM_BASE_URL,
    api_key="sk-local-dummy-key"
)

async def generate_chat_response(query: str, context: str) -> str:
    """
    Generates a chat response using the LLM given a user query and a hardcoded context.
    """
    system_prompt = (
        "You are an AI Research Assistant. Answer the user's question "
        "based strictly on the provided context."
    )
    
    user_prompt = f"Context: {context}\n\nQuestion: {query}"
    
    response = await client.chat.completions.create(
        model=settings.MODEL_NAME,
        messages=[
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt},
        ],
        temperature=settings.TEMPERATURE,
    )
    
    return response.choices[0].message.content or ""
