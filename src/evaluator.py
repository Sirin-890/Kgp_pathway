import os
import google.generativeai as genai
from openai import OpenAI
from src.config import GEMINI_SYSTEM_PROMPT, MODEL

client = OpenAI()

def evaluate(research_paper: str) -> str:
    genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
    model = genai.GenerativeModel(
        model_name="gemini-1.5-flash",
        system_instruction=GEMINI_SYSTEM_PROMPT
        )
    response = model.generate_content(f"Research Paper: {research_paper} \n\n. Give a response strictly in Yes or No")
    return (response.text).replace("\n","")
