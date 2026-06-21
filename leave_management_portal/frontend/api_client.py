"""
api_client.py
--------------
Every call the Streamlit frontend makes to the FastAPI backend goes
through here -- one place to manage the base URL, the auth header, and
error handling so pages don't repeat that logic.
"""

import requests
import streamlit as st

API_BASE = "http://127.0.0.1:8000"


def _headers():
    token = st.session_state.get("access_token")
    return {"Authorization": f"Bearer {token}"} if token else {}


def _handle(resp: requests.Response):
    if resp.status_code == 401:
        st.session_state.clear()
        st.error("Your session expired. Please log in again.")
        st.stop()
    if not resp.ok:
        try:
            detail = resp.json().get("detail", resp.text)
        except Exception:
            detail = resp.text
        st.error(f"Request failed: {detail}")
        st.stop()
    return resp.json() if resp.text else None


def get(path: str, params: dict = None):
    try:
        resp = requests.get(f"{API_BASE}{path}", headers=_headers(), params=params, timeout=10)
    except requests.exceptions.ConnectionError:
        st.error("Can't reach the backend API. Is it running? (`uvicorn main:app --reload`)")
        st.stop()
    return _handle(resp)


def post(path: str, json: dict = None):
    try:
        resp = requests.post(f"{API_BASE}{path}", headers=_headers(), json=json, timeout=10)
    except requests.exceptions.ConnectionError:
        st.error("Can't reach the backend API. Is it running? (`uvicorn main:app --reload`)")
        st.stop()
    return _handle(resp)


def put(path: str, json: dict = None):
    try:
        resp = requests.put(f"{API_BASE}{path}", headers=_headers(), json=json, timeout=10)
    except requests.exceptions.ConnectionError:
        st.error("Can't reach the backend API. Is it running? (`uvicorn main:app --reload`)")
        st.stop()
    return _handle(resp)


def delete(path: str):
    try:
        resp = requests.delete(f"{API_BASE}{path}", headers=_headers(), timeout=10)
    except requests.exceptions.ConnectionError:
        st.error("Can't reach the backend API. Is it running? (`uvicorn main:app --reload`)")
        st.stop()
    return _handle(resp)
