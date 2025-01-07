from openai import OpenAI
from config import EVALUATOR_PROMPT, MODEL

client = OpenAI()

def evaluate(research_paper: str, benchmark_papers: str) -> str:
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
      {   
          "role": "system", 
          "content": "You are a helpful assistant." + EVALUATOR_PROMPT
      },
      {
          "role": "user",
          "content": f" Research Paper: {research_paper} \n\n Benchmark Papers: {benchmark_papers}"
      }
  ]
  )
  return completion.choices[0].message.content