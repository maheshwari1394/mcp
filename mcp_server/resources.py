"""HR Leave Balancer Assistant — Resources module.
Each function exposes structured data resources (employee, policy, holidays).
"""
import json
from mcp.server.fastmcp import FastMCP
from .db import _load_store
from .helpers import _ensure_employee

mcp = FastMCP("HR Leave Balancer Assistant (v5)")

@mcp.resource("employee://{employee_id}")
def employee_resource(employee_id: str) -> str:
    store = _load_store()
    emp = _ensure_employee(store, employee_id)
    snapshot = {
        "id": emp.id,
        "name": emp.name,
        "balances": emp.balances,
        "requests": [r.__dict__ for r in emp.requests],
    }
    return json.dumps(snapshot, indent=2)

@mcp.resource("policy://")
def policy_resource() -> str:
    store = _load_store()
    return json.dumps(store.policies, indent=2)

@mcp.resource("holidays://")
def holidays_resource() -> str:
    store = _load_store()
    return json.dumps(store.holidays, indent=2)
