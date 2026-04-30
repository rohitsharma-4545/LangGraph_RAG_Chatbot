from langchain_openai import ChatOpenAI
from app.config import settings
from openai import RateLimitError

llm = ChatOpenAI(
    base_url=settings.LLM_BASE_URL,
    api_key=settings.LLM_API_KEY,
    model=settings.MODEL_NAME,
    streaming=True
)

def generate_response(prompt: str):
    response = llm.invoke(prompt)
    return response.content

def stream_response(prompt: str):
    try:
        for chunk in llm.stream(prompt):
            if chunk.content:
                yield chunk.content

    except RateLimitError:
        yield "ERROR: Rate limit exceeded. Please try again later."

    except Exception as e:
        yield f"ERROR: {str(e)}"

# def stream_response(prompt: str):
#     mock_answer = [
#         "This is a test response.",
#         "No LLM API was called.",
#         "This is a fixed 4-line output.",
#         "Used only for local testing."
#     ]

#     for line in mock_answer:
#         yield line + "\n"