from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from config import *
from loguru import logger

client = OpenAI()

def cvpr_suggestion(research_paper: str) -> str:
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": CVPR_SYSTEM_PROMPT},
    {"role": "user", "content": research_paper}
  ]
  )
  return completion.choices[0].message.content

def neurips_suggestion(research_paper: str) -> str:
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": NS_SYSTEM_PROMPT},
    {"role": "user", "content": research_paper}
  ]
  )
  return completion.choices[0].message.content

def emnlp_suggestion(research_paper: str) -> str:
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": EMNLP_SYSTEM_PROMPT},
    {"role": "user", "content": research_paper}
  ]
  )
  return completion.choices[0].message.content

def kdd_suggestion(research_paper: str) -> str:
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": KDD_SYSTEM_PROMPT},
    {"role": "user", "content": research_paper}
  ]
  )
  return completion.choices[0].message.content

def tmlr_suggestion(research_paper: str) -> str:
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": TMLR_SYSTEM_PROMPT},
    {"role": "user", "content": research_paper}
  ]
  )
  return completion.choices[0].message.content

def final_conference(research_paper: str) -> str:
  with ThreadPoolExecutor() as executor:
    future_cvpr = executor.submit(cvpr_suggestion, research_paper)
    future_tmlr = executor.submit(cvpr_suggestion, research_paper)
    future_kdd = executor.submit(cvpr_suggestion, research_paper)
    future_emnlp = executor.submit(cvpr_suggestion, research_paper)
    future_neurips = executor.submit(cvpr_suggestion, research_paper)

    score_cvpr = future_cvpr.result()
    score_tmlr = future_tmlr.result()
    score_kdd = future_kdd.result()
    score_emnlp = future_emnlp.result()
    score_neurips = future_neurips.result()

  scores = {
      "cvpr": score_cvpr,
      "tmlr": score_tmlr,
      "kdd": score_kdd,
      "emnlp": score_emnlp,
      "neurips": score_neurips
  }

  logger.info(f"Scores: {scores}")

  final_conference = max(scores, key=scores.get)
  return final_conference

if __name__=='_main_':
  research_paper=''
  final_conference(research_paper)
  

