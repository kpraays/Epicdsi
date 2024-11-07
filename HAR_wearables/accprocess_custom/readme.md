#### AccProcess custom
- AccProcess generates features from the csv values of the recorded accelerometer data of CAPTURE-24 dataset. That subset of features can be found [here](../processAcc/features.txt). We 
additionally generated percentile features per direction from accelerometer data hoping it will lead to greater accuracy because it will capture greater movement data separately but there was no significant improvement in accuracy.

- Some changes were made to accelerometer [package](https://pypi.org/project/accelerometer/) because it was not working out the box on capture-24 dataset for walmsley prediction. [More info](accelerometer_lib_mod/readme.md).