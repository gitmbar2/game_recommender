# Source for various Spark tests

# Testing client
pyspark \
  --master yarn \
        --deploy-mode client \
	--executor-memory 10G \
        --executor-cores 4 \
	--driver-memory 10G \
        --driver-cores 4 \
	--packages com.databricks:spark-csv_2.11:1.5.0 \
	--packages com.amazonaws:aws-java-sdk-pom:1.10.34 \
	--packages org.apache.hadoop:hadoop-aws:2.7.3 \
	--files go_to_sleep.in \
  spark_test.py

# Testing cluster
/usr/bin/spark-submit \
  --master yarn \
  --deploy-mode cluster \
  --queue default \
  --num-executors 20 \
  --executor-memory 1G \
  --executor-cores 2 \
  --driver-memory 1G \
  --files go_to_sleep.in \
  spark_test.py

# merge and get files
hadoop fs -getmerge go_to_sleep.out/ combined_file.out
