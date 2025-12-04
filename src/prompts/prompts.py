"""
Legal-RAG System Prompts Module

Author: mandito
Version: 1.0
"""

from typing import Dict
import yaml

PROMPT_FILEPATH = "./prompts/prompts.yaml"

def get_all_prompts(path: str = PROMPT_FILEPATH) -> Dict[str, str]:
    """
    Loads all available prompts from .yaml and returns them as a dict.

    Args:
        path (str): Filepath to a .yaml file containing the prompts. Defaults to "./prompts/prompts.yaml".

    Returns:
        A dict containing the prompts.

    Examples:
        >>> all_prompts = get_all_prompts()
        >>> print(all_prompts["defense"])
        ROLE: You are a criminal defense attorney representing the defendant. ...

    """
    with open(path, "r") as f:
        prompt_dict = yaml.safe_load(f)
    return prompt_dict

def get_prompt(prompt: str, path: str = PROMPT_FILEPATH) -> str:
    """
    Loads the specified prompt from .yaml and returns it as a str.

    Args:
        prompt (str): Key of the desired prompt. Available options can be found in `prompts.AVAILABLE_PROMPTS`.
        path (str): Filepath to a .yaml file containing the prompts. Defaults to "./prompts/prompts.yaml".
    
    Returns:
        A str containing the prompt.

    Examples:
        >>> defense_prompt = get_prompt("defense")
        >>> print(defense_prompt)
        ROLE: You are a criminal defense attorney representing the defendant. ...

    """
    prompt_dict = get_all_prompts(path)
    return prompt_dict[prompt]
