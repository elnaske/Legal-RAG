import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# from src.agents.prosecutor import ProsecutorAgent
# from src.agents.defendant import DefendantAgent
# from src.agents.judge import JudgeAgent

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

    # llm = ChatOpenAI(
    #     model="llama-3.1-8b-instant",
    #     api_key=os.getenv("GROQ_API_KEY"),
    #     base_url="https://api.groq.com/openai/v1",
    #     temperature=0.3,
    # )

    prosecutor = ProsecutorAgent(llm)
    defense = DefendantAgent(llm)
    judge = JudgeAgent(llm)

    pros_response = prosecutor.respond(
        user_question,
        prior_turns=""
    )
    print("\n--- Prosecution Opening ---")
    print(pros_response)

    defense_response = defense.respond(
        user_question,
        prior_turns=pros_response
    )
    print("\n--- Defense Opening ---")
    print(defense_response)

    judge_summary = judge.summarize(
        question=user_question,
        prosecution=pros_response,
        defense=defense_response
    )
    print("\n--- Judge Summary ---")
    print(judge_summary)

    return judge_summary

