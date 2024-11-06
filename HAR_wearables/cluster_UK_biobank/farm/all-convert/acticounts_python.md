1. Beluga is not connected to internet but all the packages we need are available as wheels prebuilt for the cluster.

2. In our case, we will launch multiple jobs handling more than 1 cwa files to get acticounts. These jobs can be put on any combination of nodes available in the Beluga cluster. This means that we need to make sure that the node contains the packages and tools we require for processing the data. Further, we will also need to consider that reading and writing data (for small files) will lead to more transactions causing avoidable delay per job.

3. So,
    - We will create virtualenv for each job in the temporary local storage of each node (which gets released when the job finishes). But multiple jobs can be allocated to same node.