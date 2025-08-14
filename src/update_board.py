import json
from pathlib import Path

import requests

from src.utils import API_URL, headers, RESULT_BOARD_ID


def update_master_board(master_board_id, aggregated_data):
    """Update Monday board with aggregated employee statistics."""

    query = """
    mutation($boardId: ID!, $itemName: String!, $columnValues: JSON!) {
        create_item(
        board_id: $boardId, item_name: $itemName, column_values: $columnValues
        ) {
            id
        }
    }
    """

    for employee_name, stats in aggregated_data.items():
        print(f"Processing {employee_name}: {stats}")
        column_values = {
            "numeric_mktskysa": stats["active"],
            "numeric_mkts539e": stats["workload"],
            "numeric_mktsp120": stats["completed"],
            "numeric_mkttp4j4": stats["additional_payment"],
        }
        print(f"Sending request with column values: {column_values}")

        variables = {
            "boardId": master_board_id,
            "itemName": employee_name,
            "columnValues": json.dumps(column_values),
        }

        response = requests.post(
            API_URL,
            json={"query": query, "variables": variables},
            headers=headers,
        )
        print(
            f"Response status: "
            f"{response.status_code}, response: {response.text}"
        )


if __name__ == "__main__":
    root = Path(__file__).parent.parent
    data_file = root / "storage" / "employee_summary.json"

    if not data_file.exists():
        print(f"Error: {data_file} does not exist.")
    else:
        with data_file.open("r", encoding="utf-8") as f:
            aggregated_data = json.load(f)

        update_master_board(RESULT_BOARD_ID, aggregated_data)
