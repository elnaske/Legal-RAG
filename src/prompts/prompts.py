"""
Legal-RAG System Prompts Module

Author: mandito
Version: 1.0
"""

from typing import Dict
import yaml

PROMPT_FILEPATH = "./prompts/prompts.yaml"

def get_all_prompts(path: str = PROMPT_FILEPATH) -> Dict[str, str]:
    with open(path, "r") as f:
        prompt_dict = yaml.safe_load(f)
    return prompt_dict

def get_prompt(prompt: str, path: str = PROMPT_FILEPATH) -> str:
    prompt_dict = get_all_prompts(path)
    return prompt_dict[prompt]