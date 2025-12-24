# mcp_server/models.py
from dataclasses import dataclass
from typing import Dict, List, Optional, Literal

LeaveType = Literal["CL", "SL", "PL"]

@dataclass
class LeaveRequest:
    id: str
    employee_id: str
    leave_type: LeaveType
    start_date: str
    end_date: str
    days: float
    reason: str
    status: Literal["approved", "pending", "cancelled", "rejected"]
    created_at: str
    approver: Optional[str] = None

@dataclass
class Employee:
    id: str
    name: str
    balances: Dict[LeaveType, float]
    requests: List[LeaveRequest]

@dataclass
class Store:
    employees: Dict[str, Employee]
    policies: Dict[str, Dict[str, float]]
    holidays: List[str]
