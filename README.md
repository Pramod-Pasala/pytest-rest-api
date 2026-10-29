# pytest-rest-api

A REST API test automation suite built with [pytest](https://pytest.org) and [requests](https://requests.readthedocs.io), targeting the Todo practice API at [https://todo.pixegami.io](https://todo.pixegami.io).

## Project Structure

```
pytest-rest-api/
├── pyproject.toml              # Project config, dependencies, and pytest settings
├── README.md
├── src/
│   └── pytest_rest_api/
│       └── __init__.py
└── tests/
    └── test_todo_api.py        # API tests for the Todo service
```

## Prerequisites

- Python 3.12 or later
- [uv](https://docs.astral.sh/uv/) (recommended) or pip

Dependencies (declared in `pyproject.toml`):

- `pytest` — test framework
- `requests` — HTTP client

## Getting Started

Clone the repository and install dependencies:

```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

## Running the Tests

```bash
# Run all tests with verbose output
uv run -m pytest -v

# Run a single test
uv run -m pytest tests/test_todo_api.py::test_can_create_task -v

# Run with a detailed summary of failures
uv run -m pytest -v --tb=short
```

> **Note:** The tests run against the live API at `https://todo.pixegami.io`, so an internet connection is required.

## Test Coverage

The suite covers the main CRUD operations of the Todo API:

| Test | Description |
|------|-------------|
| `test_can_call_endpoint` | Verifies the API endpoint is reachable and returns `200 OK` |
| `test_can_create_task` | Creates a task, then fetches it and validates `content` and `user_id` match |
| `test_can_update_task` | Updates a task's `content` and `is_done` fields and verifies the changes |
| `test_can_get_all_tasks` | Creates `n` tasks for a user and confirms all are listed via `list-tasks` |
| `test_can_delete_task` | Deletes a task and confirms it returns `404 Not Found` afterwards |

## API Endpoints Under Test

| Method | Endpoint | Purpose |
|--------|----------|---------|
| `PUT` | `/create-task` | Create a new task |
| `GET` | `/get-task/{task_id}` | Fetch a single task |
| `PUT` | `/update-task` | Update an existing task |
| `GET` | `/list-tasks/{user_id}` | List all tasks for a user |
| `DELETE` | `/delete-task/{task_id}` | Delete a task |

## How the Tests Work

Each test uses unique, randomly generated data (via `uuid4`) so tests remain independent and repeatable, even against a shared live API:

- `new_task_payload()` — builds a task payload with a unique `user_id` and `content`
- `create_task(payload)` — sends a `PUT` request to create a task
- `get_task(task_id)` — retrieves a task by its ID
- `update_task(payload)` — updates an existing task
- `get_all_tasks(user_id)` — lists all tasks belonging to a user
- `delete_task(task_id)` — deletes a task by its ID

Because every test creates its own user with a fresh UUID, tests can run in any order without interfering with each other.

## License

This project is for learning and practice purposes.
