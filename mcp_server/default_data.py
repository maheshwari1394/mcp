"""Default dataset for HR Leave Balancer Assistant (v5).
Used to initialize hr_leave_store_v4.json if missing.
"""

DEFAULT_DATASET = {
    "employees": {
        "E001": {
            "id": "E001",
            "name": "Asha Rao",
            "balances": {"CL": 6.0, "SL": 2.0, "PL": 8.0},
            "requests": [
                {
                    "id": "REQ-E001-20251025090100",
                    "employee_id": "E001",
                    "leave_type": "PL",
                    "start_date": "2025-11-05",
                    "end_date": "2025-11-06",
                    "days": 2.0,
                    "reason": "Family function",
                    "status": "approved",
                    "created_at": "2025-10-25T09:01:00Z",
                    "approver": "HR",
                }
            ],
        },
        "E002": {
            "id": "E002",
            "name": "Rohan Shah",
            "balances": {"CL": 3.0, "SL": 1.0, "PL": 5.0},
            "requests": [],
        },
        "E003": {
            "id": "E003",
            "name": "Neha Patel",
            "balances": {"CL": 4.0, "SL": 2.0, "PL": 10.0},
            "requests": [
                {
                    "id": "REQ-E003-20251023114500",
                    "employee_id": "E003",
                    "leave_type": "CL",
                    "start_date": "2025-11-10",
                    "end_date": "2025-11-11",
                    "days": 2.0,
                    "reason": "Personal work",
                    "status": "pending",
                    "created_at": "2025-10-23T11:45:00Z",
                    "approver": "HR",
                }
            ],
        },
        "E004": {"id": "E004", "name": "Karan Mehta", "balances": {"CL": 5.0, "SL": 3.0, "PL": 12.0}, "requests": []},
        "E005": {
            "id": "E005",
            "name": "Priya Singh",
            "balances": {"CL": 2.0, "SL": 4.0, "PL": 9.0},
            "requests": [
                {
                    "id": "REQ-E005-20251020081500",
                    "employee_id": "E005",
                    "leave_type": "SL",
                    "start_date": "2025-10-28",
                    "end_date": "2025-10-29",
                    "days": 2.0,
                    "reason": "Fever",
                    "status": "approved",
                    "created_at": "2025-10-20T08:15:00Z",
                    "approver": "Manager",
                }
            ],
        },
        "E006": {"id": "E006", "name": "Vikram Desai", "balances": {"CL": 6.0, "SL": 2.0, "PL": 15.0}, "requests": []},
        "E007": {"id": "E007", "name": "Sneha Iyer", "balances": {"CL": 3.0, "SL": 3.0, "PL": 7.0}, "requests": []},
        "E008": {"id": "E008", "name": "Amit Kumar", "balances": {"CL": 4.0, "SL": 1.0, "PL": 10.0}, "requests": []},
        "E009": {"id": "E009", "name": "Divya Nair", "balances": {"CL": 2.0, "SL": 2.0, "PL": 8.0}, "requests": []},
        "E010": {"id": "E010", "name": "Suresh Menon", "balances": {"CL": 5.0, "SL": 2.0, "PL": 11.0}, "requests": []},
        "E011": {"id": "E011", "name": "Anita D'Souza", "balances": {"CL": 3.0, "SL": 4.0, "PL": 9.0}, "requests": []},
        "E012": {"id": "E012", "name": "Rajiv Bhatia", "balances": {"CL": 5.0, "SL": 2.0, "PL": 6.0}, "requests": []},
        "E013": {"id": "E013", "name": "Meena Joshi", "balances": {"CL": 4.0, "SL": 3.0, "PL": 8.0}, "requests": []},
        "E014": {"id": "E014", "name": "Arjun Kapoor", "balances": {"CL": 6.0, "SL": 2.0, "PL": 12.0}, "requests": []},
        "E015": {"id": "E015", "name": "Lakshmi Krishnan", "balances": {"CL": 3.0, "SL": 3.0, "PL": 10.0}, "requests": []},
        "E016": {"id": "E016", "name": "Mohit Agarwal", "balances": {"CL": 2.0, "SL": 1.0, "PL": 5.0}, "requests": []},
        "E017": {"id": "E017", "name": "Pooja Malhotra", "balances": {"CL": 4.0, "SL": 2.0, "PL": 9.0}, "requests": []},
        "E018": {"id": "E018", "name": "Gaurav Khanna", "balances": {"CL": 3.0, "SL": 3.0, "PL": 7.0}, "requests": []},
        "E019": {"id": "E019", "name": "Shweta Pillai", "balances": {"CL": 5.0, "SL": 2.0, "PL": 6.0}, "requests": []},
        "E020": {"id": "E020", "name": "Nikhil Verma", "balances": {"CL": 2.0, "SL": 2.0, "PL": 8.0}, "requests": []},
    },
    "policies": {
        "CL": {"accrual_per_month": 1.0, "carryover_limit": 6},
        "SL": {"accrual_per_month": 0.5, "carryover_limit": 10},
        "PL": {"accrual_per_month": 1.5, "carryover_limit": 30},
    },
    "holidays": [
        "2025-01-26",
        "2025-08-15",
        "2025-10-02",
        "2025-12-25",
    ],
}
