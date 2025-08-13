from data_fetcher import get_board_data, get_all_users
from data_saver import save_json
from utils import board_ids, print_boards_data


def main():
    """Fetch and save boards and users data."""

    # Fetch all boards data
    all_boards_data = []
    for bid in board_ids:
        items = get_board_data(bid)
        all_boards_data.append({"board_id": bid, "items": items})

    save_json(all_boards_data, "boards_data.json")

    # Fetch all users data
    users = get_all_users()
    print(f"Fetched {len(users)} users.")
    # Optionally save users data too
    save_json(users, "users_data.json")


if __name__ == "__main__":
    main()
