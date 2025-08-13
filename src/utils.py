import os

from dotenv import load_dotenv


load_dotenv()


# .env variables
API_TOKEN = os.getenv("MONDAY_API_TOKEN")
if not API_TOKEN:
    raise ValueError("API_TOKEN environment variable is not set")

board_ids_str = os.getenv("MONDAY_BOARD_IDS")
if not board_ids_str:
    raise ValueError("MONDAY_BOARD_IDS environment variable is not set")
board_ids = [bid.strip() for bid in board_ids_str.split(",")]

RESULT_BOARD_ID = os.getenv("MONDAY_RESULT_BOARD_ID")
if not RESULT_BOARD_ID:
    raise ValueError("RESULT_BOARD_ID environment variable is not set")


# others
headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}

API_URL = "https://api.monday.com/v2"


def print_boards_data(boards):
    """Print board IDs, tasks, and their column details."""

    for board in boards:
        print(f"Board ID: {board['board_id']}")
        items = board.get("items", [])
        for item in items:
            print(f"  Task: {item['name']}")
            for col in item["column_values"]:
                print(f"    {col.get('id')}: {col.get('text')}")
