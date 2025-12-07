import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from src.agents import ProsecutorAgent, DefendantAgent, JudgeAgent

def run_agent_pipeline(user_question: str, config: dict):
    print("\n=== Legal-RAG Agent System ===")
    
    load_dotenv()
    
    llm = ChatOpenAI(
        model=config["agents"]["model_name"],
        api_key=os.getenv(config["agents"]["API_key_name"]),
        base_url=config["agents"]["API_base_url"],
        temperature=config["agents"]["temperature"],
    )
    
    prosecutor = ProsecutorAgent(llm)
    defense = DefendantAgent(llm)
    judge = JudgeAgent(llm)
    
    print("\n--- Prosecution Opening ---")
    pros_response = prosecutor.respond(
        user_question,
        prior_turns=""
    )
    print(pros_response)
    
    print("\n--- Defense Opening ---")
    defense_response = defense.respond(
        user_question,
        prior_turns=pros_response
    )
    print(defense_response)
    
    print("\n--- Judge Summary ---")
    judge_summary = judge.summarize(
        question=user_question,
        prosecution=pros_response,
        defense=defense_response
    )
    print(judge_summary)
    
    return judge_summary
