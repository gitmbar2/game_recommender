Spin up Amazon EMR cluster

To send startup files to cluster:
scp -i '~/.ssh/Spark.pem' '{filename}' hadoop@{cluster}:/home/hadoop/{filename}

1) scp a copy of the jupyspark-emr.sh script to the master node of EMR cluster  

2) ssh to cluster  

3) bash jupyspark-emr.sh

4) ssh tunnel port 48888  
ssh -NfL 48888:localhost:48888 spark