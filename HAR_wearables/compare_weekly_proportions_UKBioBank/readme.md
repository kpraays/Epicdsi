### Summary
1. We had to check if the proportions supplied for the activity classification per week for 100,000 participants was similar to the output we got for walmsley model /and our custom trained model to decide whether we need to calculate these proportions again if there are significant deviations in the predicted vs supplied proportions of activities for our sample.

2. We made random selection of 22 participants and calculated proportions of predicted activities across the week using walmsley and our custom model. This was repeated twice using different set of participants.

3. We found that the supplied proportions were similar to the output seen from the walmsley predictions so we did not calculate the proportions again for 100,000 participants.

### What was done?
- Trained a new model for 5 seconds epoch using capture24 to be used for accProcess prediction on random 22 second set so that 5 seconds epochs can be correctly compared. Then used that for making predictions on the randomly selected set of 22 participants for 5 second epoch.

- The model was trained with 100 participants as training data and remaining 50 as test data. Had to run parallel because it was slow (~90 minutes after parallel - 5)

### Result
We trained new models for 30 sec epoch and 5 sec epoch where the train set was 100 participants and 3000 trees for 5 sec epoch.

This is the conclusion:
random 22 - old set of random 22: we used the model with complete set of data as training and we got close results. Same seen from the idea behind walmsley.
random-22 - new set of random 22: we used new models with 100 participants for train set like they had done in new paper - we did not get close results.
We used walmsley and we got close results.

We would like to trust the development based on 100/50 (new script from the better paper) rather than Walmsley, but we think the duration of MVPA form the new model is impossibly high, so we have to settle with the original accprocess Walmsley.