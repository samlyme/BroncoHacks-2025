import requests
import os
from dotenv import load_dotenv
import httpx

load_dotenv()
BASE_URL = (os.getenv("SERVICE_ROOT") or "lmao")


print(BASE_URL)


# -------------------- Resources --------------------


def get_resources():
    response = requests.get(f"{BASE_URL}/resources/")
    return response.json()


def create_resource(data):
    response = requests.post(f"{BASE_URL}/resources/", json=data)
    return response.json()


def get_resource(resource_id):
    response = requests.get(f"{BASE_URL}/resources/{resource_id}")
    return response.json()


def update_resource(resource_id, data):
    response = requests.patch(f"{BASE_URL}/resources/{resource_id}", json=data)
    return response.json()


def delete_resource(resource_id):
    response = requests.delete(f"{BASE_URL}/resources/{resource_id}")
    return response.json()

# -------------------- Users --------------------


def get_users():
    response = requests.get(f"{BASE_URL}/users/")
    return response.json()


def create_user(data):
    response = requests.post(f"{BASE_URL}/users/", json=data)
    return response.json()


def get_user(user_id):
    response = requests.get(f"{BASE_URL}/users/{user_id}")
    return response.json()


def update_user(user_id, data):
    response = requests.patch(f"{BASE_URL}/users/{user_id}", json=data)
    return response.json()


def delete_user(user_id):
    response = requests.delete(f"{BASE_URL}/users/{user_id}")
    return response.json()

# -------------------- Chats --------------------


def get_chats():
    response = requests.get(f"{BASE_URL}/chats/")
    return response.json()


def create_chat(data):
    response = requests.post(f"{BASE_URL}/chats/", json=data)
    return response.json()


def get_chat(thread_id):
    response = requests.get(f"{BASE_URL}/chats/{thread_id}")
    return response.json()


def update_chat(thread_id, data):
    response = requests.patch(f"{BASE_URL}/chats/{thread_id}", json=data)
    return response.json()


def delete_chat(thread_id):
    response = requests.delete(f"{BASE_URL}/chats/{thread_id}")
    return response.json()

# -------------------- Home --------------------


def get_home():
    response = requests.get(f"{BASE_URL}/")
    return response.json()
