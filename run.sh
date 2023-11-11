#!/bin/bash
set -e

# Set the ROOT_DIR environment variable to the script's current directory
export ROOT_DIR=$(dirname "$(realpath "$0")")
cd $ROOT_DIR

source "./setup.sh"
streamlit run app.py
