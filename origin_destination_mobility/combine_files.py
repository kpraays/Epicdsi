import os
import subprocess
from datetime import datetime

log_path = "/people_mobility_origin_dest/scripts/process_data/logs"
processed_path = "/people_mobility_origin_dest/monthly_data_processed"
stacked_path = '/people_mobility_origin_dest/monthly_files_stacked'
maxfieldsize = '131072000'

class logger:
    def __init__(self) -> None:
        timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
        log = f"{log_path}/Process_data_{timestamp}.log"
        with open(log, "w") as log_file_save:
            log_file_save.write("################################################\n")
            log_file_save.write("|Timestamp| + \t + |Func| + \t + |Message|\n")
        self.log_file = log
    
    def log(self, func, message) -> None:
        with open(self.log_file, "a") as log_file_save:
            timestamp = datetime.now().strftime("%m-%d-%Y-%H-%M-%S")
            log_message = timestamp + "\t" + func + "\t" + message
            log_file_save.write(log_message + "\n")

logging = logger()

def get_files(data_path) -> None:
    total_csv_zipped = []
    for path, dirnames, filenames in os.walk(data_path):
        logging.log("get_files", f"Looking for data files in {path}.")
        for file in filenames:
            if file.endswith(".csv"):
                # paths contains the base directory for that file.
                # dirnames contains other directories within this folder.
                # filenames contains the list of filenames within path.
                total_csv_zipped.append(os.path.join(path, file))
                logging.log("get_files", f"Found FILE:{file} in PATH:{path}.")
    logging.log("get_files", "#################################################################################")
    logging.log("get_files", f"######### Total files in the data path: {len(total_csv_zipped)} #########")
    logging.log("get_files", "#################################################################################")
    return total_csv_zipped


def combine_files(file_list):        
    logging.log("process_data", f"Store processed files in :{processed_path}.")
    for compressed_file in file_list:
        path_vars = compressed_file.split("/")
        # output_file = os.path.join(processed_path, path_vars[-2], f"{path_vars[-1][:-7]}_CA.csv")
        output_file = os.path.join(processed_path, f"{path_vars[-1][:-7]}_CA.csv")
        # command = ['csvgrep', '-c', '29', '-r', '^"CA"$', compressed_file, '--maxfieldsize', maxfieldsize]
        command = f'csvgrep -c 29 -r ^"CA"$ {compressed_file} --maxfieldsize 131072000 > {output_file}'
        logging.log("process_data", f"file to be processed: {compressed_file}")
        logging.log("process_data", f"Command to be executed: {command}")
        logging.log("process_data", f"Saved the output at: {output_file}")
        with open(output_file, "w") as outfile:
            subprocess.run(command, shell=True)
    logging.log("process_data", "Processed all the data files.")    
    
if __name__ == "__main__":
    file_list = get_files(data_path=processed_path)
    combine_files(file_list=file_list)
    