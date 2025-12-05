import re
from abc import ABC, abstractmethod
from src.prompts import get_all_prompts
from src.vectorstore.vectorstore import get_vectorstore

class LegalAgent(ABC):
    
    def __init__(self, role, llm):
        self.role = role
        self.llm = llm
        self.vectorstore = get_vectorstore()
        self.prompts = get_all_prompts()
        self.max_search_iterations = 3
    
    def get_prompt_instruction(self):
        """Build the complete prompt instruction for this agent."""
        role_prompt = self.prompts[self.role]
        response_format = self.prompts["response_format"]
        citation_format = self.prompts["citation_format"]
        checklist = self.prompts[f"{self.role}_checklist"]
        return "\n\n".join([role_prompt, response_format, citation_format, checklist])
    
    def extract_search_queries(self, text: str) -> list:
        """Extract [SEARCH: query] patterns from agent response."""
        pattern = r'\[SEARCH:\s*([^\]]+)\]'
        return [q.strip() for q in re.findall(pattern, text)]
    
    def query_vectorstore(self, query: str, n_results: int = 5) -> str:
        """Query the vector store and return formatted context."""
        contexts = self.vectorstore.query(user_query=query, n_results=n_results)
        return "\n\n".join(contexts)
    
    def format_legal_results(self, context_text: str) -> str:
        """Format vector store results per RAG Integration Protocol."""
        return f"""LEGAL RESEARCH RESULTS:

{context_text}

You may now incorporate this authority into your argument."""
    
    def process_with_rag(self, initial_prompt: str, user_question: str) -> str:
        """
        Process prompt with RAG loop: query initial context, generate response,
        detect [SEARCH:] requests, query with agent's query, continue until done.
        """
        n_results = 5
        initial_context = self.query_vectorstore(user_question, n_results)
        
        prompt_with_context = f"{initial_prompt}\n\nCONTEXT:\n{initial_context}"
        
        response = self.llm.invoke(prompt_with_context).content
        
        iteration = 0
        while iteration < self.max_search_iterations:
            queries = self.extract_search_queries(response)
            
            if not queries:
                break
            
            agent_query = queries[0]
            print(f"[{self.role.upper()}] Agent requested search: {agent_query}")
            
            search_context = self.query_vectorstore(agent_query, n_results)
            formatted_results = self.format_legal_results(search_context)
            
            continuation_prompt = f"""{formatted_results}

Continue your argument, incorporating the case law above.

Your previous response was:
{response}

Now continue with citations from the legal research results provided."""
            
            response = self.llm.invoke(continuation_prompt).content
            iteration += 1
        
        return response
    
    @abstractmethod
    def build_full_prompt(self, **kwargs) -> str:
        """Build the complete prompt for this agent. Subclasses must implement."""
        pass


class DefendantAgent(LegalAgent):
    def __init__(self, llm):
        super().__init__(role="defense", llm=llm)
    
    def build_full_prompt(self, user_question: str, prior_turns: str = "") -> str:
        prompt = self.get_prompt_instruction()
        prompt += f"""

USER QUESTION:
{user_question}

PROSECUTION'S PRIOR ARGUMENT:
{prior_turns}

Defense attorney, respond using the required structure.
"""
        return prompt
    
    def respond(self, user_question: str, prior_turns: str = "") -> str:
        prompt = self.build_full_prompt(user_question=user_question, prior_turns=prior_turns)
        return self.process_with_rag(prompt, user_question)


class ProsecutorAgent(LegalAgent):
    def __init__(self, llm):
        super().__init__(role="prosecution", llm=llm)
    
    def build_full_prompt(self, user_question: str, prior_turns: str = "") -> str:
        prompt = self.get_prompt_instruction()
        prompt += f"""

USER QUESTION:
{user_question}

DEFENSE'S PRIOR ARGUMENT:
{prior_turns}

Prosecutor, respond using required structure.
"""
        return prompt
    
    def respond(self, user_question: str, prior_turns: str = "") -> str:
        prompt = self.build_full_prompt(user_question=user_question, prior_turns=prior_turns)
        return self.process_with_rag(prompt, user_question)


class JudgeAgent(LegalAgent):
    def __init__(self, llm):
        super().__init__(role="judge", llm=llm)
    
    def build_full_prompt(self, question: str, prosecution: str, defense: str) -> str:
        prompt = self.get_prompt_instruction()
        prompt += f"""

CASE SUMMARY REQUEST:
QUESTION:
{question}

PROSECUTION POSITION:
{prosecution}

DEFENSE POSITION:
{defense}

Judge, provide a neutral, structured summary following the required SUMMARY PROTOCOL.
"""
        return prompt
    
    def summarize(self, question: str, prosecution: str, defense: str) -> str:
        prompt = self.build_full_prompt(question=question, prosecution=prosecution, defense=defense)
        return self.process_with_rag(prompt, question)
        """

        return self.llm.invoke(prompt).content
