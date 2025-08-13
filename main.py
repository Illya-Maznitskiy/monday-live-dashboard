import time

from src.data_fetcher import get_board_data, get_all_users
from src.data_saver import save_json
from src.update_board import update_master_board
from src.utils import board_ids, RESULT_BOARD_ID
from src.workload_calculator import summarize_employee


def update_dashboard():
    """Fetch data, summarize, save, and update Monday board."""
    # Fetch all boards data
    all_boards_data = []
    for bid in board_ids:
        items = get_board_data(bid)
        all_boards_data.append({"board_id": bid, "items": items})
    save_json(all_boards_data, "boards_data.json")

    # Fetch all users data
    users = get_all_users()
    print(f"Fetched {len(users)} users.")
    save_json(users, "users_data.json")

    # Summarize employee data
    employee_summary = summarize_employee(all_boards_data)
    save_json(employee_summary, "employee_summary.json")

    # Update Monday board
    update_master_board(RESULT_BOARD_ID, employee_summary)
    print("Dashboard updated!")


def main():
    """Run the update every 5 minutes."""
    while True:
        try:
            update_dashboard()
            print("Next update in 5 minutes")
        except Exception as e:
            print("Error during update:", e)
        time.sleep(300)  # 5 minutes


if __name__ == "__main__":
    main()
