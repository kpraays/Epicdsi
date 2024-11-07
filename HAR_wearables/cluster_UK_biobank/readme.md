### What was done?

#### cwa_csv_processing

1. We converted cwa raw accelerometer data files to csv files using cwa-convert [utility](https://github.com/openmovementproject/openmovement/blob/master/Software/AX3/cwa-convert/c/README.md)

2. Then we calculated acticounts using opensource implementation found [here](https://github.com/jbrond/ActigraphCounts/blob/master/R/Python_G_to_sec.py)

3. We aggregated the counts generated at per second to 60 seconds epochs.
    - input data: 100hz
    - output: 10hz
        Run sum combined the values exceeding the threshold using window size of 10hz
        making the output 1 record per 1 second.
    - more information: ![here](../../artefacts/output_freq_cwa_csv.jpeg)

#### farm
- We processed 100,000 participants cwa files in 2 days over Compute Canada cluster using job farm. Suspend and resume functionality was provided with the job submission being handled in batches.

- To obtained final activity proportions, classification based on acticounts thresholds was done.


**why 4 threads?**
Because the number of cores per machine was 2 in the SLURM request - so it will be able to run 4 threads (two threads per core is common concurrency) at the same time. Putting more would still not make them run together at the same time. This is why we can spin multiple jobs.
 


### What are the PAs?
- PA1: ENMO threshold cut-offs for x axis acceleration values
    - 'CpSB', 'CpLPA', 'CpMVPA'

- PA2: random forest classifier based walmsley model (ML) (mainly interested in moderate-vigorous performance because that is the most tricky)

- PA3: reverse engineered acticounts method


#### Generate PA1 (cutoffs)
```
funcCP <- function(x){
  SB = sum(x$acc <= 50, na.rm = TRUE) # count of non-missing below 50
  LPA = sum(x$acc > 50 & x$acc < 100, na.rm = TRUE)
  MVPA = sum(x$acc >= 125, na.rm = TRUE)
  MVPA2 = sum(x$acc >= 100, na.rm = TRUE)
  MVPA3 = sum(x$acc >= 150, na.rm = TRUE)
  VPA = sum(x$acc >= 400, na.rm = TRUE)
  total = nrow(x)
  missing = sum(is.na(x$acc), na.rm = TRUE)
  return(data.frame(
    SB=SB, 
    LPA=LPA, 
    MVPA=MVPA, 
    MVPA2=MVPA2, 
    MVPA3=MVPA3, 
    total=total, 
    missing=missing, 
    MVPA_total = MVPA/total, # proportion over total, each observation is 5 sec
    MVPA2_total = MVPA2/total, # proportion over total, each observation is 5 sec
    MVPA3_total = MVPA3/total, # proportion over total, each observation is 5 sec
    VPA_total = VPA/total,
    LPA_total = LPA/total, 
    SB_total = SB/total, 
    meanENMO = mean(x$acc, na.rm = TRUE)))
}
```


### PA 3 processing on the cluster
1. Beluga is not connected to internet but all the packages we need are available as wheels prebuilt for the cluster.

2. In our case, we will launch multiple jobs handling more than 1 cwa files to get acticounts. These jobs can be put on any combination of nodes available in the Beluga cluster. This means that we need to make sure that the node contains the packages and tools we require for processing the data. Further, we will also need to consider that reading and writing data (for small files) will lead to more transactions causing avoidable delay per job.

3. So,
    - We will create virtualenv for each job in the temporary local storage of each node (which gets released when the job finishes). But multiple jobs can be allocated to same node.

### farm details

1. We use meta farm for running the jobs. The advantage of using it being efficient job allocation and resubmit functionality. It abstracts a lot of job management tasks. On Beluga cluster, a user can submit only 1000 jobs (running and queued) at a time. Also, internet is not accessible on the Beluga cluster.

2. Our task is to launch a large number of jobs using meta farm such that each job can process a certain number of files. We have to ensure that the wait time for each job in the farm is as little as possible while ensuring that the workload is handled without issues per job. Through trial and error, found that 12GB is appropriate memory per job (keeping the reservation cost low) with 1 hour time limit (least time possible for Beluga job submission), this should cause less time to be spent in resource allocation for the job after submission. We will be submitting close to the max limit of jobs on the cluster allowed per user.

3. Since these jobs can be randomly assigned to nodes, we will copy the prebuilt binaries to nodes (assuming same OS+architecture on all nodes) for cwa-csv conversion tool. Then, we create a virtual environment on each node in the $SLURM_TEMP directory (local storage on the node for faster transactions - quick reads and writes - code files). Before creating virtual environment, we load python3.10 and scipy-stack module on the node so that we do not have to pip install these packages. We make sure to disable download options and make it use indexed packages/ wheels.

4. Some numbers:
    - Environment/ package setup - 45 secs
    - per file time: (6 min) [this is the upper bound - conservative estimate]
        - cwa to csv - 1:15 min
        - acticounts - 4 min
    - per job time: 1 hour
        - process (6 files)


