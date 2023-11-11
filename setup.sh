#!/bin/bash
set -e

# Set the ROOT_DIR environment variable to the script's current directory
export ROOT_DIR=$(dirname "$(realpath "$0")")

# Directory for the virtual environment, inside the ROOT_DIR
VENV_DIR="$ROOT_DIR/venv"

# Check if the virtual environment directory exists
if [ ! -d "$VENV_DIR" ]; then
    echo "Creating virtual environment in $ROOT_DIR..."
    python -m venv "$VENV_DIR"
fi

# Activate the virtual environment
source "$VENV_DIR/bin/activate"

# Path to the requirements.txt file
REQ_FILE="$ROOT_DIR/requirements.txt"

# Check if requirements.txt exists and install any missing packages
if [ -f "$REQ_FILE" ]; then
    echo "Installing dependencies from $REQ_FILE..."
    pip install -r "$REQ_FILE"
else
    echo "requirements.txt not found in $ROOT_DIR."
fi

echo "Setup complete."
