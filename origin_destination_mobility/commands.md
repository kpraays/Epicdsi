##### flow

process the data to get the Canada only rows --> merge them --> process the data --> load to db

##### use csvkit to filter rows
check the docs here: https://csvkit.readthedocs.io/en/latest/tutorial/1_getting_started.html

ISO_COUNTRY_CODE is column 29. It is either `"CA"` or `"US"`.

For the test sample: 
- checked most unique value from the sample filtered with CA country code. (only CA is there) (csvstat filename --maxfieldsize 131072000)
    csvgrep -c 29 -r ^"CA"$  /people_mobility_origin_dest/scripts/filtered.csv --maxfieldsize 131072000 > CA.csv
- did an inverted match with same query and compared the sum of matched + inverted match rows with the total rows --> equivalent...
    csvgrep -c 29 -r ^"CA"$  /people_mobility_origin_dest/scripts/filtered.csv --maxfieldsize 131072000 -i > US.csv

csvgrep -c 29 -r ^"CA"$ /people_mobility_origin_dest/monthly_data/2019/Monthly_Patterns_Foot_Traffic-0-DATE_RANGE_START-2019-01-01.csv.gz --maxfieldsize 131072000 > CA.csv

csvstat CA.csv --maxfieldsize 131072000

##### merging data using csvkit
nohup csvstack *.csv > ca_filtered.csv &

##### loading data in postgresql
\copy canada_data FROM '/people_mobility_origin_dest/scripts/processed_test3.csv' WITH (FORMAT csv, HEADER, NULL '');

We have strings as "" in the table which won't be accepted while loading data using copy command. Need to replace the double quote empty strings with \N which will be treated as the NULL character.

sed 's/old_char1/new_char1/g; s/old_char2/new_char2/g' large_file.csv > processed_file.csv

sed 's/,"",/,\\N,/g; s/,"\[/,{"/g' /people_mobility_origin_dest/scripts/test.csv > /people_mobility_origin_dest/scripts/processed_test1.csv

sed 's/,"",/,\\N,/g; s/\]",/}",/g' /people_mobility_origin_dest/scripts/processed_test1.csv > /people_mobility_origin_dest/scripts/processed_test.csv


sed 's/,"\[/,"{/g;s/\]",/}",/g' /people_mobility_origin_dest/weekly_data/filtered_weekly/weekly_ca_filtered.csv > /people_mobility_origin_dest/weekly_data/filtered_weekly/weekly_ca_filtered_processed.csv
