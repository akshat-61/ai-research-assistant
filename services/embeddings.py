from openai import AsyncOpenAI
from core.config import settings

# Initialize AsyncOpenAI client
# Using a dummy API key since local inference servers usually don't require one,
# but the OpenAI client expects it to be present.
client = AsyncOpenAI(
    base_url=settings.LLM_BASE_URL,
    api_key="sk-local-dummy-key"
)

async def generate_embeddings(texts: list[str]) -> list[list[float]]:
    """
    Generate vector embeddings for a list of text strings.
    """
    if not texts:
        return []
        
    response = await client.embeddings.create(
        model=settings.EMBEDDING_MODEL,
        input=texts
    )
    
    # Extract embeddings from the response
    # The response.data contains objects with the 'embedding' field
    embeddings = [item.embedding for item in response.data]
    
    return embeddings
