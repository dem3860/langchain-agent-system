import os
from langchain_community.utilities.sql_database import SQLDatabase
from langchain_core.tools import tool

# DB接続設定 (環境変数から読み込むのがベストですが、今回は直接記述または.env経由)
DB_URI = os.getenv("DB_URI", "postgresql+psycopg2://user:password@localhost:5432/ec_db")

db = SQLDatabase.from_uri(DB_URI)

@tool
def list_tables_tool():
    """データベースにあるテーブルの一覧を取得します。"""
    try:
        tables = db.get_usable_table_names()
        return f"テーブル一覧: {tables}"
    except Exception as e:
        return f"エラー: テーブル一覧の取得に失敗しました。{e}"

@tool
def get_schema_tool(table_names: str):
    """
    指定されたテーブルのスキーマ（カラム名や型）を取得します。
    引数はカンマ区切りの文字列で指定してください。例: "users, orders"
    """
    if not table_names:
        return "エラー: テーブル名を指定してください。"
    try:
        return db.get_table_info(table_names.split(", "))
    except Exception as e:
        return f"エラー: スキーマ情報の取得に失敗しました。{e}"

@tool
def execute_sql_tool(sql_query: str):
    """
    SQLクエリを実行し、結果を返します。
    更新系（INSERT, UPDATE, DELETE）は禁止です。SELECTのみ使用してください。
    """
    print(f"🔄 Executing SQL: {sql_query}")
    try:
        return db.run(sql_query)
    except Exception as e:
        return f"SQL実行エラー: {e}\nクエリを見直して再試行してください。"