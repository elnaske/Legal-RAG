from src.prompts.prompts import get_all_prompts

class DefendantAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompts = get_all_prompts()

    def respond(self, user_question: str, prior_turns: str = ""):
        defense_prompt = self.prompts["defense"]
        response_format = self.prompts["response_format"]
        citation_format = self.prompts["citation_format"]
        checklist = self.prompts["defense_checklist"]

        prompt = f"""
{defense_prompt}

{response_format}

{citation_format}

{checklist}

USER QUESTION:
{user_question}

PROSECUTION'S PRIOR ARGUMENT:
{prior_turns}

Defense attorney, respond using the required structure.
"""

        return self.llm.invoke(prompt).content

