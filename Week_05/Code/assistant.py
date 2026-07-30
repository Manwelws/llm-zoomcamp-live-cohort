import os
import sys

from db_save import save_conversation
from dotenv import load_dotenv
from ingest import build_index, load_faq_data
from metrics import RAGWithMetrics
from openai import OpenAI


def create_assistant():
    load_dotenv()

    documents = load_faq_data()
    index = build_index(documents)

    return RAGWithMetrics(
        index=index,
        llm_client=OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        ),
    )


if __name__ == "__main__":
    assistant = create_assistant()

    query = "How do I join the course?"
    if len(sys.argv) > 1:
        query = sys.argv[1]

    answer = assistant.rag(query)
    save_conversation(assistant.last_call, query, "llm-zoomcamp")
    print(answer)
