from src.prompts import get_all_prompts
from src.vectorstore.vectorstore import get_vectorstore

vectorstore = get_vectorstore()

class LegalAgent():
    def __init__(self, role, llm):
        self.role = role
        self.llm = llm
        self.vectorstore = vectorstore
        self.prompts = get_all_prompts()

    def get_prompt_instruction(self):
        role_prompt = self.prompts[self.role]
        response_format = self.prompts["response_format"]
        citation_format = self.prompts["citation_format"]
        checklist = self.prompts[f"{self.role}_checklist"]

        return "\n\n".join([role_prompt, response_format, citation_format, checklist])

class DefendantAgent(LegalAgent):
    def __init__(self, llm):
        super().__init__(role="defense", llm=llm)
    
    def respond(self, user_question: str, prior_turns: str = ""):
        prompt = self.get_prompt_instruction()

        n_results = 5
        contexts = self.vectorstore.query(user_query=user_question,
                                          n_results=n_results)
        context_text = "\n\n".join(contexts)

        print("[DEBUG] n contexts:", len(contexts))
        print("[DEBUG] first 300 chars:\n", context_text[:300])

        prompt += f"""
        CONTEXT:
        {context_text}

        USER QUESTION:
        {user_question}

        PROSECUTION'S PRIOR ARGUMENT:
        {prior_turns}

        Defense attorney, respond using the required structure.
        """

        return self.llm.invoke(prompt).content

class ProsecutorAgent(LegalAgent):
    def __init__(self, llm):
        super().__init__(role="prosecution", llm=llm)

    def respond(self, user_question: str, prior_turns: str = ""):
        prompt = self.get_prompt_instruction()

        n_results = 5
        contexts = self.vectorstore.query(user_query=user_question,
                                          n_results=n_results)
        context_text = "\n\n".join(contexts)

        prompt += f"""
        CONTEXT:
        {context_text}
        
        USER QUESTION:
        {user_question}

        DEFENSE'S PRIOR ARGUMENT:
        {prior_turns}

        Prosecutor, respond using required structure.
        """

        return self.llm.invoke(prompt).content

class JudgeAgent(LegalAgent):
    def __init__(self, llm):
        super().__init__(role="judge", llm=llm)

    def summarize(self, question, prosecution, defense):
        prompt = self.get_prompt_instruction()

        n_results = 5
        contexts = self.vectorstore.query(user_query=question,
                                          n_results=n_results)
        context_text = "\n\n".join(contexts)

        prompt += f"""
        CONTEXT:
        {context_text}

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