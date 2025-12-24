# mcp_server/helpers.py

from datetime import date, datetime, timedelta, timezone
from typing import List, Dict, Optional, Tuple, Any
from .models import Employee, Store, LeaveType
from .db import load_store, save_store

# ---------------------------------------------------------------------
# Basic date utilities
# ---------------------------------------------------------------------
def today() -> date:
    """Return today's UTC date."""
    return datetime.now(timezone.utc).date()


def parse_date(s: str) -> date:
    """Parse a string in YYYY-MM-DD format into a date."""
    return datetime.strptime(s, "%Y-%m-%d").date()


def daterange_inclusive(start: date, end: date) -> List[date]:
    """Generate all dates between start and end, inclusive."""
    return [start + timedelta(days=i) for i in range((end - start).days + 1)]


def is_weekend(d: date) -> bool:
    """Return True if the given date is a weekend."""
    return d.weekday() >= 5


def business_days_between(start: date, end: date, holidays: List[date]) -> int:
    """Count business days excluding weekends and holidays."""
    hset = set(holidays)
    return sum(
        1 for d in daterange_inclusive(start, end)
        if not is_weekend(d) and d not in hset
    )


# ---------------------------------------------------------------------
# Employee utilities
# ---------------------------------------------------------------------
def ensure_employee(store: Store, emp_id: str, name: Optional[str] = None) -> Employee:
    """Ensure an employee exists in the store; create if missing."""
    if emp_id in store.employees:
        return store.employees[emp_id]
    emp = Employee(emp_id, name or emp_id, {"CL": 0, "SL": 0, "PL": 0}, [])
    store.employees[emp_id] = emp
    return emp


# ---------------------------------------------------------------------
# Leave calculation utilities
# ---------------------------------------------------------------------
def compute_days_and_conflicts(store, emp, start_date: str, end_date: str) -> Tuple[int, List[str]]:
    """Calculate business days and detect overlapping approved requests."""
    start = parse_date(start_date)
    end = parse_date(end_date)
    if end < start:
        raise ValueError("end_date cannot be before start_date")

    holidays = getattr(store, "holidays", [])
    total_days = sum(
        1 for d in daterange_inclusive(start, end)
        if not is_weekend(d) and d not in holidays
    )

    conflicts = []
    for req in getattr(emp, "requests", []):
        if req.status == "approved":
            r_start = parse_date(req.start_date)
            r_end = parse_date(req.end_date)
            if not (end < r_start or start > r_end):
                conflicts.append(req.id)

    return total_days, conflicts


# ---------------------------------------------------------------------
# Carryover and response helpers
# ---------------------------------------------------------------------
def cap_to_carryover(policies: Dict[str, dict], balances: Dict[str, float]) -> Dict[str, float]:
    """Apply carryover caps per policy."""
    capped = balances.copy()
    for lt, policy in policies.items():
        cap = float(policy.get("carryover_cap", float("inf")))
        if capped.get(lt, 0) > cap:
            capped[lt] = cap
    return capped


def ok(message: str, **kwargs: Any) -> Dict[str, Any]:
    """Standard success response."""
    return {"ok": True, "message": message, **kwargs}


def err(message: str, **kwargs: Any) -> Dict[str, Any]:
    """Standard error response."""
    return {"ok": False, "message": message, **kwargs}


# ---------------------------------------------------------------------
# ID helper
# ---------------------------------------------------------------------
def generate_request_id(employee_id: str) -> str:
    """Generate a unique leave request ID with timestamp."""
    now_str = datetime.utcnow().strftime("%Y%m%d%H%M%S")
    return f"REQ-{employee_id}-{now_str}"


# ---------------------------------------------------------------------
# Backward compatibility aliases
# ---------------------------------------------------------------------
_ensure_employee = ensure_employee
_compute_days_and_conflicts = compute_days_and_conflicts
_generate_request_id = generate_request_id
_cap_to_carryover = cap_to_carryover
_ok = ok
_err = err
_today = today
_parse_date = parse_date
