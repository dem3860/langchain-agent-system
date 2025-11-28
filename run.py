from __future__ import annotations

from dotenv import load_dotenv
from langchain_core.messages import HumanMessage

from agent import app  # agent/__init__.py で re-export している app


load_dotenv()


def main() -> None:
    print("=== LangChain create_agent 学習サポートエージェント ===")
    print("exit / quit で終了します。\n")

    chat_history = []

    while True:
        try:
            user_input = input("User: ")
            if user_input.lower() in ["exit", "quit"]:
                break

            if not user_input.strip():
                continue

            # LangGraph / create_agent 共通の State 形式に合わせる
            message = HumanMessage(content=user_input)

            print("\n--- Agent Processing ---")

            # create_agent が返す app は .invoke で呼べる
            final_state = app.invoke({"messages": chat_history + [message]})

            # state 内の messages を更新
            chat_history = final_state["messages"]

            ai_reply = chat_history[-1].content
            print(f"\nAgent: {ai_reply}\n")

        except KeyboardInterrupt:
            print("\nExiting.")
            break
        except Exception as e:
            print(f"\nError: {e}\n")
            continue


if __name__ == "__main__":
    main()
