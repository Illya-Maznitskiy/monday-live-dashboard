import json
from collections import defaultdict
from pathlib import Path

from src.data_saver import save_json

# Define which statuses are "active", "workload", and "completed"
ACTIVE_STATUSES = {
    "IN PROGRESS",
    "NEED REVIEW",
    "LEAD FEEDBACK",
    "TO PACK",
    "SENT",
    "CLIENT FEEDBACK",
    "READY FOR CLIENT",
    "PAUSED",
}
WORKLOAD_STATUSES = {"IN PROGRESS", "NEED REVIEW"}
COMPLETED_STATUSES = {"DONE", "STOPPED"}


def summarize_employee(boards_data):
    """Summarize tasks per employee from boards data."""
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
            f"{emp:20} {stats['active']:6} {stats['workload']:8} {stats['completed']:9}"
        )

    save_json(employee_summary, "employee_summary.json")

    return employee_summary


if __name__ == "__main__":
    # Load the JSON data
    # Get the project root (assuming this script is in src/)
    PROJECT_ROOT = Path(__file__).parent.parent  # parent of src/

    # Build path to the JSON file in the root
    data_file = PROJECT_ROOT / "storage" / "boards_data.json"
    if not data_file.exists():
        print(f"Error: {data_file} not found!")
    else:
        with data_file.open("r", encoding="utf-8") as f:
            boards_data = json.load(f)
        summarize_employee(boards_data)
