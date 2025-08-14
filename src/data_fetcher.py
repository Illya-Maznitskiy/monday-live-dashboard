import requests

from src.utils import API_URL, headers


def get_board_data(board_id, columns=None, limit=500):
    """Fetch data for multiple boards from Monday.com API at once."""

    query = """
        query (
        $boardId: ID!, $columns: [ItemsPageByColumnValuesQuery!], $limit: Int!
        ) {
          items_page_by_column_values(
          board_id: $boardId, columns: $columns, limit: $limit
          ) {
            items {
              subitems {
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
        }
        """

    variables = {
        "boardId": str(board_id),
        "columns": columns if columns else [],
        "limit": limit,
    }
    response = requests.post(
        API_URL, json={"query": query, "variables": variables}, headers=headers
    )

    response.raise_for_status()
    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")

    return data["data"]["items_page_by_column_values"]["items"]


def get_all_users():
    """Retrieve all users from Monday.com API."""

    query = """
    {
      users {
        id
        name
        email
        photo_small
      }
    }
    """

    response = requests.post(API_URL, json={"query": query}, headers=headers)
    response.raise_for_status()
    data = response.json()

    if "errors" in data:
        raise Exception(f"GraphQL errors: {data['errors']}")

    return data["data"]["users"]
