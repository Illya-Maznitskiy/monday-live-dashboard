import os
import json
from pathlib import Path


PROJECT_ROOT = Path(__file__).parent.parent


def save_json(data, filename="storage/tasks_data.json"):
    """Save data as formatted JSON file, creating the directory if needed."""

    # Always save in PROJECT_ROOT/storage
    folder = PROJECT_ROOT / "storage"
    print(f"Folder: {folder}")

    # Create storage folder if it doesn't exist
    os.makedirs(folder, exist_ok=True)

    # Combine folder + filename
    file_path = folder / filename
    print(f"Saving data to {file_path}")

    try:
        with file_path.open("w", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
    except (IOError, json.JSONDecodeError) as e:
        print(f"Error saving JSON to {file_path}: {e}")
        raise
    else:
        print("Saved data to the file")
