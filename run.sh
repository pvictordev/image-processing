#!/bin/bash

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "No virtual environment found! Creating one..."
    python3 -m venv venv
    if [ $? -eq 0 ]; then
        echo "Virtual environment created!"
    else
        echo "Failed to create virtual environment. Exiting..."
        exit 1
    fi
fi

source venv/bin/activate
echo "Virtual environment activated!"

if [ -f "requirements.txt" ]; then
    echo "Checking for installed dependencies..."
    if ! pip freeze | grep -q -f requirements.txt; then
        echo "Installing dependencies from requirements.txt..."
        pip install -r requirements.txt
        if [ $? -eq 0 ]; then
            echo "Dependencies installed successfully!"
        else
            echo "Failed to install dependencies. Exiting..."
            exit 1
        fi
    else
        echo "All dependencies are already installed."
    fi
else
    echo "requirements.txt not found. Exiting..."
    exit 1
fi

echo "🚀 Starting the app..."
python3 src/main.py
if [ $? -eq 0 ]; then
    echo "App started successfully!"
else
    echo "❌ Failed to start the app. Exiting..."
    exit 1
fi
