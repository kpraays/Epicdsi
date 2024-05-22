import deweydatapy as ddp

# API Key
apikey_ = ""

# Advan product path
pp_advan_wp = ""

meta = ddp.get_meta(apikey_, pp_advan_wp, print_meta = True)

files_df = ddp.get_file_list(apikey_, pp_advan_wp, 
                             start_date = '2019-01-01',
                             end_date = '2019-12-31',
                             print_info = True)
ddp.download_files(files_df, "/people_mobility_origin_dest/monthly_data/2019", skip_exists = True)
print("######### 2019 done #######")


files_df = ddp.get_file_list(apikey_, pp_advan_wp, 
                             start_date = '2020-01-01',
                             end_date = '2020-12-31',
                             print_info = True)
ddp.download_files(files_df, "/people_mobility_origin_dest/monthly_data/2020", skip_exists = True)
print("######### 2020 done #######")

files_df = ddp.get_file_list(apikey_, pp_advan_wp, 
                             start_date = '2021-01-01',
                             end_date = '2021-12-31',
                             print_info = True)
ddp.download_files(files_df, "/people_mobility_origin_dest/monthly_data/2021", skip_exists = True)
print("######### 2021 done #######")

files_df = ddp.get_file_list(apikey_, pp_advan_wp, 
                             start_date = '2022-01-01',
                             end_date = '2022-12-31',
                             print_info = True)
ddp.download_files(files_df, "/people_mobility_origin_dest/monthly_data/2022", skip_exists = True)
print("######### 2022 done #######")

files_df = ddp.get_file_list(apikey_, pp_advan_wp, 
                             start_date = '2023-01-01',
                             end_date = '2023-12-31',
                             print_info = True)
ddp.download_files(files_df, "/people_mobility_origin_dest/monthly_data/2023", skip_exists = True)
print("######### 2023 done #######")

files_df = ddp.get_file_list(apikey_, pp_advan_wp, 
                             start_date = '2024-01-01',
                             end_date = '2024-03-01',
                             print_info = True)
ddp.download_files(files_df, "/people_mobility_origin_dest/monthly_data/2024", skip_exists = True)
print("######### 2024 done #######")