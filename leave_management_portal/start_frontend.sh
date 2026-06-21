#!/bin/bash
# Starts the Streamlit frontend on http://localhost:8501
# Make sure start_backend.sh is already running in another terminal.
cd "$(dirname "$0")/frontend" || exit 1
streamlit run app.py
