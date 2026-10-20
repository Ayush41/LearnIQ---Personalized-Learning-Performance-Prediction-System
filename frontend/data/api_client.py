"""Small HTTP client used by Streamlit pages to call the FastAPI service."""

import os

import requests

API_BASE_URL = os.getenv("LEARNIQ_API_URL", "http://127.0.0.1:8000/api/v1").rstrip("/")


def get(path: str, params: dict | None = None) -> dict:
    response = requests.get(f"{API_BASE_URL}/{path.lstrip('/')}", params=params, timeout=10)
    response.raise_for_status()
    return response.json()


def post(path: str, payload: dict) -> dict:
    response = requests.post(f"{API_BASE_URL}/{path.lstrip('/')}", json=payload, timeout=20)
    response.raise_for_status()
    return response.json()