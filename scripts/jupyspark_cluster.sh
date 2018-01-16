#!/bin/bash
source ~/.bashrc
export SPARK_HOME=/usr/lib/spark
export PYTHONPATH=${SPARK_HOME}/python:$PYTHONPATH
export PYSPARK_PYTHON=$HOME/anaconda/bin/python
export PYSPARK_DRIVER_PYTHON=jupyter \
export PYSPARK_DRIVER_PYTHON_OPTS="notebook --no-browser --NotebookApp.ip='0.0.0.0' --NotebookApp.port=48888" \

${SPARK_HOME}/bin/pyspark \
	--master yarn \
        --deploy-mode cluster \
	--executor-memory 10G \
        --executor-cores 4 \
	--driver-memory 10G \
        --driver-cores 4 \
  --num-executors 50 \
	--packages com.databricks:spark-csv_2.11:1.5.0 \
	--packages com.amazonaws:aws-java-sdk-pom:1.10.34 \
	--packages org.apache.hadoop:hadoop-aws:2.7.3 \
  1000


##
/usr/bin/spark-submit \
  --master yarn \
    --deploy-mode cluster \
  --queue default \
  --num-executors 20 --executor-memory 1G --executor-cores 2 \
  --driver-memory 1G \
  --files {files}
  sleepy.py

/usr/bin/spark-submit \
  --master yarn
  --deploy-mode cluster
  --queue default
  --num-executors 20
  --executor-memory 1G
  --executor-cores 2
  --driver-memory 1G
  --files go_to_sleep.in
  spark_test.py


hadoop fs -getmerge go_to_sleep.out/ combined_file.out
