import os, sys
import pandas as pd

def get_files(data_path) -> None:
    total_csv = []
    for path, dirnames, filenames in os.walk(data_path):
        for file in filenames:
            if file.endswith(".csv"):
                total_csv.append(os.path.join(path, file))

    return sorted(total_csv)


def process_files(predicted_data_files):
    # print(f"Number of files: {len(predicted_data_files)}")
    PA3_final_all = []        
    for predicted_file in predicted_data_files:
    
        try:
            # some files do not have data or header row.
            PA3_csv = pd.read_csv(predicted_file)
            PA3_final_all.append(PA3_csv)
        
        except pd.errors.EmptyDataError:
            print(f"{predicted_file} has been skipped because header row was not there/ file empty.")
            
    return pd.concat(PA3_final_all)
    

def main(args):

    assert os.path.isdir(args[1])
    root, source_folders_names, files = next(os.walk(args[1]))
    source_folders = []
    for name in source_folders_names:
        source_folders.append(os.path.join(root, name))
    print(source_folders)
    batch_1 = get_files(source_folders[0])
    batch_2 = get_files(source_folders[1])
    predicted_data_files = batch_1 + batch_2   
    PA3_final_all = process_files(predicted_data_files)

    print(len(PA3_final_all))
    print(len(PA3_final_all[PA3_final_all.duplicated()]))
    without_duplicates = PA3_final_all.drop_duplicates()
    without_duplicates.to_csv("PA3_one_minute_without_duplicates.csv")
    
if __name__ == "__main__":
    args = sys.argv
    main(args)
    
