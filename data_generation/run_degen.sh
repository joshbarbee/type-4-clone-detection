END=$2
START=$1
for ((i=START;i<=END;i+=500)); do
    echo ON BATCH $i
    python degen.py gen $i $3
done