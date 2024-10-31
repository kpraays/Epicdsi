import os
import csv

src_files = "/home/aayush/accelerometer/cwa-csv/count_sec_python/30hz"
csv_files = next(os.walk(src_files))[2]

freq_per_sec = 1 # Run sum combined the values exceeding the threshold using window size of 10hz
# making the output 1 record per 1 second.
lines_sum = freq_per_sec * 60
# /home/aayush/accelerometer/cwa-csv/count_sec_python/30hz/30hz1049632_90001_0_0.cwa.csv

dest_path = os.path.sep.join(src_files.split(os.path.sep)[:-1]+["aggregated"])
os.makedirs(dest_path, exist_ok=True)

for data_file in csv_files:
    with open(os.path.join(src_files, data_file), "r") as csv_data:
        with open(os.path.join(dest_path, data_file), "w", newline="") as csv_out:
            fieldnames = ["axis1","axis2","axis3"]
            writer = csv.DictWriter(csv_out, fieldnames=fieldnames)
            writer.writeheader()
                    
            reader = csv.DictReader(csv_data)
            sum_axes = [0, 0, 0]
            count = 0
            
            for row in reader:                
                if count == lines_sum:
                    writer.writerow({"axis1": sum_axes[0], "axis2": sum_axes[1], "axis3": sum_axes[2]})
                    sum_axes = [0, 0, 0]
                    count = 0

                sum_axes[0] += float(row["axis1"])
                sum_axes[1] += float(row["axis2"])
                sum_axes[2] += float(row["axis3"])
                count += 1
            
            # write the last remaining values
            writer.writerow({"axis1": sum_axes[0], "axis2": sum_axes[1], "axis3": sum_axes[2]})
            

            