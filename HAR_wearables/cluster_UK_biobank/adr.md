# Processing >100k (participants) cwa files to acticounts (PA3)

## Context and Problem Statement
There are 100k participants. Each participant has a cwa file and each cwa file is ~300mb in size. It needs to be converted to csv on which we apply the acticount calculation script to get the values per 60 sec epoch. These epochs are to be classified to different categories of human activity (sedantary, moderate-vigorous, light) based upon designated thresholds. All the data is proprietary and is resides in Beluga cluster for Compute Canada and it cannot be moved out of the environment. Each converted csv file will be 1GB in size. There is no network access on Beluga for installing external dependencies. Needs to be preapproved.


## Considered Options

* Spark
* Meta Farm

## Decision Outcome

Chosen option: "MetaFarm".
Apache spark could work but not sure how fast it would be considering we used a custom PA3 method with extra libs - these would need to be taken care through spark cluster but I didnt do it as taking those allocations first on compute Canada would have slowed us down.


#### Source:
Based off adr short template example found [here](https://adr.github.io/madr/examples.html)