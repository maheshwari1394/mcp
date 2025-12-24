"""HR Leave Balancer Assistant — Tools module.
Each function is exposed as an MCP tool for Claude (or ChatGPT MCP) to invoke.
"""
from dataclasses import asdict
from typing import Optional, Literal
from datetime import datetime
from mcp.server.fastmcp import FastMCP

# Updated imports (no underscores)
from .db import load_store, save_store
from .models import LeaveType
from .helpers import (
    ensure_employee,
    compute_days_and_conflicts,
    generate_request_id,
    cap_to_carryover,
    ok,
    err,
)

# --------------------------------------------------------------------------
# Initialize MCP
# --------------------------------------------------------------------------
mcp = FastMCP("HR Leave Balancer Assistant (v5)")

# --------------------------------------------------------------------------
# Employee tools
# --------------------------------------------------------------------------
@mcp.tool(name="get_employee_snapshot")
def get_employee_snapshot(employee_id: str) -> dict:
    store = load_store()
    emp = ensure_employee(store, employee_id)
    snap = {
        "id": emp.id,
        "name": emp.name,
        "balances": emp.balances,
        "requests": [asdict(r) for r in emp.requests],
    }
    return ok(f"Snapshot for {emp.name} ({emp.id}).", employee=snap)


@mcp.tool(name="get_balance")
def get_balance(employee_id: str, leave_type: Optional[LeaveType] = None) -> dict:
    store = load_store()
    emp = ensure_employee(store, employee_id)
    if leave_type:
        val = float(emp.balances.get(leave_type, 0.0))
        return ok(
            f"{leave_type} balance for {emp.name} is {val}.",
            employee_id=emp.id,
            leave_type=leave_type,
            balance=val,
        )
    return ok(
        f"Balances for {emp.name}: {emp.balances}.",
        employee_id=emp.id,
        balances=emp.balances,
    )

# --------------------------------------------------------------------------
# Leave request tools
# --------------------------------------------------------------------------
@mcp.tool(name="request_leave")
def request_leave(
    employee_id: str,
    leave_type: LeaveType,
    start_date: str,
    end_date: str,
    reason: str = "",
    approver: Optional[str] = None,
    auto_approve: bool = True,
) -> dict:
    store = load_store()
    emp = ensure_employee(store, employee_id)
    try:
        days, conflicts = compute_days_and_conflicts(store, emp, start_date, end_date)
    except Exception as e:
        return err(str(e))

    if conflicts:
        return err(
            f"Overlaps with approved request(s): {', '.join(conflicts)}",
            conflicts=conflicts,
        )

    status: Literal["approved", "pending"] = "approved" if auto_approve else "pending"
    if status == "approved" and emp.balances.get(leave_type, 0.0) < days:
        return err(
            f"Insufficient {leave_type} balance. Needed {days}, have {emp.balances.get(leave_type, 0.0)}."
        )

    if status == "approved":
        emp.balances[leave_type] -= float(days)

    req = {
        "id": generate_request_id(employee_id),
        "employee_id": employee_id,
        "leave_type": leave_type,
        "start_date": start_date,
        "end_date": end_date,
        "days": float(days),
        "reason": reason,
        "status": status,
        "approver": approver,
        "created_at": datetime.utcnow().isoformat(timespec="seconds") + "Z",
    }

    emp.requests.append(type(emp.requests[0])(**req) if emp.requests else req)
    save_store(store)
    return ok(
        f"Leave {status} for {emp.name}: {leave_type} {days} day(s).",
        request=req,
        balances=emp.balances,
    )


@mcp.tool(name="approve_request")
def approve_request(employee_id: str, request_id: str) -> dict:
    store = load_store()
    emp = ensure_employee(store, employee_id)
    req = next((r for r in emp.requests if r.id == request_id), None)
    if not req:
        return err("Request not found", employee_id=employee_id, request_id=request_id)
    if req.status == "approved":
        return ok("Already approved.", request=asdict(req), balances=emp.balances)
    if emp.balances.get(req.leave_type, 0.0) < req.days:
        return err(
            "Insufficient balance at approval time.",
            needed=req.days,
            have=emp.balances.get(req.leave_type, 0.0),
        )
    emp.balances[req.leave_type] -= float(req.days)
    req.status = "approved"
    save_store(store)
    return ok("Approved.", request=asdict(req), balances=emp.balances)


@mcp.tool(name="cancel_request")
def cancel_request(employee_id: str, request_id: str) -> dict:
    store = load_store()
    emp = ensure_employee(store, employee_id)
    req = next((r for r in emp.requests if r.id == request_id), None)
    if not req:
        return err("Request not found")
    if req.status == "cancelled":
        return ok("Already cancelled.", request=asdict(req))
    if req.status == "approved":
        emp.balances[req.leave_type] += float(req.days)
        emp.balances = cap_to_carryover(store.policies, emp.balances)
    req.status = "cancelled"
    save_store(store)
    return ok("Cancelled.", request=asdict(req), balances=emp.balances)

# --------------------------------------------------------------------------
# Admin tools
# --------------------------------------------------------------------------
@mcp.tool(name="accrue_balances")
def accrue_balances(months: int = 1) -> dict:
    if months <= 0:
        return err("months must be >= 1")
    store = load_store()
    for emp in store.employees.values():
        for lt, pol in store.policies.items():
            emp.balances[lt] += float(pol.get("accrual_per_month", 0)) * months
        emp.balances = cap_to_carryover(store.policies, emp.balances)
    save_store(store)
    return ok(f"Accrued for {len(store.employees)} employees ({months} month(s)).")
