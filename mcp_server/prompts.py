"""HR Leave Balancer Assistant — Prompts module.
Provides reusable natural language prompt templates for Claude.
"""
import json
from datetime import datetime
from mcp.server.fastmcp import FastMCP
from .db import _load_store
from .helpers import _ensure_employee, _today, _parse_date

mcp = FastMCP("HR Leave Balancer Assistant (v5)")

@mcp.prompt(name="draft_leave_email")
def draft_leave_email(name: str, approver: str, start_date: str, end_date: str, reason: str = "") -> str:
    sd = _parse_date(start_date).strftime("%d %b %Y")
    ed = _parse_date(end_date).strftime("%d %b %Y")
    return (
        f"Subject: Leave Request ({sd} to {ed})\n\n"
        f"Hi {approver},\n\n"
        f"I would like to request leave from {sd} to {ed}."
        + (f" Reason: {reason}." if reason else "")
        + "\n\nThanks,\n"
        f"{name}\n"
    )

@mcp.prompt(name="balance_summary_prompt")
def balance_summary_prompt(employee_id: str) -> str:
    store = _load_store()
    emp = _ensure_employee(store, employee_id)
    upcoming = [r for r in emp.requests if r.status == "approved" and _parse_date(r.end_date) >= _today()]
    summary = {
        "employee": {"id": emp.id, "name": emp.name},
        "balances": emp.balances,
        "upcoming": [r.__dict__ for r in upcoming],
        "policies": store.policies,
    }
    return (
        "Summarize the employee's remaining balances and upcoming approved leaves.\n\nDATA:\n"
        + json.dumps(summary, indent=2)
    )
