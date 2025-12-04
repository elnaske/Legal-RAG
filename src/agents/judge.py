from src.prompts.prompts import get_all_prompts

class JudgeAgent:
    def __init__(self, llm):
        self.llm = llm
        self.prompts = get_all_prompts()   # loads ALL protocols

    def summarize(self, question, prosecution, defense):
        judge_prompt = self.prompts["judge"]
        response_format = self.prompts["response_format"]
        citation_format = self.prompts["citation_format"]
        checklist = self.prompts["judge_checklist"]

        prompt = f"""
{judge_prompt}

{response_format}

{citation_format}

{checklist}

CASE SUMMARY REQUEST:

QUESTION:
{question}

PROSECUTION POSITION:
{prosecution}

DEFENSE POSITION:
{defense}

Judge, provide a **neutral**, structured summary following the required SUMMARY PROTOCOL.
"""

        return self.llm.invoke(prompt).content

