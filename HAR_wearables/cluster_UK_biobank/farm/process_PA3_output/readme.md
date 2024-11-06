### what is happening here?

We are assigning labels to PA3 activities based on the following thresholds.

```
def categorize_activity(axis1_value):
    if axis1_value < 2860/2:
        return 'sedentary'
    elif 2860/2 <= axis1_value <= 3940/2:
        return 'light'
    elif axis1_value >= 3941/2:
        return 'moderate-vigorous'
    else:
        return 'NaN'  # In case there's an unexpected value
```

We do it for each folder containing roughly 1000 participants and then determine proportion of the assigned labels per participant.

Reminder: the data contains aggregated values per 1 min for each participant over a whole week. So, each participant's data file has roughly 10000 rows.

We store 2 output files:
1. csv with assigned labels to the 1 min epochs.
2. A single proportion file per folder for 1000 participants.


### Steps:

1. Call convert.py on the output files per folder of UKBioBank dataset. We processed 100,000 cwa files to csv then calculated acticounts. About 800 candidates were processed together per job on cluster and outputs stored per job folder. We read those output files as input to this script and labels are assigned based on the thresholds. Later, proportions are calculated based on those labels.

2. Then we merge all the separate files into single pandas dataframe we store as csv.


### Note on duplicates

We had run the jobs in two batches. We had run multiple parallel jobs per batch over a span of two days. In between, there was an interruption where we lost access to data in beluga because of UKBioBank registration issue. During that time, the jobs which were already in progress had failed one by one. They were later resubmitted to get the final output.
 
The duplication in entries is likely because of those resubmitted jobs. Fortunately, when we were generating PA3 proportions we were doing it on the basis of file paths which will be different even though the participantID is the same. We retrieved duplicate files per participant. 

There are multiple participant IDs in the combined dataframe because of some participants being processed again after interruption to Beluga cluster when processing was in progress.
We checked the number of lines and the last processed record for ALL such double participants and found only 40 participants where the line count or the last line does not match. This means we only need to inspect those 40 participants out 100,000 in the final proportion list.

So this means in the combined dataframe, there should be duplicate rows such that the values for each of the following will be the same [participant_id	light	moderate-vigorous	sedentary]. We checked this and in the combined dataframe there are about 2951 records which are duplicates of existing ones.

- In the combined dataframe, We will drop the duplicate records corresponding to 2951 participants.
- For these 40 participants, each has got two files - one of them is always empty. When we had generated proportions for all 100,000 participants, we had added a condition to check for and ignore empty files so for these 40 participants we should have included the valid data files. So, we should be good for these participants as well.
 
So conclusion: If we combine all the proportion csv files and drop duplicates - about 2951 records will be dropped and we should have 102,899 records in the end.
 
For reference, there should be 105795 participants in the combined file out of which 2951 are duplicates which after dropping will yield in total 102845 participants as seen in the csv attached.