module load python/3.10
# all the packages we need except resampy get loaded with scipy-stack
module load scipy-stack

# Define the environment directory
ENV_DIR="$SLURM_TMPDIR/env"

# Check if the directory exists and contains a valid virtual environment
if [ -d "$ENV_DIR" ] && [ -f "$ENV_DIR/bin/activate" ]; then
    echo "Virtual environment already exists in $ENV_DIR."
else
    echo "Creating new virtual environment in $ENV_DIR..."
    virtualenv --no-download "$ENV_DIR"
fi

source $SLURM_TMPDIR/env/bin/activate
pip install --no-index resampy

METAJOB_ID=$2

mkdir -p $SLURM_TMPDIR/$METAJOB_ID
mkdir -p $SLURM_TMPDIR/$METAJOB_ID/csv
csv_dir="$SLURM_TMPDIR/$METAJOB_ID/csv"

second_dir="/home/kapmcgil/projects/def-hiroshi/kapmcgil/processed_output/second/$METAJOB_ID"
minute_dir="/home/kapmcgil/projects/def-hiroshi/kapmcgil/processed_output/minute/$METAJOB_ID"

mkdir -p $second_dir
mkdir -p $minute_dir

cp -r /home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/scripts $SLURM_TMPDIR/$METAJOB_ID
echo `ls $SLURM_TMPDIR/$METAJOB_ID/scripts`

filelist="/home/kapmcgil/projects/def-hiroshi/kapmcgil/all-convert/helper/create_filelist/files.txt"

for(( ith=$1; ith<=$1+6; ith++ )); do
    FILE=`sed -n ${ith}p $filelist`
    $SLURM_TMPDIR/$METAJOB_ID/scripts/cwa-convert $FILE -out $csv_dir/$(basename $FILE).csv &> /dev/null
    echo $SLURM_TMPDIR/$METAJOB_ID
    echo $FILE
    echo $csv_dir/$(basename $FILE).csv

done

python $SLURM_TMPDIR/$METAJOB_ID/scripts/csv_to_counts.py $csv_dir $second_dir $minute_dir 100
echo $csv_dir
echo $second_dir
echo $minute_dir
# echo `cat $SLURM_TMPDIR/$METAJOB_ID/scripts/csv_to_counts.py| head -1`
# echo `ls $SLURM_TMPDIR/$METAJOB_ID/scripts`


