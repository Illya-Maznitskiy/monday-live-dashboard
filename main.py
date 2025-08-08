import requests

from utils import API_URL, headers, board_ids


def get_board_data(board_id, columns=None, limit=10):
    """Fetch data for multiple boards from Monday.com API at once."""
    query = """
    query (
    $boardId: ID!, $columns: [ItemsPageByColumnValuesQuery!], $limit: Int!
    ) {
      items_page_by_column_values(
      board_id: $boardId, columns: $columns, limit: $limit
      ) {
        items {
          id
          name
          column_values {
            id
            text
            value
          }
        }
      }
    }
    """
    variables = {
        "boardId": str(board_id),
        "columns": (columns if columns else []),
        "limit": limit,
    }

    json_data = {"query": query, "variables": variables}

    response = requests.post(API_URL, json=json_data, headers=headers)
    print("Response status:", response.status_code)
    print("Response content:", response.text)
    response.raise_for_status()

    data = response.json()
    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")

    return data["data"]["items_page_by_column_values"]["items"]


def print_boards_data(boards):
    """Print board IDs, tasks, and their column details."""
    for board in boards:
        print(f"Board ID: {board['board_id']}")
        items = board.get("items", [])
        for item in items:
            print(f"  Task: {item['name']}")
            for col in item["column_values"]:
                print(f"    {col.get('id')}: {col.get('text')}")


if __name__ == "__main__":
    all_boards_data = []
    for bid in board_ids:
        items = get_board_data(bid)
        all_boards_data.append({"board_id": bid, "items": items})

    print_boards_data(all_boards_data)
