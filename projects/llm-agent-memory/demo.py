"""Offline CLI demo for persistent agent memory."""

from agent import build_local_agent


def main() -> None:
    agent = build_local_agent()
    agent.remember("I am building an AI engineering portfolio with Python and machine learning.")
    agent.remember("My current LLM project uses Gemini, LangChain, and SQLite memory.")

    print("LLM Agent Memory Demo")
    print(f"stored_messages={agent.stats()}")
    for result in agent.recall("Gemini SQLite"):
        print(f"{result['role']}: {result['content']}")
    print("Offline memory path verified; connect Gemini separately for live generation.")


if __name__ == "__main__":
    main()
