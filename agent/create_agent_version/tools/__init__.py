# agent/create_agent_version/tools/__init__.py
from __future__ import annotations

from .sql_tool import list_tables_tool,get_schema_tool,execute_sql_tool

# create_agent に渡す tools 一覧
tools = [
    list_tables_tool,
    get_schema_tool,
    execute_sql_tool,
]
