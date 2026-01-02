#!/bin/bash
# Simple test runner for Phase I

echo "Setting up virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "Installing dependencies..."
pip install -q -r requirements.txt

echo "Running tests..."
python -m pytest tests/ -v

echo "Running tests with coverage..."
python -m pytest --cov=src --cov-report=term-missing tests/

deactivate
