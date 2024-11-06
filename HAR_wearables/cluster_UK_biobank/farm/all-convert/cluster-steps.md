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
     
5. Implementation details:
Within the conversion-cluster folder, from where we launch the meta farm - we have: (dont forget to load the meta module)
job_script.h --> decides the agruments per job.
We take 1 hour per job and use 12GB memory based on running dummy conversion.

Once one or more metajobs in your farm are running, the following files will be created in the farm directory:
OUTPUT/slurm-$JOBID.out, one file per metajob containing its standard output,
STATUSES/status.$JOBID, one file per metajob containing the status of each case that was processed.

submit.run N [-auto] --> using auto will take care of all the cases - automatic resubmit

Each cluster has a limit on how many jobs a user can have at one time. (e.g. for Graham, it is 1000.)
With a very large number of cases, each case computation is typically short. If one case runs for <20 min, CPU cycles may be wasted due to scheduling overheads.
META mode is the solution to these problems. Instead of submitting a separate job for each case, a smaller number of metajobs are submitted, each of which processes multiple cases. 

Not all of the requested metajobs will necessarily run, depending on how busy the cluster is. But as described above, in META mode you will eventually get all your results regardless of how many metajobs run, although you might need to use resubmit.run to complete a particularly large farm.


We are executing this COMMAND for each case. Here, case means a line in table.dat.
For each line, we run this COMMAND="$COMM $METAJOB_ID", which is:
1 /home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/conversion_cluster/execute.sh 1
2 /home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/conversion_cluster/execute.sh 7
3 /home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/conversion_cluster/execute.sh 13
(note the line numberings are added automatically)

We are executing:
/home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/conversion_cluster/execute.sh 7  $METAJOB_ID
Within execute.sh:
We create $SLURM_TMPDIR - which is a temporary directory on the node where our script is running.
For 6 participants, we convert cwa to csv - (14GB space used)
Then use csv for getting acticounts which we store directly in our home account.

clean.run: clean all the files in the cluster directory except for job_script.sh, single_case.sh, final.sh, resubmit_script.sh, config.h, and table.dat.

submit.run N: submit N meta jobs.


When you submit the job, they will be queued by the SLURM scheduler then launched when they get resources allocated. Once, the jobs start being launched in the array, meta farm will start showing the status.

Status.run - current status of the cases.
query.run - status of jobs in the whole farm.