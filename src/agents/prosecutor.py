from src.prompts.prompts import get_all_prompts

class ProsecutorAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompts = get_all_prompts()

    def respond(self, user_question: str, prior_turns: str = ""):
        prosecution_prompt = self.prompts["prosecution"]
        response_format = self.prompts["response_format"]
        citation_format = self.prompts["citation_format"]
        checklist = self.prompts["prosecution_checklist"]

        prompt = f"""
{prosecution_prompt}

{response_format}

{citation_format}

{checklist}

USER QUESTION:
{user_question}

DEFENSE PRIOR ARGUMENT:
{prior_turns}

Prosecutor, respond using required structure.
"""

        return self.llm.invoke(prompt).content

