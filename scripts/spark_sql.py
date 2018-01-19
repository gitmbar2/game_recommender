import time
from pyspark import SparkContext, SparkConf, SQLContext, Row
import logging
import json
import subprocess

def sleep_mapper(seconds):
    time.sleep(seconds)


if __name__ == "__main__":
    conf = SparkConf().setAppName("Test_App")
    sc = SparkContext(conf=conf)
    sqlContext = SQLContext(sc)
    logging.getLogger("py4j").setLevel(logging.ERROR)


    # subprocess.call(
    #     ["hadoop", "fs", "-get", "/user/thomas/go_to_sleep.in"]
    # )

    result = sqlContext.sql("""
        SELECT user_id FROM `/../data/sample_sql.sql` LIMIT 20
    """)

    # with open("../data/sample_sql.sql", 'r') as f_in:
    #     data = json.load(f_in)
    # sc.\
    #     parallelize(
    #         [data.get("duration") for number in xrange(10000)]
    #     ).\
    #     map(sleep_mapper)

    with open("test.out", "w") as f:
        f.write(result)

    # sc.\
    #     parallelize(["Congratulations!"]).\
    #     saveAsTextFile("go_to_sleep.out")

    # subprocess.call(
    #     ["hadoop", "fs", "-put", "go_to_sleep.out", "/test/go_to_sleep.out"]
    # )
