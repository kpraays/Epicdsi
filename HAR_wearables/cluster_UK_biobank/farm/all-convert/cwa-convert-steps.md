1. Beluga does not have access to internet so we need to manually load the files for cwa-convert tool. Obtain the build files here and add them in the folder: cwa-convert.build - https://github.com/digitalinteraction/openmovement/tree/master/Software/AX3/cwa-convert/c (Files needed: main.c, cwa.c, cwa.h)


2. Build the tool as follows: (assuming executed from within parent director) - cd cwa-convert.build && gcc main.c cwa.c -lm -O2 -o ../cwa-convert && cd -

3. Check if everything alright: cwa-convert --help
    Expected output:
        $ ./cwa-convert --help
        ERROR: File not specified
        CWA-Convert by Daniel Jackson, 2010-2021
        Usage: CWA <filename.cwa> [-f:csv|-f:raw|-f:wav] [-v:float|-v:int] [-t:timestamp|-t:none|-t:sequence|-t:secs|-t:days|-t:serial|-t:excel|-t:matlab|-t:block] [-no<data|accel|gyro|mag>] [-light] [-temp[c]] [-batt[v|p|r]] [-events] [-amplify 1.0] [-start 0] [-length <len>] [-step 1] [-out <outfile>] [-blockstart 0] [-blockcount <count>]

4. ./cwa-convert filename -out output_filename
    What we use?
    ./cwa-convert filename -out output_filename &> /dev/null
    The tool prints the '*' for each character in stderr on terminal. We do not want this to take up space in the log files when run in meta farm so we are silencing the output.
    **WARNING: This means if the tool is not able to process some cwa file for some reason, that job's error will be suppressed and the only indication will be not obtaining the csv file for that cwa input.**
    We silence the output because the space in scratch directory is limited though we have 8TB buffer. (`TODO: for later if needed`)

