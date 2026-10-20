"""Small HTTP client used by Streamlit pages to call the FastAPI service."""

import os

import requests

API_BASE_URL = os.getenv("LEARNIQ_API_URL", "http://127.0.0.1:8000/api/v1").rstrip("/")


class ApiClientError(RuntimeError):
    """Raised when the FastAPI service cannot complete a frontend request."""


def get(path: str, params: dict | None = None) -> dict:
    try:
        response = requests.get(f"{API_BASE_URL}/{path.lstrip('/')}", params=params, timeout=10)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        raise ApiClientError(str(error)) from error


def post(path: str, payload: dict) -> dict:
    try:
        response = requests.post(f"{API_BASE_URL}/{path.lstrip('/')}", json=payload, timeout=20)
        response.raise_for_status()
        return response.json()
    except requests.RequestException as error:
        raise ApiClientError(str(error)) from error