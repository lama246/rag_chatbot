import os

from groq import Groq
from dotenv import load_dotenv

load_dotenv()

client = Groq(
    api_key=os.getenv(
        "GROQ_API_KEY"
    )
)


def generate_answer(
        question,
        context):

    prompt = f"""
            You are an advanced Website RAG Assistant.

            Answer ONLY using the retrieved context.

            Instructions:

            - Give a detailed answer.
            - Mention important facts.
            - Combine information from multiple sources.
            - If a title exists, mention it.
            - Do not invent information.
            - If the answer is unavailable in the context, clearly say so.

            Context:
            {context}

            Question:
            {question}
            """

    response = (
        client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ],
            temperature=0
        )
    )

    return (
        response
        .choices[0]
        .message
        .content
    )