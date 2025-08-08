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


# others
headers = {"Authorization": API_TOKEN, "Content-Type": "application/json"}

API_URL = "https://api.monday.com/v2"
