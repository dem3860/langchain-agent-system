# agent/create_agent_version/agent.py
from __future__ import annotations
from langchain.agents import create_agent
from .tools import tools

from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain.messages import ToolMessage
from langchain.agents.middleware import wrap_tool_call


load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
# 1. モデルを用意
model = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",
            temperature=0,
            api_key=api_key,
        )

# システムプロンプト
system_prompt = """
あなたは社内データベースを管理する優秀なデータアナリストです。
ユーザーの質問に対し、正確なデータを抽出して答えてください。

【重要：思考プロセス】
いきなりSQLを書かず、必ず以下のステップを踏んでください：
1. `list_tables_tool` でテーブル一覧を確認する。
2. 必要なテーブルのスキーマを `get_schema_tool` で確認する（カラム名の間違いを防ぐため）。
3. 適切な SQL クエリを作成し `execute_sql_tool` で実行する。
4. 得られた結果を元に、ユーザーにわかりやすく回答する。

もしSQLエラーが起きた場合は、スキーマを再確認してクエリを修正してください。
"""
# エラーハンドリング用ミドルウェア
@wrap_tool_call
def handle_tool_errors(request, handler):
    """Handle tool execution errors with custom messages."""
    try:
        return handler(request)
    except Exception as e:
        # Return a custom error message to the model
        return ToolMessage(
            content=f"Tool error: Please check your input and try again. ({str(e)})",
            tool_call_id=request.tool_call["id"]
        )

app = create_agent(
    model=model,
    tools=tools,
    system_prompt=system_prompt,
    middleware=[handle_tool_errors],
)
