import json
from collections import defaultdict

# Load your JSON data (replace with your actual data source)
with open("boards_data.json", "r", encoding="utf-8") as f:
    boards_data = json.load(f)

# Define which statuses are "active" and "completed"
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

# Dictionary to store summary per employee
employee_summary = defaultdict(
    lambda: {"active": 0, "workload": 0, "completed": 0}
)

# Process boards → items → subitems
for board in boards_data:
    for item in board.get("items", []):
        for sub in item.get("subitems", []):
            # Get assigned person(s)
            for col in sub.get("column_values", []):
                if col["id"] == "person" and col["text"]:
                    person_name = col["text"]

                    # Get status (you may have multiple status columns; pick the relevant one)
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
