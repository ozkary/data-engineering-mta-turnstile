#!/bin/bash
# Submit Python code to SparkMaster
# ref 
# https://spark.apache.org/docs/latest/structured-streaming-kafka-integration.html#deploying

# As with any Spark applications, spark-submit is used to launch your application. spark-sql-kafka-0-10_2.12 and its dependencies can be directly added to spark-submit using --packages, such as,

# ./bin/spark-submit --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2 ...
# For experimenting on spark-shell, you can also use --packages to add spark-sql-kafka-0-10_2.12 and its dependencies directly,

# ./bin/spark-shell --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.apache.spark:spark-core_2.12:3.3.2,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.2

# org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,
# org.apache.spark:spark-core_2.12:3.3.2,
# org.apache.spark:spark-avro_2.12:3.3.2,
# org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.2 \			 

if [ $# -lt 1 ]
then
	echo "Usage: $0 <pyspark-job.py> [ executor-memory ]"
	echo "(specify memory in string format such as \"512M\" or \"2G\")"
	exit 1
fi
PYTHON_JOB=$1

if [ -z $2 ]
then
	EXEC_MEM="1G"
else
	EXEC_MEM=$2
fi

# spark-submit program.py --topic mta-turnstile --group turnstile --client appTurnstile --config ~/.kafka/azure.properties
spark-submit --num-executors 2 \
	         --executor-memory $EXEC_MEM --executor-cores 1 \
             --packages org.apache.spark:spark-sql-kafka-0-10_2.12:3.3.2,org.apache.spark:spark-avro_2.12:3.3.2,org.apache.spark:spark-streaming-kafka-0-10_2.12:3.3.2,com.microsoft.azure:azure-eventhubs-spark_2.12:2.3.22 \
             $PYTHON_JOB --topic mta-turnstile --group com.microsoft.azure --client appTurnstile --config ~/.kafka/azure.properties > output.log

# run as bash submit-program.sh program.py             