import json


def save_json(data, filename="tasks_data.json"):
    """Save data as formatted JSON file."""
    print(f"Saving data to {filename}")

    try:
        with open(filename, "w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving JSON to {filename}: {e}")
        raise

    else:
        print("Saved data to the file")
