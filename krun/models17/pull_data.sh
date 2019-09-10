DIR_PATH="/tmp/results"
mkdir -p $DIR_PATH

while [ true ]
do
  rsync -r --archive benchmarks@buis.irisa.fr:~/results $DIR_PATH
  ls -l $DIR_PATH/results | wc -l
  sleep 30
done
