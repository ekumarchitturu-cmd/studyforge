import openai
import os
from dotenv import load_dotenv

load_dotenv()

class AIAgent:
    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        if not self.api_key:
            raise ValueError("OpenAI API key not found in .env file")
        openai.api_key = self.api_key

    def generate_study_plan(self, prompt):
        """
        Call OpenAI API to generate study plan
        """
        try:
            response = openai.chat.completions.create(
                model="gpt-4",  # or "gpt-3.5-turbo" for cheaper option
                messages=[
                    {
                        "role": "system",
                        "content": "You are an expert educational consultant who creates personalized, detailed study plans for students of all ages and fields."
                    },
                    {
                        "role": "user",
                        "content": prompt
                    }
                ],
                temperature=0.7,
                max_tokens=3000
            )

            return response.choices[0].message.content

        except Exception as e:
            return f"Error generating study plan: {str(e)}"
