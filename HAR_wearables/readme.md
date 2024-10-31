1. Using accelerometer package, processed csv data files and predicted activities using walmsley model for CAPTURE-24 labelled dataset. Generated category classification for 30 second epochs using GNU parallel (40 jobs/ threads per batch).

2. Implemented random forest classifier for 100 participants of CAPTURE-24 dataset [https://ora.ox.ac.uk/objects/uuid:99d7c092-d865-4a19-b096-cc16440cd001] to compare the performance with reported findings from walmsley paper: [https://bjsm.bmj.com/content/56/18/1008#DC1].

What is CAPTURE-24 dataset?
This dataset contains Axivity AX3 wrist-worn activity tracker data that were collected from 151 participants in 2014-2016 around the Oxfordshire area. Participants were asked to wear the device in daily living for a period of roughly 24 hours, amounting to a total of almost 4,000 hours. Vicon Autograph wearable cameras and Whitehall II sleep diaries were used to obtain the ground truth activities performed during the period (e.g. sitting watching TV, walking the dog, washing dishes, sleeping), resulting in more than 2,500 hours of labelled data. 

3. Compared with cp values based on thresholding approach. Epochs were classified into activities based on thresholds of cp values.
    cpMVPA: moderate-vigorous
    cpSB:   sedentary
    cpLPA:  light

    if x_axis_value < 2860:             return 'sedentary'
    elif 2860 <= x_axis_value <= 3940:  return 'light'
    elif x_axis_value >= 3941:          return 'moderate-vigorous'

    Then compared using confusion matrix overall and based on gender of the participants because dataset had much more female participants.


#### AccProcess custom
4. AccProcess generates features from the csv values of the recorded accelerometer data of CAPTURE-24 dataset. That subset of features can be found [here](processAcc/features.txt). We 
additionally generated percentile features per direction from accelerometer data hoping it will lead to greater accuracy because it will capture greater movement data separately but there was no significant improvement in accuracy.


#### compare csv
5. Compared the performance of classification for HAR across walmsley prediction and cp values based cut-off thresholds.


### UKBioBank 100,000 participants
What is UKBioBank accelerometer data?
The acceleration data provides Physical Activity measurements recorded for 103,660 participants. The data is accessible through Beluga. The path for each data fields are provided in this document.

Biobank notes: "These files contain the raw acceleration data, per participant, from a single use (over a 7-day period) of the physical activity monitor. Format is native cwa as returned by the device. Files are typically 250MB each in the raw state and usually compress to around 100MB".

The UKBB raw data intially comes in a CWA file extension. Once converted to CSV, there are, we can observe that there are 4 variables: time, x, y, and z. There is data for 103,660 participants and 115,432 item counts. [docs](https://biobank.ndph.ox.ac.uk/ukb/field.cgi?id=90001)

Documentation by Yacine: [here](artefacts/Accelerometer_Project_Yacine.pdf)

6.  Defined PAs: What was the goal?

- PA1: ENMO threshold cut-offs for x axis acceleration values
    - 'CpSB', 'CpLPA', 'CpMVPA' (see point 3 above)

- PA2: random forest classifier based walmsley model (ML) (mainly interested in moderate-vigorous performance because that is the most tricky)

- PA3: reverse engineered acticounts method
    - Used open source implementation for generating the ActiGraph physical activity counts from acceleration measured with an alternative device available [here](https://github.com/jbrond/ActigraphCounts/tree/master) specifically this [python script](https://github.com/jbrond/ActigraphCounts/blob/master/R/Python_G_to_sec.py).



7. accProcess predicted output for 22 randomly chosen participants from UKBioBank dataset
This was done to calculate the proportions of moderate-vigourous, light, sedantary and sleep activities in the UKBioBank dataset with the accProcess outputs over the whole week so that we do not have to generate PA2 for all 100,000 participants if they are the similar.

- Note on suitability of walmsley model and using weekly predicted proportions for PA2 supplied as part of UKBioBank dataset: [here](compare_weekly_proportions_UKBioBank/readme.md)


8. cwa conversion to csv files and acticount calculation: [cwa_csv_processing](cluster_UK_biobank/cwa_csv_processing)


9. This paper [Self-supervised learning for human activity recognition using 700,000 person-days of wearable data] (https://www.nature.com/articles/s41746-024-01062-3) discussed the latest landscape of accelerometer research in the industry - using transfer learning and foundational models.
    Questions explored:
    1. target domain has new classes as part of mvpa - if the source domain only has mvpa, pa lpa, sedentary and sleeping - and if the target domain has additional activities like bicycling within mpa - we have one more class in the target domain which is not present in the source domain - is it feasible based on what they presented in the paper? ) [reference: mvpa can be divided into several diff activities] 
    2. we have the same features in the source and target  but the target may contain extra activities within mvpa - mvpa is divided into running, bicycling riding - how much labelled information do we need to do accurate classification of unseen classes? - original training data does not have the unseen labels - how much new labelled data we need for the old model to work on with the new labels?
    3. How much data has been used to create the foundational model?


10. Cluster work
    - PA1: We predicted categories of activities for 60 sec epochs across 100,000 participants. Multiple jobs were submitted on compute Canada Beluga cluster.
    
    - PA2: We used the weekly proportions already provided since they were same as walmsley predictions.

    - PA3: We calculated this for 100,000 participants from raw cwa data.
        - This involved converting cwa data to csv data files and calculating acticounts for all participants. Then using cutoffs, epochs were mapped to activity category ranging from moderate-vigorous, light, sedentary. As the number of participants is so large and per participant, we have ~1GB sized csv file - this meant we had to distributed the computation over cluster using meta farm. Over 2 days, processing was done in batches of 800 jobs with upper bound of 1 hour per batch. Due to scheduling delays on cluster since we did not have exclusive access, final time taken was 2 days. More information: [cluster_UK_biobank](cluster_UK_biobank)

the threhold count, for 60 second epoch is  
Light: 0 - 2689 CPM
Moderate: 2690 - 6166 CPM
Vigorous: 6167 - 9642 CPM


10. Foundation model

11. 
How does the whole picture fit? What is the purpose of this work?