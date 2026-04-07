import os
from groq import Groq

class GPTHandler:
    def __init__(self):
        api_key = os.getenv("GROQ_API_KEY")
        if not api_key:
            raise ValueError("GROQ_API_KEY is not set")
        self.client = Groq(api_key=api_key)

    def generate_response(self, chat_history, username="Founder"):
        messages = [
            {
                "role": "system",
                "content": (
                    f"You are a Startup Mentor AI helping {username} in India.\n"
                    "Provide responses as friendly, mentor-like guidance."
                )
            }
        ]
        messages.extend(chat_history)

        try:
            completion = self.client.chat.completions.create(
                model="llama-3.1-8b-instant",
                messages=messages,
                max_tokens=650,
                temperature=0.4
            )
            raw_response = completion.choices[0].message.content.strip()
            return raw_response
        except Exception as e:
            return f"Error generating response: {str(e)}"
