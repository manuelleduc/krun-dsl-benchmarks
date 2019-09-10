DIR_PATH="/tmp/results"
mkdir -p $DIR_PATH

while [ true ]
do
  ssh benchmarks@buis.irisa.fr 'rm ~/krun/models17/models17.manifest; reboot'
  sleep 30
done
