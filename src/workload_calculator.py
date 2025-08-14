import json
from collections import defaultdict
from pathlib import Path

from src.data_saver import save_json
from src.utils import (
    employee_rates,
    ACTIVE_STATUSES,
    WORKLOAD_STATUSES,
    COMPLETED_STATUSES,
)


def summarize_employee(boards_data):
    """Summarize tasks per employee from boards data."""

    # Automatically creates a new employee dict with zero counts if missing
    employee_summary = defaultdict(
        lambda: {"active": 0, "workload": 0, "completed": 0}
    )

    for board in boards_data:
        for item in board.get("items", []):
            for sub in item.get("subitems", []):
                for col in sub.get("column_values", []):
                    if col["id"] == "person" and col["text"]:
                        person_name = col["text"]

                        # Find the status column
                        status_col = next(
                            (
                                c
                                for c in sub["column_values"]
                                if c["id"].startswith("status")
                            ),
                            None,
                        )
                        if status_col:
                            status_text = status_col["text"]

                            # Update counts
                            if status_text in ACTIVE_STATUSES:
                                employee_summary[person_name]["active"] += 1
                            if status_text in WORKLOAD_STATUSES:
                                employee_summary[person_name]["workload"] += 1
                            if status_text in COMPLETED_STATUSES:
                                employee_summary[person_name]["completed"] += 1

    # Print summary table
    print(f"{'Employee':20} {'Active':6} {'Workload':8} {'Completed':9}")
    print("-" * 50)
    for emp, stats in employee_summary.items():
        print(
            f"{emp:20} {stats['active']:6} {stats['workload']:8} "
            f"{stats['completed']:9}"
        )

    save_json(employee_summary, "employee_summary.json")

    return employee_summary


def calculate_additional_payments():
    """Calculate Additional Payments, and save to JSON."""

    # Define path to project root
    path = Path(__file__).parent.parent

    # Load the employee summary JSON first
    try:
        with (path / "storage" / "employee_summary.json").open(
            "r", encoding="utf-8"
        ) as f:
            employee_summary_json = json.load(f)
    except FileNotFoundError:
        print("employee_summary.json not found!")
        return

    print(f"Employee Summary JSON: {employee_summary_json}")

    # Calculate Additional Payments
    employee_payments = {}
    for name, summary in employee_summary_json.items():
        hours_worked = summary.get("active", 0) + summary.get("workload", 0)
        print(f"Employee {name} has {hours_worked} hours")
        rate = employee_rates.get(name, 0)  # fallback to 0 if missing
        print(f"Employee {name} has {rate:.2f} %")
        additional_payment = hours_worked * rate
        print(f"Employee {name} has {additional_payment:.2f} %")
        employee_payments[name] = {
            **summary,
            "additional_payment": additional_payment,
        }

    # Save results to JSON
    save_json(employee_payments, "employee_summary_with_payments.json")

    # Optional: print results
    print("Employee Additional Payments:")
    for name, data in employee_payments.items():
        print(f"{name}: {data['additional_payment']}")

    return employee_payments


if __name__ == "__main__":
    # 1. Summarize employees first (build employee_summary.json)
    PROJECT_ROOT = Path(__file__).parent.parent
    data_file = PROJECT_ROOT / "storage" / "boards_data.json"

    if not data_file.exists():
        print(f"Error: {data_file} not found!")
    else:
        with data_file.open("r", encoding="utf-8") as f:
            boards_data = json.load(f)
        summarize_employee(boards_data)

    # 2. Then calculate additional payments
    calculate_additional_payments()
