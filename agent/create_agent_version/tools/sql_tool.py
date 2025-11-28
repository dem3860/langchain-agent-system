import os
import json
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.tools import tool

# DB接続
DB_URI = os.getenv("DB_URI", "postgresql+psycopg2://user:password@localhost:5432/ec_db")
db = SQLDatabase.from_uri(DB_URI)

@tool
def list_tables_tool() -> str:
    """データベースに存在するテーブル一覧を返します。"""
    try:
        tables = db.get_usable_table_names()
        return json.dumps({"tables": list(tables)}, ensure_ascii=False)
    except Exception as e:
        return f"エラー: テーブル一覧の取得に失敗しました: {e}"

@tool
def get_schema_tool(table_names: str) -> str:
    """
    指定されたテーブルのスキーマ情報（カラム名・型など）を返します。
    複数指定する場合はカンマ区切りで入力してください。
    例: "users, orders"

    無効なテーブル名がある場合はエラーを返します。
    """
    if not table_names:
        return "エラー: テーブル名を指定してください。"

    names = [name.strip() for name in table_names.split(",")]

    try:
        schema = db.get_table_info(names)
        return schema
    except Exception as e:
        return f"スキーマ情報の取得に失敗しました: {e}"

@tool
def execute_sql_tool(sql_query: str) -> str:
    """
    SQLクエリ（SELECT文のみ）を実行し、結果を返します。
    更新系（INSERT, UPDATE, DELETE, DROP 等）は禁止です。

    実行前にクエリが SELECT で始まるか検証します。
    結果は JSON 形式で返します。
    """
    sql = sql_query.strip().lower()

    # 安全対策：SELECT 以外を禁止
    if not sql.startswith("select"):
        return "エラー: SELECT 文のみ実行可能です。更新系クエリは禁止されています。"

    print(f"[SQL Execute] {sql_query}")

    try:
        result = db.run(sql_query)
        return json.dumps({"rows": result}, ensure_ascii=False)
    except Exception as e:
        return f"SQL実行エラー: {e}"
