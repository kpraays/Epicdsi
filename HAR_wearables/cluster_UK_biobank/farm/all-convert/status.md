When lost access to data:

[kapmcgil@beluga4 conversion_cluster]$ query.run
140 running jobs, 0 queued jobs, 660 done jobs, 1 autoresubmit/final.sh jobs
 * 244/2121 successfully computed cases (current run)
 * 4790/6667 successfully computed cases (total)


 [kapmcgil@beluga4 conversion_cluster]$ query.run
Current run is done; out of 6667 total cases:
 * 0 cases failed
 * 1869 cases never ran


Which means 4,798 were done.
We would have to resume from 4790 - would need to check in which ordering did they pick from 4790 till 4798.