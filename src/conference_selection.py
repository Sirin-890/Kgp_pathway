from openai import OpenAI
from config import *

client = OpenAI()

def cvpr_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": CVPR_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message.content

def neurips_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": NS_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message.content

def emnlp_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": EMNLP_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message.content

def kdd_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": KDD_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message.content

def tmlr_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": TMLR_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message.content

def final_conference():
  query = ''
  score_cvpr = cvpr_suggestion(query)
  score_tmlr = tmlr_suggestion(query)
  score_kdd = kdd_suggestion(query)
  score_emnlp = emnlp_suggestion(query)
  score_neurips = neurips_suggestion(query)

  scores = {
      "cvpr": score_cvpr,
      "tmlr": score_tmlr,
      "kdd": score_kdd,
      "emnlp": score_emnlp,
      "neurips": score_neurips
  }

  final_conference = max(scores, key=scores.get)
  return final_conference

if __name__=='_main_':
  query=''
  final_conference(query)
  

