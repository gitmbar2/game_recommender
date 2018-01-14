## Spin up Amazon EMR cluster

To send startup files to cluster:
scp -i '~/.ssh/{.pem file}' '{filename}' hadoop@{cluster}:/home/hadoop/{filename}

1) scp a copy of the jupyspark-emr.sh script to the master node of EMR cluster  

2) ssh to cluster  

3) bash jupyspark-emr.sh

4) ssh tunnel port 48888  
ssh -NfL 48888:localhost:48888 spark


## Launch Cluster with n Nodes
bash scripts/start_emr.sh '{s3 bucket}' '{key name on aws}' 6

# Other
Change jupyspark 'export SPARK_HOME=/usr/lib/spark'
conda create --name py36 python=3.6
maybe remove some python path stuff from jupyspark-emr and hope it loads

## Hadoop stuff (unconfirmed)
$HADOOP_HOME/bin/hadoop fs -mkdir /user/input
$HADOOP_HOME/bin/hadoop fs -put /home/file.txt /user/input
$HADOOP_HOME/bin/hadoop fs -ls /user/input
