#!/bin/bash

file_list="/random-22/file_paths.txt"
destination="/random-22/cwa_files"
cd `uk bio bank path`

# Check if the destination directory exists, if not, create it
if [ ! -d "$destination" ]; then
    mkdir -p "$destination"
fi

# Read each file path from the file list and copy it to the destination
while IFS= read -r file_path; do
    if [ -f "$file_path" ]; then  # Check if the file exists
        echo "Copying $file_path to $destination"
        cp "$file_path" "$destination"
    else
        echo "File not found: $file_path"
    fi
done < "$file_list"

echo "All files have been copied."
