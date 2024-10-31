##### accelerometer package issue

Problem: when training the model using trainClassificationModel, test-predictions.csv was not being created.
Error:Traceback (most recent call last):
  File "/home/aayush/accelerometer/process_acc.py", line 4, in <module>
    trainClassificationModel(
  File "/home/aayush/people_mobility_origin_dest/.oridest_venv/lib/python3.10/site-packages/accelerometer/classification.py", line 226, in trainClassificationModel
    Ypred = model.predict(Xtest)
  File "/home/aayush/people_mobility_origin_dest/.oridest_venv/lib/python3.10/site-packages/sklearn/ensemble/_forest.py", line 808, in predict
    proba = self.predict_proba(X)
  File "/home/aayush/people_mobility_origin_dest/.oridest_venv/lib/python3.10/site-packages/sklearn/ensemble/_forest.py", line 850, in predict_proba
    X = self._validate_X_predict(X)
  File "/home/aayush/people_mobility_origin_dest/.oridest_venv/lib/python3.10/site-packages/sklearn/ensemble/_forest.py", line 579, in _validate_X_predict
    X = self._validate_data(X, dtype=DTYPE, accept_sparse="csr", reset=False)
  File "/home/aayush/people_mobility_origin_dest/.oridest_venv/lib/python3.10/site-packages/sklearn/base.py", line 566, in _validate_data
    X = check_array(X, **check_params)
  File "/home/aayush/people_mobility_origin_dest/.oridest_venv/lib/python3.10/site-packages/sklearn/utils/validation.py", line 805, in check_array
    raise ValueError(
ValueError: Found array with 0 sample(s) (shape=(0, 70)) while a minimum of 1 is required.

Solution: The test dataframe was not having any sample. This was because the filtering being done in def trainClassificationModel() method in classification.py on line 157 was missing the testPIDs because it was comparing floats to string.

Changed the comparison with floats and it populated the testPIDs which made the rest of the pipeline work. So, the code was no longer escaping at testing phase due to empty test dataframe.

    if testParticipants is not None:
        testPIDs = testParticipants.split(',')
        PIDs_float = []
        for i in testPIDs:
            PIDs_float.append(float(i))
        test = data[data[participantCol].isin(PIDs_float)].copy()
        train = data[~data[participantCol].isin(PIDs_float)].copy()
        print(testPIDs)
        print(PIDs_float)
        print(data[participantCol].isin(PIDs_float))
        print(data[participantCol])
        print(test)

We were getting this error, "ValueError: Found array with 0 sample(s) (shape=(0, 70)) while a minimum of 1 is required." from sklearn/utils/validation.py because the test dataframe was not having any sample.
 
Specifically, in the trainClassificationModel() function (within the “classification.py” script), the comparison for "testPIDs" was only reading floats, while our participant IDs were recorded as strings. This caused the function to compare floats to strings, preventing the pipeline from functioning correctly and resulting in an empty Xtest matrix. Consequently, we were unable to obtain prediction results.
 
Therefore, he compared the participant IDs from the input as float datatype for the isin function.
 
Example:
>>> testpids = "37.0, 54.0"
>>> test_pids = testpids.split(",")
>>> test_pids
['37.0', ' 54.0']
>>> pd_data
   participantCol
0            37.0
1            54.0
>>> pd_data.dtypes
participantCol    float64
dtype: object
>>> test = pd_data[pd_data["participantCol"].isin(test_pids)]
>>> test
Empty DataFrame
Columns: [participantCol]
Index: []
>>> test_floats = [float(i) for i in test_pids]
>>> test = pd_data[pd_data["participantCol"].isin(test_floats)]
>>> test
   participantCol
0            37.0
1            54.0


##### Increasing accuracy of model we train using BalancedRandomForest

The problem might be with the features we generate from time series accelerometer values of (x, y, z). We need to generate better features to get accuracy close to what they report in their paper.

We have to convert features from time domain to frequency domain.

###### More info:
- We take the following features in temporal domain x,y,x and convert to spectral domain using FFT to obtain a set of 87 features.

- Frequency domain: https://pysdr.org/content/frequency_domain.html
Understanding what is frequency domain, conversion from time to frequency domain, properties in frequency domain without proofs and fast fourier transform.

- Different sources for feature extraction:
https://github.com/srvds/Human-Activity-Recognition?tab=readme-ov-file
https://github.com/jeandeducla/ML-Time-Series/tree/master
https://tsfel.readthedocs.io/en/latest/descriptions/get_started.html

This work is based on: https://arxiv.org/html/2402.19229v1

Faeture engineering techniques: https://www.youtube.com/watch?v=GduT2ZCc26E

what-is-the-best-way-to-remember-the-difference-between-sensitivity-specificity: [link](https://stats.stackexchange.com/questions/122225/what-is-the-best-way-to-remember-the-difference-between-sensitivity-specificity)

https://www.analyticsvidhya.com/blog/2022/07/step-by-step-exploratory-data-analysis-eda-using-python/
https://www.analyticsvidhya.com/blog/2021/09/complete-guide-to-feature-engineering-zero-to-hero/

https://nipunbatra.github.io/hmm/

https://mcgill-my.sharepoint.com/personal/hiroshi_mamiya_mcgill_ca/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fhiroshi%5Fmamiya%5Fmcgill%5Fca%2FDocuments%2FMicrosoft%20Teams%20Chat%20Files%2Fbjsports%2D2022%2DSeptember%2D56%2D18%2D1008%2Dinline%2Dsupplementary%2Dmaterial%2D1%20%283%29%2Epdf&parent=%2Fpersonal%2Fhiroshi%5Fmamiya%5Fmcgill%5Fca%2FDocuments%2FMicrosoft%20Teams%20Chat%20Files&ga=1

https://medium.com/@rehanmbl/extracting-time-domain-and-frequency-domain-features-from-a-signal-python-implementation-1-2-d36148c949ba

https://harvard-edge.github.io/cs249r_book/contents/dsp_spectral_features_block/dsp_spectral_features_block.html

https://scikit-learn.org/stable/modules/cross_validation.html#leave-one-group-out
https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.LeaveOneOut.html

https://bjsm.bmj.com/content/56/18/1008#DC1
https://learncsdesigns.medium.com/understanding-data-engineering-236cf6c16563

#### Features from csv
these are the features we do not generate by accProcess:
fft11
fft12
vmfft1
vmfft2
vmfft3
vmfft4
vmfft5
vmfft6
vmfft7
vmfft8
vmfft9
vmfft10
vmfft11
vmfft12

fft11 and fft12: These features represent the power of the accelerometry signal at 11 Hz and 12 Hz, respectively. In behavior classification, different frequencies can be indicative of different types of movement or activity. For instance, higher frequencies might be associated with more vigorous activities.

vmfft1 to vmfft12: These are likely normalized versions of the FFT (Fast Fourier Transform) results, possibly scaled by a factor like 1/30 Hz. These features provide insight into the power distribution across a range of frequencies, adjusted for a particular scaling factor. This can be especially useful in understanding finer gradations in movement frequencies, which might differentiate between subtle behaviors or types of motion.

#### Confusion matrix calculation (rows dropped)
adding more details for my own notes:

Confusion matrix for HMM --> generate model using trainClassification and use it for classifying outputs of accProcess by giving custom model as input.

Strange grey area in accPlot --> load in notebook and analyse data frame



Our findings for dropping rows in dataframes while calculating confusion matrix:

we drop NA items in predicted df
we drop duplicate time stamps in predicted df
we drop timestamps from predicted df which do not exist in actual_labels df
we drop NA items in actual_labels df
we drop timestamps from actual_labels df which do not exist in predicted df

So far, we found that (Number of dropped items from predicted df due to timestamp mismatch with actual_label df) was equal to sum of (Number of dropped items from actual_label df due to NA values) and (Number of dropped items from actual_label df due to timestamp mismatch with predicted df).



With the main drop coming from Number of dropped items from actual_label df due to NA values.

For this, we made the graph of MET values because if no MET value present then no annotation present.



We correlated this graph (as a representation of available actual_label values) with the output of accPlot (as a representation of output of accPlot). We found that there are indeed points in time where there are missing values from actual_label and we cannot do anything about it.



But then we found some values in accPlot which were leading to grey areas in the plot and yet we had records for them. We could not explain it and that is why we are looking explanation as mentioned above.


for the train process - get the processed epochs from /home/yacine/accel/epoch
then combine them for all participants then sort them based on timestamp.

Add these columns - participant,MET,label,annotation, remove time column.

then use it to train the HMM file.


### Clarification for walmsley epoch counts
Original Walmsley paper: https://bjsm.bmj.com/content/56/18/1008#DC1
 
In their calculation:
2501 hours
how many 30 second data rows?
2501 * 60 * 2 = 300,120 ~ total data rows
- Q: Did they mention anything about dropping data rows from this set?
- Because in table-1, they have 150,086 total observations.
Clarification:
if you consider 24 hour data for 151 participants, it means: 24*151 = 3624
which means they did not use all the data.
 
In our confusion matrix:
We used 24 * 151 * 60 * 2 = 434,880 (total set)
we dropped 169,301 out of this (NA values, duplicates, time stamp mismatch) leaving us with = 265,579 usable data


### Custom features added to walmsley model before HAR
We have x, y, z coordinates. They were combining x,y,z coordinates by taking the vector magnitude and then getting the median, min, max, 25thp, 75thp for those values.
What we added was, we took the median, min, max, 25thp, 75thp values for x,y,z directions separately. We added these extra 5 features per direction (~15 in total) to the existing feature set they had. We also kept existing percentiles as well for the combined vector.
 
        header += ",medianx,minx,maxx,25thpx,75thpx, iqrx";
        header += ",mediany,miny,maxy,25thpy,75thpy, iqry";
        header += ",medianz,minz,maxz,25thpz,75thpz, iqrz";               
        header += ",median,min,max,25thp,75thp";

### Default values for cp
def activityClassification(
    epoch,
    activityModel: str = "walmsley",
    mgCpLPA: int = 45,
    mgCpMPA: int = 100,
    mgCpVPA: int = 400):


