### what was done?

- PA1: ENMO threshold cut-offs for x axis acceleration values
    - 'CpSB', 'CpLPA', 'CpMVPA' (see point 3 above)

"why 4 threads?"
Because the number of cores per machine was 2 in the SLURM request - so it will be able to run 4 threads (two threads per core is common concurrency) at the same time. Putting more would still not make them run together at the same time. This is why we can spin multiple jobs.
 
"it imght get a slightly more larger job load, if we have to conver CWA into CSV  and apply a filter to generate PA3 in the future as extra work , so good to anticipate for that"
For this, submitting multiple jobs approach will be the best because we will need external library to convert CWA to CSV.
 
"can you then generate the CP-MVPA and others I programmed for each timeeries with, with eid (filename of each time-series) asap, and if not let me know I will generate myself as it is urgent - and importantly measure the computation time"
Yes, I can using the script you gave. By the time, you wake up and read this message, it should be underway.

PA1 scripts from beluga


- PA2: random forest classifier based walmsley model (ML) (mainly interested in moderate-vigorous performance because that is the most tricky)

- PA3: reverse engineered acticounts method

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