from src.utils import load_config
# from src.agents.agent_controller import run_agent_pipeline
from src.agents import run_agent_pipeline

def main():
    config = load_config()

    print("=== Legal-RAG Agent System ===")
    user_query = input("Ask a legal question:\n> ")

    answer = run_agent_pipeline(user_query, config)

    print("\n=== Final Answer ===\n")
    print(answer)

if __name__ == "__main__":
    main()
