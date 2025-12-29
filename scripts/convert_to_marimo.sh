#!/bin/bash

# Directory containing notebooks
NOTEBOOKS_DIR="notebooks"

# Check if marimo is installed
if ! command -v marimo &> /dev/null; then
    # Try using uv run if marimo is not in path directly
    if command -v uv &> /dev/null; then
         CMD="uv run marimo"
    else
        echo "Error: marimo is not installed and uv is not found."
        exit 1
    fi
else
    CMD="marimo"
fi

echo "Converting notebooks in $NOTEBOOKS_DIR using $CMD..."

# Loop through all .ipynb files in the notebooks directory
for notebook in "$NOTEBOOKS_DIR"/*.ipynb; do
    if [ ! -e "$notebook" ]; then
        echo "No notebooks found in $NOTEBOOKS_DIR"
        exit 0
    fi

    # Determine output filename (replace .ipynb with .py)
    output="${notebook%.ipynb}.py"

    echo "Converting: $notebook -> $output"
    
    # Run conversion
    $CMD convert "$notebook" -o "$output"
    
    if [ $? -eq 0 ]; then
        echo "Success: $output"
    else
        echo "Failed to convert: $notebook"
    fi
done

echo "Conversion complete."
