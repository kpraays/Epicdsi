'''
Use as follows:
python /process_PA3_output/convert.py /processed_minute/batch_1 /process_PA3_output/assigned_labels/batch_1 /process_PA3_output/proportions_one_minute/batch_1
python convert.py location_batch_1_per_folder_output batch_1_assigned_labels output_proportions
'''

import os, sys
import pandas as pd

def get_files(data_path) -> None:
    total_csv = []
    for path, dirnames, filenames in os.walk(data_path):
        for file in filenames:
            if file.endswith("_0_0.cwa.csv"):
                total_csv.append(os.path.join(path, file))

    return sorted(total_csv)


def categorize_activity(axis1_value):
    if axis1_value < 2860:
        return 'sedentary'
    elif 2860 <= axis1_value <= 3940:
        return 'light'
    elif axis1_value >= 3941:
        return 'moderate-vigorous'
    else:
        return 'NaN'  # In case there's an unexpected value

def process_files(predicted_data_files):
    # print(f"Number of files: {len(predicted_data_files)}")
    PA3_final_all = []        
    for predicted_file in predicted_data_files:
        
        predicted_id = int(predicted_file.split("/")[-1].split("_")[0])
        # print(predicted_id)
        try:
            # some files do not have data or header row.
            PA3_csv = pd.read_csv(predicted_file)
            PA3_csv["participant_id"] = predicted_id
            
            # Apply the function to categorize each row based on axis1 values
            PA3_csv["PA3_predicted"] = PA3_csv['axis1'].apply(categorize_activity)
            PA3_final_all.append(PA3_csv)
        
        except pd.errors.EmptyDataError:
            print(f"{predicted_file} has been skipped because header row was not there/ file empty.")
            
    return PA3_final_all    
    

def main(args):

    assert os.path.isdir(args[1])
    root, source_folders_names, files = next(os.walk(args[1]))
    source_folders = []
    for name in source_folders_names:
        source_folders.append(os.path.join(root, name))
        
    assigned_labels_dest = args[2]
    proportions_dest = args[3]
    
    for each_folder in sorted(source_folders):
        # folder_name is /home/kapmcgil/projects/def-hiroshi/processed_minute/batch_1/folder_1/1007834_90001_0_0.cwa.csv
        folder_name = each_folder.split("/")[-1]
        
        predicted_data_files = get_files(each_folder)
        print(len(predicted_data_files))
        PA3_final_all = process_files(predicted_data_files)

        PA3_final_all_pd = pd.concat(PA3_final_all, ignore_index=True, axis=0)
        PA3_dest_path = os.path.join(assigned_labels_dest, f"{folder_name}_activities.csv")
        PA3_final_all_pd.to_csv(PA3_dest_path, index=False)
            
        PA3_proportions = PA3_final_all_pd.groupby("participant_id", group_keys=True)["PA3_predicted"].value_counts(normalize=True).unstack()
        PA3_proportions_dest = os.path.join(proportions_dest, f"{folder_name}_proportions.csv")
        PA3_proportions.to_csv(PA3_proportions_dest, index=True)


if __name__ == "__main__":
    args = sys.argv
    main(args)
    
