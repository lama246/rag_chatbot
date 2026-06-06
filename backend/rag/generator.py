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

        Format:

        ## Title

        ## Detailed Explanation

        ## Important Points

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