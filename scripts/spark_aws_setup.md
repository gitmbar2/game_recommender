## Spin up Amazon EMR cluster

To send startup files to cluster:
scp -i '~/.ssh/{.pem file}' '{filename}' hadoop@{cluster}:/home/hadoop/{filename}

ex:
scp -i '~/.ssh/{.pem file}' ./scripts/start_emr hadoop@{master}:/home/hadoop/start_emr

1) scp a copy of the jupyspark-emr.sh script to the master node of EMR cluster  

2) ssh to cluster  
ex:
ssh -i '~/.ssh/{key}.pem' hadoop@{master}

3) bash jupyspark-emr.sh

4) ssh tunnel port 48888  
ssh -NfL 48888:localhost:48888 spark


## Launch Cluster with n Nodes
bash scripts/start_emr.sh '{s3 bucket}' '{key name on aws}' 6

# Hadoop Commands
hadoop fs -mkdir /steam
hadoop fs -put /home/file.txt /steam
hadoop fs -ls /steam

# Get data from S3
df -hk (free disk space)

aws s3 cp s3://michaelbarton-first-bucket/steam_big.sql.gz steam_big.sql.gz


# Attempt to unzip and read from stdin
hdfs dfsadmin -report (free space on hdfs)

gunzip -c compressed.tar.gz | hadoop fs -put - /user/files/uncompressed_data

hadoop fs -mkdir /steam
gunzip -c steam_big.sql.gz | hadoop fs -put - /steam/steam_big.sql

# Get Data From hdfs
## Normal
bin/hadoop fs -copyToLocal /hdfs/source/path /localfs/destination/path

## Get merge
hadoop fs -getmerge /output/dir/on/hdfs/ /desired/local/output/file.txt
