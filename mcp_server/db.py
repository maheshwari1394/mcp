# mcp_server/db.py
import json
from pathlib import Path
from dataclasses import asdict
from .models import Employee, LeaveRequest, Store
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
DATA_FILE = DATA_DIR / "hr_leave_store_v4.json"

logging.info(f"HR Leave DB path: {DATA_FILE}")

class _RealDB:
    def load(self) -> Store:
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        if not DATA_FILE.exists():
            from .default_data import DEFAULT_DATASET
            DATA_FILE.write_text(json.dumps(DEFAULT_DATASET, indent=2), encoding="utf-8")

        raw = json.loads(DATA_FILE.read_text(encoding="utf-8"))
        employees = {}
        for emp_id, e in raw.get("employees", {}).items():
            requests = [LeaveRequest(**r) for r in e.get("requests", [])]
            employees[emp_id] = Employee(
                id=e["id"], name=e["name"],
                balances={k: float(v) for k, v in e["balances"].items()},
                requests=requests
            )
        return Store(employees, raw["policies"], raw["holidays"])

    def save(self, store: Store) -> None:
        payload = {
            "employees": {
                e.id: {
                    "id": e.id, "name": e.name,
                    "balances": e.balances,
                    "requests": [asdict(r) for r in e.requests],
                } for e in store.employees.values()
            },
            "policies": store.policies,
            "holidays": store.holidays
        }
        DATA_DIR.mkdir(parents=True, exist_ok=True)
        DATA_FILE.write_text(json.dumps(payload, indent=2), encoding="utf-8")

_DB = _RealDB()
def load_store() -> Store: return _DB.load()
def save_store(store: Store) -> None: _DB.save(store)
_load_store = load_store
_save_store = save_store
