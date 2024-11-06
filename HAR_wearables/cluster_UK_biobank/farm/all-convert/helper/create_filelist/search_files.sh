#!/bin/bash

cd /lustre03/project/6008063/neurohub/UKB/Bulk/90001
output_file="/home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/helper/create_filelist/files.txt"

# Loop through each directory and search for files matching the IDs
for dir in */ ; do
    if [[ -d "$dir" && "$dir" =~ ^[0-9]+ ]]; then  # Only search in numeric directories
        echo "Searching in directory $dir"
        ls `pwd`/$dir* >> $output_file
        
    fi
done
