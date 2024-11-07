### What was done?
1. Monthly data downloaded for origin destination source dataset: for 5 years (2019-2024)
    - Loaded in lab database. Data located locally in people_mobility_origin_dest directory.
    - filtering and stacking done before it was loaded in postgresql database.
    - Weekly data across 6 weeks from different period (per 2 weeks batch) also stored there.

2. Data was pulled from [https://www.deweydata.io/](https://www.deweydata.io/). Size over 100GB. API keys and tokens have not been mentioned in the uploaded code.
    - [get_monthly_data](get_monthly_data.py): retrieved data
    - filtering, processing done using: [filter_data](filter_data.py) [combine_files](combine_files.py)
    - refer to commands used here: [commands_dewey_pull](commands.md)
 

