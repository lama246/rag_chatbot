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
        You are an AI Website Assistant.

        Answer ONLY from the retrieved website content.

        Answer in this format:

        # Summary

        Short answer.

        # Key Points

        • Point 1

        • Point 2

        • Point 3

        # Website Evidence

        Mention which page supplied the information.

        # Confidence

        State whether answer is directly found or inferred.

        Rules:

        - Use information from the context only.
        - Combine information from multiple pages if relevant.
        - Give detailed explanations.
        - If information is unavailable, say:
        "The indexed website does not contain information about this."

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