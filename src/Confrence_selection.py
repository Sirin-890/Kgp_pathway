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
  return completion.choices[0].message

def neurips_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": NeurIPS_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message
def emnlp_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": EMNLP_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message
def kdd_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": KDD_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message
def tmlr_suggestion(query):
  completion = client.chat.completions.create(
  model=MODEL,
  messages=[
    {"role": "system", "content": TMLR_SYSTEM_PROMPT},
    {"role": "user", "content": query}
  ]
  )
  return completion.choices[0].message

def final_conference():
  query=''
  score_cvpr= cvpr_suggestion(query)
  score_tmlr= tmlr_suggestion(query)
  score_kdd=  kdd_suggestion(query)
  score_emnlp = emnlp_suggestion(query)
  score_neurips= neurips_suggestion(query)
  final_score = max(score_cvpr,score_emnlp,score_kdd,score_neurips,score_tmlr)
  return final_score
    

if __name__=='_main_':
  query=''
  final_conference(query)
  

