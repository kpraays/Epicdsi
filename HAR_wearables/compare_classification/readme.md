### What was done?

We wanted to compare the classification performance across different epoch window sizes and different models.

For this, we picked:
    - following epochs: 10 seconds and 30 seconds
    - following models: walmsley original, custom walmsley with per direction percentile features added.

Which meant, We generated:
    - model for 10 seconds epoch without extra features.
    - model for 10 seconds epoch with extra features.
    - model for 30 seconds epoch with extra features.
    - (30 seconds epoch without extra features was the default)

We retrieved training data from CAPTURE-24:
    - It was captured per centi second. We divided based on epoch sizes.
    - Separated the labels and correlated it with the annotation dict [here](../accprocess/anno-label.csv). Divided 151 participants as 100 for training and 51 for test.