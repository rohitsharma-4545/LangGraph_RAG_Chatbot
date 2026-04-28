from langchain_openai import ChatOpenAI
from app.config import settings

llm = ChatOpenAI(
    base_url=settings.LLM_BASE_URL,
    api_key=settings.LLM_API_KEY,
    model=settings.MODEL_NAME,
    streaming=True
)

# def stream_response(prompt: str):
#     for chunk in llm.stream(prompt):
#         if chunk.content:
#             yield chunk.content

def stream_response(prompt: str):
    mock_answer = [
        "This is a test response.",
        "No LLM API was called.",
        "This is a fixed 4-line output.",
        "Used only for local testing."
    ]

    for line in mock_answer:
        yield line + "\n"