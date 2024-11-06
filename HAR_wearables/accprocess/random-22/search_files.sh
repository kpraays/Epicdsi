#!/bin/bash

id_file="/random-22/eids.txt"
cd `uk bio bank location`

pattern=$(awk '{print $1}' $id_file | paste -sd '|')

# Loop through each directory and search for files matching the IDs
for dir in */ ; do
    if [[ -d "$dir" && "$dir" =~ ^[0-9]+ ]]; then
        echo "Searching in directory $dir"
        find "$dir" -type f -regextype posix-extended -regex ".*($pattern).*" -print
    fi
done
