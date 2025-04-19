import os
from dotenv import load_dotenv
import httpx

load_dotenv()
BASE_URL = "https://" + (os.getenv("SERVICE_ROOT") or "lmao")

# -------------------- Resources --------------------


async def get_resources():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/resources/")
        return response.json()


async def create_resource(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/resources/", json=data)
        return response.json()


async def get_resource(resource_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/resources/{resource_id}")
        return response.json()


async def update_resource(resource_id, data):
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{BASE_URL}/resources/{resource_id}", json=data)
        return response.json()


async def delete_resource(resource_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/resources/{resource_id}")
        return response.json()

# -------------------- Users --------------------


async def get_users():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/")
        return response.json()


async def create_user(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/users/", json=data)
        return response.json()


async def get_user(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/users/{user_id}")
        return response.json()


async def update_user(user_id, data):
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{BASE_URL}/users/{user_id}", json=data)
        return response.json()


async def delete_user(user_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/users/{user_id}")
        return response.json()

# -------------------- Chats --------------------


async def get_chats():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/chats/")
        return response.json()


async def create_chat(data):
    async with httpx.AsyncClient() as client:
        response = await client.post(f"{BASE_URL}/chats/", json=data)
        return response.json()


async def get_chat(thread_id):
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/chats/{thread_id}")
        return response.json()


async def update_chat(thread_id, data):
    async with httpx.AsyncClient() as client:
        response = await client.patch(f"{BASE_URL}/chats/{thread_id}", json=data)
        return response.json()


async def delete_chat(thread_id):
    async with httpx.AsyncClient() as client:
        response = await client.delete(f"{BASE_URL}/chats/{thread_id}")
        return response.json()

# -------------------- Home --------------------


async def get_home():
    async with httpx.AsyncClient() as client:
        response = await client.get(f"{BASE_URL}/")
        return response.json()
