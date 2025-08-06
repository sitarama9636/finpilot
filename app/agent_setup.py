from langchain.agents import initialize_agent, AgentType
from langchain_community.llms import Ollama
from app.main_tools import all_tools

# Step 1: Load your LLM
llm = Ollama(model="llama3.2")  # Update model name if needed

# Step 2: Initialize the Agent with tools and config
agent = initialize_agent(
    tools=all_tools,
    llm=llm,
    agent=AgentType.OPENAI_FUNCTIONS,
    verbose=True,
    handle_parsing_errors=True  # ✅ Prevent crash on LLM parsing errors
)

# Step 3: Run interactive CLI
if __name__ == "__main__":
    while True:
        try:
            user_input = input("Ask your financial assistant: ")
            if user_input.lower() in ["exit", "quit"]:
                print("[👋 Exiting FinPilot]")
                break
            response = agent.invoke({"input": user_input})  # ✅ invoke instead of run
            print("\n🧠 Agent Response:\n", response, "\n")
        except KeyboardInterrupt:
            print("\n[⛔ Stopped]")
            break
