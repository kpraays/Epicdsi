#!/bin/bash
# done till here - 6665 /home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/conversion_cluster/execute.sh 59977
output_file="table.dat"
for ((i=59967; i<=115425; i=i+9)); do
    echo "/home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/conversion_cluster/execute.sh $i" >> "${output_file}"
done
