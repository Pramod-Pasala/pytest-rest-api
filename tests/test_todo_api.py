"""
End-to-end tests for the Todo REST API at https://todo.pixegami.io.

Covers the full task lifecycle: creating, reading, updating,
listing, and deleting tasks via the REST endpoints.
"""

import uuid

import requests

# Base URL of the API under test.
ENDPOINT = "https://todo.pixegami.io"


def test_can_call_endpoint():
    # Sanity check: the API is up and responding.
    response = requests.get(ENDPOINT)
    assert response.status_code == 200


def test_can_create_task():
    # Create a new task from a randomly generated payload.
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()

    # Fetch the task back using the ID returned on creation.
    task_id = create_task_data["task"]["task_id"]
    get_task_response = get_task(task_id)

    # The stored task should match the payload that was sent.
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == payload["content"]
    assert get_task_data["user_id"] == payload["user_id"]


def test_can_update_task():
    # Create a task to update.
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()

    # Build an update payload with new content, marked as done.
    task_id = create_task_data["task"]["task_id"]
    update_payload = {
        "user_id": payload["user_id"],
        "task_id": task_id,
        "content": "Updated Task Content",
        "is_done": True,
    }
    update_response = update_task(update_payload)
    assert update_response.status_code == 200

    # Fetch the task again and verify the updates were persisted.
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 200
    get_task_data = get_task_response.json()
    assert get_task_data["content"] == update_payload["content"]
    assert get_task_data["is_done"] == update_payload["is_done"]


def test_can_get_all_tasks():

    # Create n tasks for a specific user.
    n = 3
    payload = new_task_payload()

    for task in range(n):
        create_task_response = create_task(payload)
        assert create_task_response.status_code == 200

    # List all tasks for the user and verify the count matches.
    get_all_tasks_response = get_all_tasks(payload["user_id"])
    assert get_all_tasks_response.status_code == 200
    get_all_tasks_data = get_all_tasks_response.json()

    tasks = get_all_tasks_data["tasks"]
    assert len(tasks) == n


def test_can_delete_task():
    # Create a task to delete.
    payload = new_task_payload()
    create_task_response = create_task(payload)
    assert create_task_response.status_code == 200
    create_task_data = create_task_response.json()

    # Delete the task using its ID.
    task_id = create_task_data["task"]["task_id"]
    delete_response = delete_task(task_id)
    assert delete_response.status_code == 200

    # The deleted task should no longer exist (404 Not Found).
    get_task_response = get_task(task_id)
    assert get_task_response.status_code == 404


def new_task_payload():
    # Generate a unique user_id and content so parallel/repeated runs don't collide.
    user_id = f"user_{uuid.uuid4().hex}"
    content = f"My New Task {uuid.uuid4().hex}"

    return {
        "content": content,
        "user_id": user_id,
        "is_done": False,
    }


def create_task(payload):
    # PUT /create-task: create a new task from the given payload.
    response = requests.put(ENDPOINT + "/create-task", json=payload)
    return response


def get_task(task_id):
    # GET /get-task/{task_id}: fetch a single task by its ID.
    response = requests.get(ENDPOINT + f"/get-task/{task_id}")
    return response


def update_task(payload):
    # PUT /update-task: overwrite an existing task with the given payload.
    response = requests.put(ENDPOINT + f"/update-task", json=payload)
    return response


def get_all_tasks(user_id):
    # GET /list-tasks/{user_id}: list all tasks belonging to a user.
    response = requests.get(ENDPOINT + f"/list-tasks/{user_id}")
    return response


def delete_task(task_id):
    # DELETE /delete-task/{task_id}: remove a task by its ID.
    response = requests.delete(ENDPOINT + f"/delete-task/{task_id}")
    return response
