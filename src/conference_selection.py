from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor
from src.config import *
from loguru import logger
import json
import re

client = OpenAI()

def parse_tool_call_str(tool_call_str: str):
    pattern = r'</?tool_call>'
    clean_tags = re.sub(pattern, '', tool_call_str)
    
    try:
        tool_call_json = json.loads(clean_tags)
        return tool_call_json
    except json.JSONDecodeError:
        return clean_tags
    except Exception as e:
        print(f"Unexpected error: {e}")
        return "There was some error parsing the Tool's output"

def cvpr_suggestion(research_paper: str) -> dict:
    tool_chat_history = [
        {
            "role": "system",
            "content": TOOL_SYSTEM_PROMPT_CVPR
        }
    ]

    user_msg = {
        "role": "user",
        "content": research_paper
    }

    tool_chat_history.append(user_msg)

    output = client.chat.completions.create(
        messages=tool_chat_history,
        model=MODEL
    ).choices[0].message.content

    # Extract tool call strings using regular expressions
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_calls = re.findall(tool_call_pattern, output, re.DOTALL)

    # Loop over each tool call and extract arguments
    tool_call_json = parse_tool_call_str(tool_calls[0])  # Parse the cleaned tool call string
    if isinstance(tool_call_json, dict) and "arguments" in tool_call_json:
        args = tool_call_json["arguments"]
    return args      

def neurips_suggestion(research_paper: str) -> str:
    tool_chat_history = [
        {
            "role": "system",
            "content": TOOL_SYSTEM_PROMPT_NEUR_IPS
        }
    ]

    user_msg = {
        "role": "user",
        "content": research_paper
    }

    tool_chat_history.append(user_msg)

    output = client.chat.completions.create(
        messages=tool_chat_history,
        model=MODEL
    ).choices[0].message.content

    # Extract tool call strings using regular expressions
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_calls = re.findall(tool_call_pattern, output, re.DOTALL)

    # Loop over each tool call and extract arguments
    tool_call_json = parse_tool_call_str(tool_calls[0])  # Parse the cleaned tool call string
    if isinstance(tool_call_json, dict) and "arguments" in tool_call_json:
        args = tool_call_json["arguments"]
    return args 

def emnlp_suggestion(research_paper: str) -> str:
    tool_chat_history = [
        {
            "role": "system",
            "content": TOOL_SYSTEM_PROMPT_EMNLP
        }
    ]

    user_msg = {
        "role": "user",
        "content": research_paper
    }

    tool_chat_history.append(user_msg)

    output = client.chat.completions.create(
        messages=tool_chat_history,
        model=MODEL
    ).choices[0].message.content

    # Extract tool call strings using regular expressions
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_calls = re.findall(tool_call_pattern, output, re.DOTALL)

    # Loop over each tool call and extract arguments
    tool_call_json = parse_tool_call_str(tool_calls[0])  # Parse the cleaned tool call string
    if isinstance(tool_call_json, dict) and "arguments" in tool_call_json:
        args = tool_call_json["arguments"]
    return args 

def kdd_suggestion(research_paper: str) -> str:
    tool_chat_history = [
        {
            "role": "system",
            "content": TOOL_SYSTEM_PROMPT_KDD
        }
    ]

    user_msg = {
        "role": "user",
        "content": research_paper
    }

    tool_chat_history.append(user_msg)

    output = client.chat.completions.create(
        messages=tool_chat_history,
        model=MODEL
    ).choices[0].message.content

    # Extract tool call strings using regular expressions
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_calls = re.findall(tool_call_pattern, output, re.DOTALL)

    # Loop over each tool call and extract arguments
    tool_call_json = parse_tool_call_str(tool_calls[0])  # Parse the cleaned tool call string
    if isinstance(tool_call_json, dict) and "arguments" in tool_call_json:
        args = tool_call_json["arguments"]
    return args 

def tmlr_suggestion(research_paper: str) -> str:
    tool_chat_history = [
        {
            "role": "system",
            "content": TOOL_SYSTEM_PROMPT_TMLR
        }
    ]

    user_msg = {
        "role": "user",
        "content": research_paper
    }

    tool_chat_history.append(user_msg)

    output = client.chat.completions.create(
        messages=tool_chat_history,
        model=MODEL
    ).choices[0].message.content

    # Extract tool call strings using regular expressions
    tool_call_pattern = r'<tool_call>(.*?)</tool_call>'
    tool_calls = re.findall(tool_call_pattern, output, re.DOTALL)

    # Loop over each tool call and extract arguments
    tool_call_json = parse_tool_call_str(tool_calls[0])  # Parse the cleaned tool call string
    if isinstance(tool_call_json, dict) and "arguments" in tool_call_json:
        args = tool_call_json["arguments"]
    return args 

def final_conference(research_paper: str) -> list:
    with ThreadPoolExecutor() as executor:
      future_cvpr = executor.submit(cvpr_suggestion, research_paper)
      future_tmlr = executor.submit(tmlr_suggestion, research_paper)
      future_kdd = executor.submit(kdd_suggestion, research_paper)
      future_emnlp = executor.submit(emnlp_suggestion, research_paper)
      future_neurips = executor.submit(neurips_suggestion, research_paper)

      dict_cvpr = future_cvpr.result()
      dict_tmlr = future_tmlr.result()
      dict_kdd = future_kdd.result()
      dict_emnlp = future_emnlp.result()
      dict_neurips = future_neurips.result()

    # Consolidating scores into a dictionary with their names
    all_dicts = {
        "cvpr": dict_cvpr,
        "tmlr": dict_tmlr,
        "kdd": dict_kdd,
        "emnlp": dict_emnlp,
        "neurips": dict_neurips
    }

    logger.debug(f"CVPR: {all_dicts['cvpr']['score']} | TMLR: {all_dicts['tmlr']['score']} | KDD: {all_dicts['kdd']['score']} | EMNLP: {all_dicts['emnlp']['score']} | NEURIPS: {all_dicts['neurips']['score']}")

    # Finding the dict with the maximum score
    max_name, max_dict = max(all_dicts.items(), key=lambda x: x[1]["score"])

    # Displaying the name and reason in the desired format
    output = [max_name, max_dict["reason"]]
    return output 

if __name__=='_main_':
  research_paper=''
  print(final_conference(research_paper))