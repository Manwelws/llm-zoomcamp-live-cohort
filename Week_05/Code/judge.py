import json  # noqa: F401
import os
from typing import Literal

import instructor
from dotenv import load_dotenv
from evaluation_utils import instructor_or
from openai import OpenAI
from pydantic import BaseModel


class RelevanceVerdict(BaseModel):
    relevance: Literal["NON_RELEVANT", "PARTLY_RELEVANT", "RELEVANT"]
    explanation: str


judge_instructions = """
You are an expert evaluator for a RAG system.
Analyze the relevance of the generated answer to the given question.

Classify the answer as:
- RELEVANT: the answer addresses the question
- PARTLY_RELEVANT: the answer partially addresses the question
- NON_RELEVANT: the answer does not address the question
""".strip()

judge_prompt = """
Question: {question}
Generated Answer: {answer}
""".strip()


def evaluate_relevance(question, answer, client=None):
    if client is None:
        client = OpenAI(
            base_url="https://openrouter.ai/api/v1",
            api_key=os.getenv("OPENROUTER_API_KEY"),
        )

    prompt = judge_prompt.format(question=question, answer=answer)

    result = instructor_or(client, judge_instructions, prompt, RelevanceVerdict)

    return result.relevance, result.explanation


if __name__ == "__main__":
    load_dotenv()

    question = "Can I still join the course?"
    answer = "Yes, you can still join. The course is self-paced."

    relevance, explanation = evaluate_relevance(question, answer)
    print(relevance)
    print(explanation)
